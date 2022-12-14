from CTC.CTC_Scheduler import CTC_Scheduler
from CTC.CTC_GUI import Ui_MainWindow
#from TrackModel import TrackModel
from CTC.CTC_Clock import CTC_Clock
#from CTC.CTC_main import CTCWindowClass

#import sys
from PyQt5 import QtWidgets

from Signals import signals
from TrackController.TCTools import convert_to_block


class CTC(): 
    def __init__(self):
        super().__init__()

        self.clock = CTC_Clock()
        self.schedule = CTC_Scheduler()
        # self.setupUi()
        self.setup_signals()
        #self.add_ui()
    #CREATE UI
    def add_ui(self):
        pass
        #ctcmainwindow = CTCWindowClass(self)
        #self.MainWindow.setupUi(self.MainWindow)
        #self.MainWindow.show()
        #sys.exit(app.exec_())
    def setup_signals(self):
        signals.ctc_update.connect(self.tick)
        signals.send_ctc_ticket_sales.connect(self.update_ticket_sales)
        signals.send_ctc_occupancy.connect(self.update_occupancy)
        signals.send_ctc_failure.connect(self.update_failure)
        signals.broadcast_switch.connect(self.update_switch)
        signals.broadcast_light.connect(self.update_light)
        signals.broadcast_gate.connect(self.update_gate)
    def update_occupancy(self,line,block_num,occ):
        print("updating occupancy")
        print("occ: " + str(occ))
        num_trains = self.schedule.train_table.get_table_length()
        if occ == 0:
            for i in range(num_trains):
                train = self.schedule.train_table.get_entry(i)
                temp = train[5].upper()
                if temp == line and train[1] == block_num:
                    #waiting state
                    print("Waiting State")
                    train[1] = -1
        else:
            print("Occupied")
            for i in range(num_trains):
                train = self.schedule.train_table.get_entry(i)
                temp = train[5].upper()
                if temp == line and train[1] == -1:
                    #change block position
                    train[1] = block_num
                    #decrement authority
                    print("authority decremented")
                    train[4] -= 1
        self.schedule.block_table.add_occupancy(line,block_num,occ)
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
        # if len(schedule_train) > 0:
        #     self.ui.schedule_output(schedule_train)
        #self.ui.update_current_time()
        for i in range(self.schedule.train_table.get_table_length()): 
            tc_block = convert_to_block(self.schedule.train_table.get_line(i),self.schedule.train_table.get_position(i))
            signals.send_tc_authority.emit(tc_block,self.schedule.train_table.get_authority(i))
            if self.schedule.train_table.get_line(i) == "Red":
                signals.send_tc_speed.emit(tc_block,self.schedule.red_speed)
            elif self.schedule.train_table.get_line(i) == "Green":
                signals.send_tc_speed.emit(tc_block,self.schedule.green_speed)
        self.clock.update_time()

