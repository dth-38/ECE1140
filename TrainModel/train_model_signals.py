#from Pyqt5.Qt import pyqtSignal
from PyQt5.QtCore import QObject, pyqtSignal


class SignalsClass(QObject):
    train_model_transfer_engine_falure = pyqtSignal()
    train_model_transfer_signal_pickup_failure = pyqtSignal()
    train_model_transfer_brake_failure = pyqtSignal()
    train_model_fix_failure = pyqtSignal()
    train_model_transfer_passenger_ebrake = pyqtSignal()

    test_power = pyqtSignal(float)    


signals = SignalsClass()