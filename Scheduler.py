from PyQt5.QtCore import QRunnable
from Signals import signals

#imports signals class whenever we sort that out

#scheduler is a separate class to allow it to be multithreaded
class Scheduler(QRunnable):

    def __init__(self):
        super().__init__()
    
    #ovverides run method to have it be run in threadpool
    def run(self):
        signals.tc_update.emit()