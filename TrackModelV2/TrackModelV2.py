from collections import deque
import copy

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSlot

from TrackModelV2 import TrackBlock
from TrackModelV2 import FancyTrain
from TrackModelV2.TrackParser import TrackParser
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
        self.parser = TrackParser()

        self.next_train_id = 0


        super().__init__()


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

