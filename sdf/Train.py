class Train:
    def __init__(self, id=0, start_block="Yard",dest_block="Yard",line="Red",time=0,speed=0,f_authority=0,b_authority=0):
        self.train_id = id
        self.suggested_speed = speed
        self.forward_authority = f_authority
        self.backward_authority = b_authority
        self.starting_block = start_block
        self.destination_block = dest_block
        self.line_on = line
        self.departure_time = time
        self.index_on_route = 0
        self.route_switches_arr = []
        self.route_blocks_arr = []
    def get_train_id(self):
        return self.train_id
    def get_line(self):
        return self.line_on
    def get_start_block(self):
        return self.starting_block
    def get_dest_block(self):
        return self.destination_block
    def get_time(self):
        return self.departure_time
    def get_suggested_speed(self):
        return self.suggested_speed
    def get_forward_authority(self):
        return self.forward_authority
    def get_backward_authority(self):
        return self.backward_authority
    
    