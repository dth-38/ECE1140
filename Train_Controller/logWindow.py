import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5 import uic

form_class = uic.loadUiType("Train_Controller/log.ui")[0]

class logWindow(QtWidgets.QMainWindow, form_class) :
    def __init__(self) :
        super(logWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setupUi(self)
        self.log_close_button.clicked.connect(self.close_window)

    def close_window(self):
        self.close()

    def insert_str(self, str):
        self.read_result.append(str)
    
    def display(self):
        self.show()

    def clear_log_win(self):
        self.read_result.clear()
