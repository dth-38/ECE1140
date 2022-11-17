import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5 import uic

form_class = uic.loadUiType("Train_Controller/warning.ui")[0]

class warningWindow(QtWidgets.QMainWindow, form_class) :
    def __init__(self) :
        super(warningWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setupUi(self)
        self.closing_button.clicked.connect(self.close_window)
        self.warning_label.setWordWrap(True)

    def close_window(self):
        self.close()

    def signal_detected(self, text):
        self.show()
        self.warning_label.setText("{}".format(text))

