from tkinter import W
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow
from matplotlib.widgets import Widget

import pandas as pd



class Train_Schedule():
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(QPushButton("Select Train Viewing"))
    layout.addWidget(QPushButton("Select Throughput Display Line"))
    window.setLayout(layout)
    window.show()
    app.setStyle('Windows')
    app.exec_()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        button_sched = QPushButton("Train Schedule")
        button_disp = QPushButton("Dispatch Train")
        button_maint = QPushButton("Maintenance Mode")
        button_test = QPushButton("Test Inputs")


