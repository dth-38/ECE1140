import sys
from simple_pid import PID
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
from errorWindow import warningWindow
from logWindow import logWindow

form_testWindow = uic.loadUiType("TrainControllerTest.ui")[0]

#for train
class trainBody:

    def __init__(self):
        self.speed_limit = 60 #mph in default
        self.commanded_speed = 0.0
        self.speed = 0.0
        self.authority = 0.0
        self.door_left = ""
        self.door_right = ""
        self.internal_light = ""
        self.external_light = ""
        self.annun = ""
        self.ad = ""
        self.horn = ""
        self.temp = 0.0
        
        self.ki = 0.01
        self.kp = 1
        self.pid = PID(self.kp, self.ki, 0, setpoint=self.commanded_speed) # initialize pid with fixed values
        self.pid.outer_limits = (0, 120000)                                  # clamp at max power output specified in datasheet 120kW
        self.power = 0

    #set methods
    def set_authority(self, num):
        self.authority = num
    def set_commanded_speed(self, num):
        self.commanded_speed = num
    def set_speed(self, num):
        self.speed = num
    def set_speed_limit(self, num):
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
    def set_ki(self, num):
        self.ki = num
    def set_kp(self, num):
        self.kp = num
    def set_power(self, num):
        self.power = num

    #get methods
    def get_speed_limit(self):
        return self.speed_limit
    def get_commanded_speed(self):
        return self.commanded_speed
    def get_speed(self):
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

    def reset_all_train(self):
        self.ki = 0.0
        self.kp = 0.0
        self.power = 0.0

    def get_power(self):
        return self.power

    def initialize_PID(self, kp_val, ki_val):
        self.k_p = kp_val
        self.k_i = ki_val
        self.pid = PID(self.k_p, self.k_i, 0, setpoint=self.commanded_speed)
        self.pid.outer_limits = (0, 120000) # clamp at max power output specified in datasheet 120kW

    def get_power_output(self): 
        self.pid.setpoint = self.commanded_speed    #commanded speed = desired speed
        self.power = self.pid(self.speed)   #if train has speed, you get less power to speed up than starting from speed = 0
        if self.power > 0:
            return self.power
        
        else:
            self.power = 0
            return self.power

    def update_power(self):
        self.initialize_PID()
        self.get_power_output()

class testWindow(QtWidgets.QMainWindow, form_testWindow) :
    #signal for window changing
    back_signal = QtCore.pyqtSignal()

    def __init__(self) :
        super(testWindow, self).__init__()
        self.init_ui()
        self.show()

    def init_ui(self):

        self.warning_win = warningWindow()
        self.log_win = logWindow()
        self.thomas = trainBody()

        self.setupUi(self)
        self.close_button.clicked.connect(self.close_button_pressed)   #cancel button closes window
        self.automatic_button.clicked.connect(self.auto_mode)
        self.manual_button.clicked.connect(self.manual_mode)
        self.clear_input_button.clicked.connect(self.clear_input)

        self.door_left_cb.setCurrentIndex(-1)   #display empty CB
        self.door_right_cb.setCurrentIndex(-1)
        self.internal_cb.setCurrentIndex(-1)
        self.external_cb.setCurrentIndex(-1)
        self.annun_cb.setCurrentIndex(-1)
        self.ad_cb.setCurrentIndex(-1)
        self.horn_cb.setCurrentIndex(-1)
        
        #brakes
        self.normal_brake_button.setEnabled(False)
        self.emer_brake_button.setEnabled(False)
        self.apply_button.setEnabled(False)
        self.normal_brake_button.clicked.connect(self.normal_slow)
        self.emer_brake_button.clicked.connect(self.emer_slow)
        self.apply_button.clicked.connect(self.apply_changes)

        #failures
        self.activate_failure_button.clicked.connect(self.activate_failure)
        self.reset_failure_button.clicked.connect(self.reset_failure)

        self.failure_cb.setCurrentIndex(-1)

        #test
        self.run_button.clicked.connect(self.run_test)
        self.pause_button.clicked.connect(self.pause_test)
        self.stop_button.clicked.connect(self.stop_test)
        self.reset_button.clicked.connect(self.reset_all)
        self.log_button.clicked.connect(self.file_open)
        self.clear_log_button.clicked.connect(self.file_clear)

        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.reset_button.setEnabled(False) #Enabled when test is finished

        self.clear_result_button.setEnabled(False)
        self.clear_result_button.clicked.connect(self.clear_result)

        self.speed_input_box.setText("0")

        self.norm_brake = False
        self.emer_brake = False

        self.pause_flag = False
        self.stop_flag = False
        self.failure_flag = False

        self.auto_flag = False
        self.manual_flag = False
        self.display_flag = False   #if failure message has been displayed, then this becomes true

    #close the test UI
    def close_button_pressed(self):
        self.close()
        self.back_signal.emit() #returns back_signal to mainwindow when test window closes

    #run the test
    def run_test(self):
        #check all the values to make sure that they're accurate
        if (self.check_value() == False):
            return
        
        self.update_value() #update input to train body

        #disable ki & kp from changes as train starts
        self.ki_input.setReadOnly(True)
        self.kp_input.setReadOnly(True)
        self.ki_input.setStyleSheet("background-color: gray")
        self.kp_input.setStyleSheet("background-color: gray")

        self.pause_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        self.reset_button.setEnabled(False)
        self.run_button.setEnabled(False)

        self.normal_brake_button.setEnabled(True)
        self.emer_brake_button.setEnabled(True)
        self.apply_button.setEnabled(True)

        self.pause_button.setText("Pause")
        self.pause_button.setStyleSheet("background-color: light gray")

        #train moving for the number of authority
        #num_auth = self.thomas.get_authority()
        #for i in range(num_auth):
        #    self.show_result(i)    #append result to log

        self.block_num = 1
        self.timer = QtCore.QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.show_result)

    def pause_test(self):
        text = self.pause_button.text()

        if (text == "Pause"):
            self.pause_flag = True
            self.pause_button.setText("Resume")
            self.pause_button.setStyleSheet("background-color: red")
        
        else:   #resume
            self.pause_flag = False
            self.pause_button.setText("Pause")
            self.pause_button.setStyleSheet("background-color: light gray")
            self.resume_test()

    def resume_test(self):
        self.result_block.append("===== Test Resumes =====")
        self.timer = QtCore.QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.show_result)

    def stop_test(self):
        self.stop_flag = True
        self.stop_button.setEnabled(False)

    #check all the values
    def check_value(self):

        if (self.auto_flag == False and self.manual_flag == False):
            self.warning_win.signal_detected("Please select the mode")
            return False
        #commanded speed & actual speed can be 0
        elif(self.cs_input_box.toPlainText().isdigit() == False):
            self.warning_win.signal_detected("Your commanded speed is incorrect. Try again with different value")
            return False
        elif(self.speed_input_box.toPlainText().isdigit() == False):
            self.warning_win.signal_detected("Your speed is incorrect. Try again with different value")
            return False
        elif(self.auth_input_box.toPlainText().isdigit() == False or self.auth_input_box.toPlainText() == "0"):
            self.warning_win.signal_detected("Your authority is incorrect. Try again with different value")
            return False
        elif(
            self.door_left_cb.currentIndex() == -1 or self.door_right_cb.currentIndex() == -1 or 
            self.internal_cb.currentIndex() == -1 or self.external_cb.currentIndex() == -1 or
            self.annun_cb.currentIndex() == -1 or self.ad_cb.currentIndex() == -1 or
            self.horn_cb.currentIndex() == -1
        ):
            self.warning_win.signal_detected("Please choose either On/Off for all the combo boxes")
            return False
        elif(self.temp_box.toPlainText().isdigit() == False or float(self.temp_box.toPlainText()) < 50):  #default temp = 50 F
            self.warning_win.signal_detected("Your temperature is incorrect. Try again with different value")
            return False
        elif(self.ki_input.toPlainText().isdigit() == False or self.ki_input.toPlainText() == "0"):
            self.warning_win.signal_detected("Your KI value is incorrect. Try again with different value")
            return False
        elif(self.kp_input.toPlainText().isdigit() == False or self.kp_input.toPlainText() == "0"):
            self.warning_win.signal_detected("Your KP value is incorrect. Try again with different value")
            return False

        return True

    def update_value(self):
        #self.thomas.set_speed_limit(float(self.speed_limit_box.toPlainText()))
        self.thomas.set_commanded_speed(float(self.cs_input_box.toPlainText()))
        if (self.thomas.get_speed_limit() < self.thomas.get_commanded_speed()): #if exceeds speed limit, set it at max
            self.thomas.set_commanded_speed(self.thomas.get_speed_limit())
        elif (0 > self.thomas.get_commanded_speed()):   #if negative speed given
            self.thomas.set_commanded_speed(0)

        #if speed has 0, ignore (it's default is 0, so no need to update)
        if (self.speed_input_box.toPlainText() != "0"):
            self.thomas.set_speed(float(self.speed_input_box.toPlainText()))    #actual speed
        #if below 0, set to 0
        elif (float(self.speed_input_box.toPlainText()) < 0):
            self.thomas.set_speed(0)

        self.thomas.set_authority(float(self.auth_input_box.toPlainText()))
        self.thomas.set_door_left(self.door_left_cb.currentText())
        self.thomas.set_door_right(self.door_right_cb.currentText())
        self.thomas.set_internal_light(self.internal_cb.currentText())
        self.thomas.set_external_light(self.external_cb.currentText())
        self.thomas.set_annun(self.annun_cb.currentText())
        self.thomas.set_ad(self.ad_cb.currentText())
        self.thomas.set_horn(self.horn_cb.currentText())
        self.thomas.set_temp(float(self.temp_box.toPlainText()))

        #set Ki, Kp
        self.thomas.set_ki(float(self.ki_input.toPlainText()))
        self.thomas.set_kp(float(self.kp_input.toPlainText()))


    #for normal brake
    def normal_slow(self):
        text = self.normal_brake_button.text()

        if (text == "Normal Brake"):
            self.normal_brake_button.setText("Release")
            self.normal_brake_button.setStyleSheet("background-color: red")
            self.norm_brake = True

        else:
            self.normal_brake_button.setText("Normal Brake")
            self.normal_brake_button.setStyleSheet("background-color: light gray")
            self.norm_brake = False

    #for emergency brake
    def emer_slow(self):
        text = self.emer_brake_button.text()

        if (text == "Emergency Brake"):
            self.emer_brake_button.setText("Release")
            self.emer_brake_button.setStyleSheet("background-color: red")
            self.emer_brake = True
        else:
            self.emer_brake_button.setText("Emergency Brake")
            self.emer_brake_button.setStyleSheet("background-color: light gray")
            self.emer_brake = False

    #run selected failure
    def activate_failure(self):
        failure_name = self.failure_cb.currentText()

        if (failure_name == "Engine Failure"):
            self.failure_1.setStyleSheet("background-color: red;")
            self.failure_cb.model().item(1).setEnabled(False)
            self.failure_flag = True

        elif (failure_name == "Broken Rail"):
            self.failure_2.setStyleSheet("background-color: red")
            self.failure_cb.model().item(2).setEnabled(False)
            self.failure_flag = True

        elif (failure_name == "Track Circuit Failure"):
            self.failure_3.setStyleSheet("background-color: red")
            self.failure_cb.model().item(3).setEnabled(False)
            self.failure_flag = True

    #reset failure frame
    def reset_failure(self):
        self.failure_cb.model().item(1).setEnabled(True)
        self.failure_cb.model().item(2).setEnabled(True)
        self.failure_cb.model().item(3).setEnabled(True)
        self.failure_1.setStyleSheet("background-color: white;")
        self.failure_2.setStyleSheet("background-color: white;")
        self.failure_3.setStyleSheet("background-color: white;")
        self.failure_flag = False
    
    #reset input frame
    def clear_input(self):
        #self.speed_limit_box.clear()
        self.cs_input_box.clear()
        self.speed_input_box.setText("0")
        self.auth_input_box.clear()
        #display empty CB
        self.door_left_cb.setCurrentIndex(-1)
        self.door_right_cb.setCurrentIndex(-1)
        self.internal_cb.setCurrentIndex(-1)
        self.external_cb.setCurrentIndex(-1)
        self.annun_cb.setCurrentIndex(-1)
        self.ad_cb.setCurrentIndex(-1)
        self.horn_cb.setCurrentIndex(-1)
        self.temp_box.clear()

        #ki, kp
        self.ki_input.clear()
        self.kp_input.clear()

    def clear_result(self):
        self.result_block.clear()

    def clear_flag(self):
        self.display_flag = False
        self.auto_flag = False
        self.manual_flag = False
        self.stop_flag = False
        self.pause_flag = False
        self.failure_flag = False
        self.emer_brake = False
        self.norm_brake = False
    
    def set_to_zero(self):
        self.speed_input_box.setReadOnly(False)
        self.speed_input_box.setText("0")
        self.thomas.set_speed(float(self.speed_input_box.toPlainText()))    #set actual speed to 0

    #revert status of brakes after reset
    def clear_brakes(self):
        if self.emer_brake_button.text() == "Release":
            self.emer_brake_button.setText("Emergency Brake")
            self.emer_brake_button.setStyleSheet("background-color: light gray")
        
        if self.normal_brake_button.text() == "Release":
            self.normal_brake_button.setText("Normal Brake")
            self.normal_brake_button.setStyleSheet("background-color: light gray")

    #reset everything
    def reset_all(self):
        self.clear_brakes()
        self.clear_input()
        self.reset_failure()
        self.clear_result()
        self.clear_flag()
        self.manual_input_state()
        self.automatic_button.setEnabled(True)
        self.manual_button.setEnabled(True)
        self.run_button.setEnabled(True)
        self.thomas.reset_all_train()

    #append the result to log
    def show_result(self):

        #For speed of train in beginning & end--------------------------
        #Reaches current speed + half of commanded speed during 1st block
        #slow down to stop the train

        #if no brake is taking place, change speed to commanded speed
        if (self.norm_brake == False and self.emer_brake == False):

            #reduce speed by half before the authority
            if (self.block_num == (self.thomas.get_authority())):
                self.thomas.set_speed(self.thomas.get_speed() - self.thomas.get_commanded_speed()/2)

            #if speeds are not the same
            elif (self.thomas.get_speed() != self.thomas.get_commanded_speed()):

                #if speed < commanded speed
                if (self.thomas.get_speed() < self.thomas.get_commanded_speed()):
                    self.thomas.set_speed(self.thomas.get_speed() + self.thomas.get_commanded_speed() / 2)

                    #if exceeds the maximum
                    if (self.thomas.get_speed() > self.thomas.get_commanded_speed()):
                        self.thomas.set_speed(self.thomas.get_commanded_speed())

                #if speed > commanded speed
                elif (self.thomas.get_speed() > self.thomas.get_commanded_speed()):
                    prev_val = self.thomas.get_speed()
                    self.thomas.set_speed(self.thomas.get_speed() - self.thomas.get_commanded_speed() / 2)

                    #if subtraction resulted in speed < commanded speed
                    if (self.thomas.get_speed() < prev_val):
                        self.thomas.set_speed(self.thomas.get_commanded_speed())

        #NOTE: when actual speed > commended speed, actual speed just becomes commanded speed (weird)

        #if (self.block_num == (self.thomas.get_authority())):
        #    self.thomas.set_speed(self.thomas.get_speed() - self.thomas.get_commanded_speed() / 2)
        #-----------------------------------------------------------------

        if (self.apply_button.text() == "Applied!"):
            self.apply_button.setText("Apply Changes")
            self.apply_button.setStyleSheet("background-color: light gray")

        #give access accordingly
        if (self.auto_flag == True):
            self.auto_input_state()
            self.speed_input_box.setReadOnly(True)
        elif (self.manual_flag == True):
            self.manual_input_state()
            #enable changing value of actual speed
            self.speed_input_box.setReadOnly(False)

        #if failure occurs in auto mode, automatically press emergency brake (this only runs once)-----------------
        if (self.failure_flag == True and self.display_flag == False):
            self.display_flag = True
            self.result_block.append("****Failure Occurred!****")
            if (self.auto_flag == True):
                self.emer_slow()    #change the appearance of emergency button

        if (self.auto_flag == True and self.failure_flag == True):  #emergency brake raised automatically in auto mode
            self.emer_brake = True
            self.thomas.set_commanded_speed(self.thomas.get_commanded_speed() - 25)
            if (self.thomas.get_commanded_speed() < 0):
                self.thomas.set_commanded_speed(0)
            self.thomas.set_speed(self.thomas.get_speed() - 25)
            #self.thomas.set_commanded_speed(self.thomas.get_speed())

        elif(self.manual_flag == True):
            if (self.emer_brake == True):
                self.thomas.set_speed(self.thomas.get_commanded_speed() - 25)

            elif (self.norm_brake == True):
                self.thomas.set_speed(self.thomas.get_commanded_speed() - 10)

        #if speed <= 0, stop train immediately
        if (self.thomas.get_speed() <= 0):
            self.train_stop()
            self.timer.stop()
            return

        #update values
        #self.update_value()

        #prints----------------------------------------------------------------------------
        if (self.block_num == 1):
            self.result_block.append("-----Passing {}st Block------".format(self.block_num))
        elif(self.block_num == 2):
            self.result_block.append("-----Passing {}nd Block------".format(self.block_num))
        elif(self.block_num == 3):
            self.result_block.append("-----Passing {}rd Block------".format(self.block_num))
        else:
            self.result_block.append("-----Passing {}th Block-----".format(self.block_num))
        
        self.result_block.append("Commanded Speed: {}".format(self.thomas.get_commanded_speed()))
        self.result_block.append("Actual Speed: {}".format(self.thomas.get_speed()))
        self.result_block.append("Door Status: ")
        self.result_block.append("  - Left: {}".format(self.thomas.get_left_door()))
        self.result_block.append("  - Right: {}".format(self.thomas.get_right_door()))
        self.result_block.append("Light Status:") 
        self.result_block.append("  - Internal: {}".format(self.thomas.get_internal_light()))
        self.result_block.append("  - External: {}".format(self.thomas.get_external_light()))
        self.result_block.append("Annunciation: {}".format(self.thomas.get_annun()))
        self.result_block.append("Advertisement: {}".format(self.thomas.get_ad()))
        self.result_block.append("Horn: {}".format(self.thomas.get_horn()))
        self.result_block.append("Temperature: {}".format(self.thomas.get_temp()))

        #power calculation
        self.thomas.update_power()
        if (self.emer_brake == True or self.block_num == self.thomas.get_authority()):
            self.thomas.set_power(0)
        elif self.norm_brake == True:
            self.thomas.set_power(0)

        self.result_block.append("Power: {}".format(self.thomas.get_power()))

        #-------------------------------------------------------------------------------------

        #if block_num is same as authority, stop timer
        #or stop flag is raised or pause flag is raised
        if (self.block_num == self.thomas.get_authority() or self.stop_flag == True):
            self.timer.stop()
            if self.stop_flag == True:
                self.result_block.append("===== TRAIN FORCEFULLY STOPPED =====")
                self.result_block.append("")
            else:
                self.result_block.append("===== TEST ENDED (reached authority) =====")
                self.result_block.append("")
            self.disable_test()

        if (self.pause_flag == True):
            self.timer.stop()
            self.result_block.append("===== PAUSED (Resume to Continue...) =====")

        self.block_num += 1

    #when speed = 0
    def train_stop(self):
        self.result_block.append("===== TRAIN STOPPED FROM SLOW DOWN =====")
        self.disable_test()
    
    #disable test & add to log
    def disable_test(self):
        #after done
        self.write_to_file("##### Train Departure #####\n")
        self.write_to_file(self.result_block.toPlainText())

        self.set_to_zero()
        self.run_button.setEnabled(False)   #user must press reset button to run another test
        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.reset_button.setEnabled(True)

        #ki & kp comes back
        self.ki_input.setReadOnly(False)
        self.kp_input.setReadOnly(False)
        self.ki_input.setStyleSheet("background-color: light gray")
        self.kp_input.setStyleSheet("background-color: light gray")

    def auto_mode(self):
        self.auto_flag = True
        self.manual_flag = False
        self.automatic_button.setEnabled(False)
        self.manual_button.setEnabled(True)

    def manual_mode(self):
        self.manual_flag = True
        self.auto_flag = False
        self.automatic_button.setEnabled(True)
        self.manual_button.setEnabled(False)

    def apply_changes(self):
        #when apply button pressed, update_value gets called (while train is moving)
        self.update_value()
        #self.thomas.set_speed(self.thomas.get_speed())
        self.apply_button.setText("Applied!")
        self.apply_button.setStyleSheet("background-color: green")

    # def change_emer_button(self):
    #     text = self.emer_brake_button.text()
    #     self.emer_brake_button.setEnabled(False)

    #     if (text == "Emergency Brake"):
    #         self.emer_brake_button.setText("Release")
    #         self.emer_brake_button.setStyleSheet("background-color: red")
    #         self.emer_brake = True

    def file_open(self):
        f = open("train_controller_log.txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            self.log_win.insert_str(line)  #write to log window & display

        self.log_win.display()
        f.close()
    
    def write_to_file(self, str):
        f = open("train_controller_log.txt", 'a')
        f.write(str)    #append to file
        f.close()
    
    def file_clear(self):
        open("train_controller_log.txt", 'w').close()   #clear the file
        self.log_win.clear_log_win()
        self.warning_win.signal_detected("Log successfully cleared!")

    def auto_input_state(self):
        
        #DriverFrame
        self.speed_input_box.setReadOnly(True)
        self.cs_input_box.setReadOnly(True)
        self.temp_box.setReadOnly(True)
        self.auth_input_box.setReadOnly(True)
        self.door_left_cb.setEnabled(False)
        self.door_right_cb.setEnabled(False)
        self.internal_cb.setEnabled(False)
        self.external_cb.setEnabled(False)
        self.annun_cb.setEnabled(False)
        self.ad_cb.setEnabled(False)
        self.horn_cb.setEnabled(False)

    def manual_input_state(self):
        
        #DriverFrame
        self.cs_input_box.setReadOnly(False)
        self.speed_input_box.setReadOnly(False)
        self.auth_input_box.setReadOnly(False)
        self.temp_box.setReadOnly(False) 
        self.door_left_cb.setEnabled(True)
        self.door_right_cb.setEnabled(True)
        self.internal_cb.setEnabled(True)
        self.external_cb.setEnabled(True)
        self.annun_cb.setEnabled(True)
        self.ad_cb.setEnabled(True)
        self.horn_cb.setEnabled(True)