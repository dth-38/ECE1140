class Beacon:
    def __init__(self, s1, s2, s3):
        self.station1 = s1
        self.station2 = s2
        self.side = s3

    def get_station1(self):
        return self.station1

    def get_station2(self):
        return self.station2

    def set_station1(self, s):
        self.station1 = s

    def set_station2(self, s):
        self.station2 = s

    def set_side(self, s):
        self.side = s