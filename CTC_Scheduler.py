from copyreg import dispatch_table
import sched
import pandas as pd
import numpy as np
from CTC_Clock import CTC_Clock
#TODO: GROUP SIGNALS FILE
#from signals import signals
#TODO: GET TRAIN FROM TRAIN MODEL AND LINE,STATION, AND TRACKMODEL FROM TRACK MODEL
from common import Train, Line, Station, TrackModel
from Train_Table import Train_Table
from Block_Table import Block_Table
from CTC_Clock import  CTC_Clock

class CTC_Scheduler: 
    def __init__(self,auth=0,speed=0,through=0):
        self.authority = auth
        self.suggested_speed = speed
        self.throughput = through
        self.time = CTC_Clock()
        #TODO: ASK HOW DISPATCH QUEUE WORKS
        self.dispatch_queue = []
        self.train_table = Train_Table()
        self.block_table = Block_Table()
        self.train_id = 1
        #TODO: CREATE OBJECT OF TRACKMODEL
        self.track_model = TrackModel()
        self.green_route_blocks = [-1, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76,
                                   77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92,
                                   93, 94, 95, 96, 97, 98, 99, 100, 85, 84, 83, 82, 81, 80, 79, 78,
                                   77, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112,
                                   113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125,
                                   126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138,
                                   139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 29,
                                   28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13,
                                   1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
                                   19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
                                   35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
                                   51, 52, 53, 54, 55, 56, 57, 58, -1]
        self.red_route_blocks = [-1, 9, 8, 7, 6, 5, 4, 3, 2, 1, 16, 17, 18, 19, 20, 21, 22, 23,
                                 24, 25, 26, 27, 76, 75, 74, 73, 72, 33, 34, 35, 36, 37, 38, 71,
                                 70, 69, 68, 67, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55,
                                 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 52, 51, 50, 49, 48,
                                 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32,
                                 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16,
                                 1, 2, 3, 4, 5, 6, 7, 8, 9, -1]
        self.block_occupancies = []
        self.block_failures = []
        self.ticket_sales = 0
        self.train_states = []
        self.train_position = 0
        self.red_speed = 50
        self.green_speed = 50
        #TODO: GET SIGNALS FROM OTHER MODULES
        """"
        signals.update_occupancy.connect(self.get_block_occupancies)
        signals.update_failure.connect(self.get_block_failures)
        signals.update_ticket_sales.connect(self.get_ticket_sales)
        signals.update_train_states(self.get_train_states)
        signals.update_train_position(self.get_train_position)
        """
    def upload_schedule(self,schedule):
        schedule = pd.read_excel(schedule,sheet_name=6)
        print(schedule)
        for index, row in schedule.iterrows():
            if str(row[0]) == "nan" or str(row["Infrastructure"]) == "nan" or str(row["total time to station w/dwell (min)"]) == "nan":
                continue
            else: 
                line = row[0]
                print("Line: " + str(line))
                infrastructure = str(row["Infrastructure"])
                stations = infrastructure.split(";")
                if len(stations) >= 2:
                    station = stations[1]
                    print("station: " + str(station))
                #print("Infrastructure: " + str(infrastructure))
                time_to_station = row["total time to station w/dwell (min)"]
                print("time to station: " + str(time_to_station))
                arrival_time = row["Arrival time"]
                self.schedule_dispatch(arrival_time,self.train_id,line,station)
                self.train_id += 1
                self.calc_authority()
    def manual_dispatch_train(self,arrival_time,train_id,line,destinations):
        print("MANUAL DISPATCH!!!!")
        if line == "Red":
            new_train = Train(train_id,route=self.red_route_blocks)
        elif line == "Green":
            new_train = Train(train_id,route=self.green_route_blocks)
        self.dispatch_queue.append([arrival_time,new_train])
        self.sort_dispatch_queue()
        #TODO: GET TRAIN STATES FROM TRAIN MODEL???
        #TODO: GET BLOCK OCCUPANCIES AND BLOCK FAILURES ARRAYS FROM TRACK CONTROLLER
        self.calc_authority(new_train,line,self.block_occupancies,self.block_failures)
        self.train_table.add_entry(id=self.train_id,position=self.train_position,states=self.train_states,authority=self.authority)
        self.train_id += 1
    #TODO: FIND WAY TO CALL THIS FUNCTION CONTINUOUSLY?
    def schedule_dispatch(self,schedule_arrival,schedule_id,schedule_line,schedule_destinations):
        print("SCHEDULE DISPATCH!!!!!")
        #Calculate travel time to dest
        arrival_time = (int(schedule_arrival[0:2]),int(schedule_arrival[3:5]),schedule_arrival[6:8])
        #IS THIS RIGHT?????
        scheduled_time = arrival_time - self.time
        if scheduled_time == 0:
            #TODO: dispatch train
            if schedule_line == "Red":
                new_train = Train(self.train_id,route=self.red_route_blocks)
            elif schedule_line == "Green":
                new_train = Train(self.train_id,route=self.green_route_blocks)
            self.dispatch_queue.append([scheduled_time,new_train])
            self.sort_dispatch_queue()
            self.train_table.add_entry(id=self.train_id,position=self.train_position,states=self.train_states)
            self.train_id += 1
            #TODO: GET BLOCK OCCUPANCIES AND BLOCK FAILURES ARRAYS FROM TRACK CONTROLLER
            self.calc_authority(new_train,schedule_line,self.block_occupancies,self.block_failures)
    def view_throughput(self,line):
        self.throughput = self.calc_throughput(line)
    def calc_throughput(self,line):
        #TODO: GET TICKET SALES FROM TRACK MODEL
        ticket_sales = line.get_ticket_sales()
        self.throughput = self.ticket_sales/self.time.get_hours()
        #TODO: FIND WAY TO DISPLAY THROUGHPUT
        return self.throughput
    def set_authority(self,new_train,authority):
        print("SET AUTHORITY!!!!")
        #TODO: CAN I DO THIS????
        new_train.set_authority(authority)
    #TODO: FIND OUT HOW TO SET SUGGESTED SPEED
    def set_speed(self,new_train,speed):
        print("SET SPEED!!!!")
        #TODO: CAN I DO THIS????
        new_train.set_speed(speed)
    def calc_authority(self,new_train,line,block_occ,block_failure):
        self.authority = 0
        if line.get_name() == "Red":
            for i in range(len(self.red_route_blocks) - 1):
                next_block_index = self.red_route_blocks[i + 1]
                #check if next block ins't occupied
                if block_occ[next_block_index + 1] == 0 and block_failure == 0:
                    self.authority += 1
        elif line.get_name() == "Green":
            for i in range(len(self.green_route_blocks) - 1):
                next_block_index = self.red_route_blocks[i + 1]
                #check if next block ins't occupied
                if block_occ[next_block_index + 1] == 0 and block_failure == 0:
                    self.authority += 1
        #AM I ALLOWED TO DO THIS???
        #PROBABLY SHOULD SEND A SIGNAL TO TRACK CONTROLLER HERE WITH THE AUTHORITY  
        new_train.set_auhtority(self.authority)
    def update_authority(self,current_train,line,block_occ,block_failure):
        #TODO: CHECK EDGE CASES     
        location = current_train.get_position()
        if line.get_name() == "Red":
            next_block_index = self.red_route_blocks[location + 1]
            if block_occ[next_block_index + 1] == 0 and block_failure[next_block_index + 1] == 0:
                self.authority += 1
        elif line.get_name() == "Green":
            next_block_index = self.green_route_blocks[location + 1]
            if block_occ[next_block_index + 1] == 0 and block_failure[next_block_index + 1] == 0:
                self.authority += 1
    def sort_dispatch_queue(self):
        dtype = [int,Train]
        self.dispatch_queue = np.array(self.dispatch_queue,dtype=dtype)
        self.dispatch_queue = np.sort(self.dispatch_queue,order=Train)
    def calc_travel_time(self,line):
        dist = 0
        if line == "Red":
            for i in range(len(self.red_route_blocks)):
                dist += self.red_route_blocks[i]
            travel_time = self.red_speed/dist
        elif line == "Green":
            for i in range(len(self.green_route_blocks)):
                dist += self.red_route_blocks[i]
            travel_time = self.green_speed/dist
    def get_block_occupancies(self,block_occupancies):
        self.block_occupancies = block_occupancies
    def get_block_failures(self,block_failures):
        self.block_failures = block_failures
    def get_ticket_sales(self,ticket_sales):
        self.ticket_sales = ticket_sales
    def get_train_states(self,engine_failure,brake_failure):
        self.train_states = [engine_failure,brake_failure]
    def get_train_position(self,position):
        self.train_position = position
    """"
    def calculate_route(self,line):
        print("ROUTE!!!!")
        if line.get_name() == "Red":
            for i in range(len(self.red_route_blocks)):
                self.red_route_blocks[i]
        elif line.get_name() == "Green":
            for j in range(len(self.green_route_blocks)):
                self.green_route_blocks[j]
    """
