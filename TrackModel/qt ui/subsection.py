from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import pandas as pd

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons

class Ui_SubsectionWindow(object):
    def setupUi(self, SubsectionWindow):
        SubsectionWindow.setObjectName("SubsectionWindow")
        SubsectionWindow.resize(1170, 648)
        self.centralwidget = QtWidgets.QWidget(SubsectionWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(930, 30, 141, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(930, 80, 141, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(930, 130, 141, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(480, 20, 391, 421))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(15)
        self.tableWidget.setVerticalHeaderLabels(['', 'Line', 'Section', 'Block #', 'Block Length',
                                                      'Block Grade (%)', 'Commanded Speed (mph)', 
                                                      'Elevation', 'Authority (blocks)', 'Failure', 'Stop Signal', 'Beacon',
                                                      'Oncoming Passengers', 'Crew Count', 'Block Occupancy'])
        self.verticalLayout.addWidget(self.tableWidget)
        
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 20, 431, 521))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        SubsectionWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SubsectionWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1170, 22))
        self.menubar.setObjectName("menubar")
        SubsectionWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SubsectionWindow)
        self.statusbar.setObjectName("statusbar")
        SubsectionWindow.setStatusBar(self.statusbar)

        self.pushButton.clicked.connect(lambda: self.power_failure(self.tableWidget))
        self.pushButton_2.clicked.connect(lambda: self.broken_rail(self.tableWidget))
        self.pushButton_3.clicked.connect(lambda: self.track_circuit_failure(self.tableWidget))

        self.retranslateUi(SubsectionWindow)
        QtCore.QMetaObject.connectSlotsByName(SubsectionWindow)

    def retranslateUi(self, SubsectionWindow):
        _translate = QtCore.QCoreApplication.translate
        SubsectionWindow.setWindowTitle(_translate("SubsectionWindow", "SubsectionWindow"))
        self.pushButton.setText(_translate("SubsectionWindow", "Power Failure"))
        self.pushButton_2.setText(_translate("SubsectionWindow", "Broken Rail"))
        self.pushButton_3.setText(_translate("SubsectionWindow", "Track Circuit Failure"))
        self.label.setText(_translate("SubsectionWindow", "TextLabel"))

    def loadInSubData(self, line, block_num,  speed, auth, scd, lscd, gcd):
        table = self.tableWidget
        
        if line == 'red':
            worksheet_name = 'Red Line'
        elif line == 'green':
            worksheet_name = 'Green Line'

        df = pd.read_excel('track_layout.xlsx', worksheet_name)
        # Find matching block number and section ID, get other info
        for j in range(151):
            if df._get_value(2, j, takeable=True) == block_num:
                section = df._get_value(1, j, takeable=True)
                block_length = df._get_value(3, j, takeable=True)
                block_grade = df._get_value(4, j, takeable=True)
                elevation = df._get_value(8, j, takeable=True)
                break
        
        # Add current data to the subsection table
        cell = QTableWidgetItem(str(line))
        table.setItem(0, 1, cell)
        cell = QTableWidgetItem(str(section))
        table.setItem(1, 1, cell)
        cell = QTableWidgetItem(str(block_num))
        table.setItem(2, 1, cell)
        cell = QTableWidgetItem(str(block_length))
        table.setItem(3, 1, cell)
        cell = QTableWidgetItem(str(block_grade))
        table.setItem(4, 1, cell)
        cell = QTableWidgetItem("70")
        table.setItem(5, 1, cell)
        cell = QTableWidgetItem(str(elevation))
        table.setItem(6, 1, cell)
        cell = QTableWidgetItem("4")
        table.setItem(7, 1, cell)
        cell = QTableWidgetItem("none")
        table.setItem(8, 1, cell)
        cell = QTableWidgetItem("off")
        table.setItem(9, 1, cell)
        cell = QTableWidgetItem("Shadyside; Left/Right")
        table.setItem(10, 1, cell)
        cell = QTableWidgetItem("26")
        table.setItem(11, 1, cell)
        cell = QTableWidgetItem("3")
        table.setItem(12, 1, cell)
        cell = QTableWidgetItem("on")
        table.setItem(13, 1, cell)

    def loadSubsectionData(self, table, line, block_num):
        if line == 'red':
            worksheet_name = 'Red Line'
        elif line == 'green':
            worksheet_name = 'Green Line'

        df = pd.read_excel('track_layout.xlsx', worksheet_name)
        # Find matching block number and section ID, get other info
        for j in range(151):
            if df._get_value(2, j, takeable=True) == block_num:
                section = df._get_value(1, j, takeable=True)
                block_length = df._get_value(3, j, takeable=True)
                block_grade = df._get_value(4, j, takeable=True)
                speed_limit = df._get_value(5, j, takeable=True)
                elevation = df._get_value(8, j, takeable=True)
                break
        
        # Add current data to the subsection table
        cell = QTableWidgetItem(str(line))
        table.setItem(0, 1, cell)
        cell = QTableWidgetItem(str(section))
        table.setItem(1, 1, cell)
        cell = QTableWidgetItem(str(block_num))
        table.setItem(2, 1, cell)
        cell = QTableWidgetItem(str(block_length))
        table.setItem(3, 1, cell)
        cell = QTableWidgetItem(str(block_grade))
        table.setItem(4, 1, cell)
        cell = QTableWidgetItem(str(speed_limit))
        table.setItem(5, 1, cell)
        cell = QTableWidgetItem(str(elevation))
        table.setItem(6, 1, cell)
        
        cell = QTableWidgetItem("none")
        table.setItem(7, 1, cell)
        cell = QTableWidgetItem("none")
        table.setItem(8, 1, cell)
        cell = QTableWidgetItem("none")
        table.setItem(9, 1, cell)
        cell = QTableWidgetItem("none")
        table.setItem(10, 1, cell)
        cell = QTableWidgetItem("none")
        table.setItem(11, 1, cell)
        cell = QTableWidgetItem("none")
        table.setItem(12, 1, cell)

    def power_failure(self, table):
        cell = QTableWidgetItem("POWER FAILURE")
        table.setItem(8, 1, cell)

    def broken_rail(self, table):
        cell = QTableWidgetItem("BROKEN RAIL")
        table.setItem(8, 1, cell)

    def track_circuit_failure(self, table):
        cell = QTableWidgetItem("TRACK CIRCUIT FAILURE")
        table.setItem(8, 1, cell)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SubsectionWindow = QtWidgets.QMainWindow()
    ui = Ui_SubsectionWindow()
    ui.setupUi(SubsectionWindow)

    ui.loadSubsectionData(ui.tableWidget, 'red', 3)

    SubsectionWindow.show()
    sys.exit(app.exec_())
