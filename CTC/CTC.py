from CTC_Scheduler import CTC_Scheduler
from CTC_GUI import Ui_MainWindow
from common import TrackModel
from CTC_Clock import CTC_Clock
from CTC_GUI import Ui_MainWindow

import sys
from PyQt5 import QtWidgets


class CTC: 
    def __init__(self, clk, sch, a_model):
        self.clock = clk
        self.scheudle = sch
        self.track_model = a_model
    #CREATE UI
    def add_ui(self):
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow(self.scheudle,self.clock)
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
    
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
