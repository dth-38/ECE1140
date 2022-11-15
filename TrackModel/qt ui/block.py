from beacon import *
from station import *
from railwaycrossing import *

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
        self.number = number
        self.rail_crossing = None
        self.beacon = NotImplemented
        self.station = None

    def set_rail_cross(self, RailwayCrossing):
        self.rail_crossing = RailwayCrossing

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

    def get_length(self):
        return self.length

    def get_grade(self):
        return self.grade
    
    def get_occupancy(self):
        return self.occupancy