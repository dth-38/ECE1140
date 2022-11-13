from PyQt5.QtCore import QTimer ,QThreadPool
from PyQt5.QtWidgets import QMainWindow

import Scheduler
import TrackController.TrackController
import Train_Controller
import TrainModel.Train
import TrackModel
#import CTC.CTC


class NSE_Simulation(QMainWindow):

    def __init__(self, run=False):
        #idk number of track controllers yet
        self.NUM_CONTROLLERS = 25
        self.SEC_TO_MSEC = 1000

        self.UPDATE_PERIOD = 1
        self.update_period_multiplier = 1


        self.track_controllers = []
        self.track = TrackModel.main.main()
        self.ctc = 0
    

        super().__init__()

        #creates track controllers
        for i in range(self.NUM_CONTROLLERS):
            self.track_controllers.append(TrackController.TrackController(i, False))


        self.scheduler = Scheduler.Scheduler()

        self.pool = QThreadPool.globalInstance()

        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.pool.start(self.scheduler))

        #allows us to start the system automatically by passing True when declaring the NSE_Sim
        if run == True:
            self.start_Sim()
        

    def start_sim(self, multiplier=0):
        if multiplier > 0:
            self.update_period_multiplier = multiplier

        #period is calculated in miliseconds cause thats what the timer takes
        period = (self.UPDATE_PERIOD / multiplier) * self.SEC_TO_MSEC

        self.timer.start(period)

    def stop_sim(self):
        self.timer.stop()


    def simulate(self):
        pass