import math
from train_ui import TrainData_Ui
from PyQt5 import QtCore, QtWidgets
import sys
sys.path.append(".")
from train_model_signals import *
from Train_Controller.train_controller_main import WindowClass
from Signals import signals
from PyQt5.QtCore import pyqtSlot

class Train:
    
    def __init__(self, ID = 0):

        #train id
        self.id = ID

        #dispatch information???
        #self.destination_block = destination_block
        #self.line = line
        #block list = array of blocks from starting block to destination block

        #beacon info
        self.next_station = ""
        self.door_side = 0               #0 = closed, 1 = left, 2 = right, 3 = both

        #physical train info
        self.train_length = 105.6       #ft
        self.train_width = 11.2         #ft
        self.train_height = 9.7         #ft
        self.crew_count = 1
        self.passenger_count = 0
        self.mass = 40.25               #imperial tons

        #train movement info
        self.actual_speed = 0.0         #mph
        self.commanded_speed = 0.0      #mph
        self.grade = 0.0                #%ft risen per 100 ft
        self.power = 0.0                #kilowatts
        self.acceleration = 0           #ft/s^2
        self.authority = 0
        self.distance = 0               #meters
        self.force = 0

        #various train functions
        self.ac_cmd = 68.0              #degrees farenheight
        self.horn = "Off"
        self.interior_light_cmd = "On"
        self.exterior_light_cmd = "Off"
        self.right_door_cmd = "Opened"
        self.left_door_cmd = "Opened"
        self.advertisement_cmd = "On"
        self.announcement_cmd = "On"

        #failures
        self.brake_failure = False
        self.signal_pickup_failure = False
        self.engine_failure = False
        self.track_fail = False

        #brakes
        self.passenger_ebrake = False
        self.ebrake = False
        self.sbrake = False
        
        #constants
        self.GRAVITY = 9.80665                     #m/s^2
        self.FRICTION_COE = 0.02
        self.ACCELERATION_LIMIT = .5            #m/s^2
        self.DECELERATION_SERVICE = -1.2        #m/s^2
        self.DECELERATION_EMERGENCY = -2.73     #m/s^2
        self.VELOCITY_LIMIT = 43.496                #kph
        self.POWER_LIMIT = 120000              #watts
        self.PASSENGER_LIMIT = 222
        self.MAX_GRADIENT = 60

        #signals

        #track model inputs
        signals.send_tm_authority.connect(self.train_model_update_authority)
        signals.send_tm_grade.connect(self.get_grade)
        signals.send_tm_failure.connect(self.get_track_failure)
        signals.send_tm_beacon.connect(self.get_beacon)
        signals.send_tm_passenger_count.connect(self.train_model_update_passengers)
        signals.send_tm_commanded_speed.connect(self.train_model_update_command_speed)

        #open ui
        signals.open_tm_gui.connect(self.show_tm_ui)
        signals.open_tm_gui.connect(self.show_tc_ui)

        #update function
        signals.train_update.connect(self.update_values)

        #from ui
        ui_sig.train_model_transfer_brake_failure.connect(self.train_model_transfer_brake_failure)
        ui_sig.train_model_transfer_engine_falure.connect(self.train_model_transfer_engine_failure)
        ui_sig.train_model_transfer_signal_pickup_failure.connect(self.train_model_transfer_signal_pickup_failure)
        ui_sig.train_model_fix_failure.connect(self.train_model_fix_failure)
        ui_sig.train_model_transfer_passenger_ebrake.connect(self.train_model_passenger_ebrake)

        #setup ui
        self.app = QtWidgets.QApplication(sys.argv)
        self.train_model = QtWidgets.QMainWindow()
        self.ui = TrainData_Ui()
        self.ui.setupUi(self.train_model)
        #self.train_model.show()
        self.ui.train_id_line.setText(str(self.id))

        #train controller that controls this train
        self.train_ctrl = WindowClass()

        #train runs until it reaches destination
        self.run_continuously = True

        #timer for testing
        # self.train_timer = QtCore.QTimer()
        # self.train_timer.start(1000)
        # self.train_timer.timeout.connect(self.update_values)

# ---------------------------------------------------------------------------------------------
# ----------------------------- Update Train ------------------------------------------------
# ---------------------------------------------------------------------------------------------



    def update_values(self):    #run every 1 sec (infinite loop)
        #set values of connected train controller
        self.train_ctrl.real_train.set_authority(self.authority)    #authoritys
        self.train_ctrl.real_train.set_commanded_speed(self.commanded_speed) #desired speed
        self.train_ctrl.real_train.set_speed(self.actual_speed)       #actual speed
        
        #send failure to train controller
        if(self.engine_failure or self.brake_failure or self.signal_pickup_failure):
            self.train_ctrl.real_train.set_failure_flag(True)
        else:
            self.train_ctrl.real_train.set_failure_flag(False)

        #call controller update function
        self.train_ctrl.update_in_controller()

        #do run kinematics calculation
        self.power = self.train_ctrl.real_train.get_power()
        self.train_model_update_speed()

        #get updated values from train controller
        self.left_door_cmd = self.train_ctrl.real_train.get_left_door()
        self.right_door_cmd = self.train_ctrl.real_train.get_right_door()
        self.interior_light_cmd = self.train_ctrl.real_train.get_internal_light()
        self.exterior_light_cmd = self.train_ctrl.real_train.get_external_light()
        self.advertisement_cmd = self.train_ctrl.real_train.get_ad()
        self.ac_cmd = self.train_ctrl.real_train.get_temp()
        self.horn = self.train_ctrl.real_train.get_horn()
        self.sbrake = self.train_ctrl.get_norm_brake_flag()
        self.ebrake = self.train_ctrl.get_emer_brake_flag()
        self.announcement_cmd = self.train_ctrl.real_train.get_annun()
        self.advertisement_cmd = self.train_ctrl.real_train.get_ad()

        #update displayed values
        self.train_model_display_announcement()
        self.train_model_display_adv()
        self.train_model_display_temp()
        self.train_model_display_external_lights()
        self.train_model_display_internal_lights()
        self.train_model_display_horn()
        self.train_model_display_left_door()
        self.train_model_display_right_door()

        #self.door_side[] = self.train_ctrl.get_door_left()

        #update train controller display
        self.train_ctrl.update_train_display()
        #self.show_tc_ui(0)

# ---------------------------------------------------------------------------------------------
# ----------------------------- Show UIs ------------------------------------------------------
# ---------------------------------------------------------------------------------------------

    #show train model ui
    def show_tm_ui(self, id):
        if(self.id == id):
            self.train_model.show()

    #show train controller ui
    def show_tc_ui(self, ctrlid):
        if(self.id == ctrlid):
            self.train_ctrl.show()

# ---------------------------------------------------------------------------------------------
# ----------------------------- Train Controller Inputs ---------------------------------------
# ---------------------------------------------------------------------------------------------

    #display internal lights
    def train_model_display_internal_lights(self):
        #print("Interior lights: ", self.interior_light_cmd)
        if(self.interior_light_cmd == "On"):
            self.ui.int_light_line.setText("On")
        else:
            self.ui.int_light_line.setText("Off")
        #signals.train_model_update.emit()

    #display external lights
    def train_model_display_external_lights(self):
        if(self.exterior_light_cmd == "On"):
            self.ui.ext_light_line.setText("On")
        else:
            self.ui.ext_light_line.setText("Off")
        #signals.train_model_update.emit()

    #display advertisement
    def train_model_display_adv(self):
        if(self.advertisement_cmd == "On"):
            self.ui.advertisement_line.setText("On")
        else:
            self.ui.advertisement_line.setText("Off")
        #signals.train_model_update.emit()

    #sets status of doors
    # def train_model_toggle_doors(self):
    #     #opens doors depending on the station
    #     if(self.door_side == 1):
    #         self.left_door_cmd = 1
    #         self.right_door_cmd = 0
    #     elif(self.door_side == 2):
    #         self.right_door_cmd = 1
    #         self.left_door_cmd = 0
    #     elif(self.door_side == 3):
    #         self.left_door_cmd = 1
    #         self.right_door_cmd = 1
    #     else:
    #         self.left_door_cmd = 0
    #         self.right_door_cmd = 0
        #signals.train_model_update.emit()

    #display left door
    def train_model_display_left_door(self):
        if(self.left_door_cmd == "Opened"):
            self.ui.left_door_line.setText("Opened")
        else:
            self.ui.left_door_line.setText("Closed")
        #signals.train_model_update.emit()

    #display right door
    def train_model_display_right_door(self):
        if(self.right_door_cmd == "Opened"):
            self.ui.right_door_line.setText("Opened")
        else:
            self.ui.right_door_line.setText("Closed")
        #signals.train_model_update.emit()

    #display announcement
    def train_model_display_announcement(self):
        if(self.announcement_cmd == "On"):
            self.ui.announcement_line.setText("On")
        else:
            self.ui.announcement_line.setText("Off")
        #signals.train_model_update.emit()

    #display horn
    def train_model_display_horn(self):
        if(self.horn == "On"):
            self.ui.horn_line.setText("On")
        else:
            self.ui.horn_line.setText("Off")
        #signals.train_model_update.emit()

    #display advertisement
    def train_model_transfer_ads(self):
        if(self.advertisement_cmd):
            self.ui.advertisement_line.setText("On")
        else:
            self.ui.advertisement_line.setText("Off")
        #signals.train_model_update.emit()

    #display temp
    def train_model_display_temp(self):
        self.ui.temp_line.setText(str(self.ac_cmd))
        #signals.train_model_update.emit()

# ---------------------------------------------------------------------------------------------
# ----------------------------- Track Model Inputs --------------------------------------------
# ---------------------------------------------------------------------------------------------

    #get beacon info: doorside, station name, others
    def get_beacon(self, beacon):
        self.station_name = beacon
        #signals.train_model_update.emit()

    #get grade from track model
    def get_grade(self, trainnum, new_grade):
        if(self.id == trainnum):
            self.grade = new_grade
            self.ui.grade_line.setText(str(self.grade))
            #signals.train_model_update.emit()        

    #update authority
    def train_model_update_authority(self, trainnum, new_auth):
        if(self.id == trainnum):
            if(self.signal_pickup_failure):
                self.authority = 0
            else:    
                self.authority = new_auth

            self.ui.authority_line.setText(str(self.authority))
        #signals.train_model_update.emit()

    #update commanded speed
    def train_model_update_command_speed(self, trainnum, new_cmd_speed):
        if(self.id == trainnum):
            if(self.signal_pickup_failure):
                self.commanded_speed = 0
            else:    
                self.commanded_speed = new_cmd_speed

            self.ui.suggested_speed_line.setText(str(self.commanded_speed))
        #signals.train_model_update.emit()

    #update passenger count and calculate new mass
    def train_model_update_passengers(self, trainnum, pass_count):
        if(self.id == trainnum):
            if(pass_count > self.PASSENGER_LIMIT):
                self.passenger_count = self.PASSENGER_LIMIT
            else:
                self.passenger_count = pass_count
            if(pass_count > 0):
                self.mass = 40.25 + ((self.crew_count + self.passenger_count) * 0.0738155)
            self.ui.mass_line.setText(str(self.mass))
            self.ui.passenger_line.setText(str(self.passenger_count))
            #signals.train_model_update.emit()

    #sets beacon info
    def train_model_transfer_beacon(self, trainnum, door_side, station):
        if(self.id == trainnum):
            self.door_side = door_side
            self.next_station = station
            self.ui.station_line = station
            #signals.train_model_update.emit()

    #get if track is in failure
    def get_track_failure(self, failure):
            self.track_fail = failure
    
    #stops train
    def stop_train(self):
        self.run_continuously = False
    
# ---------------------------------------------------------------------------------------------
# ----------------------------- Murphy Inputs -------------------------------------------------
# ---------------------------------------------------------------------------------------------

    #murphy fixes any failure
    def train_model_fix_failure(self):
        self.brake_failure = False
        self.engine_failure = False
        self.signal_pickup_failure = False
        self.ui.brake_button.setStyleSheet("background-color : white")
        self.ui.engine_button.setStyleSheet("background-color : white")
        self.ui.sp_button.setStyleSheet("background-color : white")

        #signals.train_model_update.emit()

    #murphy sets failure
    def train_model_transfer_brake_failure(self):
        self.brake_failure = True
        self.ui.brake_button.setStyleSheet("background-color: red")
        #signals.train_model_update.emit()

    #murphy sets failure
    def train_model_transfer_engine_failure(self):
        self.engine_failure = True
        self.power = 0
        self.ui.engine_button.setStyleSheet("background-color: red")
        #signals.train_model_update.emit()

    #murphy sets failure
    def train_model_transfer_signal_pickup_failure(self):
        self.signal_pickup_failure = True
        self.ui.sp_button.setStyleSheet("background-color: red")
        #signals.train_model_update.emit()

# ---------------------------------------------------------------------------------------------
# ----------------------------- Passenger Inputs ----------------------------------------------
# ---------------------------------------------------------------------------------------------
 
    #get emergency brake from passenger
    def train_model_passenger_ebrake(self):
        self.passenger_ebrake = not(self.passenger_ebrake)
        if(self.passenger_ebrake):
            self.ui.pbrake_button.setStyleSheet("background-color: red")
        else:
            self.ui.pbrake_button.setStyleSheet("background-color: white")
        #signals.train_model_update.emit()

# ---------------------------------------------------------------------------------------------
# ----------------------------- Newtons laws calculation --------------------------------------
# ---------------------------------------------------------------------------------------------

    def train_model_update_speed(self):
        #convert kW to watts
        power = self.power
        power *= 1000

        # if(self.track_fail):
        #     power = 0
        #     self.ebrake = True

        #if train is running
        self.run_continuously = True
        if (self.run_continuously):

            #set power to 0 if engine failed
            if(self.engine_failure):
                power = 0
            
            #if power exceeds limit, set to limit of engine
            if(power > self.POWER_LIMIT):
                power = self.POWER_LIMIT

            #convert imperial to metric
            #ft/s^2 to m/s^2
            prev_acceleration = self.acceleration / 3.28084
            sample_period = 1
            prev_distance = self.distance
            #mph to m/s
            temp_actual_speed = self.actual_speed / 2.237
            #imperial tons to metric tons
            mass = self.mass * 1.01605


            run = True
            #if there is a route, set current block and run
            # if (len(self.block_list) > 0):
            #     #if theres block is not a station, run
            #     if (self.block_list[0].station == ""):
            #         current_block = self.block_list[0]
            #         current_block_length = current_block.block_length
            #         self.grade = current_block.grade
            #         run = True
            #     else:
            #         #stop the train if block is a station
            #         self.run_continuously = False
            #         run = False
            # else:
            #     #stop the train if route doesnt exist
            #     self.run_continuously = False
            #     run = False

            #stop when controller tells me

            #test
            run = True

            if (run):
                #FORCE CALCULATION
                #if (self.sbrake or self.ebrake or self.passenger_ebrake or self.power == 0):
                #if power is 0 and train is moving
                if (self.power == 0 and temp_actual_speed > 0):
                    self.force = 0
                    self.force -= self.FRICTION_COE * mass * self.GRAVITY * math.cos(self.grade)
                #else if power is 0 and train is not moving
                elif (self.power == 0 and temp_actual_speed == 0):
                    self.force = 0
                #else power is greater than 0 and train is moving
                else:
                    if(temp_actual_speed == 0):
                        self.force = self.FRICTION_COE * mass * self.GRAVITY * math.cos(self.grade)
                    # if brakes off
                    elif(not(self.sbrake) and not(self.ebrake) and not(self.passenger_ebrake)):
                    #else:
                        self.force = (power / temp_actual_speed)
                        self.force -= self.FRICTION_COE * mass * self.GRAVITY * math.cos(self.grade)
                    else:
                        self.force = 0
                    #if service brake on
                    #elif(self.sbrake and not self.ebrake and not self.passenger_ebrake):
                    #    self.force = (power / temp_actual_speed)
                    #    self.force -= self.FRICTION_COE * mass * self.GRAVITY * math.cos(self.grade)
                    #    self.force -= self.DECELERATION_SERVICE * self.mass
                    #if passenger ebrake or ebrake is on
                    #elif(self.ebrake or self.passenger_ebrake):
                    #    self.force = (power / temp_actual_speed)
                    #    self.force -= self.FRICTION_COE * mass * self.GRAVITY * math.cos(self.grade)
                    #    self.force -= self.DECELERATION_EMERGENCY * self.mass
                    #if(self.force < 0):
                    #    self.force = 0

                    #MOVE EBRAKE PASSENGER BRAKE

                # pprint("Force: ")
                # pprint(force)
                #self.ui.grade_line.setText(str(round(self.force,1)))

                #ACCELERATION CALCULATION
                #pprint(self.passenger_ebrake)
                #print("pass brake: ", self.passenger_ebrake)
                #print("force: ", self.force)
                #print("mass", self.mass)
                #print("sbrake: ", self.sbrake)
                #print("ebrake: ", self.ebrake)
                temp_acceleration = self.force/mass
                if(temp_acceleration > self.ACCELERATION_LIMIT):
                    temp_acceleration = self.ACCELERATION_LIMIT
                elif(self.brake_failure):
                    temp_acceleration = temp_acceleration
                elif(self.sbrake and not(self.ebrake or self.passenger_ebrake)):
                    temp_acceleration = self.DECELERATION_SERVICE
                elif(self.ebrake or self.passenger_ebrake):
                    temp_acceleration = self.DECELERATION_EMERGENCY
                
                
                #pprint(temp_acceleration)

                #VELOCITY CALCULATION

                #print("temp accel: ", temp_acceleration)
                #print("prev accel: ", prev_acceleration)
                temp_velocity = temp_actual_speed + ((sample_period/2) * (temp_acceleration + prev_acceleration))
                if(temp_velocity > self.VELOCITY_LIMIT):
                    temp_velocity = self.VELOCITY_LIMIT
                elif(temp_velocity < 0):
                    temp_velocity = 0

                #pprint(temp_velocity)

                #DISTANCE CALCULATION
                temp_distance = prev_distance + (temp_velocity * sample_period)
                self.distance = temp_distance
                signals.send_tm_distance.emit(self.id, self.distance)
                
                # #if position length is greater than block length, move to next block
                # if (temp_position > current_block_length):
                #     #if at last block in route, at destnation, stop
                #     if (len(self.block_list) <= 1):
                #         self.block_list.pop(0)
                #         temp_position = current_block_length
                #         self.run_continuously = False
                #     else:
                #         #move to next block
                #         temp_position -= current_block_length
                #         #remove block that train has passed, update current block
                #         self.block_list.pop(0)
                #         self.current_block = self.block_list[0]
                #         current_block = self.block_list[0]
                
                        #send block occupancy to track model
                        #signals.track_model_update_block_occupancy.emit(self.id, current_block)
                
                self.actual_speed = temp_velocity * 2.237
                #if (self.actual_speed > self.VELOCITY_LIMIT):
                #    self.actual_speed = self.VELOCITY_LIMIT
                #if (self.actual_speed > self.train_ctrl.real_train.get_commanded_speed()):
                #    self.actual_speed = self.train_ctrl.real_train.get_commanded_speed()

                #print("speed: ", self.actual_speed)
                self.ui.velocity_line.setText(str(round(self.actual_speed, 2)))

                self.acceleration = temp_acceleration * 3.28084
                self.ui.acceleration_line.setText(str(round(self.acceleration,2)))
                # pprint("Acceleration: ")
                # pprint(self.acceleration)

                #send speed to train ctrl, get new power
                self.power = power / 1000

                #self.actual_speed = 20
                #self.real_train.set_commanded_speed(self.commanded_speed)
                #self.power = self.train_ctrl.real_train.power_calculation(self.actual_speed)

                #print("power:" , self.power)
                #pprint("-------------------------------")

                self.ui.power_line.setText(str(round(self.power,1)))

                #signals.train_model_update.emit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    TrainModel = Train()
    sys.exit(app.exec_())
