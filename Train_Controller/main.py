import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
from errorWindow import warningWindow
from testWindow import testWindow, trainBody

form_mainWindow = uic.loadUiType("TrainController.ui")[0]

class WindowClass(QtWidgets.QMainWindow, form_mainWindow) :
    def __init__(self) :
        super().__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setupUi(self)
        self.test_program.triggered.connect(self.pop_test)  #menu button opens test window
        self.automatic_button.clicked.connect(self.automatic_mode)
        self.manual_button.clicked.connect(self.manual_mode)
        self.login_button.clicked.connect(self.login)
        self.reset_button.clicked.connect(self.reset)
        self.apply_button.clicked.connect(self.apply_driver_change)
        self.engineer_apply_button.clicked.connect(self.apply_engineer_change)
        self.activate_button.clicked.connect(self.activate_program)

        self.normal_brake.clicked.connect(self.normal_slow)
        self.emergency_brake.clicked.connect(self.emergency_slow)
        
        self.user_cb.setCurrentIndex(-1)

        self.begin_state()

        self.main_warning = warningWindow()  #warning window
        self.real_train = trainBody()   #train body

        self.auto_f = False     #flag for auto mode
        self.manual_f = False   #flag for manual mode
        #self.failure_main_flag = False

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

    def normal_slow(self):
        val = self.real_train.get_speed() - 10
        if (val < 0) : val = 0
        self.real_train.set_speed(val)
        self.train_speed.display(val)

    def emergency_slow(self):
        val = self.real_train.get_speed() - 25
        if (val < 0) : val = 0
        self.real_train.set_speed(val)
        self.train_speed.display(val)

    def activate_program(self):
        t = self.activate_button.text()
        if t == "Activate":
            #self.apply_driver_change()
            self.activate_button.setText("Waiting..")
            self.activate_button.setStyleSheet("background-color: red")
        elif t == "Waiting..":
            self.activate_button.setText("Activate")
            self.activate_button.setStyleSheet("background-color: light gray")

        #also add ki, kp

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
        self.real_train.set_temp(float(self.temperature_box.toPlainText()))
        self.real_train.set_annun(self.check_annun())
        self.real_train.set_ad(self.check_ad())
        self.real_train.set_horn(self.check_horn())

        self.copy_to_train_frame()

    def check_value(self):

        if (self.auto_f == False and self.manual_f == False):
            self.main_warning.signal_detected("You must choose the mode. Try again")
            return False
        elif (self.cs_box.toPlainText().isdigit() == False or self.cs_box.toPlainText() == "0"):
            self.main_warning.signal_detected("Your commanded speed is incorrect. Try again")
            return False
        elif (self.temperature_box.toPlainText().isdigit() == False or self.temperature_box.toPlainText() == "0"):
            self.main_warning.signal_detected("Your temperature is incorrect. Try again")
            return False
        elif self.check_radio_box() == False:
            self.main_warning.signal_detected("Didn't select On/Off for all. Try again")
            return False
        elif self.check_ki_kp() == False:
            self.main_warning.signal_detected("Incorrect Ki, KP value. Try again")
            return False
        return True

    def control_speed(self):
        if self.real_train.get_commanded_speed() > self.real_train.get_speed_limit():
            self.real_train.set_speed(self.real_train.get_speed_limit())
        else:
            self.real_train.set_speed(self.real_train.get_commanded_speed())    #for now

    def apply_engineer_change(self):
        if self.check_ki_kp() == False:
            return

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

    def copy_to_train_frame(self):
        self.train_speed.display(self.real_train.get_speed())
        self.train_left.setPlainText(self.real_train.get_left_door())
        self.train_right.setPlainText(self.real_train.get_right_door())
        self.train_internal.setPlainText(self.real_train.get_internal_light())
        self.train_external.setPlainText(self.real_train.get_external_light())
        self.train_temp.setPlainText(str(self.real_train.get_temp()))
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

    def reset(self):
        self.real_train.reset_all_train()
        self.train_speed.display(0)
        self.train_left.clear()
        self.train_right.clear()
        self.train_internal.clear()
        self.train_external.clear()
        self.train_temp.clear()
        self.train_annun.clear()
        self.train_ad.clear()
        self.train_horn.clear()

        self.manual_button.setEnabled(True)
        self.automatic_button.setEnabled(True)

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

        #ki, kp
        self.ki_box.clear()
        self.kp_box.clear()
    
    def partial_reset(self):
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

    def automatic_mode(self):
        self.partial_reset()    #clear out partially

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


#threadL https://ybworld.tistory.com/39