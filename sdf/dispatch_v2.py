# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dispatch_screen.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1440, 875)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 440, 201, 271))
        self.label.setObjectName("label")
        self.line_Selection = QtWidgets.QComboBox(Form)
        self.line_Selection.setGeometry(QtCore.QRect(50, 480, 104, 26))
        self.line_Selection.setObjectName("Line_Selection")
        self.starting_Location_Selection = QtWidgets.QComboBox(Form)
        self.starting_Location_Selection.setGeometry(QtCore.QRect(130, 520, 104, 26))
        self.starting_Location_Selection.setObjectName("Starting_Location_Selection")
        self.destination_Selection = QtWidgets.QComboBox(Form)
        self.destination_Selection.setGeometry(QtCore.QRect(100, 550, 104, 26))
        self.destination_Selection.setObjectName("Destination_Selection")
        self.departure_Selection = QtWidgets.QComboBox(Form)
        self.departure_Selection.setGeometry(QtCore.QRect(120, 580, 104, 26))
        self.departure_Selection.setObjectName("Departure_Selection")
        self.train_Selection = QtWidgets.QSpinBox(Form)
        self.train_Selection.setGeometry(QtCore.QRect(70, 450, 48, 24))
        self.train_Selection.setObjectName("Train_Selection")
        self.dispatch_button = QtWidgets.QPushButton(Form)
        self.dispatch_button.setGeometry(QtCore.QRect(60, 400, 113, 32))
        self.dispatch_button.setObjectName("Dispatch_button")
        self.main_button = QtWidgets.QPushButton(Form)
        self.main_button.setGeometry(QtCore.QRect(330, 570, 1101, 201))
        self.main_button.setObjectName("Main_button")
        self.speed_selection = QtWidgets.QComboBox(Form)
        self.speed_selection.setGeometry(QtCore.QRect(130, 610, 104, 26))
        self.speed_selection.setObjectName("Departure_Selection_2")
        self.forward_auth_selection = QtWidgets.QComboBox(Form)
        self.forward_auth_selection.setGeometry(QtCore.QRect(140, 650, 104, 26))
        self.forward_auth_selection.setObjectName("Departure_Selection_3")
        self.backward_auth_selection = QtWidgets.QComboBox(Form)
        self.backward_auth_selection.setGeometry(QtCore.QRect(150, 680, 104, 26))
        self.backward_auth_selection.setObjectName("Departure_Selection_4")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

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
"- Departure Time: \n"
"\n"
"- Suggested Speed: \n"
"\n"
"- Forward Authority: \n"
"\n"
"- Backward Authority: "))
        self.dispatch_button.setText(_translate("Form", "Dispatch Train"))
        self.main_button.setText(_translate("Form", "Back to Main Window"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())