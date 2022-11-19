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

                self.next_train_id += 1

                self.lines[line][YARD].occupied = new_train.id

                self.trains[new_train.id] = new_train
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

        #loops while the train is past the length of the current block
        while self.trains[train_id].position_in_block > self.lines[self.trains[train_id].line][self.trains[train_id].block].LENGTH:
            #gets the position in the next block by subtracting the length of the current block
            self.trains[train_id].position_in_block -= self.lines[self.trains[train_id].line][self.trains[train_id].block].LENGTH

            #remove train from previous block
            self.lines[self.trains[train_id].line][self.trains[train_id].block].occupied = -1

            #TODO: finish this




