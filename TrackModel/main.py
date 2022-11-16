from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from trackmodel import *
import pandas as pd
import sys

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Track Model'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.table_widget = MyWidget(self)
        self.setCentralWidget(self.table_widget)
        
        self.show()
    
class MyWidget(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.home = QWidget()
        self.track_info = QWidget()
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.home,"Home")
        self.tabs.addTab(self.track_info,"Track Info")
        
        ## TRACK INFO TAB
        # Create second tab with 2 tabs on it
        self.track_info.layout = QVBoxLayout(self)
        self.lines = QTabWidget()
        self.red_line = QWidget()
        self.green_line = QWidget()
        self.lines.addTab(self.red_line, "Red Line")
        self.lines.addTab(self.green_line, "Green Line")

        # Create 2 table widgets and place them on the corresponing line tabs
        self.green_line.layout = QVBoxLayout(self)
        self.green_table = QTableWidget(self.green_line)

        self.red_line.layout = QVBoxLayout(self)
        self.red_table = QTableWidget(self.red_line)

        # Add green line table to green line tab
        self.green_line.layout.addWidget(self.green_table)
        self.green_line.setLayout(self.green_line.layout)

        # Add red line table to red line tab
        self.red_line.layout.addWidget(self.red_table)
        self.red_line.setLayout(self.red_line.layout)

        # Edit table entries
        model = TrackModel()
        model.load_model(self.red_table, self.green_table)

        # Add line tabs to track info tab widget
        self.track_info.layout.addWidget(self.lines)
        self.track_info.setLayout(self.track_info.layout)

        ## HOME TAB
        # Create first tab
        self.home.layout = QHBoxLayout(self)

        # Create track layout .png
        self.label = QLabel(self)
        pixmap = QPixmap('C:/Users/rachs/OneDrive/Documents/ECE1140/ECE1140/TrackModel/tracklayout.png')
        self.label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

        # Create table widget to display current block values
        self.table = QTableWidget(self.home)
        model.curr_table_setup(self.table)
        model.print_table(self.table)

        # Add track layout .png to the home tab
        self.home.layout.addWidget(self.label)
        self.home.setLayout(self.home.layout)
        
        # Add table to the home page
        self.home.layout.addWidget(self.table)
        self.home.setLayout(self.home.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())