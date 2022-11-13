# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test_screen.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from common import Train, TrackModel, Line, Station

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1440, 875)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(0, 130, 211, 371))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(0, 480, 60, 16))
        self.label_2.setObjectName("label_2")
        self.switch_selection = QtWidgets.QComboBox(Form)
        self.switch_selection.setGeometry(QtCore.QRect(100, 220, 104, 26))
        self.switch_selection.setObjectName("switch_selection")
        self.occupancy_selection = QtWidgets.QComboBox(Form)
        self.occupancy_selection.setGeometry(QtCore.QRect(120, 260, 104, 26))
        self.occupancy_selection.setObjectName("occupancy_selection")
        self.failure_selection = QtWidgets.QComboBox(Form)
        self.failure_selection.setGeometry(QtCore.QRect(100, 290, 104, 26))
        self.failure_selection.setObjectName("failure_selection")
        self.light_decision_selection = QtWidgets.QComboBox(Form)
        self.light_decision_selection.setGeometry(QtCore.QRect(110, 390, 104, 26))
        self.light_decision_selection.setObjectName("light_decision_selection")
        self.gate_crossing_decision_selection = QtWidgets.QComboBox(Form)
        self.gate_crossing_decision_selection.setGeometry(QtCore.QRect(160, 420, 104, 26))
        self.gate_crossing_decision_selection.setObjectName("gate_crossing_decision_selection")
        self.line_selection = QtWidgets.QComboBox(Form)
        self.line_selection.setGeometry(QtCore.QRect(40, 450, 104, 26))
        self.line_selection.setObjectName("line_selection")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(680, 160, 60, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(670, 80, 201, 361))
        self.label_4.setObjectName("label_4")
        self.main_button = QtWidgets.QPushButton(Form)
        self.main_button.setGeometry(QtCore.QRect(1260, 470, 161, 291))
        self.main_button.setObjectName("main_button")
        self.test_log_button = QtWidgets.QPushButton(Form)
        self.test_log_button.setGeometry(QtCore.QRect(1060, 470, 191, 291))
        self.test_log_button.setObjectName("test_log_button")
        self.test_button = QtWidgets.QPushButton(Form)
        self.test_button.setGeometry(QtCore.QRect(2, 90, 231, 71))
        self.test_button.setObjectName("test_button")
        self.train_selection = QtWidgets.QSpinBox(Form)
        self.train_selection.setGeometry(QtCore.QRect(60, 160, 48, 24))
        self.train_selection.setObjectName("train_selection")
        self.authority_output = QtWidgets.QLineEdit(Form)
        self.authority_output.setGeometry(QtCore.QRect(750, 240, 113, 21))
        self.authority_output.setObjectName("authority_output")
        self.throughput_output = QtWidgets.QLineEdit(Form)
        self.throughput_output.setGeometry(QtCore.QRect(760, 270, 113, 21))
        self.throughput_output.setObjectName("throughput_output")
        self.maintenance_signal_output = QtWidgets.QLineEdit(Form)
        self.maintenance_signal_output.setGeometry(QtCore.QRect(810, 300, 113, 21))
        self.maintenance_signal_output.setObjectName("maintenance_signal_output")
        self.speed_output = QtWidgets.QLineEdit(Form)
        self.speed_output.setGeometry(QtCore.QRect(800, 200, 113, 21))
        self.speed_output.setObjectName("speed_output")
        self.block_selection = QtWidgets.QSpinBox(Form)
        self.block_selection.setGeometry(QtCore.QRect(50, 190, 48, 24))
        self.block_selection.setObjectName("block_selection")
        self.location_selection = QtWidgets.QComboBox(Form)
        self.location_selection.setGeometry(QtCore.QRect(70, 350, 104, 26))
        self.location_selection.setObjectName("location_selection")
        self.ticket_sales_selection = QtWidgets.QSpinBox(Form)
        self.ticket_sales_selection.setGeometry(QtCore.QRect(90, 320, 48, 24))
        self.ticket_sales_selection.setObjectName("ticket_sales_selection")
        self.section_selection = QtWidgets.QComboBox(Form)
        self.section_selection.setGeometry(QtCore.QRect(70, 480, 104, 26))
        self.section_selection.setObjectName("location_selection")
        

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.main_button.clicked.connect(lambda:self.closescr(Form))
        self.set_inputs()
        self.test_button.clicked.connect(lambda:self.output())

    
    
    def set_inputs(self):
        tf = ["True","False"]
        self.switch_selection.addItems(tf)
        self.occupancy_selection.addItems(tf)
        self.failure_selection.addItems(tf)
        self.location_selection.addItems(["Shadyside","Herron Ave"])
        self.light_decision_selection.addItems(["Red","Yellow","Green"])
        self.gate_crossing_decision_selection.addItems(["Open","Close"])
        self.line_selection.addItems(["Red","Green"])
        self.section_selection.addItems(["A","B","C"])
    
    def output(self):
        output_train = Train(id=self.train_selection.value(),line=self.line_selection.currentText())
        #TODO: NEEDS TO BE UPDATED
       
    def closescr(self,Form):
        Form.close()
    

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "- Train #: \n"
"\n"
"- Block: \n"
"\n"
"- Switch Status: \n"
"\n"
"- Track Occupancy: \n"
"\n"
"- Failure Status: \n"
"\n"
"- Ticket Sales: \n"
"\n"
"- Location: \n"
"\n"
"- Light Decision: \n"
"\n"
"- Gate Crossing Decision: \n"
"\n"
"- Line:"))
        self.label_2.setText(_translate("Form", "- Section: "))
        self.label_3.setText(_translate("Form", "Outputs"))
        self.label_4.setText(_translate("Form", "- Suggested Speed: \n"
"\n"
"- Authority: \n"
"\n"
"- Throughput: \n"
"\n"
"- Maintenance Signal: "))
        self.main_button.setText(_translate("Form", "Back to Main Window"))
        self.test_log_button.setText(_translate("Form", "Test Log"))
        self.test_button.setText(_translate("Form", "Test"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
