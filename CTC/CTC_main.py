import sys
from PyQt5 import QtWidgets
from PyQt5 import uic

#this is how you import ui directly
#if changes need to be made to ui, go to QtDesigner -> redesign -> simply save
form_mainWindow = uic.loadUiType("ctc_main.ui")[0]

class CTCWindowClass(QtWidgets.QMainWindow, form_mainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setupUi(self)
        self.show()

    #some temporarily function.
    def init_ui(self):
        
        

#to run this file as main
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ctc_window = CTCWindowClass()
    sys.exit(app.exec_())