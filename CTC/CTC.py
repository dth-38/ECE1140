from CTC_Scheduler import CTC_Scheduler
from CTC_GUI import Ui_MainWindow
from common import TrackModel
from CTC_Clock import CTC_Clock
from CTC_GUI import Ui_MainWindow

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget

from Signals import signals
from TCTools import convert_to_block

class CTC(QWidget): 
    def __init__(self, clk, sch, a_model):
        self.clock = clk
        self.scheudle = sch
        self.track_model = a_model
        self.setup_signals()
    #CREATE UI
    def add_ui(self,ctc):
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow(ctc)
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
    def setup_signals(self):
        signals.ctc_update.connect(self.tick)
        signals.send_ctc_occupancy.connect(self.update_occupancy)
        signals.send_ctc_failure.connect(self.update_failure)
        signals.broadcast_switch.connect(self.update_switch)
        signals.broadcast_light.connect(self.update_light)
        signals.broadcast_gate.connect(self.update_gate)
    def update_occupancy(self,line,block_num,occ):
        num_trains = self.scheudle.train_table.get_table_length()
        if occ == 0:
            for i in range(num_trains):
                train = self.schedule.train_table.get_entry(i)
                if train[5] == line and train[1] == block_num:
                    #waiting state
                    train[1] = -1
        else:
            for i in range(num_trains):
                train = self.schedule.train_table.get_entry(i)
                if train[5] == line and train[1] == -1:
                    #change block position
                    train[1] = block_num
                    #decrement authority
                    train[4] -= 1
        self.scheudle.block_table.add_occupancy(line,block_num,occ)
    def update_failure(self,line,block_num,failure):
        self.schedule.block_table.add_failure(line,block_num,failure)
    def update_switch(self,line,block_num,next_block_num):
        self.scheudle.block_table.add_switch(line,block_num,next_block_num)
    def update_light(self,line,block,color):
        self.schedule.block_table.add_light(line,block,color)
    def update_gate(self,line,block_num,status):
        self.scheudle.block_table.add_gate(line,block_num,status)
    def tick(self): 
        if self.scheudle.train_table.get_table_length() > 0:
            tc_block = convert_to_block(self.scheudle.train_table.get_line(0),self.scheudle.train_table.get_position(0))
            signals.send_tc_authority.emit(tc_block,self.train_table.get_authority())
            if self.scheudle.train_table.get_line(0) == "Red":
                signals.send_tc_speed.emit(tc_block,self.scheudle.red_speed)
            elif self.scheudle.train_table.get_line(0) == "Green":
                signals.send_tc_speed.emit(tc_block,self.scheudle.green_speed)
            signals.send_tc_maintenance.emit(tc_block,0)
    


    #GET LAYOUT FROM TRACKMODEL
    def add_track_model(self):
        self.track_model.get_layout()
    
    def add_schedule(self):
        print("ADD SCHEDULE!!!!!")
        self.scheudle.upload_schedule("./input/Schedule_v2.xlsx")
        while self.clock.get_time() < (23,59,59):
            self.scheudle.update_authority()
            self.clock.update_time(10)
    
    def maintenance_mode(self):
        print("MAINTENANCE!!!!!!!")
    
    def manual_dispatch(self):
        print("MANUAL DISPATCH")
        while self.clock.get_time() < (23,59,59):
            self.clock.update_time(10)
