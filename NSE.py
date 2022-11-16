import sys


from PyQt5.QtCore import QTimer ,QThreadPool
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QGridLayout, QLineEdit, QWidget
from PyQt5.QtGui import QFont

import Scheduler
from TrackController.TrackController import TrackController
#import Train_Controller
#import TrainModel.Train
#import TrackModel
#import CTC.CTC


class NSE_Simulation(QMainWindow):

    def __init__(self, run=False):
        #idk number of track controllers yet
        self.NUM_CONTROLLERS = 14
        self.SEC_TO_MSEC = 1000

        self.X_OFFSET = 80
        self.Y_OFFSET = 600
        self.WIDTH = 600
        self.HEIGHT = 400

        self.UPDATE_PERIOD = 1
        self.MULTIPLIER_LIMIT = 15
        self.update_period_multiplier = 1


        self.track_controllers = []
        #self.track = TrackModel.main.main()
        self.ctc = 0
    

        super().__init__()


        #creates track controllers + calls tick to setup default track state
        for i in range(self.NUM_CONTROLLERS):
            self.track_controllers.append(TrackController(i, True))
            self.track_controllers[i].tick()


        self.scheduler = Scheduler.Scheduler()

        self.pool = QThreadPool.globalInstance()

        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.pool.start(self.scheduler))


        self.setup_GUI()
        self.show()

        #allows us to start the system automatically by passing True when declaring the NSE_Sim
        if run == True:
            self.start_clicked()
        else:
            self.stop_clicked()
        

    def start_sim(self, multiplier=0):
        if multiplier > 0 and multiplier < self.MULTIPLIER_LIMIT:
            self.update_period_multiplier = multiplier

        #period is calculated in miliseconds cause thats what the timer takes
        period = (self.UPDATE_PERIOD / multiplier) * self.SEC_TO_MSEC

        self.timer.start(period)

    def stop_sim(self):
        self.timer.stop()

#-------------------------------------------------------------
# UI Functionality
#-------------------------------------------------------------
    def setup_GUI(self):
        self.setGeometry(self.X_OFFSET, self.Y_OFFSET, self.WIDTH, self.HEIGHT)
        self.setWindowTitle("North Shore Extension Simulation")
        self.setMinimumSize(self.WIDTH, self.HEIGHT)

        self.main_widget = QWidget()

        widget_font = QFont('Times', 16)

        min_width = (self.WIDTH // 2) - 20
        min_height = (self.HEIGHT // 4) - 20

        self.ctc_button = QPushButton("CTC Office", self)
        self.ctc_button.clicked.connect(self.open_ctc)
        self.ctc_button.setFont(widget_font)
        self.ctc_button.setMinimumWidth(min_width)
        self.ctc_button.setMinimumHeight(min_height)

        self.track_model_button = QPushButton("Track Model", self)
        self.track_model_button.clicked.connect(self.open_track_model)
        self.track_model_button.setFont(widget_font)
        self.track_model_button.setMinimumWidth(min_width)
        self.track_model_button.setMinimumHeight(min_height)

        self.num_select_textbox = QLineEdit()
        self.num_select_textbox.setMaxLength(2)
        self.num_select_textbox.setMinimumWidth(min_width)
        self.num_select_textbox.setFont(widget_font)
        #self.num_select_textbox.setMinimumHeight(self.HEIGHT // 4)

        self.track_controller_button = QPushButton("Open Track Controller", self)
        self.track_controller_button.clicked.connect(self.open_track_controller)
        self.track_controller_button.setFont(widget_font)
        self.track_controller_button.setMinimumWidth(min_width)
        self.track_controller_button.setMinimumHeight(min_height)

        self.train_model_button = QPushButton("Open Train", self)
        self.train_model_button.clicked.connect(self.open_train_model)
        self.train_model_button.setFont(widget_font)
        self.train_model_button.setMinimumWidth(min_width)
        self.train_model_button.setMinimumHeight(min_height)

        self.train_controller_button = QPushButton("Open Train Controller", self)
        self.train_controller_button.clicked.connect(self.open_train_controller)
        self.train_controller_button.setFont(widget_font)
        self.train_controller_button.setMinimumWidth(min_width)
        self.train_controller_button.setMinimumHeight(min_height)
        
        self.start_button = QPushButton("Run Simulation", self)
        self.start_button.clicked.connect(self.start_clicked)
        self.start_button.setFont(widget_font)
        self.start_button.setMinimumWidth(min_width)
        self.start_button.setMinimumHeight(min_height)

        self.stop_button = QPushButton("Stop Simulation", self)
        self.stop_button.clicked.connect(self.stop_clicked)
        self.stop_button.setFont(widget_font)
        self.stop_button.setMinimumWidth(min_width)
        self.stop_button.setMinimumHeight(min_height)

        self.nse_layout = QGridLayout()

        self.nse_layout.addWidget(self.start_button, 0, 0)
        self.nse_layout.addWidget(self.stop_button, 0, 1)
        self.nse_layout.addWidget(self.ctc_button, 1, 0)
        self.nse_layout.addWidget(self.track_model_button, 1, 1)
        self.nse_layout.addWidget(self.num_select_textbox, 3, 0)
        self.nse_layout.addWidget(self.track_controller_button, 2, 1)
        self.nse_layout.addWidget(self.train_model_button, 3, 1)
        self.nse_layout.addWidget(self.train_controller_button, 4, 1)

        self.main_widget.setLayout(self.nse_layout)
        self.setCentralWidget(self.main_widget)


    def start_clicked(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.start_sim()

    def stop_clicked(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.stop_sim()

    def open_ctc(self):
        #self.ctc.show()
        pass


    def open_track_controller(self):
        try:
            num = int(self.num_select_textbox.text())

            if num > -1 and num < self.NUM_CONTROLLERS:
                self.track_controllers[num].show()
            else:
                print("Error: Selection does not exist.")
        except:
            print("Error: Selection is not a number.")

    def open_track_model(self):
        #self.track_model.show()
        pass

    def open_train_model(self):
        try:
            num = int(self.num_select_textbox.text())

            #check num is in valid range
            #open corresponding train model
        except:
            print("Error: Selection is not a number.")

        
    def open_train_controller(self):
        try:
            num = int(self.num_select_textbox.text())

            #check num is in valid range
            #open corresponding train controller
        except:
            print("Error: Selection is not a number.")




#-------------------------------------------
# MAIN FOR WHOLE PROJECT
#-------------------------------------------
if __name__ == "__main__":
    nse_simulation_app = QApplication([])

    sim = NSE_Simulation()

    sys.exit(nse_simulation_app.exec())
