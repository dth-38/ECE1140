from TrackModel.beacon import *
from TrackModel.station import *
from TrackModel.railwaycrossing import *
from TrackModel.failure import *
from TrackModel.light import *

class Block:
    def __init__(self, section, number):
        self.section = section
        self.length = 0
        self.grade = 0
        self.commanded_speed = 0
        self.elevation = 0
        self.authority = 0
        self.occupancy = False
        self.failure = None
        self.direction = 0
        self.bidirectional = False
        self.number = number
        self.rail_crossing = None
        self.beacon = NotImplemented
        self.station = None
        self.light = None
        self.infra_text = ""

    def set_infra(self, t):
        self.infra_text = t

    def set_directionality(self):
        bi_sections = []
        uni_sections = []
        s = self.get_section()

    def get_bidirectional(self):
        # False -- train can only move 1 way
        # True -- train can move both ways
        return self.bidirectional

    def set_rail_cross(self, RailwayCrossing):
        self.rail_crossing = RailwayCrossing

    def set_light(self, Light):
        self.light = Light

    def set_beacon(self, s1, s2, s3):
        ## s1 = Outgoing Station
        #  s2 = Incoming Station
        #  s3 = track side
        self.beacon.set_station1(s1)
        self.beacon.set_station2(s2)
        self.beacon.set_side(s3)

    def set_station(self, Station):
        self.station = Station

    def get_station(self):
        return self.station

    def get_number(self):
        return self.number

    def get_section(self):
        return self.section

    def get_beacon(self):
        return "stat"

    def get_length(self):
        return self.length

    def get_grade(self):
        return self.grade
    
    def get_occupancy(self):
        return self.occupancy

    def get_authority(self):
        return self.authority

    def get_commanded_speed(self):
        return self.commanded_speed

    def get_failure_status(self):
        if self.failure is not None:
            return self.failure.get_state()
        else:
            return False

    def get_elevation(self):
        return self.elevation

    def get_light_status(self):
        return "GREEN"