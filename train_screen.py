
import enum
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QVBoxLayout, QFileDialog, QTableView
from PyQt5.QtCore import QTime, Qt, QEvent
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *

from CTC_Scheduler import CTC_Scheduler
from CTC_Clock import CTC_Clock
from Code.Block_Table import Block_Table
from Code.Train_Table import Train_Table

#TRAIN SCREEN WINDOW 
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1440, 875)
        self.train_selection = QtWidgets.QSpinBox(Form)
        self.train_selection.setGeometry(QtCore.QRect(70, 620, 48, 24))
        self.train_selection.setSpecialValueText("")
        self.train_selection.setMinimum(0)
        self.train_selection.setObjectName("train_selection")
        self.hour_selection = QtWidgets.QSpinBox(Form)
        self.hour_selection.setGeometry(QtCore.QRect(120, 760, 48, 24))
        self.hour_selection.setObjectName("hour_selection")
        self.minute_selection = QtWidgets.QSpinBox(Form)
        self.minute_selection.setGeometry(QtCore.QRect(170, 760, 48, 24))
        self.minute_selection.setObjectName("minute_selection")
        self.second_selection = QtWidgets.QSpinBox(Form)
        self.second_selection.setGeometry(QtCore.QRect(220, 760, 48, 24))
        self.second_selection.setObjectName("second_selection")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 590, 141, 201))
        self.label.setObjectName("label")
        self.dispatch_button = QtWidgets.QPushButton(Form)
        self.dispatch_button.setGeometry(QtCore.QRect(2, 550, 271, 32))
        self.dispatch_button.setObjectName("train_button")
        self.throughput_button = QtWidgets.QPushButton(Form)
        self.throughput_button.setGeometry(QtCore.QRect(300, 550, 261, 32))
        self.throughput_button.setObjectName("throughput_button")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(310, 570, 211, 131))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(590, 550, 60, 16))
        self.label_3.setObjectName("label_3")
        self.main_button = QtWidgets.QPushButton(Form)
        self.main_button.setGeometry(QtCore.QRect(1210, 580, 231, 221))
        self.main_button.setObjectName("main_button")
        self.current_time = QtWidgets.QTimeEdit(Form)
        self.current_time.setGeometry(QtCore.QRect(1320, 0, 118, 24))
        self.current_time.setObjectName("current_time")
        self.line_train_selection = QtWidgets.QComboBox(Form)
        self.line_train_selection.setGeometry(QtCore.QRect(60, 650, 104, 26))
        self.line_train_selection.setObjectName("line_train_selection")
        self.line_throughput_selection = QtWidgets.QComboBox(Form)
        self.line_throughput_selection.setGeometry(QtCore.QRect(350, 610, 104, 26))
        self.line_throughput_selection.setObjectName("line_throughput_selection")
        self.starting_location_selection = QtWidgets.QComboBox(Form)
        self.starting_location_selection.setGeometry(QtCore.QRect(130, 680, 113, 21))
        self.starting_location_selection.setObjectName("starting_location_output")
        self.destination_selection = QtWidgets.QTextEdit(Form)
        self.destination_selection.setGeometry(QtCore.QRect(100, 710, 200, 40))
        self.destination_selection.setObjectName("destination_output")
        self.throughput_output = QtWidgets.QLineEdit(Form)
        self.throughput_output.setGeometry(QtCore.QRect(400, 640, 113, 21))
        self.throughput_output.setObjectName("throughput_output")
        self.schedule_button = QtWidgets.QPushButton(Form)
        self.schedule_button.setGeometry(QtCore.QRect(650,540,113,32))
        self.schedule_button.setObjectName("schedule_button")
        self.schedule_list = QtWidgets.QListWidget(Form)
        self.schedule_list.setGeometry(QtCore.QRect(580, 570, 431, 201))
        self.schedule_list.setObjectName("schedule_list")
        self.train_table_display = QtWidgets.QListWidget(Form)
        self.train_table_display.setGeometry(QtCore.QRect(140,50,500,300))
        self.train_table_display.setObjectName("train_table_display")
        self.block_table_display = QtWidgets.QListWidget(Form)
        self.block_table_display.setGeometry(QtCore.QRect(810,50,500,300))
        self.block_table_display.setObjectName("block_table_display")
        self.current_hour = QtWidgets.QSpinBox(Form)
        self.current_hour.setGeometry(QtCore.QRect(1280,10,48,24))
        self.current_hour.setObjectName("current_hour")
        self.current_minute = QtWidgets.QSpinBox(Form)
        self.current_minute.setGeometry(QtCore.QRect(1330,10,48,24))
        self.current_minute.setObjectName("current_minute")
        self.current_second = QtWidgets.QSpinBox(Form)
        self.current_second.setGeometry(QtCore.QRect(1380,10,48,24))
        self.current_second.setObjectName("current_second")

        self.label.raise_()
        self.dispatch_button.raise_()
        self.throughput_button.raise_()
        self.label_2.raise_()
        self.main_button.raise_()
        self.current_time.raise_()
        self.line_train_selection.raise_()
        self.line_throughput_selection.raise_()
        self.train_selection.raise_()
        self.starting_location_selection.raise_()
        self.destination_selection.raise_()
        self.throughput_output.raise_()

        self.schedule = CTC_Scheduler()
        self.train_table = Train_Table()
        self.block_table = Block_Table()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.main_button.clicked.connect(lambda:self.closescr(Form))
        self.setup_inputs(Form)
        self.dispatch_button.clicked.connect(lambda:self.pressed(Form))
        self.throughput_button.clicked.connect(lambda:self.output_throughput())
        self.schedule_button.clicked.connect(lambda:self.add_schedule())
    
    def closescr(self,Form):
        Form.close()
    
    
    def setup_inputs(self,Form):
        print("DISPATCH")
        lines = ["Red","Green"]
        stations = ["Shadyside", "Herron Ave", "Swissville", "Penn Station", "Steel Plaza", "First Ave", "Station Square", "South Hills Junction"]
        self.line_train_selection.addItems(lines)
        self.starting_location_selection.addItems(stations)
        #self.destination_selection.addItems(stations)
        self.line_throughput_selection.addItems(lines)

    def pressed(self,Form):
        arrival_time = (self.hour_selection.value(),self.minute_selection.value(),self.second_selection.value())
        destinations = self.destination_selection.toPlainText()
        self.schedule.manual_dispatch_train(arrival_time,self.train_selection.value(),self.line_train_selection.currentText(),destinations)
        #TODO: ADD DATA FROM TRAIN TABLE
        train_entry = self.train_table.get_entry(self.train_selection.value() - 1)
        self.train_table_display.addItem("NEW TRAIN DISPATCHED!!!!!!!!!")
        self.train_table_display.addItem("Train #: " + str(train_entry[0]))
        self.train_table_display.addItem("Position: " + str(train_entry[1]))
        self.train_table_display.addItem("States: " + str(train_entry[2]))
        self.schedule.view_throughput(self.line_throughput_selection.currentText())
        
    
    #TODO: WHEN TO DISPLAY BLOCK TABLE?
        
    def output_throughput(self):
        line = Line(self.line_throughput_selection.currentText())
        self.schedule.view_throughput(line)
        self.throughput_output.setText(str(line.get_throughput()))
    
    def add_schedule(self):
        file = QFileDialog.getOpenFileName(self,"Open File", "", "All Files (*);;Xlsx Files(*.xlsx)")
        self.schedule.upload_schedule(file)
    

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "- Train #: \n"
"\n"
"- Line:\n"
"\n"
"- Starting Location: \n"
"\n"
"- Destination: \n"
"\n"
"- Arrival Time: "))
        self.dispatch_button.setText(_translate("Form", "Dispatch Train"))
        self.throughput_button.setText(_translate("Form", "Select Throughput"))
        self.label_2.setText(_translate("Form", "- Line: \n"
"\n"
" - Throughput:"))
        self.main_button.setText(_translate("Form", "Back to Main Window"))
        self.label_3.setText(_translate("Form", "Schedule:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
