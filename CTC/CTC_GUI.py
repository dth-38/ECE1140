from re import T
from PyQt5 import QtCore, QtGui, QtWidgets


QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling,True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps,True)

import enum
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QVBoxLayout 
from PyQt5.QtCore import QTime, Qt, QEvent
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *

from train_screen import Ui_Form as UI
from maintenance_screen import Ui_Form as UI2
from test_sceeen import Ui_Form as UI3

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 875)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.train_button = QtWidgets.QPushButton(self.centralwidget)
        self.train_button.setGeometry(QtCore.QRect(50, 130, 661, 481))
        self.train_button.setObjectName("train_button")
        self.maintenance_button = QtWidgets.QPushButton(self.centralwidget)
        self.maintenance_button.setGeometry(QtCore.QRect(700, 130, 661, 481))
        self.maintenance_button.setObjectName("maintenance_button")
        self.test_button = QtWidgets.QPushButton(self.centralwidget)
        self.test_button.setGeometry(QtCore.QRect(0, 0, 113, 32))
        self.test_button.setObjectName("test_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1440, 22))
        self.menubar.setObjectName("menubar")
        self.menuCTC_Office = QtWidgets.QMenu(self.menubar)
        self.menuCTC_Office.setObjectName("menuCTC_Office")
        self.menuMain_Window = QtWidgets.QMenu(self.menubar)
        self.menuMain_Window.setObjectName("menuMain_Window")
        MainWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.menuCTC_Office.menuAction())
        self.menubar.addAction(self.menuMain_Window.menuAction())

        self.train_button.clicked.connect(self.train_screen)
        self.maintenance_button.clicked.connect(self.maintenance_screen)
        self.test_button.clicked.connect(self.test_screen)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    def train_screen(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.Form = QtWidgets.QWidget()
        self.ui = UI()
        self.ui.setupUi(self.Form)
        self.Form.show()

    def maintenance_screen(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.Form = QtWidgets.QWidget()
        self.ui = UI2()
        self.ui.setupUi(self.Form)
        self.Form.show()
        
    def test_screen(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.Form = QtWidgets.QWidget()
        self.ui = UI3()
        self.ui.setupUi(self.Form)
        self.Form.show()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.train_button.setText(_translate("MainWindow", "Train Schedule"))
        self.maintenance_button.setText(_translate("MainWindow", "Maintenance Mode"))
        self.test_button.setText(_translate("MainWindow", "Test Inputs"))
        self.menuCTC_Office.setTitle(_translate("MainWindow", "CTC Office"))
        self.menuMain_Window.setTitle(_translate("MainWindow", "Main Window"))

""""
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
"""