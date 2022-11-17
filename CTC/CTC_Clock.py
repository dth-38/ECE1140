
class CTC_Clock:
    def __init__(self,hr=0,min=0,sec=0):
        self.hour = hr
        self.minute = min
        self.second = sec 
    def update_time(self,timeStep=10):
        #print("TIME UPDATE")
        #TODO: FIND A WAY TO CALL THIS EVERY SECOND DURING SIMULATION
        temp_time = self.second + timeStep
        if temp_time < 60:
            self.second += timeStep
        elif temp_time >= 60 and self.minute < 59:
            self.minute += 1
            self.second = 0
        elif temp_time >= 60 and self.minute >= 59:
            self.hour += 1
            self.minute = 0
            self.second = 0
    def check_dispatch(self,hr,min,sec):
        #if theres a train to dispatch at self.hour,..... 
        dispatch = False
        if self.hour == hr and self.minute == min and self.second == sec:
            dispatch = True
        #then dispatch train to yard 
        #remove dispatch order
        return dispatch 
    def get_time(self):
        return (self.hour,self.minute,self.second)
    def get_hours(self):
        return self.hour 
    def get_minutes(self):
        return self.minute 
    def get_seconds(self):
        return self.second
        