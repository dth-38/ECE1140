import sys
import math

from PyQt5.QtCore import QTimer ,QThreadPool, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QGridLayout, QLineEdit, QWidget, QSlider, QComboBox
from PyQt5.QtGui import QFont

import Scheduler
from TrackController.TrackController import TrackController
from CTC.CTC_main import CTCWindowClass
from TrackModelV2.TrackModel import TrackModel
from Signals import signals


class NSE_Simulation(QMainWindow):

    def __init__(self, run=False):
        #idk number of track controllers yet
        self.NUM_CONTROLLERS = 18
        self.SEC_TO_MSEC = 1000

        self.X_OFFSET = 80
        self.Y_OFFSET = 600
        self.WIDTH = 600
        self.HEIGHT = 400

        self.UPDATE_PERIOD = 1
        self.MULTIPLIER_LIMIT = 50
        self.update_period_multiplier = 1


        self.track_controllers = []
        self.ctc = CTCWindowClass()
        self.track = TrackModel()
        self.run_state = False
        self.running_trains = 0
        

        super().__init__()


        #creates track controllers + calls tick to setup default track state
        for i in range(self.NUM_CONTROLLERS):
            self.track_controllers.append(TrackController(i, True))
            self.track_controllers[i].tick()


        self.pool = QThreadPool.globalInstance()

        self.timer = QTimer()
        self.timer.timeout.connect(self.create_scheduler)


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

            #updates gui with new multiplier
            try:
                label_str = "Multiplier: " + str(self.update_period_multiplier)
            except:
                label_str = "Multiplier: "
            self.multiplier_label.setText(label_str)

        #self.multiplier_input.setText(str(self.update_period_multiplier))

        #period is calculated in miliseconds cause thats what the timer takes
        period = (self.UPDATE_PERIOD / self.update_period_multiplier) * self.SEC_TO_MSEC
        period = math.floor(period)

        self.timer.start(period)

    def stop_sim(self):
        self.timer.stop()

#-------------------------------------------------------------
# UI Functionality
#-------------------------------------------------------------
    def setup_GUI(self):
        signals.update_main.connect(self.tick)

        self.setGeometry(self.X_OFFSET, self.Y_OFFSET, self.WIDTH, self.HEIGHT)
        self.setWindowTitle("North Shore Extension Simulation")
        self.setMinimumSize(self.WIDTH, self.HEIGHT)

        self.main_widget = QWidget()

        widget_font = QFont('Times', 16)

        min_width = (self.WIDTH // 2) - 20
        min_height = (self.HEIGHT // 6) - 20

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

        self.tc_dropdown = QComboBox()
        self.tc_dropdown.setFont(widget_font)
        try:
            cont_strings = []
            for i in range(self.NUM_CONTROLLERS):
                cont_strings.append(str(i))
        except Exception as e:
            print(e)
            cont_strings = [""]

        self.tc_dropdown.addItems(cont_strings)
        self.tc_dropdown.setMinimumWidth(min_width)
        self.tc_dropdown.setMinimumHeight(min_height)

        self.tm_dropdown = QComboBox()
        self.tm_dropdown.setFont(widget_font)
        self.tm_dropdown.setMinimumWidth(min_width)
        self.tm_dropdown.setMinimumHeight(min_height)

        self.tmc_dropdown = QComboBox()
        self.tmc_dropdown.setFont(widget_font)
        self.tmc_dropdown.setMinimumHeight(min_height)
        self.tmc_dropdown.setMinimumWidth(min_width)

        # self.tc_textbox = QLineEdit()
        # self.tc_textbox.setMaxLength(2)
        # self.tc_textbox.setMinimumWidth(min_width / 5)
        # self.tc_textbox.setAlignment(Qt.AlignRight)
        # self.tc_textbox.setFont(widget_font)
        # #self.num_select_textbox.setMinimumHeight(self.HEIGHT // 4)

        # self.tm_textbox = QLineEdit()
        # self.tm_textbox.setMaxLength(2)
        # self.tm_textbox.setMinimumWidth(min_width / 5)
        # self.tm_textbox.setFont(widget_font)
        # self.tm_textbox.setAlignment(Qt.AlignRight)

        # self.tmc_textbox = QLineEdit()
        # self.tmc_textbox.setMaxLength(2)
        # self.tmc_textbox.setMinimumWidth(min_width / 5)
        # self.tmc_textbox.setFont(widget_font)
        # self.tmc_textbox.setAlignment(Qt.AlignRight)

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
        
        self.start_button = QPushButton("Start/Stop Simulation", self)
        self.start_button.clicked.connect(self.toggle_clicked)
        self.start_button.setFont(QFont('Times', 18))
        self.start_button.setMinimumWidth(min_width)
        self.start_button.setMinimumHeight(min_height)

        self.running_label = QLabel("Stopped")
        self.running_label.setFont(QFont('Times', 18))
        self.running_label.setStyleSheet("color: red")
        self.running_label.setAlignment(Qt.AlignCenter)
        self.running_label.setMinimumWidth(min_width)
        self.running_label.setMinimumHeight(min_height)

        self.multiplier_input = QLineEdit()
        self.multiplier_input.setMaxLength(2)
        self.multiplier_input.setMinimumWidth(min_width)
        self.multiplier_input.setFont(widget_font)
        self.multiplier_input.setText(str(self.update_period_multiplier))
        
        self.multiplier_label = QLabel()
        try:
            label_str = "Multiplier: " + str(self.update_period_multiplier)
        except:
            label_str = "Multiplier: "
        self.multiplier_label.setText(label_str)
        self.multiplier_label.setMinimumWidth(min_width)
        self.multiplier_label.setMinimumHeight(min_height)
        self.multiplier_label.setFont(widget_font)

        self.multiplier_slider = QSlider(Qt.Horizontal)
        self.multiplier_slider.setFont(widget_font)
        self.multiplier_slider.setMinimumWidth(min_width)
        self.multiplier_slider.setMinimumHeight(min_height)
        self.multiplier_slider.setMinimum(1)
        self.multiplier_slider.setMaximum(self.MULTIPLIER_LIMIT)
        self.multiplier_slider.valueChanged.connect(self.check_multiplier)
        self.multiplier_slider.setSingleStep(5)
        self.multiplier_slider.setValue(1)
        self.multiplier_slider.setTickPosition(QSlider.TicksBelow)
        self.multiplier_slider.setTickInterval(10)

        self.nse_layout = QGridLayout()

        self.nse_layout.addWidget(self.start_button, 0, 0)
        self.nse_layout.addWidget(self.running_label, 0, 1)
        self.nse_layout.addWidget(self.multiplier_label, 1, 0)
        self.nse_layout.addWidget(self.multiplier_slider, 1, 1)
        self.nse_layout.addWidget(self.ctc_button, 2, 0)
        self.nse_layout.addWidget(self.track_model_button, 2, 1)
        self.nse_layout.addWidget(self.tc_dropdown, 3, 0)
        self.nse_layout.addWidget(self.tm_dropdown, 4, 0)
        self.nse_layout.addWidget(self.tmc_dropdown, 5, 0)
        self.nse_layout.addWidget(self.track_controller_button, 3, 1)
        self.nse_layout.addWidget(self.train_model_button, 4, 1)
        self.nse_layout.addWidget(self.train_controller_button, 5, 1)

        self.main_widget.setLayout(self.nse_layout)
        self.setCentralWidget(self.main_widget)


    def toggle_clicked(self):
        #toggles the running state
        #and runs the appropriate function to start/stop
        if self.run_state == True:
            self.run_state = False
            self.stop_clicked()

        else:
            self.run_state = True
            self.start_clicked()


    def start_clicked(self):
        #mult = self.multiplier_input.text()
        #try:
        #    mult = int(mult)
        #except:
            #mult = 0
            #print("Error: multiplier not a number")

        self.running_label.setText("Running")
        self.running_label.setStyleSheet("color: green")
        self.start_sim()

    def stop_clicked(self):
        self.running_label.setText("Stopped")
        self.running_label.setStyleSheet("color: red")
        self.stop_sim()

    def open_ctc(self):
        self.ctc.show()


    def open_track_controller(self):
        try:
            #num = int(self.tc_textbox.text())
            num = int(self.tc_dropdown.currentText())

            if num > -1 and num < self.NUM_CONTROLLERS:
                self.track_controllers[num].show()
            else:
                print("Error: Selection does not exist.")
        except:
            print("Error: Selection is not a number.")

    def open_track_model(self):
        self.track.gui.show()

    def open_train_model(self):
        try:
            num = int(self.tm_dropdown.currentText())
            #num = int(self.tm_textbox.text())
            #check num is in valid range
            #open corresponding train model
            if num > -1:
                signals.open_tm_gui.emit(num)
            else:
                print("Error: Selection does not exist.")
        except:
            print("Error: Selection is not a number.")

        
    def open_train_controller(self):
        try:
            #num = int(self.tmc_textbox.text())
            num = int(self.tmc_dropdown.currentText())

            #check num is in valid range
            #open corresponding train controller
            if num > -1:
                signals.open_tc_gui.emit(num)
            else:
                print("Error: Selection does not exist.")

        except:
            print("Error: Selection is not a number.")


    def create_scheduler(self):
        s = Scheduler.Scheduler()
        self.pool.start(s)

    def check_multiplier(self):
        self.update_period_multiplier = self.multiplier_slider.value()

        try:
            label_str = "Multiplier: " + str(self.update_period_multiplier)
        except:
            label_str = "Multiplier: "

        self.multiplier_label.setText(label_str)

        if self.run_state == True:
            self.start_sim()

    def tick(self):
        train_amount = len(self.track.trains)
        if self.running_trains != train_amount:

            self.running_trains = train_amount

            if train_amount != 0:
                trains = list(self.track.trains.keys())
                
                try:
                    for i in range(len(trains)):
                        trains[i] = str(trains[i])
                except Exception as e:
                    print(e)
                    trains = [""]
            else:
                trains = [""]

            self.tm_dropdown.clear()
            self.tm_dropdown.addItems(trains)

            self.tmc_dropdown.clear()
            self.tmc_dropdown.addItems(trains)

#-------------------------------------------
# MAIN FOR WHOLE PROJECT
#-------------------------------------------
if __name__ == "__main__":
    nse_simulation_app = QApplication([])

    sim = NSE_Simulation()

    sys.exit(nse_simulation_app.exec())
