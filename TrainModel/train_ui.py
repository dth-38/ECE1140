# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'train_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from TrainModel.train_model_signals import *

class TrainData_Ui(object):
    def setupUi(self, train_model):
        train_model.setObjectName("MainWindow")
        train_model.resize(1000, 853)
        self.centralwidget = QtWidgets.QWidget(train_model)
        self.centralwidget.setObjectName("centralwidget")
        self.train_id_label = QtWidgets.QLabel(self.centralwidget)
        self.train_id_label.setGeometry(QtCore.QRect(350, 10, 201, 101))
        self.train_id_label.setObjectName("train_id_label")
        self.train_id_line = QtWidgets.QLineEdit(self.centralwidget)
        self.train_id_line.setGeometry(QtCore.QRect(560, 40, 81, 51))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.train_id_line.setFont(font)
        self.train_id_line.setText("")
        self.train_id_line.setObjectName("train_id_line")
        self.velocity_label = QtWidgets.QLabel(self.centralwidget)
        self.velocity_label.setGeometry(QtCore.QRect(110, 120, 211, 61))
        self.velocity_label.setObjectName("velocity_label")
        self.suggsted_speed_label = QtWidgets.QLabel(self.centralwidget)
        self.suggsted_speed_label.setGeometry(QtCore.QRect(110, 170, 331, 61))
        self.suggsted_speed_label.setObjectName("suggsted_speed_label")
        self.velocity_line = QtWidgets.QLineEdit(self.centralwidget)
        self.velocity_line.setGeometry(QtCore.QRect(30, 130, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.velocity_line.setFont(font)
        self.velocity_line.setObjectName("velocity_line")
        self.suggested_speed_line = QtWidgets.QLineEdit(self.centralwidget)
        self.suggested_speed_line.setGeometry(QtCore.QRect(30, 180, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.suggested_speed_line.setFont(font)
        self.suggested_speed_line.setObjectName("suggested_speed_line")
        self.acceleration_line = QtWidgets.QLineEdit(self.centralwidget)
        self.acceleration_line.setGeometry(QtCore.QRect(30, 240, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.acceleration_line.setFont(font)
        self.acceleration_line.setObjectName("acceleration_line")
        self.acceleration_label = QtWidgets.QLabel(self.centralwidget)
        self.acceleration_label.setGeometry(QtCore.QRect(110, 230, 331, 61))
        self.acceleration_label.setObjectName("acceleration_label")
        self.power_line = QtWidgets.QLineEdit(self.centralwidget)
        self.power_line.setGeometry(QtCore.QRect(30, 300, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.power_line.setFont(font)
        self.power_line.setObjectName("power_line")
        self.authority_line = QtWidgets.QLineEdit(self.centralwidget)
        self.authority_line.setGeometry(QtCore.QRect(30, 350, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.authority_line.setFont(font)
        self.authority_line.setObjectName("authority_line")
        self.grade_line = QtWidgets.QLineEdit(self.centralwidget)
        self.grade_line.setGeometry(QtCore.QRect(30, 400, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.grade_line.setFont(font)
        self.grade_line.setObjectName("grade_line")
        self.station_line = QtWidgets.QLineEdit(self.centralwidget)
        self.station_line.setGeometry(QtCore.QRect(30, 460, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.station_line.setFont(font)
        self.station_line.setText("")
        self.station_line.setObjectName("station_line")
        self.power_label = QtWidgets.QLabel(self.centralwidget)
        self.power_label.setGeometry(QtCore.QRect(110, 290, 331, 61))
        self.power_label.setObjectName("power_label")
        self.authority_label = QtWidgets.QLabel(self.centralwidget)
        self.authority_label.setGeometry(QtCore.QRect(110, 340, 331, 61))
        self.authority_label.setObjectName("authority_label")
        self.grade_label = QtWidgets.QLabel(self.centralwidget)
        self.grade_label.setGeometry(QtCore.QRect(110, 370, 331, 61))
        self.grade_label.setObjectName("grade_label")
        self.station_label = QtWidgets.QLabel(self.centralwidget)
        self.station_label.setGeometry(QtCore.QRect(260, 450, 201, 61))
        self.station_label.setObjectName("station_label")
        self.width_label = QtWidgets.QLabel(self.centralwidget)
        self.width_label.setGeometry(QtCore.QRect(440, 170, 331, 61))
        self.width_label.setObjectName("width_label")
        self.height_line = QtWidgets.QLineEdit(self.centralwidget)
        self.height_line.setGeometry(QtCore.QRect(360, 240, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.height_line.setFont(font)
        self.height_line.setObjectName("height_line")
        self.horn_line = QtWidgets.QLineEdit(self.centralwidget)
        self.horn_line.setGeometry(QtCore.QRect(360, 400, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.horn_line.setFont(font)
        self.horn_line.setObjectName("horn_line")
        self.length_label = QtWidgets.QLabel(self.centralwidget)
        self.length_label.setGeometry(QtCore.QRect(440, 120, 211, 61))
        self.length_label.setObjectName("length_label")
        self.announcement_line = QtWidgets.QLineEdit(self.centralwidget)
        self.announcement_line.setGeometry(QtCore.QRect(360, 350, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.announcement_line.setFont(font)
        self.announcement_line.setObjectName("announcement_line")
        self.width_line = QtWidgets.QLineEdit(self.centralwidget)
        self.width_line.setGeometry(QtCore.QRect(360, 180, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.width_line.setFont(font)
        self.width_line.setObjectName("width_line")
        self.horn_label = QtWidgets.QLabel(self.centralwidget)
        self.horn_label.setGeometry(QtCore.QRect(440, 390, 331, 61))
        self.horn_label.setObjectName("horn_label")
        self.length_line = QtWidgets.QLineEdit(self.centralwidget)
        self.length_line.setGeometry(QtCore.QRect(360, 130, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.length_line.setFont(font)
        self.length_line.setObjectName("length_line")
        self.height_label = QtWidgets.QLabel(self.centralwidget)
        self.height_label.setGeometry(QtCore.QRect(440, 230, 331, 61))
        self.height_label.setObjectName("height_label")
        self.announcement_label = QtWidgets.QLabel(self.centralwidget)
        self.announcement_label.setGeometry(QtCore.QRect(440, 340, 331, 61))
        self.announcement_label.setObjectName("announcement_label")
        self.mass_line = QtWidgets.QLineEdit(self.centralwidget)
        self.mass_line.setGeometry(QtCore.QRect(360, 300, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.mass_line.setFont(font)
        self.mass_line.setObjectName("mass_line")
        self.mass_label = QtWidgets.QLabel(self.centralwidget)
        self.mass_label.setGeometry(QtCore.QRect(440, 290, 331, 61))
        self.mass_label.setObjectName("mass_label")
        self.crew_label = QtWidgets.QLabel(self.centralwidget)
        self.crew_label.setGeometry(QtCore.QRect(780, 170, 331, 61))
        self.crew_label.setObjectName("crew_label")
        self.temp_line = QtWidgets.QLineEdit(self.centralwidget)
        self.temp_line.setGeometry(QtCore.QRect(700, 450, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.temp_line.setFont(font)
        self.temp_line.setObjectName("temp_line")
        self.left_door_line = QtWidgets.QLineEdit(self.centralwidget)
        self.left_door_line.setGeometry(QtCore.QRect(700, 340, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.left_door_line.setFont(font)
        self.left_door_line.setObjectName("left_door_line")
        self.right_door_label = QtWidgets.QLabel(self.centralwidget)
        self.right_door_label.setGeometry(QtCore.QRect(780, 380, 331, 61))
        self.right_door_label.setObjectName("right_door_label")
        self.passenger_label = QtWidgets.QLabel(self.centralwidget)
        self.passenger_label.setGeometry(QtCore.QRect(780, 120, 211, 61))
        self.passenger_label.setObjectName("passenger_label")
        self.ext_light_line = QtWidgets.QLineEdit(self.centralwidget)
        self.ext_light_line.setGeometry(QtCore.QRect(700, 290, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.ext_light_line.setFont(font)
        self.ext_light_line.setObjectName("ext_light_line")
        self.crew_line = QtWidgets.QLineEdit(self.centralwidget)
        self.crew_line.setGeometry(QtCore.QRect(700, 180, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.crew_line.setFont(font)
        self.crew_line.setObjectName("crew_line")
        self.left_door_label = QtWidgets.QLabel(self.centralwidget)
        self.left_door_label.setGeometry(QtCore.QRect(780, 330, 331, 61))
        self.left_door_label.setObjectName("left_door_label")
        self.passenger_line = QtWidgets.QLineEdit(self.centralwidget)
        self.passenger_line.setGeometry(QtCore.QRect(700, 130, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.passenger_line.setFont(font)
        self.passenger_line.setObjectName("passenger_line")
        self.temp_label = QtWidgets.QLabel(self.centralwidget)
        self.temp_label.setGeometry(QtCore.QRect(780, 440, 331, 61))
        self.temp_label.setObjectName("temp_label")
        self.ext_light_label = QtWidgets.QLabel(self.centralwidget)
        self.ext_light_label.setGeometry(QtCore.QRect(780, 280, 331, 61))
        self.ext_light_label.setObjectName("ext_light_label")
        self.int_light_line = QtWidgets.QLineEdit(self.centralwidget)
        self.int_light_line.setGeometry(QtCore.QRect(700, 240, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.int_light_line.setFont(font)
        self.int_light_line.setObjectName("int_light_line")
        self.int_light_label = QtWidgets.QLabel(self.centralwidget)
        self.int_light_label.setGeometry(QtCore.QRect(780, 230, 331, 61))
        self.int_light_label.setObjectName("int_light_label")
        self.right_door_line = QtWidgets.QLineEdit(self.centralwidget)
        self.right_door_line.setGeometry(QtCore.QRect(700, 390, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.right_door_line.setFont(font)
        self.right_door_line.setObjectName("right_door_line")
        self.murphy_label = QtWidgets.QLabel(self.centralwidget)
        self.murphy_label.setGeometry(QtCore.QRect(320, 510, 171, 61))
        self.murphy_label.setObjectName("murphy_label")
        self.p_label = QtWidgets.QLabel(self.centralwidget)
        self.p_label.setGeometry(QtCore.QRect(790, 520, 171, 61))
        self.p_label.setObjectName("p_label")
        self.repair_button = QtWidgets.QPushButton(self.centralwidget)
        self.repair_button.setGeometry(QtCore.QRect(10, 580, 181, 171))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.repair_button.setFont(font)
        self.repair_button.setObjectName("repair_button")
        self.engine_button = QtWidgets.QPushButton(self.centralwidget)
        self.engine_button.setGeometry(QtCore.QRect(200, 580, 181, 171))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.engine_button.setFont(font)
        self.engine_button.setObjectName("engine_button")
        self.sp_button = QtWidgets.QPushButton(self.centralwidget)
        self.sp_button.setGeometry(QtCore.QRect(390, 580, 181, 171))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sp_button.setFont(font)
        self.sp_button.setObjectName("sp_button")
        self.brake_button = QtWidgets.QPushButton(self.centralwidget)
        self.brake_button.setGeometry(QtCore.QRect(580, 580, 181, 171))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.brake_button.setFont(font)
        self.brake_button.setObjectName("brake_button")
        self.pbrake_button = QtWidgets.QPushButton(self.centralwidget)
        self.pbrake_button.setGeometry(QtCore.QRect(770, 580, 211, 171))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pbrake_button.setFont(font)
        self.pbrake_button.setObjectName("pbrake_button")
        self.advertisement_line = QtWidgets.QLineEdit(self.centralwidget)
        self.advertisement_line.setGeometry(QtCore.QRect(360, 460, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.advertisement_line.setFont(font)
        self.advertisement_line.setObjectName("advertisement_line")
        self.advertisement_label = QtWidgets.QLabel(self.centralwidget)
        self.advertisement_label.setGeometry(QtCore.QRect(450, 450, 181, 61))
        self.advertisement_label.setObjectName("advertisement_label")
        train_model.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(train_model)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 26))
        self.menubar.setObjectName("menubar")
        train_model.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(train_model)
        self.statusbar.setObjectName("statusbar")
        train_model.setStatusBar(self.statusbar)

        self.retranslateUi(train_model)
        QtCore.QMetaObject.connectSlotsByName(train_model)

        self.engine_button.pressed.connect(self.toggle_engine_failure)
        self.sp_button.pressed.connect(self.toggle_sp_failure)
        self.brake_button.pressed.connect(self.toggle_brake_failure)
        self.repair_button.pressed.connect(self.toggle_fix_failure)

        self.pbrake_button.pressed.connect(self.toggle_pbrake)
        

    def toggle_engine_failure(self):
        ui_sig.train_model_transfer_engine_falure.emit()

    def toggle_sp_failure(self):
        ui_sig.train_model_transfer_signal_pickup_failure.emit()

    def toggle_brake_failure(self):
        ui_sig.train_model_transfer_brake_failure.emit()

    def toggle_fix_failure(self):
        ui_sig.train_model_fix_failure.emit()
        
    def toggle_pbrake(self):
        ui_sig.train_model_transfer_passenger_ebrake.emit()
    def retranslateUi(self, train_model):
        _translate = QtCore.QCoreApplication.translate
        train_model.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.train_id_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:36pt;\">Train #</span></p></body></html>"))
        self.velocity_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Velocity (mph)</span></p></body></html>"))
        self.suggsted_speed_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Suggested Sped (mph)</span></p></body></html>"))
        self.velocity_line.setText(_translate("MainWindow", "0"))
        self.suggested_speed_line.setText(_translate("MainWindow", "0"))
        self.acceleration_line.setText(_translate("MainWindow", "0"))
        self.acceleration_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Acceleration (ft/s²)</span></p></body></html>"))
        self.power_line.setText(_translate("MainWindow", "0"))
        self.authority_line.setText(_translate("MainWindow", "0"))
        self.grade_line.setText(_translate("MainWindow", "0"))
        self.power_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Power (kilowatts)</span></p></body></html>"))
        self.authority_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Authority</span></p></body></html>"))
        self.grade_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\"><br/>Grade</span></p></body></html>"))
        self.station_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Station</span></p></body></html>"))
        self.width_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Width (ft)</span></p></body></html>"))
        self.height_line.setText(_translate("MainWindow", "9.7"))
        self.horn_line.setText(_translate("MainWindow", "Off"))
        self.length_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Length (ft)</span></p></body></html>"))
        self.announcement_line.setText(_translate("MainWindow", "Off"))
        self.width_line.setText(_translate("MainWindow", "11.2"))
        self.horn_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Horn</span></p></body></html>"))
        self.length_line.setText(_translate("MainWindow", "105.6"))
        self.height_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Height (ft)</span></p></body></html>"))
        self.announcement_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Announcement</span></p></body></html>"))
        self.mass_line.setText(_translate("MainWindow", "40.25"))
        self.mass_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Mass (tons)</span></p></body></html>"))
        self.crew_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Crew Count</span></p></body></html>"))
        self.temp_line.setText(_translate("MainWindow", "70"))
        self.left_door_line.setText(_translate("MainWindow", "Closed"))
        self.right_door_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Right Doors</span></p></body></html>"))
        self.passenger_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Passenger Count</span></p></body></html>"))
        self.ext_light_line.setText(_translate("MainWindow", "Off"))
        self.crew_line.setText(_translate("MainWindow", "1"))
        self.left_door_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Left Doors</span></p></body></html>"))
        self.passenger_line.setText(_translate("MainWindow", "0"))
        self.temp_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Temperature (°F)</span></p></body></html>"))
        self.ext_light_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Exterior Lights</span></p></body></html>"))
        self.int_light_line.setText(_translate("MainWindow", "Off"))
        self.int_light_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Interior Lights</span></p></body></html>"))
        self.right_door_line.setText(_translate("MainWindow", "Closed"))
        self.murphy_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:22pt;\">Murphy</span></p></body></html>"))
        self.p_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:22pt;\">Passenger</span></p></body></html>"))
        self.repair_button.setText(_translate("MainWindow", "Repair Failures"))
        self.engine_button.setText(_translate("MainWindow", "Engine"))
        self.sp_button.setText(_translate("MainWindow", "Signal Pickup"))
        self.brake_button.setText(_translate("MainWindow", "Brake"))
        self.pbrake_button.setText(_translate("MainWindow", "Pull Emergency Brake"))
        self.advertisement_line.setText(_translate("MainWindow", "Off"))
        self.advertisement_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Advertisement</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    train_model = QtWidgets.QMainWindow()
    ui = TrainData_Ui()
    ui.setupUi(train_model)
    train_model.show()
    sys.exit(app.exec_())
