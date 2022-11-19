
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
        self.BEACON = []
        self.switch = []
        self.light = []
        self.gate = []
        self.failed = False
        self.CONNECTED_BLOCKS = []
        self.TRANSITION_DIRECTIONS = []
        self.LENGTH = 0

        #might be useful for displaying stuff so im putting this here
        self.section = ""


    def set_switch(self, to_block):
        pass

    def set_light(self, color):
        self.light[0] = color

    def set_gate(self, gate):
        self.gate[0] = gate

    def get_occupancy(self):
        if self.occupied != -1:
            return True
        else:
            return False

    def get_occupancy_value(self):
        return self.occupied