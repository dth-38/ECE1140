from PyQt5.QtCore import QRunnable

#imports signals class whenever we sort that out

#scheduler is a separate class to allow it to be multithreaded
class Scheduler(QRunnable):

    def __init__(self):
        super().__init__()
    
    #ovverides run method to have it be run in threadpool
    def run(self):
        #each module's update function is called using signals
        #still gotta figure it out
        pass