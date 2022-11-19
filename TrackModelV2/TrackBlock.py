
#constants
STATION_LEFT = 0
STATION_RIGHT = 1
STATION_BOTH = 2

SWITCH_STATE = 0
SW_OFF_BLOCK = 1
SW_ON_BLOCK = 2

CLOSED = 1
OPEN = 0

GREEN = 1
RED = 0

REVERSE_DIR = -1
CONTINUE_DIR = 0
FORWARD_DIR = 1

PREVIOUS_BLOCK = 0
NEXT_BLOCK = 1



class TrackBlock:
    def __init__(self):
        self.occupied = -1
        self.authority = 0
        self.commanded_speed = 0
        self.GRADE = 0
        self.STATION = ""
        self.BEACON = 0
        self.switch = []
        self.light = []
        self.gate = []
        self.failed = False
        self.CONNECTED_BLOCKS = 0
        self.TRANSITION_DIRECTIONS = 0
        self.LENGTH = 0

        #might be useful for displaying stuff so im putting this here
        self.SECTION = ""

    #to_block is the block the switch is connecting to as an int
    def set_switch(self, to_block):
        if to_block == self.switch[SW_ON_BLOCK]:
            self.switch[SWITCH_STATE] = True
        elif to_block == self.switch[SW_OFF_BLOCK]:
            self.switch[SWITCH_STATE] = False

    def set_light(self, color):
        if self.light != []:
            self.light[0] = color

    def set_gate(self, gate):
        if self.gate != []:
            self.gate[0] = gate

    def get_occupancy(self):
        if self.occupied != -1:
            return True
        else:
            return False

    def get_occupancy_value(self):
        return self.occupied

    def get_next(self, dir):
        #first gets the next/previous block from array
        if dir == FORWARD_DIR:
            next_block = self.CONNECTED_BLOCKS[NEXT_BLOCK]
        else:
            next_block = self.CONNECTED_BLOCKS[PREVIOUS_BLOCK]

        #checks where a switch is going, if temp_next is a switch
        if next_block == "SWITCH":
            if self.switch[SWITCH_STATE] == True:
                next_block = self.switch[SW_ON_BLOCK]
            else:
                next_block = self.switch[SW_OFF_BLOCK]

        return next_block

    def get_previous(self, dir):
        if dir == FORWARD_DIR:
            previous_block = self.CONNECTED_BLOCKS[PREVIOUS_BLOCK]
        else:
            previous_block = self.CONNECTED_BLOCKS[NEXT_BLOCK]

        if previous_block == "SWITCH":
            if self.switch[SWITCH_STATE] == True:
                previous_block = self.switch[SW_ON_BLOCK]
            else:
                previous_block = self.switch[SW_OFF_BLOCK]

        return previous_block
