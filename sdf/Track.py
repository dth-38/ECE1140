from pdb import line_prefix


class Track:
    def __init__(self,id_n=0,sec="A",l="Red",main_signal="False",track_occupancy="False",block_failure="False"):
        self.block_n = id_n
        self.section = sec
        self.line = l
        self.maintenance_signal = main_signal
        self.occupancy = track_occupancy
        self.failure = block_failure  
    def get_id(self):
        return self.id
    def get_occupancy(self):
        return self.occupancy
    def get_failure(self):
        return self.failure
    def get_section(self):
        return self.section 
    def get_line(self):
        return self.line
    def get_maintenance_signal(self):
        return self.maintenance_signal 

    



