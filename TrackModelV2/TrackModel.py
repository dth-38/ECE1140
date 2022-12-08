from collections import deque
import copy
import pandas
import numpy
import pathlib
import os
import random

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication

from TrackModelV2.TrackBlock import TrackBlock
from TrackModelV2.TrackBlock import STATION_BOTH, STATION_LEFT, STATION_RIGHT, SW_OFF_BLOCK, SW_ON_BLOCK
from TrackModelV2.TrackBlock import OPEN, CLOSED, NEXT_BLOCK, PREVIOUS_BLOCK, FORWARD_DIR, REVERSE_DIR, GREEN, RED
from TrackModelV2.FancyTrain import FancyTrain
from TrackModelV2.TrackModelGUI import TrackModelGUI
from Signals import signals


#constants
YARD = 0

TRAIN_ID = 0
DELX = 1

#conversion factor since train length is in feet
FEET_TO_METERS = 0.3408

class TrackModel(QObject):
    def __init__(self):
        self.lines = {}
        self.trains = {}

        #simple queue for updating train positions
        #since update function is slightly slower and should be run on tick
        self.update_queue = deque()

        self.gui = TrackModelGUI(self.get_track)

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
        signals.send_tm_stopped_at_station.connect(self.station_calc)



    @pyqtSlot()
    def tick(self):
        while len(self.update_queue) > 0:
            position_update = self.update_queue.popleft()
            self.update_train_position(position_update[TRAIN_ID], position_update[DELX])

        

    def station_calc(self, trainid):
        temp_pass_count = self.trains[trainid].passenger_count
        
        #calculate passengers deboarding subtract from count
        passengers_exiting = random.randint(1,15)
        temp_pass_count -= passengers_exiting
        if(temp_pass_count < 0):
            temp_pass_count = 0

        #calcualte passengers onboarding add to count
        passengers_boarding = random.randint(1,15)
        temp_pass_count += passengers_boarding
        #train model handles if it goes over passenger limit

        #send new passenger count to train
        signals.send_tm_passenger_count.emit(trainid, temp_pass_count)

        #send sales for station train is in
        signals.send_ctc_ticket_sales.emit(self.trains[trainid].line, passengers_boarding)

        #calculate ticket sales based on passengers onboarding, send to ctc


    @pyqtSlot(str, int, int)
    def handle_authority(self, line, block_num, auth):
        line = line.lower()

        try:
            self.lines[line][block_num].authority = copy.copy(auth)
        except:
            print("Invalid track location in authority signal.")
            print("Line: " + line + ", Block: " + str(block_num))

        self.gui.update_authority(line, block_num)
        train_id = self.lines[line][block_num].occupied
        signals.send_tm_authority.emit(train_id, copy.copy(auth))

    @pyqtSlot(str, int, int)
    def handle_speed(self, line, block_num, speed):
        line = line.lower()

        try:
            self.lines[line][block_num].commanded_speed = copy.copy(speed)
        except:
            print("Invalid track location in speed signal.")
            print("Line: " + line + ", Block: " + str(block_num))

        self.gui.update_spd(line, block_num)
        train_id = self.lines[line][block_num].occupied
        signals.send_tm_commanded_speed.emit(train_id, copy.copy(speed))

    @pyqtSlot(str, int, int)
    def handle_switch(self, line, sw_block, to_block):
        line = line.lower()
        print("switching switch in block " + str(sw_block) + " to " + str(to_block))

        try:
            self.lines[line][sw_block].set_switch(to_block)
        except Exception as e:
            print(e)

        self.gui.update_switch(line, sw_block)

    @pyqtSlot(str, int, str)
    def handle_light(self, line, block_num, color_str):
        line = line.lower()

        if color_str == "GREEN":
            color = GREEN
        else:
            color = RED

        try:
            self.lines[line][block_num].set_light(color)
        except:
            print("Invalid track location in light signal.")
            print("Line: " + line + ", Block: " + str(block_num))

        self.gui.update_light(line, block_num)

    @pyqtSlot(str, int, str)
    def handle_gate(self, line, block_num, gate):
        line = line.lower()

        if gate == "OPEN":
            gate_encoding = OPEN
        else:
            gate_encoding = CLOSED

        try:
            self.lines[line][block_num].set_gate(gate_encoding)
        except:
            print("Invalid track location in gate signal.")
            print("Line: " + line + ", Block: " + str(block_num))

        self.gui.update_gate(line, block_num)

    @pyqtSlot(str)
    def dispatch(self, line):
        line = line.lower()

        try:
            #cant dispatch a train if one is in the yard (starting block)
            if self.lines[line][YARD].occupied == -1:
                #setup initial train state
                new_train = FancyTrain(self.next_train_id)
                new_train.line = copy.copy(line)

                self.lines[line][YARD].occupied = new_train.id

                self.trains[self.next_train_id] = new_train

                self.next_train_id += 1

                signals.send_tc_occupancy.emit(line+"___0", True)
            else:
                print("Cannot dispatch train, yard is occupied.")
        except:
            print("Invalid track location in dispatch signal.")
            print("Line :" + line)

        self.gui.update_occupancy(line, YARD)


    @pyqtSlot(int, float)
    def handle_train_update(self, train_id, delta_x):
        self.update_queue.append((train_id, delta_x))


    #not handling errors here since something is fundamentally wrong if it errors
    def update_train_position(self, train_id, delta_x):
        #begins by adding the change in position to the current position
        self.trains[train_id].position_in_block += delta_x

        line = self.trains[train_id].line

        #checks if the previous block will no longer be occupied
        pos = self.trains[train_id].position_in_block
        length = self.trains[train_id].train_length
        blk = self.trains[train_id].block
        if pos - length < 0 and blk != YARD:
            prev_block = self.lines[line][blk].get_previous(self.trains[train_id].movement_direction)
            self.lines[line][prev_block].occupied = -1

            self.gui.update_occupancy(line, prev_block)
            tc_block = line + "_" + self.lines[line][prev_block].SECTION + "_" + str(prev_block)
            #signals.send_tc_occupancy.emit(tc_block, False)

        #loops while the train is past the length of the current block
        while self.trains[train_id].position_in_block > self.lines[line][self.trains[train_id].block].LENGTH:
            current_block = copy.copy(self.trains[train_id].block)

            #gets the position in the next block by subtracting the length of the current block
            self.trains[train_id].position_in_block -= self.lines[line][current_block].LENGTH

            #remove train from previous block
            self.lines[line][current_block].occupied = -1

            #updates gui after removing train from previous block
            self.gui.update_occupancy(line, current_block)
            tc_block = line + "_" + self.lines[line][current_block].SECTION + "_" + str(current_block)
            signals.send_tc_occupancy.emit(tc_block, False)

            #check validity of move

            #gets next block based on movement direction
            next_block = self.lines[line][current_block].get_next(self.trains[train_id].movement_direction)

            #determines which way the train will be moving through the next block
            if self.trains[train_id].movement_direction == FORWARD_DIR and self.lines[line][current_block].TRANSITION_DIRECTIONS[NEXT_BLOCK] != 0:
                next_dir = self.lines[line][current_block].TRANSITION_DIRECTIONS[NEXT_BLOCK]
            elif self.trains[train_id].movement_direction == REVERSE_DIR and self.lines[line][current_block].TRANSITION_DIRECTIONS[PREVIOUS_BLOCK] != 0:
                next_dir = self.lines[line][current_block].TRANSITION_DIRECTIONS[PREVIOUS_BLOCK]
            else:
                next_dir = self.trains[train_id].movement_direction

            if self.lines[line][next_block].get_previous(next_dir) == current_block:
                #valid move

                if not self.lines[line][next_block].get_occupancy():
                    #no collision has occured

                    #REMOVES TRAIN UPON REACHING YARD
                    if self.lines[line][current_block].get_next(self.trains[train_id].movement_direction) == YARD:
                        #unoccupies block
                        self.lines[line][current_block].occupied = -1

                        #updates gui before deleting train so the gui knows what block to check
                        self.gui.update_occupancy(line, current_block)
                        tc_block = line + "_" + self.lines[line][current_block].SECTION + "_" + str(current_block)
                        signals.send_tc_occupancy.emit(tc_block, False)

                        #remove train from dictionary
                        self.trains.pop(train_id)

                        print("TRAIN " + str(train_id) + " HAS BEEN REMOVED FROM THE TRACK.")

                        return 0

                    #moves train
                    self.lines[line][next_block].occupied = train_id
                    self.trains[train_id].block = next_block

                    #update movement direction for next block
                    self.trains[train_id].movement_direction = next_dir

                    #calls gui update function
                    self.gui.update_occupancy(line, next_block)

                    #update occupancy in track controllers
                    tc_block = line + "_" + self.lines[line][next_block].SECTION + "_" + str(next_block)
                    signals.send_tc_occupancy.emit(tc_block, True)

                    #send beacon signal to train if necessary
                    if self.lines[line][next_block].BEACON[0] != "":
                        station = self.lines[line][next_block].BEACON[0]
                        if self.lines[line][next_block].BEACON[1] == "LEFT":
                            side = STATION_LEFT
                        elif self.lines[line][next_block].BEACON[1] == "RIGHT":
                            side = STATION_RIGHT
                        else:
                            side = STATION_BOTH

                        signals.send_tm_beacon.emit(station, side)

                    #send grade
                    signals.send_tm_grade.emit(train_id, self.lines[line][next_block].GRADE)
                    #send failure
                    #send tunnel
                    signals.send_tm_tunnel.emit(train_id, self.lines[line][next_block].UNDERGROUND)
                    #send at station
                    signals.send_tm_station.emit(train_id, self.lines[line][next_block].STATION != "")
                    #Send new authority to train.
                    #TODO: comment back in after ctc is working
                    #signals.send_tm_authority.emit(self.lines[line][next_block].authority)
                    #Send new commanded speed to train.
                    #signals.send_tm_commanded_speed.emit(self.lines[line][next_block].commanded_speed)

                    
                else:
                    #collision has occurred
                    print("UH OH: TRAIN " + str(train_id) + " HAS COLLIDED WITH TRAIN " + str(self.lines[line][next_block].get_occupancy_value()) + " AT " + line + ":" + str(next_block))
                    self.trains.pop(train_id)
                    self.trains.pop(self.lines[line][next_block].get_occupancy_value())
                    self.lines[line][next_block].occupied = -1

                    tc_block = line + "_" + self.lines[line][next_block].SECTION + "_" + str(next_block)
                    signals.send_tc_occupancy.emit(tc_block, False)
                    self.gui.show_incident(line, next_block)
                    return 0

            else:
                print("wtf, current block = " + str(current_block) + ", checked against = " + str(self.lines[line][next_block].get_previous(next_dir)))

                #train has derailed
                print("UH OH: TRAIN " + str(train_id) + " DERAILED ENTERING LINE: " + self.trains[train_id].line + ", BLOCK: " + str(next_block))
                self.trains.pop(train_id)

                self.gui.show_incident(line, next_block)
                return 0

            #checks if train is in two blocks at once
            pos = self.trains[train_id].position_in_block
            length = self.trains[train_id].train_length
            blk = self.trains[train_id].block
            if pos - length < 0 and blk != YARD:
                prev_block = self.lines[line][self.trains[train_id].block].get_previous(self.trains[train_id].movement_direction)
                self.lines[line][prev_block].occupied = train_id

                self.gui.update_occupancy(line, prev_block)
                tc_block = line + "_" + self.lines[line][prev_block].SECTION + "_" + str(prev_block)
                #signals.send_tc_occupancy.emit(tc_block, True)


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
            #2 fills in track infrastructure

            #opens excel file and determines which workbooks are lines
            trk_excel = pandas.ExcelFile(filename)
            sheets = trk_excel.sheet_names
            r_sheets = []
            for sheet in sheets:
                if sheet[len(sheet)-1] == "!":
                    r_sheets.append(sheet)
            

            #im so tired of writing parsers
            for l_sheet in r_sheets:
                new_line = {}
                l_name = l_sheet[:len(l_sheet)-6]
                l_data = trk_excel.parse(l_sheet)


                #add yard since it isnt a block in the excel sheet
                new_line[YARD] = TrackBlock()

                for i in range(l_data.shape[0]):
                    block_num = l_data.iloc[i,2]
                    block_num = int(block_num)
                    new_line[block_num] = TrackBlock()
                    new_line[block_num].GRADE = l_data.iloc[i,4]
                    new_line[block_num].LENGTH = l_data.iloc[i,3]
                    new_line[block_num].SECTION = l_data.iloc[i,1]

                #2nd parse for track infrastructure
                #this is done to ensure all blocks exist before trying to connect with switches and add beacons
                for i in range(l_data.shape[0]):
                    block_num = l_data.iloc[i,2]
                    equipment = l_data.iloc[i,6]

                    block_num = int(block_num)
                    equipment = str(equipment)

                    equipment = self.remove_whitespace(equipment)

                    val = ""
                    j = 0
                    length = len(equipment)
                    fix_flag = False
                    while j < length:
                        if equipment[j] == ";" or fix_flag == True:
                            match val:
                                case "SWITCH":
                                    #do switch stuff
                                    j += 1
                                    path1 = ""
                                    path2 = ""
                                    while equipment[j] != ";":
                                        path1 += equipment[j]
                                        j += 1
                                    
                                    j += 1
                                    while equipment[j] != ")":
                                        path2 += equipment[j]
                                        j += 1

                                    p1_divider = path1.find("-")
                                    p2_divider = path2.find("-")

                                    path1_1 = int(path1[1:p1_divider])
                                    path1_2 = int(path1[p1_divider+1:])
                                    path2_1 = int(path2[:p2_divider])
                                    path2_2 = int(path2[p2_divider+1:])


                                    #this is so wack
                                    if path1_1 == block_num:
                                        #switch goes to next blocks
                                        new_line[block_num].CONNECTED_BLOCKS[NEXT_BLOCK] = "SWITCH"
                                        new_line[block_num].switch.append(0)
                                        new_line[block_num].switch.append(path1_2)
                                        new_line[block_num].switch.append(path2_2)

                                        #add lights to next blocks
                                        new_line[path1_2].light.append(0)
                                        new_line[path2_2].light.append(0)

                                        if path1_2 == block_num + 1:
                                            #path1_2 is the next block numerically 
                                            new_line[block_num].TRANSITION_DIRECTIONS[NEXT_BLOCK] = FORWARD_DIR
                                            new_line[block_num].SWITCH_TRANSITIONS[0] = FORWARD_DIR
                                            new_line[block_num].SWITCH_TRANSITIONS[1] = REVERSE_DIR
                                            new_line[path2_2].TRANSITION_DIRECTIONS[NEXT_BLOCK] = REVERSE_DIR
                                            new_line[path2_2].CONNECTED_BLOCKS[NEXT_BLOCK] = block_num
                                        else:
                                            #path2_2 is the next block numerically
                                            new_line[block_num].TRANSITION_DIRECTIONS[NEXT_BLOCK] = REVERSE_DIR
                                            new_line[block_num].SWITCH_DIRECTIONS[0] = REVERSE_DIR
                                            new_line[block_num].SWITCH_DIRECTIONS[1] = FORWARD_DIR
                                            new_line[path1_2].TRANSITION_DIRECTIONS[NEXT_BLOCK] = REVERSE_DIR
                                            new_line[path1_2].CONNECTED_BLOCKS[NEXT_BLOCK] = block_num

                                    else:
                                        #switch goes to previous blocks
                                        new_line[block_num].CONNECTED_BLOCKS[PREVIOUS_BLOCK] = "SWITCH"
                                        new_line[block_num].switch.append(0)
                                        new_line[block_num].switch.append(path1_1)
                                        new_line[block_num].switch.append(path2_1)

                                        #add lights to previous blocks
                                        new_line[path1_1].light.append(0)
                                        new_line[path2_1].light.append(0)

                                        if path1_1 == block_num - 1:
                                            #path1_1 is the previous block numerically
                                            new_line[block_num].TRANSITION_DIRECTIONS[PREVIOUS_BLOCK] = REVERSE_DIR
                                            new_line[block_num].SWITCH_TRANSITIONS[0] = REVERSE_DIR
                                            #to check for override
                                            if not numpy.isnan(l_data.iloc[i,10]):
                                                t_o = l_data.iloc[i,10]
                                                new_line[block_num].SWITCH_TRANSITIONS[1] = t_o
                                            else:
                                                new_line[block_num].SWITCH_TRANSITIONS[1] = FORWARD_DIR
                                            new_line[path2_1].TRANSITION_DIRECTIONS[PREVIOUS_BLOCK] = FORWARD_DIR
                                            new_line[path2_1].CONNECTED_BLOCKS[PREVIOUS_BLOCK] = block_num
                                        else:
                                            #path2_1 is the previous block numerically
                                            new_line[block_num].SWITCH_TRANSITIONS[1] = REVERSE_DIR
                                            if not numpy.isnan(l_data.iloc[i,10]):
                                                t_o = l_data.iloc[i,10]
                                                new_line[block_num].SWITCH_TRANSITIONS[0] = t_o
                                                new_line[block_num].TRANSITION_DIRECTIONS[PREVIOUS_BLOCK] = t_o
                                            else:
                                                new_line[block_num].SWITCH_TRANSITIONS[0] = FORWARD_DIR
                                                new_line[block_num].TRANSITION_DIRECTIONS[PREVIOUS_BLOCK] = FORWARD_DIR
                                            new_line[path1_1].TRANSITION_DIRECTIONS[PREVIOUS_BLOCK] = FORWARD_DIR
                                            new_line[path1_1].CONNECTED_BLOCKS[PREVIOUS_BLOCK] = block_num

                                    
                                case "STATION":
                                    #do station stuff
                                    j += 1
                                    station = ""
                                    for k in range(j, len(equipment)):
                                        if equipment[k] != ";":
                                            station += equipment[k]
                                        else:
                                            j = k
                                            break
                                    
                                    #sets station name
                                    if station == "":
                                        new_line[block_num].STATION = "?"
                                    else:
                                        new_line[block_num].STATION = station

                                    #sets beacon in next/previous blocks
                                    station_side = l_data.iloc[i,7]
                                    if station_side == "Left":
                                        new_line[block_num-1].BEACON[0] = station
                                        new_line[block_num-1].BEACON[1] = "LEFT"
                                    elif station_side == "Right":
                                        new_line[block_num-1].BEACON[0] = station
                                        new_line[block_num-1].BEACON[1] = "RIGHT"
                                    else:
                                        for b in range(len(new_line[block_num].CONNECTED_BLOCKS)):
                                            if new_line[block_num].CONNECTED_BLOCKS[b] == "SWITCH":
                                                conn1 = new_line[block_num].switch[SW_OFF_BLOCK]
                                                conn2 = new_line[block_num].switch[SW_ON_BLOCK]
                                                new_line[conn1].BEACON[0] = station
                                                new_line[conn1].BEACON[1] = "BOTH"
                                                new_line[conn2].BEACON[0] = station
                                                new_line[conn2].BEACON[1] = "BOTH"
                                            else:
                                                if b == 0:
                                                    new_line[block_num-1].BEACON[0] = station
                                                    new_line[block_num-1].BEACON[1] = "BOTH"
                                                else:
                                                    new_line[block_num+1].BEACON[0] = station
                                                    new_line[block_num+1].BEACON[1] = "BOTH"

                                    #add station light
                                    new_line[block_num].light.append(0)


                                case "UNDERGROUND":
                                    new_line[block_num].UNDERGROUND = True
                                case "RAILWAYCROSSING":
                                    new_line[block_num].gate.append(OPEN)
                                case "SWITCHTOYARD":
                                    new_line[block_num].CONNECTED_BLOCKS[NEXT_BLOCK] = "SWITCH"
                                    new_line[block_num].switch.append(0)
                                    new_line[block_num].switch.append(YARD)
                                    new_line[block_num].switch.append(block_num+1)

                                    new_line[YARD].CONNECTED_BLOCKS[PREVIOUS_BLOCK] = block_num

                                    #add lights
                                    new_line[block_num+1].light.append(0)
                                    if new_line[YARD].light == []:
                                        new_line[YARD].light.append(0)

                                case "SWITCHFROMYARD":
                                    new_line[block_num].CONNECTED_BLOCKS[PREVIOUS_BLOCK] = "SWITCH"
                                    new_line[block_num].switch.append(0)
                                    new_line[block_num].switch.append(block_num-1)
                                    new_line[block_num].switch.append(YARD)

                                    new_line[YARD].CONNECTED_BLOCKS[NEXT_BLOCK] = block_num

                                    #add lights
                                    new_line[block_num-1].light.append(0)
                                    if new_line[YARD].light == []:
                                        new_line[YARD].append(0)

                                case "SWITCHTO/FROMYARD":
                                    new_line[block_num].CONNECTED_BLOCKS[NEXT_BLOCK] = "SWITCH"
                                    new_line[block_num].switch.append(0)
                                    new_line[block_num].switch.append(YARD)
                                    new_line[block_num].switch.append(block_num+1)

                                    new_line[YARD].CONNECTED_BLOCKS[PREVIOUS_BLOCK] = block_num
                                    new_line[YARD].CONNECTED_BLOCKS[NEXT_BLOCK] = block_num

                                    new_line[YARD].light.append(0)
                                    new_line[block_num+1].light.append(0)

                                case _:
                                    pass
                            val = ""
                        else:
                            val += equipment[j]

                        j += 1

                        if fix_flag == False and j == length:
                            j -= 1
                            fix_flag = True


                    #connects block to previous/next if a switch was not added
                    if new_line[block_num].CONNECTED_BLOCKS[PREVIOUS_BLOCK] == -1:
                        new_line[block_num].CONNECTED_BLOCKS[PREVIOUS_BLOCK] = block_num-1

                    if new_line[block_num].CONNECTED_BLOCKS[NEXT_BLOCK] == -1:
                        new_line[block_num].CONNECTED_BLOCKS[NEXT_BLOCK] = block_num+1

                #adds new line to lines dictionary
                l_name = l_name.lower()
                self.lines[l_name] = new_line

            self.gui.initialize_lines()
        
        else:
            print("Track layout file does not exist.")

        
    def remove_whitespace(self, s):
        new_s = ""
        for i in range(len(s)):
            if s[i] != " " and s[i] != "\n":
                new_s += s[i]

        return new_s

    def get_track(self):
        return self.lines
        
    
if __name__ == "__main__":
    track_app = QApplication()

    t_model = TrackModel()

    track_app.exec()

