class Train:
    
    def _init_(self,trainId):

        #integers
        self.forward_authority = 0
        self.backward_authority = 0
        self.oncoming_passengers = 0
        self.crew_count = 0
        self.passengers_deboarding = 0
        self.failure_type = 0
        self.passenger_count = 0

        #float
        self.commanded_speed = 0.0
        self.grade = 0.0
        self.power = 0.0
        self.ac_cmd = 70.0
        self.actual_speed = 0
        self.acceleration = 0
        self.mass = 0
        self.train_length = 105.6
        self.train_width = 11.2
        self.train_height = 9.7

        #boolean
        self.track_failure = 0
        self.interior_light_cmd = 0
        self.exterior_light_cmd = 0
        self.right_door_cmd = 0
        self.left_door_cmd = 0
        self.advertisement_cmd = 0
        self.announcement_cmd = 0
        self.passenger_ebrake = 0
        self.ebrake = 0
        self.sbrake = 0
        self.failure_signal = 0

        
        
        
