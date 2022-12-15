import sys
from simple_pid import PID
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
from Train_Controller.errorWindow import warningWindow
from Train_Controller.testWindow import testWindow

form_mainWindow = uic.loadUiType("Train_Controller/temp_ui/TrainController_1.ui")[0]

#for keeping values of train
class train_status:

    def __init__(self):
        self.speed_limit = 43.496  #maximum speed in mph (70km/hr)
        self.commanded_speed = 0  #commended speed (from manual mode) OR desired speed, 100 by default
        self.speed = 0            #actual speed of train
        self.authority = 0
        self.door_left = "Opened"
        self.door_right = "Opened"
        self.internal_light = "Off"
        self.external_light = "Off"
        self.annun = "On"
        self.ad = "On"
        self.horn = "On"
        self.temp = 68
        self.failure_flag = False
        #self.passenger_brake_flag = False

        self.beacon = ""
        self.ki = 0.01
        self.kp = 1
        self.pid = PID(self.kp, self.ki, 0, setpoint=self.commanded_speed) # initialize pid with fixed values
        self.pid.outer_limits = (0, 120000)                                  # clamp at max power output specified in datasheet 120kW
        self.power = 0.0

    #set methods
    def set_authority(self, num):
        self.authority = num
    def set_commanded_speed(self, num):
        self.commanded_speed = num
    def set_speed(self, num):       #actual speed
        self.speed = num
    def set_speed_limit(self, num): #desired speed
        self.speed_limit = num
    def set_door_left(self, state):
        self.door_left = state
    def set_door_right(self, state):
        self.door_right = state
    def set_internal_light(self, state):
        self.internal_light = state
    def set_external_light(self, state):
        self.external_light = state
    def set_annun(self, state):
        self.annun = state
    def set_ad(self, state):
        self.ad = state
    def set_horn(self, state):
        self.horn = state
    def set_temp(self, num):
        self.temp = num
    def set_failure_flag(self, state):
        self.failure_flag = state
    # def set_passenger_brake_flag(self, state):
    #     self.passenger_brake_flag = state
    def set_ki(self, num):
        self.ki = num
    def set_kp(self, num):
        self.kp = num
    def set_power(self, num):
        self.power = num

    #get methods
    def get_speed_limit(self):  #desired speed from train model
        return self.speed_limit
    def get_commanded_speed(self):  #commended speed from manual mode (driver)
        return self.commanded_speed
    def get_speed(self):    #current speed of the train
        return self.speed
    def get_authority(self):
        return self.authority
    def get_left_door(self):
        return self.door_left
    def get_right_door(self):
        return self.door_right
    def get_internal_light(self):
        return self.internal_light
    def get_external_light(self):
        return self.external_light
    def get_annun(self):
        return self.annun
    def get_ad(self):
        return self.ad
    def get_horn(self):
        return self.horn
    def get_temp(self):
        return self.temp
    def get_failure_flag(self):
        return self.failure_flag
    # def get_passenger_brake_flag(self):
    #     return self.passenger_brake_flag
    def get_power(self):
        return self.power
    def get_ki(self):
        return self.ki
    def get_kp(self):
        return self.kp

    def train_running(self):
        self.door_left = "Closed"
        self.door_right = "Closed"
        self.internal_light = "On"
        self.external_light = "On"
        self.ad = "Off"
        self.annun = "Off"
        self.horn = "Off"

    def initialize_PID(self, kp_val, ki_val):   #whenever values change, re-initalize the PID
        self.k_p = kp_val
        self.k_i = ki_val
        self.pid = PID(self.k_p, self.k_i, 0, setpoint=self.commanded_speed)
        self.pid.outer_limits = (0, 120000) # clamp at max power output specified in datasheet 120kW

    def get_power_output(self): 

        self.pid.setpoint = self.commanded_speed    #commanded speed = desired speed
        self.power = self.pid(self.speed)   #if train has speed, you get less power to speed up than starting from speed = 0

        if self.power < 0:
            self.power = 0.0

    def update_power(self):
        self.initialize_PID(self.get_kp(), self.get_ki())
        self.get_power_output()

    def set_beacon(self, str):
        self.beacon = str
    
    def get_beacon(self):
        return self.beacon

class WindowClass(QtWidgets.QMainWindow, form_mainWindow) :
    def __init__(self) :
        super().__init__()
        self.init_ui()
        #self.show()

    def init_ui(self):
        self.setupUi(self)
        self.test_program.triggered.connect(self.pop_test)  #menu button opens test window
        self.automatic_button.clicked.connect(self.automatic_mode)
        self.manual_button.clicked.connect(self.manual_mode)
        self.login_button.clicked.connect(self.login)
        self.reset_button.clicked.connect(self.reset)
        self.apply_button.clicked.connect(self.apply_driver_change)
        self.engineer_apply_button.clicked.connect(self.apply_engineer_change)

        self.normal_brake.clicked.connect(self.normal_slow)
        self.emergency_brake.clicked.connect(self.emergency_slow)
        
        self.user_cb.setCurrentIndex(-1)
        self.cs_box.setReadOnly(False)

        self.begin_state()

        self.main_warning = warningWindow()  #warning window
        self.real_train = train_status()   #train body

        self.auto_f = False     #flag for auto mode
        self.manual_f = False   #flag for manual mode

        self.norm_brake_flag = False
        self.emer_brake_flag = False
        self.train_authority_stop_flag = False

        self.automatic_mode()   #auto mode on by default

        self.train_speed_overexceed_flag = False
        self.train_tunnel_flag = False
        self.auto_emergency_brake_flag = False

        self.ki_box.setPlainText(str(self.real_train.get_ki()))
        self.kp_box.setPlainText(str(self.real_train.get_kp()))

        #update train controller display every 1 sec
        # self.timer_update = QtCore.QTimer(self) 
        # self.timer_update.start(1000)
        # self.timer_update.timeout.connect(self.update_in_controller) 

        # print(self.real_train.get_power())

        # self.real_train.set_commanded_speed(60) #whereas speed = 0
        # self.real_train.update_power()
        # print(self.real_train.get_power())

        # self.real_train.set_speed(self.real_train.get_commanded_speed())    #60
        # self.real_train.set_commanded_speed(40)
        # self.real_train.update_power()
        # print(self.real_train.get_power())

        # self.real_train.set_speed(10)
        # self.real_train.set_commanded_speed(50)
        # self.real_train.update_power()
        # print(self.real_train.get_power())

    def pop_test(self):
        self.hide()
        self.test = testWindow()
        self.test.back_signal.connect(self.show)    #when get signal back, self.show to show mainwindow back

    def login(self):
        content = self.user_cb.currentText()    #read the content of user_cb

        if (content == "Driver"):
            self.button_frame.show()
            self.failure_frame.show()
            self.train_frame.show()
            self.driver_frame.show()

            self.engineer_frame.hide()

        elif (content == "Train Controller Engineer"):
            self.button_frame.hide()
            self.failure_frame.hide()
            self.train_frame.hide()
            self.driver_frame.hide()

            self.engineer_frame.show()

        else:
            self.main_warning.signal_detected("You must login. Try again")

    #normal brake
    def normal_slow(self):
        if self.normal_brake.text() == "Normal Brake":
            self.normal_brake.setStyleSheet("background-color: red")
            self.normal_brake.setText("Normal Brake On")
            self.norm_brake_flag = True

            # val = self.real_train.get_speed() - 10
            # if (val < 0) : val = 0
            # self.real_train.set_speed(val)

        else:
            self.normal_brake.setStyleSheet("background-color: light gray")
            self.normal_brake.setText("Normal Brake")
            self.norm_brake_flag = False

    #ememrgency brake
    def emergency_slow(self):
        if self.emergency_brake.text() == "Emergency Brake":
            self.emergency_brake.setStyleSheet("background-color: red")
            self.emergency_brake.setText("Emergency Brake On")
            self.emer_brake_flag = True

            # val = self.real_train.get_speed() - 25  #deacceleration rate = 25
            # if (val < 0) : val = 0
            # self.real_train.set_speed(val)

        else:
            self.emergency_brake.setStyleSheet("background-color: light gray")
            self.emergency_brake.setText("Emergency Brake")
            self.emer_brake_flag = False

    def begin_state(self):
        self.failure_frame.hide()
        self.engineer_frame.hide()
        self.train_frame.hide()
        self.driver_frame.hide()
        self.button_frame.hide()

    def apply_driver_change(self):
        #check value before updating
        if (self.check_value() == False):
            return
        
        self.real_train.set_commanded_speed(float(self.cs_box.toPlainText()))
        self.control_speed()    #keep below speed limit
        self.real_train.set_door_left(self.check_left_door())
        self.real_train.set_door_right(self.check_right_door())
        self.real_train.set_internal_light(self.check_internal_light())
        self.real_train.set_external_light(self.check_external_light())
        self.real_train.set_temp(int(self.temperature_box.toPlainText()))
        self.real_train.set_annun(self.check_annun())
        self.real_train.set_ad(self.check_ad())
        self.real_train.set_horn(self.check_horn())

        #self.update_train_display()

    #Check if all the inputs are in.
    def check_value(self):

        if (self.auto_f == False and self.manual_f == False):
            self.main_warning.signal_detected("You must choose the mode. Try again")
            return False

        if self.auto_f == False and self.manual_f == True:
            if (self.cs_box.toPlainText().isdigit() == False):
                self.main_warning.signal_detected("Your commanded speed is incorrect. Try again")
                return False
            elif (self.temperature_box.toPlainText().isdigit() == False):   # or self.temperature_box.toPlainText() == "0"
                self.main_warning.signal_detected("Your temperature is incorrect. Try again")
                return False
            elif self.check_radio_box() == False:
                self.main_warning.signal_detected("Didn't select On/Off for all. Try again")
                return False
        # elif self.check_ki_kp() == False:
        #     self.main_warning.signal_detected("Incorrect Ki, KP value. Try again")
        #     return False
        return True

    #prevent speed from exceeding the limit
    def control_speed(self):
        if self.real_train.get_commanded_speed() > self.real_train.get_speed_limit():
            self.real_train.set_commanded_speed(self.real_train.get_speed_limit())

    def apply_engineer_change(self):
        #if self.check_ki_kp() == False:
        #    return

        #apply ki kp values
        self.real_train.set_ki(float(self.ki_box.toPlainText()))
        self.real_train.set_kp(float(self.kp_box.toPlainText()))

    def check_ki_kp(self):
        if self.ki_box.toPlainText().isdigit() == False or self.ki_box.toPlainText() == "0":
            self.main_warning.signal_detected("Incorrect Ki value. Try again")
            return False
        elif self.kp_box.toPlainText().isdigit() == False or self.kp_box.toPlainText() == "0":
            self.main_warning.signal_detected("Incorrect Kp value. Try again")
            return False
        return True

    #check if all radio buttons are selected
    def check_radio_box(self):
        if (
            (self.left_on.isChecked() or self.left_off.isChecked()) and 
            (self.right_on.isChecked() or self.right_off.isChecked()) and 
            (self.internal_on.isChecked() or self.internal_off.isChecked()) and 
            (self.external_on.isChecked() or self.external_off.isChecked()) and 
            (self.annun_on.isChecked() or self.annun_off.isChecked()) and 
            (self.ad_on.isChecked() or self.ad_off.isChecked()) and 
            (self.horn_on.isChecked() or self.horn_off.isChecked())
        ) == False:
            return False

    #display values to train screen
    def update_train_display(self):
        self.train_speed.display(self.real_train.get_speed())
        self.train_power.display(self.real_train.get_power())
        self.train_left.setPlainText(self.real_train.get_left_door())
        self.train_right.setPlainText(self.real_train.get_right_door())
        self.train_internal.setPlainText(self.real_train.get_internal_light())
        self.train_external.setPlainText(self.real_train.get_external_light())
        self.train_temp.setPlainText(str(self.real_train.get_temp()))
        if self.real_train.get_annun() == "On":
            self.train_annun.setPlainText(self.real_train.get_annun() + " - " + self.real_train.get_beacon())
        else:
            self.train_annun.setPlainText(self.real_train.get_annun())
        self.train_ad.setPlainText(self.real_train.get_ad())
        self.train_horn.setPlainText(self.real_train.get_horn())

    def check_left_door(self):
        if self.left_on.isChecked(): return self.left_on.text()
        elif self.left_off.isChecked(): return self.left_off.text()

    def check_right_door(self):
        if self.right_on.isChecked(): return self.right_on.text()
        elif self.right_off.isChecked(): return self.right_off.text()
    
    def check_internal_light(self):
        if self.internal_on.isChecked(): return self.internal_on.text()
        elif self.internal_off.isChecked(): return self.internal_off.text()

    def check_external_light(self):
        if self.external_on.isChecked(): return self.external_on.text()
        elif self.external_off.isChecked(): return self.external_off.text()
    
    def check_annun(self):
        if self.annun_on.isChecked(): return self.annun_on.text()
        elif self.annun_off.isChecked(): return self.annun_off.text()

    def check_ad(self):
        if self.ad_on.isChecked(): return self.ad_on.text()
        elif self.ad_off.isChecked(): return self.ad_off.text()

    def check_horn(self):
        if self.horn_on.isChecked(): return self.horn_on.text()
        elif self.horn_off.isChecked(): return self.horn_off.text()

    #runs in train model
    def update_in_controller(self):
        #if failure occurs
        if self.real_train.get_failure_flag() == True:
            #decrease speed
            if self.auto_f == True: 
                self.emer_brake_flag = True
                self.emergency_brake.setStyleSheet("background-color: red")
                self.emergency_brake.setText("Emergency Brake On")
                self.auto_emergency_brake_flag = True

            self.failure_frame.setStyleSheet("background-color: red")
            self.failure_output.clear()
            self.failure_output.append("Exists!")
        else:
            #if failure doesn't exist, but auto_emergency_brake_flag is still on
            if self.auto_emergency_brake_flag == True and self.auto_f == True:
                self.auto_emergency_brake_flag = False
                self.emer_brake_flag = False
                self.emergency_brake.setStyleSheet("background-color: light gray")
                self.emergency_brake.setText("Emergency Brake")
            
            #changes the interface of the button back to original color
            self.failure_frame.setStyleSheet("background-color: white")
            self.failure_output.clear()
            self.failure_output.append("N/A")

        if self.auto_f == True and self.real_train.get_authority() > 0 and self.train_tunnel_flag == False:
            self.real_train.set_door_left("Closed")
            self.real_train.set_door_right("Closed")
            self.real_train.set_external_light("Off")
            self.real_train.set_internal_light("Off")
            self.real_train.set_annun("Off")
            self.real_train.set_horn("Off")
            self.real_train.set_ad("On")

        #if train came to stop (fully) in auto mode
        # if self.real_train.get_power() == 0 and self.auto_f == True:
        #     self.auto_train_stopped()

        #NOTE Update power. Train model uses power --> speed & pass actual speed + commanded speed to train controller
        self.real_train.update_power() 

        #if train reaches the end of track (authority = 0), set power = 0
        if self.real_train.get_speed() > self.real_train.get_commanded_speed() + 3:
            self.train_speed_overexceed_flag = True
            self.set_norm_brake_flag(True)
        elif self.get_norm_brake_flag() == True and self.train_speed_overexceed_flag == True and self.real_train.get_speed() < self.real_train.get_commanded_speed() + 3:
            self.set_norm_brake_flag(False)
            self.train_speed_overexceed_flag = False

        if self.real_train.get_authority() == 0:
            self.train_authority_stop_flag = True
            self.set_norm_brake_flag(True)
        #if train moving & normal brake flag is on & train authority stop flag is still True then:
        elif self.real_train.get_authority != 0 and self.get_norm_brake_flag() == True and self.train_authority_stop_flag == True:
            self.set_norm_brake_flag(False)
            self.train_authority_stop_flag = False

        #update to screen
        self.update_train_display()

    #if in tunnel
    def train_in_tunnel(self, tunnel_status):

        #only change states when in automatic mode
        if self.manual_f == True:
            return

        if tunnel_status == True:
            self.train_tunnel_flag = True
            self.real_train.set_external_light("On")
            self.real_train.set_internal_light("On")
        else:
            self.train_tunnel_flag = False
            self.real_train.set_external_light("Off")
            self.real_train.set_internal_light("Off")

    def train_in_station(self, station_status):

        #if in manual mode, reject
        if self.manual_f == True:
            return

        if station_status == True and self.real_train.speed == 0:
            self.real_train.set_door_left("Opened")
            self.real_train.set_door_right("Opened")
        else:
            self.real_train.set_door_left("Closed")
            self.real_train.set_door_right("Closed")

    #if train is at stop, status changes accordingly
    # def auto_train_stopped(self):
    #     self.real_train.set_door_left("Opened")
    #     self.real_train.set_door_right("Opened")
    #     self.real_train.set_external_light("On")
    #     self.real_train.set_annun("On")
    #     self.real_train.set_horn("On")

    def get_emer_brake_flag(self):
        return self.emer_brake_flag
    
    def get_norm_brake_flag(self):
        return self.norm_brake_flag

    def set_emer_brake_flag(self, state):
        self.emer_brake_flag = state

    def set_norm_brake_flag(self, state):
        self.norm_brake_flag = state

    def reset(self):
        #self.real_train.reset_all_train()
        # self.train_speed.display(0)
        # self.train_left.clear()
        # self.train_right.clear()
        # self.train_internal.clear()
        # self.train_external.clear()
        # self.train_temp.clear()
        # self.train_annun.clear()
        # self.train_ad.clear()
        # self.train_horn.clear()

        #clear input boxes
        self.cs_box.clear()
        self.temperature_box.clear()

        self.left_on.setAutoExclusive(False)
        self.left_on.setChecked(False)
        self.left_on.setAutoExclusive(True)

        self.left_off.setAutoExclusive(False)
        self.left_off.setChecked(False)
        self.left_off.setAutoExclusive(True)
        
        self.right_on.setAutoExclusive(False)
        self.right_on.setChecked(False)
        self.right_on.setAutoExclusive(True)

        self.right_off.setAutoExclusive(False)
        self.right_off.setChecked(False)
        self.right_off.setAutoExclusive(True)

        self.internal_on.setAutoExclusive(False)
        self.internal_on.setChecked(False)
        self.internal_on.setAutoExclusive(True)

        self.internal_off.setAutoExclusive(False)
        self.internal_off.setChecked(False)
        self.internal_off.setAutoExclusive(True)

        self.external_on.setAutoExclusive(False)
        self.external_on.setChecked(False)
        self.external_on.setAutoExclusive(True)

        self.external_off.setAutoExclusive(False)
        self.external_off.setChecked(False)
        self.external_off.setAutoExclusive(True)

        self.annun_on.setAutoExclusive(False)
        self.annun_on.setChecked(False)
        self.annun_on.setAutoExclusive(True)

        self.annun_off.setAutoExclusive(False)
        self.annun_off.setChecked(False)
        self.annun_off.setAutoExclusive(True)

        self.ad_on.setAutoExclusive(False)
        self.ad_on.setChecked(False)
        self.ad_on.setAutoExclusive(True)

        self.ad_off.setAutoExclusive(False)
        self.ad_off.setChecked(False)
        self.ad_off.setAutoExclusive(True)

        self.horn_on.setAutoExclusive(False)
        self.horn_on.setChecked(False)
        self.horn_on.setAutoExclusive(True)

        self.horn_off.setAutoExclusive(False)
        self.horn_off.setChecked(False)
        self.horn_off.setAutoExclusive(True)

        # self.emergency_brake.setStyleSheet("background-color: light gray")
        # self.emergency_brake.setText("Emergency Brake")

        # self.normal_brake.setStyleSheet("background-color: light gray")
        # self.normal_brake.setText("Normal Brake")

        # self.failure_frame.setStyleSheet("background-color: light gray")
        # self.failure_output.clear()
        # self.failure_output.append("N/A")

    def partial_reset(self):    #when switch from manual -> automatic, clear out manual section
        #clear input boxes
        self.cs_box.clear()
        self.temperature_box.clear()

        self.left_on.setAutoExclusive(False)
        self.left_on.setChecked(False)
        self.left_on.setAutoExclusive(True)

        self.left_off.setAutoExclusive(False)
        self.left_off.setChecked(False)
        self.left_off.setAutoExclusive(True)
        
        self.right_on.setAutoExclusive(False)
        self.right_on.setChecked(False)
        self.right_on.setAutoExclusive(True)

        self.right_off.setAutoExclusive(False)
        self.right_off.setChecked(False)
        self.right_off.setAutoExclusive(True)

        self.internal_on.setAutoExclusive(False)
        self.internal_on.setChecked(False)
        self.internal_on.setAutoExclusive(True)

        self.internal_off.setAutoExclusive(False)
        self.internal_off.setChecked(False)
        self.internal_off.setAutoExclusive(True)

        self.external_on.setAutoExclusive(False)
        self.external_on.setChecked(False)
        self.external_on.setAutoExclusive(True)

        self.external_off.setAutoExclusive(False)
        self.external_off.setChecked(False)
        self.external_off.setAutoExclusive(True)

        self.annun_on.setAutoExclusive(False)
        self.annun_on.setChecked(False)
        self.annun_on.setAutoExclusive(True)

        self.annun_off.setAutoExclusive(False)
        self.annun_off.setChecked(False)
        self.annun_off.setAutoExclusive(True)

        self.ad_on.setAutoExclusive(False)
        self.ad_on.setChecked(False)
        self.ad_on.setAutoExclusive(True)

        self.ad_off.setAutoExclusive(False)
        self.ad_off.setChecked(False)
        self.ad_off.setAutoExclusive(True)

        self.horn_on.setAutoExclusive(False)
        self.horn_on.setChecked(False)
        self.horn_on.setAutoExclusive(True)

        self.horn_off.setAutoExclusive(False)
        self.horn_off.setChecked(False)
        self.horn_off.setAutoExclusive(True)

    ############
    #  Modes   #
    ############
    def automatic_mode(self):
        self.partial_reset()    #clear out manual input section (partially)

        self.auto_f = True
        self.manual_f = False
        self.automatic_button.setEnabled(False) #once activated, cannot press again
        self.manual_button.setEnabled(True)

        self.cs_box.setReadOnly(True)
        self.temperature_box.setReadOnly(True)
        self.left_on.setCheckable(False)
        self.left_off.setCheckable(False)
        self.right_on.setCheckable(False)
        self.right_off.setCheckable(False)
        self.internal_on.setCheckable(False)
        self.internal_off.setCheckable(False)
        self.external_on.setCheckable(False)
        self.external_off.setCheckable(False)
        self.annun_on.setCheckable(False)
        self.annun_off.setCheckable(False)
        self.ad_on.setCheckable(False)
        self.ad_off.setCheckable(False)
        self.horn_on.setCheckable(False)
        self.horn_off.setCheckable(False)

        self.apply_button.setEnabled(False)
        self.reset_button.setEnabled(False)

        self.cs_box.setStyleSheet("background-color: gray")
        self.temperature_box.setStyleSheet("background-color: gray")
    

    def manual_mode(self):
        self.manual_f = True
        self.auto_f = False
        self.manual_button.setEnabled(False)
        self.automatic_button.setEnabled(True)  #can press automatic button

        self.cs_box.setReadOnly(False)
        self.temperature_box.setReadOnly(False)
        self.left_on.setCheckable(True)
        self.left_off.setCheckable(True)
        self.right_on.setCheckable(True)
        self.right_off.setCheckable(True)
        self.internal_on.setCheckable(True)
        self.internal_off.setCheckable(True)
        self.external_on.setCheckable(True)
        self.external_off.setCheckable(True)
        self.annun_on.setCheckable(True)
        self.annun_off.setCheckable(True)
        self.ad_on.setCheckable(True)
        self.ad_off.setCheckable(True)
        self.horn_on.setCheckable(True)
        self.horn_off.setCheckable(True)

        self.apply_button.setEnabled(True)
        self.reset_button.setEnabled(True)

        self.cs_box.setStyleSheet("background-color: light gray")
        self.temperature_box.setStyleSheet("background-color: light gray")

if __name__ == "__main__" :

    app = QtWidgets.QApplication(sys.argv) 
    myWindow = WindowClass() 
    sys.exit(app.exec_())
    