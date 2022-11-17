
#import enum
#import sched
#import sys
#import time
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QTimer
#from PyQt5.QtWidgets import *
#from PyQt5.QtGui import * 
#from PyQt5.QtCore import *
#from PyQt5 import *

#from CTC.CTC_Scheduler import CTC_Scheduler
#from CTC.CTC_Clock import CTC_Clock
#from CTC.Block_Table import Block_Table
#from CTC.Train_Table import Train_Table

from Signals import signals

#TRAIN SCREEN WINDOW 
class train_screen(QtWidgets.QWidget):
    def __init__(self,ctc):
        super(train_screen,self).__init__()
        self.ctc = ctc
        self.setupUi()
        self.show()
    def setupUi(self):
        #print("SETUP UI")
        self.train_selection = QtWidgets.QSpinBox(self)
        self.train_selection.setGeometry(QtCore.QRect(70, 630, 48, 24))
        self.train_selection.setSpecialValueText("")
        self.train_selection.setMinimum(0)
        self.train_selection.setObjectName("train_selection")
        self.hour_selection = QtWidgets.QSpinBox(self)
        self.hour_selection.setGeometry(QtCore.QRect(120, 740, 48, 24))
        self.hour_selection.setObjectName("hour_selection")
        self.minute_selection = QtWidgets.QSpinBox(self)
        self.minute_selection.setGeometry(QtCore.QRect(170, 740, 48, 24))
        self.minute_selection.setObjectName("minute_selection")
        self.second_selection = QtWidgets.QSpinBox(self)
        self.second_selection.setGeometry(QtCore.QRect(220, 740, 48, 24))
        self.second_selection.setObjectName("second_selection")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(10, 590, 141, 201))
        self.label.setObjectName("label")
        self.dispatch_button = QtWidgets.QPushButton(self)
        self.dispatch_button.setGeometry(QtCore.QRect(2, 550, 271, 32))
        self.dispatch_button.setObjectName("train_button")
        self.throughput_button = QtWidgets.QPushButton(self)
        self.throughput_button.setGeometry(QtCore.QRect(300, 550, 261, 32))
        self.throughput_button.setObjectName("throughput_button")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(310, 570, 211, 131))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(590, 550, 60, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(140, 30, 100, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(810, 30, 100, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self)
        self.label_6.setGeometry(QtCore.QRect(1180, 10, 100, 16))
        self.label_6.setObjectName("label_6")
        self.main_button = QtWidgets.QPushButton(self)
        self.main_button.setGeometry(QtCore.QRect(1210, 580, 231, 221))
        self.main_button.setObjectName("main_button")
        self.line_train_selection = QtWidgets.QComboBox(self)
        self.line_train_selection.setGeometry(QtCore.QRect(60, 660, 104, 26))
        self.line_train_selection.setObjectName("line_train_selection")
        self.line_throughput_selection = QtWidgets.QComboBox(self)
        self.line_throughput_selection.setGeometry(QtCore.QRect(350, 610, 104, 26))
        self.line_throughput_selection.setObjectName("line_throughput_selection")
        #self.starting_location_selection = QtWidgets.QComboBox(self)
        #self.starting_location_selection.setGeometry(QtCore.QRect(130, 680, 113, 21))
        #self.starting_location_selection.setObjectName("starting_location_output")
        self.destination_selection = QtWidgets.QTextEdit(self)
        self.destination_selection.setGeometry(QtCore.QRect(100, 690, 200, 40))
        self.destination_selection.setObjectName("destination_output")
        self.throughput_output = QtWidgets.QLineEdit(self)
        self.throughput_output.setGeometry(QtCore.QRect(400, 640, 113, 21))
        self.throughput_output.setObjectName("throughput_output")
        self.schedule_button = QtWidgets.QPushButton(self)
        self.schedule_button.setGeometry(QtCore.QRect(650,540,113,32))
        self.schedule_button.setObjectName("schedule_button")
        self.schedule_list = QtWidgets.QListWidget(self)
        self.schedule_list.setGeometry(QtCore.QRect(580, 570, 431, 201))
        self.schedule_list.setObjectName("schedule_list")
        self.train_table_display = QtWidgets.QListWidget(self)
        self.train_table_display.setGeometry(QtCore.QRect(140,50,500,300))
        self.train_table_display.setObjectName("train_table_display")
        self.block_table_display = QtWidgets.QListWidget(self)
        self.block_table_display.setGeometry(QtCore.QRect(810,50,500,300))
        self.block_table_display.setObjectName("block_table_display")
        self.current_hour = QtWidgets.QSpinBox(self)
        self.current_hour.setGeometry(QtCore.QRect(1280,10,48,24))
        self.current_hour.setObjectName("current_hour")
        self.current_minute = QtWidgets.QSpinBox(self)
        self.current_minute.setGeometry(QtCore.QRect(1330,10,48,24))
        self.current_minute.setObjectName("current_minute")
        self.current_second = QtWidgets.QSpinBox(self)
        self.current_second.setGeometry(QtCore.QRect(1380,10,48,24))
        self.current_second.setObjectName("current_second")

        self.timer = QTimer()

    
        self.label.raise_()
        self.dispatch_button.raise_()
        self.throughput_button.raise_()
        self.label_2.raise_()
        self.main_button.raise_()
        self.line_train_selection.raise_()
        self.line_throughput_selection.raise_()
        self.train_selection.raise_()
        #self.starting_location_selection.raise_()
        self.destination_selection.raise_()
        self.throughput_output.raise_()

        
        self.train_entries = []
        self.block_entries = []

        self.retranslateUi(self)
        self.main_button.clicked.connect(lambda:self.closescr())
        self.setup_inputs()
        self.dispatch_button.clicked.connect(lambda:self.dispatch_pressed())
        self.throughput_button.clicked.connect(lambda:self.output_throughput())
        self.schedule_button.clicked.connect(lambda:self.add_schedule())

        #DISABLED TIMER BECAUSE IT IS BROKEN
        #self.timer.timeout.connect(lambda: self.update_current_time())
        self.timer.start(1000)
    
    def closescr(self):
        self.hide()
    
    
    def setup_inputs(self):
        print("DISPATCH")
        lines = ["Red","Green"]
        #stations = ["Yard","Shadyside", "Herron Ave", "Swissville", "Penn Station", "Steel Plaza", "First Ave", "Station Square", "South Hills Junction"]
        self.line_train_selection.addItems(lines)
        #self.starting_location_selection.addItems(stations)
        self.line_throughput_selection.addItems(lines)

    def dispatch_pressed(self):
        arrival_time = (self.hour_selection.value(),self.minute_selection.value(),self.second_selection.value())
        #print(arrival_time)
        destinations = self.destination_selection.toPlainText()
        self.train_entries, travel_time = self.ctc.schedule.manual_dispatch_train(arrival_time,self.train_selection.value(),self.line_train_selection.currentText(),destinations)

        #sends dispatch signal
        line = str(self.train_entries[5])
        line.upper()
        signals.send_tm_dispatch.emit(line)

        self.train_table_display.addItem("NEW TRAIN DISPATCHED!!!!!!!!!")
        self.train_table_display.addItem("Train #: " + str(self.train_entries[0]))
        self.train_table_display.addItem("Position: " + str(self.train_entries[1]))
        #self.train_table_display.addItem("States: " + str(self.train_entries[2]))
        self.train_table_display.addItem("Destinations: " + str(self.train_entries[3]))
        self.train_table_display.addItem("Authority: " + str(self.train_entries[4]))
        self.train_table_display.addItem("Line: " + str(self.train_entries[5]))
        self.train_table_display.addItem("Arrival Time: " + str(self.train_entries[6]))


        
    
    #TODO: WHEN AND HOW TO DISPLAY BLOCK TABLE?
        
    #TODO GET TICKET SALES FROM TRACKMODEL
    def output_throughput(self):
        line = self.line_throughput_selection.currentText()
        throughput = self.ctc.schedule.calc_throughput(line=line,ticket_sales=10,hours=self.current_hour.value())
        self.throughput_output.setText(str(throughput))
    
    def add_schedule(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self,"Open File", "", "All Files (*);;Xlsx Files(*.xlsx)")
        self.ctc.schedule.upload_schedule(file)
    
    def update_current_time(self):
        #print("Update Time")
        self.ctc.clock.update_time()
        #authority, position = self.ctc.schedule.update_trains()
        #print("authority: " + str(authority))
        #print("position: " + str(position))
        self.current_hour.setValue(self.ctc.clock.get_hours())
        self.current_minute.setValue(self.ctc.clock.get_minutes())
        self.current_second.setValue(self.ctc.clock.get_seconds())
        #Only one train working currently 
        if self.train_table_display.count() > 0:
            self.train_table_display.takeItem(2)
            self.train_table_display.insertItem(2,"Position: " + str(self.ctc.schedule.train_table.get_position(0)))
            self.train_table_display.takeItem(5)
            self.train_table_display.insertItem(5,"Authority: " + str(self.ctc.schedule.train_table.get_authority(0)))
        length = self.ctc.block_table.get_table_length()
        if length > 0:
            self.block_table_display.addItem(self.ctc.block_table.get_last_entry())

    def output_block_table(self):
        length = self.ctc.block_table.get_table_length()
        for i in range(length):
            self.block_table_display.addItem(self.ctc.block_table.get_entry(i))

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "- Train #: \n"
"\n"
"- Line:\n"
"\n"
"- Destination: \n"
"\n"
"- Departure Time: "))
        self.dispatch_button.setText(_translate("Form", "Dispatch Train"))
        self.throughput_button.setText(_translate("Form", "Select Throughput"))
        self.schedule_button.setText(_translate("Form","Add Schedule"))
        self.label_2.setText(_translate("Form", "- Line: \n"
"\n"
" - Throughput:"))
        self.main_button.setText(_translate("Form", "Back to Main Window"))
        self.label_3.setText(_translate("Form", "Schedule:"))
        self.label_4.setText(_translate("Form", "Train Table:"))
        self.label_5.setText(_translate("Form", "Block Table:"))
        self.label_6.setText(_translate("Form", "Current Time:"))
    

