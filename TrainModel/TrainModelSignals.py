#from Pyqt5.Qt import pyqtSignal
from PyQt5.QtCore import QObject, pyqtSignal


class SignalsClass(QObject):
    train_model_transfer_engine_falure = pyqtSignal(int)
    train_model_transfer_signal_pickup_failure = pyqtSignal(int)
    train_model_transfer_brake_failure = pyqtSignal(int)
    train_model_fix_failure = pyqtSignal(int)
    train_model_transfer_passenger_ebrake = pyqtSignal(int)
    train_model_transfer_ac_cmd = pyqtSignal(int, int)


ui_sig = SignalsClass()