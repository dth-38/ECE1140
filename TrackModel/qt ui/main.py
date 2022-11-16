# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# import pandas as pd
# import sys
# from edit_track import Ui_EditTrackWindow
# from subsection import Ui_SubsectionWindow
# from import_trackinfo_app import TrackImportApp
# from track_info import *
# from track_info_table import *
# from trackmodel import *

# QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
# QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons

# class Ui_MainWindow(object):
#     def openEditWindow(self):
#         self.window = QMainWindow()
#         self.ui = Ui_EditTrackWindow()
#         self.ui.setupUi(self.window)
#         self.window.show()

#     def openSubWindow(self):
#         self.window = QMainWindow()
#         self.ui = Ui_SubsectionWindow()
#         self.ui.setupUi(self.window)
#         self.window.show()

#     def setupUi(self, MainWindow):
#         MainWindow.setObjectName("MainWindow")
#         MainWindow.resize(904, 680)
#         self.centralwidget = QtWidgets.QWidget(MainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#         self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
#         self.tabWidget.setGeometry(QtCore.QRect(6, 9, 891, 581))
#         self.tabWidget.setMinimumSize(QtCore.QSize(891, 0))
#         self.tabWidget.setObjectName("tabWidget")
#         self.Home = QtWidgets.QWidget()
#         self.Home.setObjectName("Home")
#         self.horizontalLayoutWidget = QtWidgets.QWidget(self.Home)
#         self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 441, 541))
#         self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
#         self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
#         self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
#         self.horizontalLayout.setObjectName("horizontalLayout")
        
#         self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
#         self.label.setObjectName("label")
#         pixmap = QPixmap('C:/Users/rachs/OneDrive/Documents/ECE1140/ECE1140/TrackModel/qt ui/tracklayout.png')
#         self.label.setPixmap(pixmap)
#         self.label.resize(pixmap.width(),pixmap.height())

#         self.horizontalLayout.addWidget(self.label)
#         self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.Home)
#         self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(459, -1, 421, 541))
#         self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
#         self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
#         self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
#         self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        
#         self.tableWidget_3 = QtWidgets.QTableWidget(self.horizontalLayoutWidget_2)
#         self.tableWidget_3.setObjectName("tableWidget_3")
#         self.tableWidget_3.setColumnCount(1)
#         self.tableWidget_3.setRowCount(13)
#         self.tableWidget_3.setVerticalHeaderLabels(['Line', 'Section', 'Block #', 'Block Length',
#                                                       'Block Grade (%)', 'Commanded Speed (mph)', 'Authority (blocks)',
#                                                       'Elevation', 'Failure', 'Stop Signal', 'Beacon',
#                                                       'Oncoming Passengers', 'Crew Count', 'Block Occupancy'])
#         self.horizontalLayout_2.addWidget(self.tableWidget_3)
        
#         self.tabWidget.addTab(self.Home, "")
#         self.edit = QtWidgets.QWidget()
#         self.edit.setObjectName("edit")
#         self.textBrowser = QtWidgets.QTextBrowser(self.edit)
#         self.textBrowser.setGeometry(QtCore.QRect(220, 140, 256, 41))
#         self.textBrowser.setObjectName("textBrowser")
#         self.pushButton = QtWidgets.QPushButton(self.edit)
#         self.pushButton.setGeometry(QtCore.QRect(110, 260, 101, 41))
#         self.pushButton.setObjectName("pushButton")
#         self.pushButton_2 = QtWidgets.QPushButton(self.edit)
#         self.pushButton_2.setGeometry(QtCore.QRect(290, 260, 111, 41))
#         self.pushButton_2.setObjectName("pushButton_2")
        
#         self.pushButton_2.clicked.connect(self.openEditWindow)
        
#         self.pushButton_3 = QtWidgets.QPushButton(self.edit)
#         self.pushButton_3.setGeometry(QtCore.QRect(480, 260, 131, 41))
#         self.pushButton_3.setObjectName("pushButton_3")
#         self.tabWidget.addTab(self.edit, "")
#         self.info = QtWidgets.QWidget()
#         self.info.setObjectName("info")
#         self.tabWidget_2 = QtWidgets.QTabWidget(self.info)
#         self.tabWidget_2.setGeometry(QtCore.QRect(0, 0, 891, 491))
#         self.tabWidget_2.setObjectName("tabWidget_2")
#         self.tab = QtWidgets.QWidget()
#         self.tab.setObjectName("tab")
#         self.tableWidget = QtWidgets.QTableWidget(self.tab)
#         self.tableWidget.setGeometry(QtCore.QRect(0, 0, 891, 471))
#         self.tableWidget.setObjectName("tableWidget")
#         self.tableWidget.setColumnCount(0)
#         self.tableWidget.setRowCount(0)
#         self.tabWidget_2.addTab(self.tab, "")
#         self.tab_2 = QtWidgets.QWidget()
#         self.tab_2.setObjectName("tab_2")
#         self.tableWidget_2 = QtWidgets.QTableWidget(self.tab_2)
#         self.tableWidget_2.setGeometry(QtCore.QRect(0, 0, 891, 471))
#         self.tableWidget_2.setObjectName("tableWidget_2")
#         self.tableWidget_2.setColumnCount(0)
#         self.tableWidget_2.setRowCount(0)
#         self.tabWidget_2.addTab(self.tab_2, "")
#         self.tabWidget.addTab(self.info, "")
#         MainWindow.setCentralWidget(self.centralwidget)
#         self.statusbar = QtWidgets.QStatusBar(MainWindow)
#         self.statusbar.setObjectName("statusbar")
#         MainWindow.setStatusBar(self.statusbar)
#         self.actionedit_exisiting_track = QtWidgets.QAction(MainWindow)
#         self.actionedit_exisiting_track.setObjectName("actionedit_exisiting_track")

#         self.retranslateUi(MainWindow)
#         self.tabWidget.setCurrentIndex(0)
#         self.tabWidget_2.setCurrentIndex(0)
#         QtCore.QMetaObject.connectSlotsByName(MainWindow)

#     def retranslateUi(self, MainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
#         self.label.setText(_translate("MainWindow", "TextLabel"))
#         self.tabWidget.setTabText(self.tabWidget.indexOf(self.Home), _translate("MainWindow", "Home"))
#         self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
# "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
# "p, li { white-space: pre-wrap; }\n"
# "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
# "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt; font-weight:600;\">Edit Track Layout</span></p></body></html>"))
#         self.pushButton.setText(_translate("MainWindow", "Add New Track"))
#         self.pushButton_2.setText(_translate("MainWindow", "Edit Existing Track"))
#         self.pushButton_3.setText(_translate("MainWindow", "Remove Existing Track"))
#         self.tabWidget.setTabText(self.tabWidget.indexOf(self.edit), _translate("MainWindow", "Edit Track Layout"))
#         self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab), _translate("MainWindow", "Red Line"))
#         self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_2), _translate("MainWindow", "Green Line"))
#         self.tabWidget.setTabText(self.tabWidget.indexOf(self.info), _translate("MainWindow", "Track Information"))
#         self.actionedit_exisiting_track.setText(_translate("MainWindow", "Edit Existing Track"))
#         self.actionedit_exisiting_track.setToolTip(_translate("MainWindow", "<html><head/><body><p>some tip</p></body></html>"))


# if __name__ == "__main__":
#     import sys

#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)

#     model = TrackModel()
#     model.load_model(ui.tableWidget, ui.tableWidget_2)

#     MainWindow.show()
#     sys.exit(app.exec_())

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
        pixmap = QPixmap('C:/Users/rachs/OneDrive/Documents/ECE1140/ECE1140/TrackModel/qt ui/tracklayout.png')
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