from CTC_Scheduler import CTC_Scheduler
from Code.CTC_GUI import MainWindow
from common import TrackModel
from CTC_Clock import CTC_Clock
from CTC_GUI import Ui_MainWindow as CTC_GUI

import sys
from PyQt5 import QtWidgets


#DO I STILL NEED THIS CLASS????
class CTC: 
    def __init__(self):
        self.clock = CTC_Clock()
        self.scheudle = CTC_Scheduler(self.clock)
        self.track_model = TrackModel()
        self.ui = CTC_GUI()
        self.add_ui()
        self.add_track_model()
        self.add_schedule()
        self.maintenance_mode()
        self.manual_dispatch()
    #CREATE UI
    def add_ui(self):
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
    
    #GET LAYOUT FROM TRACKMODEL
    def add_track_model(self):
        self.track_model.get_layout()
    
    def add_schedule(self):
        print("ADD SCHEDULE!!!!!")
        self.schedule.upload_schedule("./input/Schedule_v2.xlsx")
        while self.clock.get_time() < (23,59,59):
            self.scheudle.update_authority()
            self.clock.update_time(10)
    
    def maintenance_mode(self):
        print("MAINTENANCE!!!!!!!")
    
    def manual_dispatch(self):
        print("MANUAL DISPATCH")
        while self.clock.get_time() < (23,59,59):
            self.clock.update_time(10)

