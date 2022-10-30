
#collections of functions brought from the actual Train Controller UI classes
#NOTE for some reason, uniitest could not detect pyqt5 UI. Therefore, I decided to use their functions instead.

class Train_Controller:
    
    actual_speed = 0
    speed_limit = 0
    commanded_speed = 0

    normal_brake_flag = False 
    norm_deaccel_rate = 0

    left_door_state = False #True = Opened, False = Closed
    commanded_door_state = False

    def set_speed_limit(self, value):
        self.speed_limit = value

    def set_commanded_speed(self, value):
        self.commanded_speed = value
    
    def give_actual_speed(self, value):
        if value > self.speed_limit:
            value = self.speed_limit
        self.actual_speed = value
        
    def press_norm_brake(self):
        self.normal_brake_flag = True
        if self.normal_brake_flag == True:
            self.actual_speed -= self.norm_deaccel_rate
            if self.actual_speed < 0:
                self.actual_speed = 0

    def set_left_door(self, state):
        self.commanded_left_door_state = True if state == "On" else False

    def set_actual_speed(self, value):
        self.actual_speed = value

    def set_norm_deaccel_rate(self, value):
        self.norm_deaccel_rate = value

    def get_commanded_speed(self):
        return self.commanded_speed
    
    def get_speed_limit(self):
        return self.speed_limit

    def get_norm_brake_state(self):
        return self.normal_brake_flag

    def get_actual_speed(self):
        return self.actual_speed

    def get_commanded_left_door(self):
        return self.commanded_door_state
    
    def get_left_door(self):
        return self.left_door_state
    
    def get_norm_deaccel_rate(self):
        return self.norm_deaccel_rate
    
    def apply_change(self):
        self.actual_speed = self.commanded_speed if self.commanded_speed < self.speed_limit else self.speed_limit
        self.left_door_state = self.commanded_door_state