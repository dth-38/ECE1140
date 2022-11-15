from typing import list

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

class Signals(QObject):

    #-----------------------------------------
    # Track Controller Signals
    #-----------------------------------------
    tc_update = pyqtSignal()

    broadcast_tc_vitals = pyqtSignal()
    pass

signals = Signals()