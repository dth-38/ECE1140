from smtplib import LMTP
import sys
import math
import copy
from PyQt5 import QtWidgets
from PyQt5 import uic

from Signals import signals
from CTC.CTC_Scheduler import CTC_Scheduler
from CTC.CTC_Clock import CTC_Clock

from TrackController.TCTools import convert_to_block

#this is how you import ui directly
#if changes need to be made to ui, go to QtDesigner -> redesign -> simply save
form_mainWindow = uic.loadUiType("CTC/ctc_main.ui")[0]

class CTCWindowClass(QtWidgets.QMainWindow, form_mainWindow):
    def __init__(self):
        super(CTCWindowClass,self).__init__()
        self.setupUi(self)
        self.clock = CTC_Clock()
        self.schedule = CTC_Scheduler()
        self.setup_signals()
        self.init_ui()
        # self.show()

    #some temporarily function.
    def init_ui(self):
        self.train_entries = []
        self.block_entries = []
        self.destinations = []

        self.schedule_trains = 0
        self.manual_trains = 0

        self.dispatch_frame.hide()
        self.throughput_frame.hide()
        self.schedule_frame.hide()
        self.train_table_frame.hide()
        self.block_table_frame.hide()
        self.maintenance_frame.hide()

        self.maintenance_button.clicked.connect(lambda: self.maintenance_mode())
        self.manual_button.clicked.connect(lambda: self.manual_mode())
        self.dispatch_button.clicked.connect(lambda: self.dispatch())
        self.throughput_button.clicked.connect(lambda: self.output_throughput())
        self.schedule_button.clicked.connect(lambda: self.add_schedule())
        self.line_button.clicked.connect(lambda: self.destination_select())
        self.destination_add_button.clicked.connect(lambda: self.add_destination())
        self.clear_destination.clicked.connect(lambda: self.destination_clear())
        self.set_switch_maintenance_button.clicked.connect(lambda: self.switch_maintenance_pressed())
        self.set_block_maintenance_button.clicked.connect(lambda: self.block_maintenance_pressed())
        self.destination_block_add_button.clicked.connect(lambda: self.add_dispatch_block())
    
    def manual_mode(self):
        self.maintenance_frame.hide()
        self.dispatch_frame.show()
        self.throughput_frame.show()
        self.schedule_frame.show()
        self.train_table_frame.show()
        self.block_table_frame.show()
        self.block_table_display.clear()

    def maintenance_mode(self):
        self.dispatch_frame.hide()
        self.throughput_frame.hide()
        self.schedule_frame.hide()
        self.train_table_frame.hide()
        self.block_table_frame.show()
        self.maintenance_frame.show()
        self.block_table_display.clear()
        for i in range(len(self.schedule.block_table.switch)):
            self.block_table_display.addItem(str(self.schedule.block_table.get_switch(i)))

    def switch_maintenance_pressed(self):
        tc_block = convert_to_block(self.line_maintenance_selection.currentText().upper(),self.block_selection.value())
        tc_next_block = convert_to_block(self.line_maintenance_selection.currentText().upper(),self.next_block_selection.value())
        print("tc_block: " + str(tc_block))
        print("tc_next_block: " + str(tc_next_block))
        signals.set_tc_switch.emit(tc_block,tc_next_block)

    def block_maintenance_pressed(self):
        tc_block = convert_to_block(self.line_maintenance_selection.currentText().upper(),self.block_selection.value())
        #0 = open block, 1 = close block for maintenance
        if self.status_selection.currentText() == "Open":
            signals.send_tc_maintenance.emit(tc_block,0)
        elif self.status_selection.currentText() == "Close":
            signals.send_tc_maintenance.emit(tc_block,1)
        
    def destination_select(self):
        red_stations = ["Shadyside","Herron_Ave",
        "Swissville","Penn Station","Steel Plaza","First Ave",
        "Station Square","South Hills Junction"]
        green_stations = ["Pioneer","Edgebrook","Station",
            "Railway Crossing","Whited","South Bank","Central",
            "Inglewood","Overbrook","Glenbury","Dormont",
            "Mt Lebanon","Poplar","Castle Shannon"]
        self.destination_selection.clear()
        if self.line_train_selection.currentText() == "Red":
            self.destination_selection.addItems(red_stations)
        elif self.line_train_selection.currentText() == "Green":
            self.destination_selection.addItems(green_stations)

    def add_destination(self):
        self.destination_output.append(self.destination_selection.currentText())
        self.destinations.append(self.destination_selection.currentText())

    def add_dispatch_block(self):
        self.destination_output.append(self.starting_block_selection.toPlainText())
        self.destinations.append(self.starting_block_selection.toPlainText())

    def destination_clear(self):
        self.destination_output.clear()
        if len(self.destinations) > 0:
            self.destinations.clear()

    def dispatch(self):

        if self.hour_selection.toPlainText() == "" and self.minute_selection.toPlainText() == "" and self.second_selection.toPlainText() == "" or len(self.destinations) == 0 or math.isnan(float(self.hour_selection.toPlainText())):
            pass
        else:
            arrival_time = (int(self.hour_selection.toPlainText()),int(self.minute_selection.toPlainText()),int(self.second_selection.toPlainText()))
            travel_time = self.schedule.calc_travel_time(self.line_train_selection.currentText(),0,self.destinations[0])
            #sends dispatch signal
            #bruh
            #departure_time = [int(arrival_time[0] - travel_time[0]), int(arrival_time[1] - travel_time[1]), int(arrival_time[2] - travel_time[2])]

            #converts hrs,mins,secs to just hours to simplify rollover check
            arrival_real = arrival_time[0] + (arrival_time[1] / 60) + (arrival_time[2] / 3600)
            travel_real = travel_time[0] + (travel_time[1] / 60) + (travel_time[2] / 3600)

            dispatch_time = arrival_real - travel_real

            #check for day rollover
            if dispatch_time < 0:
                dispatch_time = 24 + dispatch_time
            elif dispatch_time > 24:
                dispatch_time -= 24

            #convert dispatch time in hours to hrs,mins,secs
            t_hrs = math.floor(dispatch_time)
            
            mins = (dispatch_time - t_hrs) * 60
            t_mins = math.floor(mins)

            secs = (mins - t_mins) * 60
            t_secs = math.floor(secs)

            departure_time = [t_hrs, t_mins, t_secs]

            print("DEPARTURE TIME: " + str(departure_time))
            current_time = self.clock.get_time()
            print("CURRENT TIME: "  + str(current_time))
            if current_time[0] == departure_time[0] and current_time[1] == departure_time[1] and current_time[2] == departure_time[2]:
                self.train_entries = self.schedule.manual_dispatch_train(arrival_time,self.manual_trains,self.line_train_selection.currentText(),self.destinations)
                print("manual train entry: " + str(self.schedule.train_table.get_entry(0)))
                line = str(self.train_entries[5])
                line.upper()
                signals.send_tm_dispatch.emit(line)
                tc_block = convert_to_block(self.train_entries[5],self.train_entries[1])
                signals.send_tc_authority.emit(tc_block,self.train_entries[4])

                self.train_table_display.addItem("MANUAL TRAIN DISPATCHED!!!!!!!!!")
                self.train_table_display.addItem("Train #: " + str(self.train_entries[0]))
                self.train_table_display.addItem("Position: " + str(self.train_entries[1]))
                self.train_table_display.addItem("Destinations: " + str(self.train_entries[3]))
                self.train_table_display.addItem("Authority: " + str(self.train_entries[4]))
                self.train_table_display.addItem("Line: " + str(self.train_entries[5]))
                self.train_table_display.addItem("Arrival Time: " + str(self.train_entries[6]))
            
                self.manual_trains += 1
    
    def schedule_output(self,train):
        self.schedule_list.addItem("SCHEDULE TRAIN DISPATCHED!!!!!!!!!")
        self.schedule_list.addItem("Train #: " + str(train[0]))
        self.schedule_list.addItem("Position: " + str(train[1]))
        self.schedule_list.addItem("Destinations: " + str(train[3]))
        self.schedule_list.addItem("Authority: " + str(train[4]))
        self.schedule_list.addItem("Line: " + str(train[5]))
        self.schedule_list.addItem("Arrival Time: " + str(train[6]))

        self.schedule_trains += 1
        
        
    #TODO GET TICKET SALES FROM TRACKMODEL
    def output_throughput(self):
        line = self.line_throughput_selection.currentText()
        #TODO: GET TICKET SALES FROM THE TRACKMODEL
        if self.current_hour.toPlainText() != "":
            throughput = self.schedule.get_throughput(line)
            self.throughput_output.setText(str(throughput))
    
    def add_schedule(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self,"Open File", "", "All Files (*);;Xlsx Files(*.xlsx)")
        print("file_name: " + str(file_name[0]))
        if file_name[0] != "":
            self.schedule.upload_schedule(file_name[0])
     
    def update_current_time(self):
        self.clock.get_time()
        self.current_hour.setText(str(self.clock.get_hours()))
        self.current_minute.setText(str(self.clock.get_minutes()))
        self.current_second.setText(str(self.clock.get_seconds()))
        for i in range(self.manual_trains):
            if self.schedule.train_table.get_authority(i) == 0:
                next_destination = self.schedule.train_table.get_next_destination(i)
                print("next destination: " + str(next_destination))
                authority = self.schedule.calc_authority(self.schedule.train_table.get_train_id(i),self.schedule.train_table.get_line(i),next_destination,self.schedule.train_table.get_position(i))
                print("next authority: " + str(authority))

                #you forgot to set the new authority
                self.schedule.train_table.set_authority(i, authority)

                tc_block = convert_to_block(self.schedule.train_table.get_line(i),self.schedule.train_table.get_position(i))
                signals.send_tc_authority.emit(tc_block,self.schedule.train_table.get_authority(i))
                travel_time = self.schedule.calc_travel_time(self.schedule.train_table.get_line(i),self.schedule.train_table.get_position(i),next_destination)
                print("next travel_time: " + str(travel_time))
                arrival_time = [int(travel_time[0] + int(self.current_hour.toPlainText())), int(travel_time[1] + int(self.current_minute.toPlainText())), int(travel_time[2] + int(self.current_second.toPlainText()))]
                self.schedule.train_table.change_authority(i,authority)
                self.train_table_display.takeItem((i*6) + (i + 2))
                self.train_table_display.insertItem((i*6) + (i + 2),"Position: " + str(self.schedule.train_table.get_position(i)))
                self.train_table_display.takeItem((i*6) + (i + 4))
                self.train_table_display.insertItem((i*6) + (i + 4),"Authority: " + str(self.schedule.train_table.get_authority(i)))
                self.train_table_display.takeItem((i*6) + (i + 6))
                self.train_table_display.insertItem((i*6) + (i + 6),"Arrival Time: " + str(arrival_time))
            else:
                self.train_table_display.takeItem((i*6) + (i + 2))
                self.train_table_display.insertItem((i*6) + (i + 2),"Position: " + str(self.schedule.train_table.get_position(i)))
                self.train_table_display.takeItem((i*6) + (i + 4))
                self.train_table_display.insertItem((i*6) + (i + 4),"Authority: " + str(self.schedule.train_table.get_authority(i)))

        for i in range(self.schedule_trains):
            if self.schedule.train_table.get_authority(i) == 0:
                authority = self.schedule.calc_authority(self.schedule.train_table.get_train_id(i),self.schedule.train_table.get_line(i),self.schedule.train_table.get_next_destination(i),self.schedule.train_table.get_position(i))
                self.schedule.train_table.change_authority(i,authority)
                self.schedule_list.takeItem((i*6) + (i + 2))
                self.schedule_list.insertItem((i*6) + (i + 2),"Position: " + str(self.schedule.train_table.get_position(i)))
                self.schedule_list.takeItem((i*6) + (i + 4))
                self.schedule_list.insertItem((i*6) + (i + 4),"Authority: " + str(self.schedule.train_table.get_authority(i)))
            else:
                self.schedule_list.takeItem((i*6) + (i + 2))
                self.schedule_list.insertItem((i*6) + (i + 2),"Position: " + str(self.schedule.train_table.get_position(i)))
                self.schedule_list.takeItem((i*6) + (i + 4))
                self.schedule_list.insertItem((i*6) + (i + 4),"Authority: " + str(self.schedule.train_table.get_authority(i)))
    
    def setup_signals(self):
        signals.ctc_update.connect(self.tick)
        signals.send_ctc_ticket_sales.connect(self.update_ticket_sales)
        signals.send_ctc_occupancy.connect(self.update_occupancy)
        signals.send_ctc_failure.connect(self.update_failure)
        signals.send_ctc_train_position.connect(self.update_position)
        signals.broadcast_switch.connect(self.update_switch)
        #signals.broadcast_light.connect(self.update_light)
        #signals.broadcast_gate.connect(self.update_gate)
    def update_position(self,train_id,line,block_number):
        #print("UPDATING POSITION")
        self.schedule.train_table.change_position(train_id,block_number)
        authority = self.schedule.train_table.get_authority(train_id)
        self.schedule.train_table.change_authority(train_id,authority-1)
    def update_occupancy(self,line,block_num,occ):
        contains = False
        num_trains = self.schedule.train_table.get_table_length()
        if occ == 0:
            for i in range(num_trains):
                train = self.schedule.train_table.get_entry(i)
                temp = train[5].upper()
                if temp == line and train[1] == block_num:
                    #waiting state
                    #print("Waiting State")
                    train[1] = -1
        else:
            #print("Occupied")
            for i in range(num_trains):
                train = self.schedule.train_table.get_entry(i)
                temp = train[5].upper()
                if temp == line and train[1] == -1:
                    #change block position
                    train[1] = block_num
                    #decrement authority
                    #print("authority decremented")
                    train[4] -= 1
                for item in self.schedule.block_table.table:
                    if item[1] == line and item[2] == block_num:
                        contains == True
                if contains == False:
                    self.schedule.block_table.add_occupancy(line,block_num,occ)
                    self.block_table_display.addItem("Train " + str(i) + ": " + str(self.schedule.block_table.get_last_entry()))
            if contains == True:
                self.block_table_display.clear()
    def update_failure(self,line,block_num,failure):
        self.schedule.block_table.add_failure(line,block_num,failure)
    def update_switch(self,line,block_num,next_block_num):
        self.schedule.block_table.add_switch(line,block_num,next_block_num)
    def update_light(self,line,block,color):
        self.schedule.block_table.add_light(line,block,color)
    def update_gate(self,line,block_num,status):
        self.schedule.block_table.add_gate(line,block_num,status)
    def update_ticket_sales(self,line,ticket_sales):
        self.schedule.calc_throughput(line,ticket_sales,self.clock.get_hours())
    def tick(self):
        schedule_train = self.schedule.check_schedule(self.clock.get_time())
        if len(schedule_train) > 0:
            self.schedule_output(schedule_train)
            line = str(schedule_train[5])
            line.upper()
            signals.send_tm_dispatch.emit(line)
            tc_block = convert_to_block(self.train_entries[5],self.train_entries[1])
            signals.send_tc_authority.emit(tc_block,schedule_train[4])
        self.update_current_time()
        for i in range(self.schedule.train_table.get_table_length()): 
            tc_block = convert_to_block(self.schedule.train_table.get_line(i),self.schedule.train_table.get_position(i))
            suggested_speed = self.schedule.calc_suggested_speed(self.schedule.train_table.get_line(i),self.schedule.train_table.get_position(i))
            #print("suggested speed: " + str(suggested_speed))
            s_speed = int(round(suggested_speed, 0))
            signals.send_tc_speed.emit(tc_block,s_speed)
            # if self.schedule.train_table.get_line(i) == "Red":
            #     signals.send_tc_speed.emit(tc_block,self.schedule.red_speed)
            # elif self.schedule.train_table.get_line(i) == "Green":
            #     signals.send_tc_speed.emit(tc_block,self.schedule.green_speed)
        self.clock.update_time()
    

    


#to run this file as main
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ctc_window = CTCWindowClass()
    sys.exit(app.exec_())