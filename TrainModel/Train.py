import math
from TrainModel.TrainUi import TrainData_Ui
#from TrainUi import TrainData_Ui
from PyQt5 import QtCore, QtWidgets
import sys
sys.path.append(".")
from TrainModel.TrainModelSignals import *
from Train_Controller.train_controller_main import WindowClass
from Signals import signals
from PyQt5.QtCore import pyqtSlot



class Train:

    #constants used in calculations
    GRAVITY = 9.80665                     #m/s^2
    FRICTION_COE = 0.02
    ACCELERATION_LIMIT = .5            #m/s^2
    DECELERATION_SERVICE = -1.2        #m/s^2
    DECELERATION_EMERGENCY = -2.73     #m/s^2
    VELOCITY_LIMIT = 43.496                #kph
    POWER_LIMIT = 120000              #watts
    PASSENGER_LIMIT = 222
    MAX_GRADIENT = 60
    
    def __init__(self, ID = 0):

        #Train id of this instance of a train
        self.id = ID

        #Information stored in the most recent beacon train has passed
        self.next_station = ""
        self.door_side = -1               #0 = left, 1 = right, 2 = both

        #Information about the physical properties of the train
        self.train_length = 105.6       #Ft
        self.train_width = 11.2         #Ft
        self.train_height = 9.7         #Ft
        self.crew_count = 1
        self.passenger_count = 0
        self.mass = 40.25               #Imperial tons

        #Information about block of track train is on
        self.grade = 0.0                #%Ft risen per 100 ft
        self.in_station = False
        self.in_tunnel = False
        self.authority = 0
        self.commanded_speed = 0.0      #mph

        #Information about the movement of the train
        self.actual_speed = 0.0         #mph
        self.power = 0.0                #kilowatts
        self.acceleration = 0           #ft/s^2
        self.distance = 0               #meters
        self.force = 0

        #Information about the physical state of the train
        self.ac_command = 68              #degrees farenheight
        self.actual_temp = 68
        self.horn = "Off"
        self.interior_light_cmd = "On"
        self.exterior_light_cmd = "Off"
        self.right_door_cmd = "Opened"
        self.left_door_cmd = "Opened"
        self.advertisement_cmd = "On"
        self.announcement_cmd = "On"

        #Boolean variables for failures, True = failure occuring
        self.brake_failure = False
        self.signal_pickup_failure = False
        self.engine_failure = False
        self.track_fail = False

        #Boolean variables for brakes, True = brake activated
        self.passenger_ebrake = False
        self.ebrake = False
        self.sbrake = False

        #Who is setting the temperature
        self.temp_from_ui = False
        self.ui_temp = 0
        self.prev_station = ""
        
        #Boolean so ticket sales are only set at the first tick train is stopped and at station
        self.sent_stopped_at_station_sig = False

        #authority saved when a train must come to a stop
        #used to restart the train without sending a new authority
        self.saved_authority = 0

        #Inputs from track model
        signals.send_tm_authority.connect(self.train_model_update_authority)
        signals.send_tm_grade.connect(self.update_grade)
        signals.send_tm_failure.connect(self.get_track_failure)
        signals.send_tm_beacon.connect(self.update_beacon)
        signals.send_tm_passenger_count.connect(self.train_model_update_passengers)
        signals.send_tm_commanded_speed.connect(self.train_model_update_command_speed)
        signals.send_tm_tunnel.connect(self.train_model_update_tunnel)
        signals.send_tm_station.connect(self.train_model_update_station)
        signals.send_tm_new_block.connect(self.decrement_authority)

        #Signals to open train model and train controller ui's
        signals.open_tm_gui.connect(self.show_tm_ui)
        signals.open_tc_gui.connect(self.show_tc_ui)

        #Update function that connects to the main system
        signals.train_update.connect(self.update_values)

        #Signals from ui to train
        ui_sig.train_model_transfer_brake_failure.connect(self.train_model_transfer_brake_failure)
        ui_sig.train_model_transfer_engine_falure.connect(self.train_model_transfer_engine_failure)
        ui_sig.train_model_transfer_signal_pickup_failure.connect(self.train_model_transfer_signal_pickup_failure)
        ui_sig.train_model_fix_failure.connect(self.train_model_fix_failure)
        ui_sig.train_model_transfer_passenger_ebrake.connect(self.train_model_passenger_ebrake)
        ui_sig.train_model_transfer_ac_cmd.connect(self.train_model_set_ac)

        #Setup train model ui
        self.train_model = QtWidgets.QMainWindow()
        self.ui = TrainData_Ui(self.id)
        self.ui.setup_ui(self.train_model)
        #self.train_model.show()
        self.ui.train_id_line.setText(str(self.id))

        #Initialize train controller
        self.train_ctrl = WindowClass()

        #timer for testing
        # self.train_timer = QtCore.QTimer()
        # self.train_timer.start(1000)
        # self.train_timer.timeout.connect(self.update_values)

# ---------------------------------------------------------------------------------------------
# ----------------------------- Update Train ------------------------------------------------
# ---------------------------------------------------------------------------------------------

    #Train Update function, runs every tick in an infinite loop.
    def update_values(self):
        #Pass track circuit signals to train controller
        self.train_ctrl.real_train.set_authority(self.authority)    #authority
        self.train_ctrl.real_train.set_commanded_speed(self.commanded_speed) #desired speed
        
        #Sends actual speed of train to train controller
        self.train_ctrl.real_train.set_speed(self.actual_speed)       #actual speed
        
        #Passes information about block train is on to train controller
        #self.train_ctrl.real_train.set_tunnel(self.in_tunnel)
        #self.train_ctrl.real_train.set_station(self.in_station)

        #Tell track model that train is stopped so that it can calculate passengers and ticket sales
        if(self.actual_speed == 0 and self.in_station and self.sent_stopped_at_station_sig == False):
            self.ui.station_line.setText("")
            signals.send_tm_stopped_at_station.emit(self.id)
            self.sent_stopped_at_station_sig = True

        #Reset stopped at station boolean when train starts moving again so signal can be sent again at next station
        if(self.actual_speed > 0):
            self.sent_stopped_at_station_sig = False
        
        #If there is a failure in the train, notify train controller
        if(self.engine_failure or self.brake_failure or self.signal_pickup_failure):
            self.train_ctrl.real_train.set_failure_flag(True)
        else:
            self.train_ctrl.real_train.set_failure_flag(False)

        
        #Run kinematics calculation
        self.power = self.train_ctrl.real_train.get_power()
        self.train_model_update_speed()

        #Send Train controller actual speed and power
        self.train_ctrl.real_train.set_speed(self.actual_speed)       #Since update_speed updates speed, also apply it to controller's actual speed
        self.train_ctrl.real_train.set_power(self.power)              #send power to train controller for display
        
        #If the engine is not in failure, display power in ui, else display 0
        if(not(self.engine_failure)):
            self.ui.power_line.setText(str(round(self.train_ctrl.real_train.power,1)))
        else:
            self.ui.power_line.setText(str(0.0))

        #Call controller update function
        self.train_ctrl.update_in_controller()
        

        #Configure door signal from train controller to correct door side
        self.left_door_cmd = self.train_ctrl.real_train.get_left_door()
        self.right_door_cmd = self.train_ctrl.real_train.get_right_door()
        if(self.in_station):
            self.train_model_update_doors()
        self.train_ctrl.real_train.set_door_left(self.left_door_cmd)
        self.train_ctrl.real_train.set_door_right(self.right_door_cmd)
        
        #Obtain light and advertisement commands from train controller
        self.interior_light_cmd = self.train_ctrl.real_train.get_internal_light()
        self.exterior_light_cmd = self.train_ctrl.real_train.get_external_light()
        self.advertisement_cmd = self.train_ctrl.real_train.get_ad()

        #Temp from passenger override temperature set from driver
        if(self.temp_from_ui == False):
            self.ac_command = self.train_ctrl.real_train.get_temp()
        else:
            self.ac_command = self.ui_temp
            self.train_ctrl.real_train.set_temp(self.ui_temp)
        self.regulate_temp()

        #Obtain various commands from train controller
        self.horn = self.train_ctrl.real_train.get_horn()
        self.sbrake = self.train_ctrl.get_norm_brake_flag()
        #Only turn off brakes if train isnt supposed to be stopped.
        if(self.brake_failure and self.authority >= 1):
            self.sbrake = False
        self.ebrake = self.train_ctrl.get_emer_brake_flag()
        self.announcement_cmd = self.train_ctrl.real_train.get_annun()
        self.advertisement_cmd = self.train_ctrl.real_train.get_ad()

        #Update values displayed in ui
        self.train_model_display_announcement()
        self.train_model_display_adv()
        self.train_model_display_temp()
        self.train_model_display_external_lights()
        self.train_model_display_internal_lights()
        self.train_model_display_horn()
        self.train_model_display_left_door()
        self.train_model_display_right_door()

        #Reset door side
        if(self.actual_speed == 0 and self.in_station and self.sent_stopped_at_station_sig == False):
            self.door_side = 3


# ---------------------------------------------------------------------------------------------
# ----------------------------- Show UIs ------------------------------------------------------
# ---------------------------------------------------------------------------------------------

    #Show train model ui
    def show_tm_ui(self, id):
        if(self.id == id):
            self.train_model.show()

    #Show train controller ui
    def show_tc_ui(self, ctrlid):
        if(self.id == ctrlid):
            self.train_ctrl.show()
            
# ---------------------------------------------------------------------------------------------
# ----------------------------- Train Controller Functions ------------------------------------
# ---------------------------------------------------------------------------------------------

    #Display internal lights
    def train_model_display_internal_lights(self):
        #print("Interior lights: ", self.interior_light_cmd)
        if(self.interior_light_cmd == "On"):
            self.ui.int_light_line.setText("On")
        else:
            self.ui.int_light_line.setText("Off")

    #Display external lights
    def train_model_display_external_lights(self):
        if(self.exterior_light_cmd == "On"):
            self.ui.ext_light_line.setText("On")
        else:
            self.ui.ext_light_line.setText("Off")

    #Display advertisement
    def train_model_display_adv(self):
        if(self.advertisement_cmd == "On"):
            self.ui.advertisement_line.setText("On")
        else:
            self.ui.advertisement_line.setText("Off")

    #Sets status of doors
    def train_model_update_doors(self):
        #opens doors depending on the station door side
        #left side
        if(self.door_side == 0):
            self.left_door_cmd = "Opened"
            self.right_door_cmd = "Closed"
        #right side
        elif(self.door_side == 1):
            self.right_door_cmd = "Closed"
            self.left_door_cmd = "Opened"
        #both sides
        elif(self.door_side == 2):
            self.left_door_cmd = "Closed"
            self.right_door_cmd = "Closed"

    #Display left door
    def train_model_display_left_door(self):
        if(self.left_door_cmd == "Opened"):
            self.ui.left_door_line.setText("Open")
        else:
            self.ui.left_door_line.setText("Closed")

    #Display right door
    def train_model_display_right_door(self):
        if(self.right_door_cmd == "Opened"):
            self.ui.right_door_line.setText("Open")
        else:
            self.ui.right_door_line.setText("Closed")

    #Display announcement
    def train_model_display_announcement(self):
        if(self.announcement_cmd == "On"):
            self.ui.announcement_line.setText("On")
        else:
            self.ui.announcement_line.setText("Off")

    #Display horn
    def train_model_display_horn(self):
        if(self.horn == "On"):
            self.ui.horn_line.setText("On")
        else:
            self.ui.horn_line.setText("Off")

    #Display advertisement
    def train_model_transfer_ads(self):
        if(self.advertisement_cmd):
            self.ui.advertisement_line.setText("On")
        else:
            self.ui.advertisement_line.setText("Off")

    #Display temp
    def train_model_display_temp(self):
        self.ui.temp_line.setText(str(self.actual_temp))

# ---------------------------------------------------------------------------------------------
# ----------------------------- Track Model Inputs --------------------------------------------
# ---------------------------------------------------------------------------------------------

    #Decrement authroity
    #@pyqtSlot()
    def decrement_authority(self):
        self.authority = self.authority - 1

        #authority cannot go below 0
        if self.authority < 0:
            self.authority = 0

        self.ui.authority_line.setText(str(self.authority))

    #Get beacon info: doorside, station name, others
    #@pyqtSlot(int, str, int)
    def update_beacon(self, id, station, side):
        if(id == self.id):
            if(station == self.prev_station):
                self.station_name = ""
            else:
                self.station_name = station
                self.prev_station = station

            self.door_side = side
            self.ui.station_line.setText(str(self.station_name))

    #Get grade from track model
    #@pyqtSlot(int, float)
    def update_grade(self, trainnum, new_grade):
        if(self.id == trainnum):
            self.grade = new_grade
            if(self.grade > Train.MAX_GRADIENT):
                self.grade = Train.MAX_GRADIENT
            self.ui.grade_line.setText(str(self.grade))        

    #Update authority
    #@pyqtSlot(int, int)
    def train_model_update_authority(self, trainnum, new_auth):
        if(self.id == trainnum):
            if(not(self.signal_pickup_failure)):
                #saves a previous authority if the train must stop
                #allows it to resume without a new authority being generated
                if new_auth == 0:
                    self.saved_authority = self.authority

                #restores old authority if a -1 is sent
                if new_auth == -1 and self.saved_authority != 0:
                    self.authority = self.saved_authority
                elif new_auth != -1:
                    self.authority = new_auth

                #workaround we might need if ctc sends wrong authority
                #self.authority = self.authority - 1

            self.ui.authority_line.setText(str(self.authority))

    #Update commanded speed
    #@pyqtSlot(int, int)
    def train_model_update_command_speed(self, trainnum, new_cmd_speed):
        if(self.id == trainnum):
            if(self.signal_pickup_failure):
                self.commanded_speed = 0
            else:    
                self.commanded_speed = new_cmd_speed

            self.ui.suggested_speed_line.setText(str(self.commanded_speed))

    #Update passenger count and calculate new mass
    #@pyqtSlot(int, int)
    def train_model_update_passengers(self, trainnum, pass_count):
        if(self.id == trainnum):
            if(pass_count > Train.PASSENGER_LIMIT):
                self.passenger_count = Train.PASSENGER_LIMIT
            else:
                self.passenger_count = pass_count
            if(pass_count > 0):
                self.mass = 40.25 + ((self.crew_count + self.passenger_count) * 0.0738155)
            self.ui.mass_line.setText(str(round(self.mass,2)))
            self.ui.passenger_line.setText(str(self.passenger_count))

    #Get if track is in failure
    def get_track_failure(self, failure):
            self.track_fail = failure

    #Track tells train if its in a tunnel
    def train_model_update_tunnel(self, trainnum, tunnel):
        if(self.id == trainnum):
                self.in_tunnel = tunnel

    #Track tells train if its at a station
    def train_model_update_station(self, trainnum, station):
        if(self.id == trainnum):
                self.in_station = station

# ---------------------------------------------------------------------------------------------
# ----------------------------- Murphy Inputs -------------------------------------------------
# ---------------------------------------------------------------------------------------------

    #Murphy fixes any failure
    def train_model_fix_failure(self, id):
        if(id == self.id):
            self.brake_failure = False
            self.engine_failure = False
            self.signal_pickup_failure = False
            self.ui.brake_button.setStyleSheet("background-color : white")
            self.ui.engine_button.setStyleSheet("background-color : white")
            self.ui.sp_button.setStyleSheet("background-color : white")

    #Murphy sets failure
    def train_model_transfer_brake_failure(self,id):
        if(id == self.id):
            self.brake_failure = True
            self.ui.brake_button.setStyleSheet("background-color: red")

    #Murphy sets failure
    def train_model_transfer_engine_failure(self, id):
        if(id == self.id):
            self.engine_failure = True
            self.power = 0.0
            self.ui.engine_button.setStyleSheet("background-color: red")

    #Murphy sets failure
    def train_model_transfer_signal_pickup_failure(self, id):
        if(id == self.id):
            self.signal_pickup_failure = True
            self.ui.sp_button.setStyleSheet("background-color: red")

# ---------------------------------------------------------------------------------------------
# ----------------------------- Passenger Inputs ----------------------------------------------
# ---------------------------------------------------------------------------------------------
 
    #Get emergency brake from passenger
    def train_model_passenger_ebrake(self, id):
        if(id == self.id):
            self.passenger_ebrake = not(self.passenger_ebrake)
            if(self.passenger_ebrake):
                self.ui.pbrake_button.setStyleSheet("background-color: red")
            else:
                self.ui.pbrake_button.setStyleSheet("background-color: white")

    #Regulate temperature in train
    def regulate_temp(self):
        if(self.actual_temp > self.ac_command):
            self.actual_temp = self.actual_temp - 1
        elif(self.actual_temp < self.ac_command):
            self.actual_temp = self.actual_temp + 1
        if(self.actual_temp == self.ac_command):
            self.temp_from_ui = False

    #Set cabin temperature
    def train_model_set_ac(self, id, ac):
        if(id == self.id):
            self.temp_from_ui = True
            self.ui_temp = ac

# ---------------------------------------------------------------------------------------------
# ----------------------------- Newtons laws calculation --------------------------------------
# ---------------------------------------------------------------------------------------------

    def train_model_update_speed(self):
        #convert kW to watts
        power = self.power
        power *= 1000

        if(self.track_fail):
            power = 0.0
            self.ebrake = True

        #if train is running
        self.run_continuously = True
        if (self.run_continuously):

            #set power to 0 if engine failed
            if(self.engine_failure):
                power = 0.0
            
            #if power exceeds limit, set to limit of engine
            if(power > Train.POWER_LIMIT):
                power = Train.POWER_LIMIT

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

            if (run):
                #FORCE CALCULATION
                #if (self.sbrake or self.ebrake or self.passenger_ebrake or self.power == 0):
                #if power is 0 and train is moving
                if (self.power == 0 and temp_actual_speed > 0):
                    self.force = 0
                    self.force -= Train.FRICTION_COE * mass * Train.GRAVITY * math.cos(self.grade)
                #else if power is 0 and train is not moving
                elif (self.power == 0 and temp_actual_speed == 0):
                    self.force = 0
                #else power is greater than 0 and train is moving
                else:
                    if(temp_actual_speed == 0):
                        self.force = Train.FRICTION_COE * mass * Train.GRAVITY * math.cos(self.grade)
                    # if brakes off
                    elif(not(self.sbrake) and not(self.ebrake) and not(self.passenger_ebrake)):
                    #else:
                        self.force = (power / temp_actual_speed)
                        self.force -= Train.FRICTION_COE * mass * Train.GRAVITY * math.cos(self.grade)
                    else:
                        self.force = 0
                    #if service brake on
                    #elif(self.sbrake and not self.ebrake and not self.passenger_ebrake):
                    #    self.force = (power / temp_actual_speed)
                    #    self.force -= Train.FRICTION_COE * mass * Train.GRAVITY * math.cos(self.grade)
                    #    self.force -= Train.DECELERATION_SERVICE * self.mass
                    #if passenger ebrake or ebrake is on
                    #elif(self.ebrake or self.passenger_ebrake):
                    #    self.force = (power / temp_actual_speed)
                    #    self.force -= Train.FRICTION_COE * mass * Train.GRAVITY * math.cos(self.grade)
                    #    self.force -= Train.DECELERATION_EMERGENCY * self.mass
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
                if(temp_acceleration > Train.ACCELERATION_LIMIT):
                    temp_acceleration = Train.ACCELERATION_LIMIT
                elif(self.sbrake and not(self.ebrake or self.passenger_ebrake)):
                    power = 0.0
                    if(self.actual_speed > 0):
                        temp_acceleration = Train.DECELERATION_SERVICE
                    else:
                        temp_acceleration = 0
                elif(self.ebrake or self.passenger_ebrake):
                    power = 0.0
                    if(self.actual_speed > 0):
                        temp_acceleration = Train.DECELERATION_EMERGENCY
                    else:
                        temp_acceleration = 0
                
                
                #pprint(temp_acceleration)

                #VELOCITY CALCULATION

                #print("temp accel: ", temp_acceleration)
                #print("prev accel: ", prev_acceleration)
                temp_velocity = temp_actual_speed + ((sample_period/2) * (temp_acceleration + prev_acceleration))
                if(temp_velocity > Train.VELOCITY_LIMIT):
                    temp_velocity = Train.VELOCITY_LIMIT
                elif(temp_velocity < 0):
                    temp_velocity = 0

                #pprint(temp_velocity)

                #DISTANCE CALCULATION
                #TODO: I think this is scuffed
                distance_moved = (1/2) * temp_acceleration * sample_period + temp_velocity * sample_period
                #temp_distance = prev_distance + (temp_velocity * sample_period)
                #temp_distance = prev_distance + (self.actual_speed + temp_velocity)/2 * sample_period
                #self.distance = temp_distance
                signals.send_tm_distance.emit(self.id, distance_moved)
                
                self.actual_speed = temp_velocity * 2.237
                #if (self.actual_speed > Train.VELOCITY_LIMIT):
                #    self.actual_speed = Train.VELOCITY_LIMIT
                #if (self.actual_speed > self.train_ctrl.real_train.get_commanded_speed()):
                #    self.actual_speed = self.train_ctrl.real_train.get_commanded_speed()

                #print("speed: ", self.actual_speed)
                self.ui.velocity_line.setText(str(round(self.actual_speed, 2)))

                self.acceleration = temp_acceleration * 3.28084
                self.ui.acceleration_line.setText(str(round(self.acceleration,2)))

                #send speed to train ctrl, get new power
                self.power = power / 1000

                #print("power:" , self.power)
                #pprint("-------------------------------")
                self.train_ctrl.real_train.set_power(self.power)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    TrainModel = Train()
    sys.exit(app.exec_())
