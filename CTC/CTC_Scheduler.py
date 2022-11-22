import pandas as pd
import numpy as np
from datetime import datetime
from CTC.CTC_Clock import CTC_Clock
#TODO: GROUP SIGNALS FILE

#TODO: GET TRAIN FROM TRAIN MODEL AND LINE,STATION, AND TRACKMODEL FROM TRACK MODEL

from CTC.Train_Table import Train_Table
from CTC.Block_Table import Block_Table
from CTC.CTC_Clock import  CTC_Clock
from TrackModel.trackmodel import TrackModel

class CTC_Scheduler: 
    def __init__(self):
        self.authority = 0
        self.position = 0
        self.red_throughput = 0
        self.green_throughput = 0
        #TODO: ASK HOW DISPATCH QUEUE WORKS
        self.dispatch_queue = []
        self.train_table = Train_Table()
        self.block_table = Block_Table()
        self.train_id = 1
        #TODO: CREATE OBJECT OF TRACKMODEL
        #self.track_model = TrackModel()
        #route for trains, 0 = yard
        self.green_route_blocks = [0, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76,
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
                                   51, 52, 53, 54, 55, 56, 57, 58, 0]
        self.red_route_blocks = [0, 9, 8, 7, 6, 5, 4, 3, 2, 1, 16, 17, 18, 19, 20, 21, 22, 23,
                                 24, 25, 26, 27, 76, 75, 74, 73, 72, 33, 34, 35, 36, 37, 38, 71,
                                 70, 69, 68, 67, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55,
                                 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 52, 51, 50, 49, 48,
                                 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32,
                                 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16,
                                 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        self.red_schedule = []
        self.green_schedule = []
        self.train_states = []
        self.train_position = 0
        self.red_speed = 44
        self.green_speed = 44
        self.destination_index = 0
        self.red_stations = [[7,"Shadyside"],[16,"Herron_Ave"],
        [21,"Swissville"],[25,"Penn_Station"],[35,"Steel_Plaza"],[45,"First_Ave"],
        [48,"Station_Square"],[60,"South_Hills_Junction"]]
        self.green_stations = [[0,"Yard"],[2,"Pioneer"],[9,"Edgebrook"],[16,"Station"],[
            19,"Railway_Crossing"],[22,"Whited"],[31,"South_Bank"],[39,"Central"],
            [48,"Inglewood"],[57,"Overbrook"],[65,"Glenbury"],[73,"Dormont"],
            [77,"Mt_Lebanon"],[88,"Poplar"],[96,"Castle_Shannon"]]
    def upload_schedule(self,schedule):
        print("schedule: " + str(schedule))
        schedule = pd.read_excel(schedule)
        for index, row in schedule.iterrows():
            #print("LOOPING")
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
                arrival_time = row["arrival time"]
                print("arrival_time: " + str(arrival_time))
                if line == "Red":
                    self.red_schedule.append([line,station,time_to_station,arrival_time])
                elif line == "Green":
                    self.green_schedule.append([line,station,time_to_station,arrival_time])
    def manual_dispatch_train(self,departure_time,train_id,line,destinations):
        self.destination_index = 0
        #Dispatch queue only for scheduled dispatches? 
        #self.dispatch_queue.append([arrival_time,train_id])
        #TODO: CALL SORT DISPATCH QUEUE
        #self.sort_dispatch_queue()
        #TODO: Find out how to track authority to other stations, only working for authority to first station
        destinations = destinations.split()
        self.authority = self.calc_authority(train_id,line,destinations[self.destination_index])
        self.destination_index += 1
        travel_time = self.calc_travel_time(line)
        travel_hours = int(travel_time)
        travel_minutes = (travel_time*60) % 60
        travel_seconds = (travel_time*3600) % 60
        travel_time = (travel_hours,travel_minutes,travel_seconds)
        arrival_time = [int(travel_time[0] + departure_time[0]), int(travel_time[1] + departure_time[1]), int(travel_time[2] + departure_time[2])]
        self.train_table.add_entry(id=self.train_id,position=0,states=self.train_states,destinations=destinations,authority=self.authority,line=line,arrival_time=arrival_time)
        self.train_id += 1
        #add it to the yard
        #return the new entry added for each train dispatched
        return self.train_table.get_entry(self.train_id - 2), travel_time
    """""
    #TODO: FIND WAY TO CALL THIS FUNCTION CONTINUOUSLY?
    def schedule_dispatch(self,schedule_arrival,schedule_id,schedule_line,schedule_destinations):
        print("SCHEDULE DISPATCH!!!!!")
        #Calculate travel time to dest
        arrival_time = (int(schedule_arrival[0:2]),int(schedule_arrival[3:5]),schedule_arrival[6:8])
        #GET CURRENT TIME
        scheduled_time = arrival_time - self.time
        if scheduled_time == 0:
            #DO I NEED DISPATCH QUEUE???
            #self.dispatch_queue.append([scheduled_time,new_train])
            #self.sort_dispatch_queue()
            self.train_table.add_entry(id=self.train_id,position=self.train_position,states=self.train_states,line=schedule_line,arrival_time=schedule_arrival)
            self.train_id += 1
            #TODO: GET BLOCK OCCUPANCIES AND BLOCK FAILURES ARRAYS FROM TRACK CONTROLLER
            self.calc_authority()
    """
    def check_schedule(self,current_time):
        print("current_time: " + str(current_time))
        for i in range(len(self.red_schedule)):
            travel_time = self.red_schedule[i][2]
            travel_minutes = int(travel_time)
            travel_seconds = (travel_time*60) % 60
            arrival_time = self.red_schedule[i][3]
            arrival_time = str(arrival_time)
            hr, min, sec = arrival_time.split(':')
            arrival_time = (int(hr),int(min),int(sec))
            #print("schedule arrival_time: " + str(arrival_time))
            schedule_time = (current_time[0],current_time[1] + travel_minutes,current_time[2] + travel_seconds)
            #print("schedule_time: " + str(schedule_time))
            if schedule_time == arrival_time:
                self.manual_dispatch_train(departure_time=current_time,train_id=self.train_id,line=self.red_schedule[i][0],destinations=self.red_schedule[i][1])
        for i in range(len(self.green_schedule)):
            if schedule_time == arrival_time:
                self.manual_dispatch_train(departure_time=current_time,train_id=self.train_id,line=self.green_schedule[i][0],destinations=self.red_schedule[i][1])

    def calc_throughput(self,line,ticket_sales,hours):
        #TODO: GET TICKET SALES FROM TRACK MODEL
        if hours > 0:
            if line == "Red":
                self.red_throughput = ticket_sales/hours
                return self.red_throughput
            elif line == "Green":
                self.green_throughput = ticket_sales/hours
                return self.green_throughput
        else:
            return 0
    def calc_authority(self,train_id,line,destination):
        print("DESTINATION: " + str(destination))
        authority = 0
        destination_block = 0
        if line == "Red":
            for i in range(len(self.red_stations)):
                if self.red_stations[i][1] == destination:
                    destination_block = self.red_stations[i][0]
            for i in range(len(self.red_route_blocks)):
                if self.red_route_blocks[i] != destination_block:
                    authority += 1
                else:
                    return authority
        elif line == "Green":
            for i in range(len(self.green_stations)):
                if self.green_stations[i][1] == destination:
                    destination_block = self.green_stations[i][0]
                    print("Destination Block: " + str(destination_block))
            for i in range(len(self.green_route_blocks)):
                if self.green_route_blocks[i] != destination_block:
                    authority += 1
                else:
                    return authority
    """""
    #only working for one train
    def update_trains(self):
        if self.train_table.get_table_length() > 0:
            table_entry = self.train_table.get_entry(0)
            if table_entry[4] > 0:
                new_authority = table_entry[4] - 1
                self.authority = new_authority
                self.train_table.change_authority(0,self.authority)
                line = table_entry[5]
                if line == "Red":
                    for j in range(len(self.red_route_blocks) - 1):
                        if table_entry[1] == self.red_route_blocks[j]:
                            new_position = self.red_route_blocks[j + 1]
                            self.position = new_position
                            self.train_table.change_position(0,new_position)
                            break
                elif line == "Green":
                    #print("GREEN LINE!!!!")
                    for j in range(len(self.green_route_blocks) - 1):
                        if table_entry[1] == self.green_route_blocks[j]:
                            new_position = self.green_route_blocks[j + 1]
                            self.position = new_position
                            self.train_table.change_position(0,new_position)
                            break
            else:
                if self.destination_index < len(table_entry[3]):
                    self.authority = self.calc_authority(train_id=table_entry[0],line=table_entry[5],destination=table_entry[3][self.destination_index])
                    self.destination_index += 1
                    self.train_table.change_authority(0,self.authority)
        return self.authority, self.position
    """
    """"
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
    """
    """""
    def sort_dispatch_queue(self):
        dtype = [int,Train]
        self.dispatch_queue = np.array(self.dispatch_queue,dtype=dtype)
        self.dispatch_queue = np.sort(self.dispatch_queue,order=Train)
    """
    #TODO: GET ACTUAL DISTANCE OF EACH BLOCK FROM TRACKMODEL? Yes
    def calc_travel_time(self,line):
        dist = 0
        if line == "Red":
            for i in range(len(self.red_route_blocks)):
                dist += self.red_route_blocks[i]
            travel_time = dist/(self.red_speed*1000)
        elif line == "Green":
            for i in range(len(self.green_route_blocks)):
                dist += self.green_route_blocks[i]
            travel_time = dist/(self.green_speed*1000)
        return travel_time

