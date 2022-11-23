from collections import deque
import copy
import pandas
import pathlib
import os

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSlot

from TrackModelV2 import TrackBlock
from TrackModelV2 import FancyTrain
from TrackModelV2.TrackModelGUI import TrackModelGUI
from Signals import signals


#constants
YARD = 0

TRAIN_ID = 0
DELX = 1

#conversion factor since train length is in feet
FEET_TO_METERS = 0.3408

class TrackModelV2(QObject):
    def __init__(self):
        self.lines = {}
        self.trains = {}

        #simple queue for updating train positions
        #since update function is slightly slower and should be run on tick
        self.update_queue = deque()

        self.gui = TrackModelGUI()

        self.next_train_id = 0


        super().__init__()

        self.setup_signals()
        self.initialize_track()


    def setup_signals(self):
        signals.track_update.connect(self.tick)
        signals.send_track_authority.connect(self.handle_authority)
        signals.send_track_speed.connect(self.handle_speed)
        signals.broadcast_switch.connect(self.handle_switch)
        signals.broadcast_light.connect(self.handle_light)
        signals.broadcast_gate.connect(self.handle_gate)
        signals.send_tm_dispatch.connect(self.dispatch)
        signals.send_tm_distance.connect(self.handle_train_update)

        #TODO: add signals for updating gui


    @pyqtSlot()
    def tick(self):
        while len(self.update_queue) > 0:
            position_update = self.update_queue.popleft()
            self.update_train_position(position_update[TRAIN_ID], position_update[DELX])

        

    @pyqtSlot(str, int, int)
    def handle_authority(self, line, block_num, auth):
        line = line.lower()

        try:
            self.lines[line][block_num].authority = copy.copy(auth)
        except:
            print("Invalid track location in authority signal.")
            print("Line: " + line + ", Block: " + str(block_num))

    @pyqtSlot(str, int, int)
    def handle_speed(self, line, block_num, speed):
        line = line.lower()

        try:
            self.lines[line][block_num].commanded_speed = copy.copy(speed)
        except:
            print("Invalid track location in speed signal.")
            print("Line: " + line + ", Block: " + str(block_num))

    @pyqtSlot(str, int, int)
    def handle_switch(self, line, sw_block, to_block):
        line = line.lower()

        try:
            self.lines[line][sw_block].set_switch(to_block)
        except Exception as e:
            print(e)

    @pyqtSlot(str, int, str)
    def handle_light(self, line, block_num, color_str):
        line = line.lower()

        if color_str == "GREEN":
            color = TrackBlock.GREEN
        else:
            color = TrackBlock.RED

        try:
            self.lines[line][block_num].set_light(color)
        except:
            print("Invalid track location in light signal.")
            print("Line: " + line + ", Block: " + str(block_num))

    @pyqtSlot(str, int, str)
    def handle_gate(self, line, block_num, gate):
        line = line.lower()

        if gate == "OPEN":
            gate_encoding = TrackBlock.OPEN
        else:
            gate_encoding = TrackBlock.CLOSED

        try:
            self.lines[line][block_num].set_gate(gate_encoding)
        except:
            print("Invalid track location in gate signal.")
            print("Line: " + line + ", Block: " + str(block_num))

    @pyqtSlot(str)
    def dispatch(self, line):
        line = line.lower()

        try:
            #cant dispatch a train if one is in the yard (starting block)
            if self.lines[line][YARD].occupied == False:
                #setup initial train state
                new_train = FancyTrain.FancyTrain(self.next_train_id)
                new_train.line = copy.copy(line)

                self.lines[line][YARD].occupied = new_train.id

                self.trains[self.next_train_id] = new_train

                self.next_train_id += 1
            else:
                print("Cannot dispatch train, yard is occupied.")
        except:
            print("Invalid track location in dispatch signal.")
            print("Line :" + line)


    @pyqtSlot(int, float)
    def handle_train_update(self, train_id, delta_x):
        self.update_queue.append((train_id, delta_x))


    #not handling errors here since something is fundamentally wrong if it errors
    def update_train_position(self, train_id, delta_x):
        #begins by adding the change in position to the current position
        self.trains[train_id].position_in_block += delta_x

        line = self.trains[train_id].line

        #checks if the previous block will no longer be occupied
        if -1 * (self.trains[train_id].position_in_block - (self.trains[train_id].length * FEET_TO_METERS)) > self.lines[line][self.trains[train_id].block].LENGTH:
            prev_block = self.lines[line][self.trains[train_id].block].get_previous(self.trains[train_id].movement_direction)
            self.lines[line][prev_block].occupied = -1
            #TODO: signal for gui update

        #loops while the train is past the length of the current block
        while self.trains[train_id].position_in_block > self.lines[line][self.trains[train_id].block].LENGTH:

            #REMOVES TRAIN UPON REACHING YARD
            if self.lines[line][self.trains[train_id].block].get_next(self.trains[train_id].movement_direction) == YARD:
                #unoccupies block
                self.lines[line][self.trains[train_id].block].occupied = -1

                #remove train from dictionary
                self.trains.pop(train_id)

                print("TRAIN " + str(train_id) + " HAS BEEN REMOVED FROM THE TRACK.")

                #TODO: signal for gui update
                break


            #gets the position in the next block by subtracting the length of the current block
            self.trains[train_id].position_in_block -= self.lines[line][self.trains[train_id].block].LENGTH

            #remove train from previous block
            self.lines[line][self.trains[train_id].block].occupied = -1
            #TODO: signal for gui update

            #check validity of move
            next_block = self.lines[line][self.trains[train_id].block].get_next(self.trains[train_id].movement_direction)
            next_dir = self.lines[line][self.trains[train_id].block].TRANSITION_DIRECTIONS[TrackBlock.NEXT_BLOCK]
            if self.lines[line][next_block].get_previous(next_dir) == self.trains[train_id].block:
                #valid move

                if not self.lines[line][next_block].get_occupancy():
                    #no collision has occured

                    #update movement direction through a block
                    if self.trains[train_id].movement_direction == TrackBlock.FORWARD_DIR:
                        self.trains[train_id].movement_direction = self.lines[line][next_block].MOVEMENT_DIRECTIONS[TrackBlock.NEXT_BLOCK]
                    elif self.trains[train_id].movement_direction == TrackBlock.REVERSE_DIR:
                        self.trains[train_id].movement_direction == self.lines[line][next_block].MOVEMENT_DIRECTIONS[TrackBlock.PREVIOUS_BLOCK]
                

                    self.lines[line][next_block].occupied = train_id
                    self.trains[train_id].block = next_block
                    #TODO: signal for gui update
                else:
                    #collision has occurred
                    print("UH OH: TRAIN " + str(train_id) + " HAS COLLIDED WITH TRAIN " + str(self.lines[line][next_block].get_occupancy_value()) + " AT " + line + ":" + str(next_block))
                    self.trains.pop(train_id)
                    self.trains.pop(self.lines[line][next_block].get_occupancy_value())
                    self.lines[line][next_block].occupied = -1
                    #TODO: signal for gui update

            else:
                #train has derailed
                print("UH OH: TRAIN " + str(train_id) + " DERAILED ENTERING LINE: " + self.trains[train_id].line + ", BLOCK: " + str(next_block))
                self.trains.pop(train_id)
                #TODO: signal for gui update


    def initialize_track(self, filename="track.xlsx"):
        #looks for track file
        if filename == "track.xlsx":
            filename = str(pathlib.Path().absolute())
            i = 0
            while filename[len(filename)-7:] != "ECE1140":
                i += 1
                filename = str(pathlib.Path(__file__).parents[i])
            #creates the expected text file based on the controller id
            filename += ("/TrackModelV2/track.xlsx")

        if os.path.isfile(filename):
            #resets variables
            self.lines.clear()
            self.trains.clear()
            self.next_train_id = 0
            self.update_queue.clear()

            #parsing done in two stages
            #1 just creates the dictionary with all blocks
            #2 fills in track equpment

            #opens excel file and determines which workbooks are lines
            trk_excel = pandas.ExcelFile(filename)
            sheets = trk_excel.sheet_names
            for sheet in sheets:
                if sheet[len(sheet)-4:] != "Line":
                    sheets.remove(sheet)

            #im so tired of writing parsers
            for l_sheet in sheets:
                new_line = {}
                l_name = l_sheet[:len(l_sheet)-5]
                l_data = trk_excel.parse(l_sheet)

                #for each row add basic info to block
                for i in range(1,l_data.shape[0]):
                    block_num = l_data.iloc[i,2]
                    new_line[block_num] = TrackBlock()
                    new_line[block_num].GRADE = l_data.iloc[i,4]
                    new_line[block_num].LENGTH = l_data.iloc[i,3]
                    new_line[block_num].SECTION = l_data.iloc[i,1]

                #2nd parse for track infrastructure
                #this is done to ensure all blocks exist before trying to connect with switches and add beacons
                for i in range(1,l_data.shape[0]):
                    block_num = l_data.iloc[i,2]
                    equipment = l_data.iloc[i,6]

                    equipment = self.remove_whitespace(equipment)

                    val = ""
                    for i in range(len(equipment)):
                        if equipment[i] == ";":
                            match val:
                                case "SWITCH":
                                    #do switch stuff
                                    i += 1
                                    path1 = ""
                                    path2 = ""
                                    while equipment[i] != ";":
                                        path1 += equipment[i]
                                        i += 1
                                    
                                    i += 1
                                    while equipment[i] != ")":
                                        path2 += equipment[i]
                                        i += 1

                                    p1_divider = path1.find("-")
                                    p2_divider = path2.find("-")

                                    path1_1 = int(path1[1:p1_divider])
                                    path1_2 = int(path1[p1_divider+1:])
                                    path2_1 = int(path2[:p2_divider])
                                    path2_2 = int(path2[p1_divider+1:])

                                    #this is so wack
                                    if path1_1 == block_num:
                                        #switch goes to next blocks
                                        new_line[block_num].CONNECTED_BLOCKS[TrackBlock.NEXT_BLOCK] = "SWITCH"
                                        new_line[block_num].switch.append(0)
                                        new_line[block_num].switch.append(path1_2)
                                        new_line[block_num].switch.append(path2_2)

                                        if path1_2 == block_num + 1:
                                            #path1_2 is the next block numerically 
                                            new_line[block_num].TRANSITION_DIRECTIONS[TrackBlock.NEXT_BLOCK] = TrackBlock.FORWARD_DIR
                                            new_line[block_num].SWITCH_TRANSITIONS[0] = TrackBlock.FORWARD_DIR
                                            new_line[block_num].SWITCH_TRANSITIONS[1] = TrackBlock.REVERSE_DIR
                                            new_line[path2_2].TRANSITION_DIRECTIONS[TrackBlock.NEXT_BLOCK] = TrackBlock.REVERSE_DIR
                                            new_line[path2_2].CONNECTED_BLOCKS[TrackBlock.NEXT_BLOCK] = block_num
                                        else:
                                            #path2_2 is the next block numerically
                                            new_line[block_num].TRANSITION_DIRECTIONS[TrackBlock.NEXT_BLOCK] = TrackBlock.REVERSE_DIR
                                            new_line[block_num].SWITCH_DIRECTIONS[0] = TrackBlock.REVERSE_DIR
                                            new_line[block_num].SWITCH_DIRECTIONS[1] = TrackBlock.FORWARD_DIR
                                            new_line[path1_2].TRANSITION_DIRECTIONS[TrackBlock.NEXT_BLOCK] = TrackBlock.REVERSE_DIR
                                            new_line[path1_2].CONNECTED_BLOCKS[TrackBlock.NEXT_BLOCK] = block_num

                                    else:
                                        #switch goes to previous blocks
                                        new_line[block_num].CONNECTED_BLOCKS[TrackBlock.PREVIOUS_BLOCK] = "SWITCH"
                                        new_line[block_num].switch.append(0)
                                        new_line[block_num].switch.append(path1_1)
                                        new_line[block_num].switch.append(path2_1)

                                        if path1_1 == block_num - 1:
                                            #path1_1 is the previous block numerically
                                            new_line[block_num].TRANSITION_DIRECTIONS[TrackBlock.PREVIOUS_BLOCK] = TrackBlock.REVERSE_DIR
                                            new_line[block_num].SWITCH_TRANSITIONS[0] = TrackBlock.REVERSE_DIR
                                            #to check for override
                                            if not l_data.iloc[i,10].isnull():
                                                t_o = l_data.iloc[i,10]
                                                new_line[block_num].SWITCH_TRANSITIONS[1] = t_o
                                            else:
                                                new_line[block_num].SWITCH_TRANSITIONS[1] = TrackBlock.FORWARD_DIR
                                            new_line[path2_1].TRANSITION_DIRECTIONS[TrackBlock.PREVIOUS_BLOCK] = TrackBlock.FORWARD_DIR
                                            new_line[path2_1].CONNECTED_BLOCKS[TrackBlock.PREVIOUS_BLOCK] = block_num
                                        else:
                                            #path2_1 is the previous block numerically
                                            new_line[block_num].SWITCH_TRANSITIONS[1] = TrackBlock.REVERSE_DIR
                                            if not l_data.iloc[i,10].isnull():
                                                t_o = l_data.iloc[i,10]
                                                new_line[block_num].SWITCH_TRANSITIONS[0] = t_o
                                                new_line[block_num].TRANSITION_DIRECTIONS[TrackBlock.PREVIOUS_BLOCK] = t_o
                                            else:
                                                new_line[block_num].SWITCH_TRANSITIONS[0] = TrackBlock.FORWARD_DIR
                                                new_line[block_num].TRANSITION_DIRECTIONS[TrackBlock.PREVIOUS_BLOCK] = TrackBlock.FORWARD_DIR
                                            new_line[path1_1].TRANSITION_DIRECTIONS[TrackBlock.PREVIOUS_BLOCK] = TrackBlock.FORWARD_DIR
                                            new_line[path1_1].CONNECTED_BLOCKS[TrackBlock.PREVIOUS_BLOCK] = block_num

                                    
                                case "STATION":
                                    #do station stuff
                                    pass
                                case "UNDERGROUND":
                                    new_line[block_num].UNDERGROUND = True
                                case "RAILWAYCROSSING":
                                    new_line[block_num].gate.append(TrackBlock.OPEN)
                                case "SWITCHTOYARD":
                                    #i hate life
                                    pass
                                case "SWITCHFROMYARD":
                                    #why does profeta have to format every switch differently
                                    pass
                                case "SWITCHTO/FROMYARD":
                                    #yay more cases
                                    pass
                                case _:
                                    pass
                            val = ""
                        else:
                            val += equipment[i]

                    #connects block to previous/next if a switch was not added
                    if new_line[block_num].CONNECTED_BLOCKS[TrackBlock.PREVIOUS_BLOCK] == -1:
                        new_line[block_num].CONNECTED_BLOCKS[TrackBlock.PREVIOUS_BLOCK] = block_num-1

                    if new_line[block_num].CONNECTED_BLOCKS[TrackBlock.NEXT_BLOCK] == -1:
                        new_line[block_num].CONNECTED_BLOCKS[TrackBlock.NEXT_BLOCK] = block_num+1

        
        else:
            print("Track layout file does not exist.")

        
    def remove_whitespace(self, s):
        new_s = ""
        for i in range(len(s)):
            if s[i] != " " and s[i] != "\n":
                new_s += s[i]

        return new_s
        

