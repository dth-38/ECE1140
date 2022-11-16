import math
from Block import Block
from train_ui import TrainData_Ui
from test_ui import test_Ui
from PyQt5 import QtCore, QtWidgets
import sys
from train_model_signals import *
from pprint import pprint

#from Train_Controller import train_controller_main
#import Train_Controller.train_controller_main as train_controller_main
import train_controller_main



class Train:
    
    def __init__(self, ID = 0, route = []):

        #pprint(sys.path)
        
        #train controller that controls this train
        # self.train_ctrl = train_controller_main.WindowClass()
        # #= self.train_ctrl.real_train.get()

        # self.real_train = self.train_ctrl.train_status()

        #train id
        self.id = ID

        #dispatch information???
        #self.destination_block = destination_block
        #self.line = line

        #block list = array of blocks from starting block to destination block
        self.block_list = route

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
        self.position = 0               #meters

        #various train functions
        self.ac_cmd = 70.0              #degrees farenheight
        self.horn = False
        self.interior_light_cmd = False
        self.exterior_light_cmd = False
        self.right_door_cmd = False
        self.left_door_cmd = False
        self.advertisement_cmd = False
        self.announcement_cmd = False

        #failures
        self.brake_failure = False
        self.signal_pickup_failure = False
        self.engine_failure = False

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
        self.VELOCITY_LIMIT = 43.497                #kph
        self.POWER_LIMIT = 120000              #watts
        self.PASSENGER_LIMIT = 222
        self.MAX_GRADIENT = 60

        #signals
        ##signals.train_model_dispatch_train.connect()
        #signals.train_model_transfer_lights.connect(self.train_model_transfer_lights)
        #signals.train_model_transfer_doors.connect(self.train_model_transfer_doors)
        #signals.train_model_transfer_announcement.connect(self.train_model_transfer_announcement)
        #signals.train_model_transfer_ads.connect(self.train_model_transfer_ads)
        #signals.train_model_transfer_temp(self.train_model_transfer_temp)
        #signals.train_model_transfer_service_brake(self.train_model_transfer_service_brake)
        #signals.train_model_transfer_emergency_brake(self.train_model_transfer_emergency_brake)
        #signals.train_model_transfer_grade(self.train_model_transfer_grade)
        #signals.train_model_update_authority(self.train_model_update_authority)
        #signals.train_model_update_command_speed(self.train_model_update_command_speed)
        #signals.train_model_update_passengers(self.train_model_update_passengers)
        #signals.train_model_update_beacon(self.train_model_update_beacon)
        signals.train_model_transfer_brake_failure.connect(self.train_model_transfer_brake_failure)
        signals.train_model_transfer_engine_falure.connect(self.train_model_transfer_engine_failure)
        signals.train_model_transfer_signal_pickup_failure.connect(self.train_model_transfer_signal_pickup_failure)
        signals.train_model_fix_failure.connect(self.train_model_fix_failure)
        signals.train_model_transfer_passenger_ebrake.connect(self.train_model_passenger_ebrake)
        #signals.train_model_transfer_circuit(self.train_model_transfer_circuit)
        #signals.train_model_transfer_horn(self.train_model_transfer_horn)

        #testui
        signals.test_power.connect(self.update_power)

        #setup ui
        self.app = QtWidgets.QApplication(sys.argv)
        train_model = QtWidgets.QMainWindow()
        self.ui = TrainData_Ui()
        self.ui.setupUi(train_model)
        train_model.show()

        #train controller that controls this train
        self.train_ctrl = train_controller_main.WindowClass()
        #= self.train_ctrl.real_train.get()


        test = QtWidgets.QMainWindow()
        self.testt = test_Ui()
        self.testt.setupUi(test)
        #test.show()

        #self.train_ctrl.myWindow

        #train runs until it reaches destination
        self.run_continuously = True

        self.ui.train_id_line.setText(str(self.id))

        #self.train_model_update_authority(100)

        self.train_timer = QtCore.QTimer()
        self.train_timer.start(1000)
        self.train_timer.timeout.connect(self.update_values)

        sys.exit(self.app.exec_())


# ---------------------------------------------------------------------------------------------
# ----------------------------- Update Train? ------------------------------------------------
# ---------------------------------------------------------------------------------------------



    def update_values(self):    #run every 1 sec (infinite loop)
        #set values of connected train controller
        self.train_ctrl.real_train.set_authority(self.authority)    #authoritys

        # self.train_ctrl.real_train.set_commanded_speed(40) #desired speed

        self.train_ctrl.real_train.set_speed(self.actual_speed)       #actual speed
        if(self.engine_failure or self.brake_failure or self.signal_pickup_failure):
            self.train_ctrl.real_train.set_failure_flag(True)
        else:
            self.train_ctrl.real_train.set_failure_flag(False)
        #self.train_ctrl.real_train.set_passenger_brake(self.passenger_ebrake)

        self.train_ctrl.update_in_controller()

        self.power = self.train_ctrl.real_train.get_power()
        
        #self.real_train.set_block_length(self.)
        self.train_model_update_speed()

        #get values from train controller
        self.left_door_cmd = self.train_ctrl.real_train.get_left_door()
        self.right_door_cmd = self.train_ctrl.real_train.get_right_door()
        self.interior_light_cmd = self.train_ctrl.real_train.get_internal_light()
        self.exterior_light_cmd = self.train_ctrl.real_train.get_external_light()
        self.advertisement_cmd = self.train_ctrl.real_train.get_ad()
        self.ac_cmd = self.train_ctrl.real_train.get_temp()
        self.horn = self.train_ctrl.real_train.get_horn()


        self.train_model_display_announcement()
        self.train_model_display_temp()
        self.train_model_display_external_lights()
        self.train_model_display_internal_lights()
        self.train_model_display_horn()


        #self.door_side[] = self.train_ctrl.get_door_left()
        #self.power = self.train_ctrl.get_train_power()

        #update train controller values
        # self.train_ctrl.update_values_controller()
        self.train_ctrl.update_train_display()
    
    def update_power(self, power):
        self.power = power
        self.ui.power_line.setText(str(self.power))
        self.train_model_update_speed()

# ---------------------------------------------------------------------------------------------
# ----------------------------- Dispatch Train? ------------------------------------------------
# ---------------------------------------------------------------------------------------------

    #dont know if need dispatch function or train can be initialized with dispatch info

    #def dispatch_train(self,destination, blockroute):
        #self.route = blockroute
        #self.destination_block = destination

        #keep track of time? 
    
        # tell controller train has bend dispatched

# ---------------------------------------------------------------------------------------------
# ----------------------------- Train Controller Inputs ---------------------------------------
# ---------------------------------------------------------------------------------------------

    #sets train lights
    def train_model_display_internal_lights(self):
        if(self.interior_light_cmd == True):
            self.ui.int_light_line.setText("On")
        else:
            self.ui.int_light_line.setText("Off")
        #signals.train_model_update.emit()

    def train_model_display_external_lights(self):
        if(self.exterior_light_cmd):
            self.ui.ext_light_line.setText("On")
        else:
            self.ui.ext_light_line.setText("Off")
        #signals.train_model_update.emit()

    #sets status of doors
    def train_model_toggle_doors(self):
        #opens doors depending on the station
        if(self.door_side == 1):
            self.left_door_cmd = 1
            self.right_door_cmd = 0
        elif(self.door_side == 2):
            self.right_door_cmd = 1
            self.left_door_cmd = 0
        elif(self.door_side == 3):
            self.left_door_cmd = 1
            self.right_door_cmd = 1
        else:
            self.left_door_cmd = 0
            self.right_door_cmd = 0
        #signals.train_model_update.emit()

    #get announcement from train controller
    def train_model_display_announcement(self):
        if(self.announcement_cmd):
            self.ui.announcement_line.setText("On")
        else:
            self.ui.announcement_line.setText("Off")
        #signals.train_model_update.emit()

    #get horn from train controller
    def train_model_display_horn(self):
        if(self.horn):
            self.ui.horn_line.setText("On")
        else:
            self.ui.horn_line.setText("Off")
        #signals.train_model_update.emit()

    #get advertisement command from train controller
    def train_model_transfer_ads(self):
        if(self.advertisement_cmd):
            self.ui.advertisement_line.setText("On")
        else:
            self.ui.advertisement_line.setText("Off")
        #signals.train_model_update.emit()

    #get temperature from train controller
    def train_model_display_temp(self):
        self.ui.temp_line.setText(str(self.ac_cmd))
        #signals.train_model_update.emit()
    
    #get service brake from train controller
    # def train_model_transfer_service_brake(self, service_brake):
    #     if(not self.brake_failure):
    #         self.sbrake = service_brake
    #     else:
    #         self.sbrake = False
    #     #signals.train_model_update.emit()

    # #get emergency brake from train controller
    # def train_model_transfer_emergency_brake(self, emergency_brake):
    #     self.ebrake = emergency_brake
    #     #signals.train_model_update.emit()

    def train_model_transfer_beacon_info(self, beacon):
        self.station_name = beacon
        #signals.train_model_update.emit()

# ---------------------------------------------------------------------------------------------
# ----------------------------- Train Controller Outputs ---------------------------------------
# ---------------------------------------------------------------------------------------------
    
    #do i need this?????!?!??!?!?
    #train_ctrl.brake_failure = self.brake_failure
    #train_ctrl.engine_failure = self.engine_failure
    #train_ctrl.signal_pickup_failure = self.signal_pickup_failure
    #pass commanded speed
    #pass authority
    
# ---------------------------------------------------------------------------------------------
# ----------------------------- Track Model Inputs --------------------------------------------
# ---------------------------------------------------------------------------------------------

    #transfer grade
    def train_model_transfer_grade(self, new_grade):
        self.grade = new_grade
        self.ui.grade_line.setText(str(self.grade))
        #signals.train_model_update.emit()        

    #update authority
    def train_model_update_authority(self, new_auth):
        if(self.signal_pickup_failure):
            self.authority = 0
        else:    
            self.authority = new_auth

        #send to train controller
        #self.train_ctrl.train_status.set_authority(self.authority)

        self.ui.authority_line.setText(str(self.authority))
        #signals.train_model_update.emit()

    #update commanded speed
    def train_model_update_command_speed(self, new_cmd_speed):
        if(self.signal_pickup_failure):
            self.commanded_speed = 0
        else:    
            self.commanded_speed = new_cmd_speed

        #send to train controller
        #self.train_ctrl.train_status.set_commanded_speed(self.commanded_speed)

        self.ui.suggested_speed_line.setText(str(self.commanded_speed))
        #signals.train_model_update.emit()

    #update passenger count and calculate new mass
    def train_model_update_passengers(self, pass_count):
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
    def train_model_transfer_beacon(self, door_side, station):
        self.door_side = door_side
        self.next_station = station
        self.ui.station_line = station
        #signals.train_model_update.emit()

    #sets route
    def transfer_block_list(self, blocklist):
       self.block_list = blocklist

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

        #trainctrl.brake_failure
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
        self.brake_failure = True
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

        self.run_continuously = True
        if (self.run_continuously):

            if(self.engine_failure):
                power = 0
            
            if(power > self.POWER_LIMIT):
                power = self.POWER_LIMIT

            #convert imperial to metric
            #ft/s^2 to m/s^2
            prev_acceleration = self.acceleration / 3.28084
            sample_period = 1
            prev_position = self.position
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
                if (self.power == 0):
                    force = 0
                    force -= self.FRICTION_COE * mass * self.GRAVITY * math.cos(self.grade)
                else:
                    if(temp_actual_speed == 0):
                        force = self.FRICTION_COE * mass * self.GRAVITY * math.cos(self.grade)
                    # if brakes off
                    #elif(not(self.sbrake) and not(self.ebrake) and not(self.passenger_ebrake)):
                    else:
                        force = (power / temp_actual_speed)
                        force -= self.FRICTION_COE * mass * self.GRAVITY * math.cos(self.grade)
                    #if service brake on
                    # elif(self.sbrake and not self.ebrake and not self.passenger_ebrake):
                    #     force = (power / temp_actual_speed)
                    #     force -= self.FRICTION_COE * (1.01605 * self.mass * 1000) * self.GRAVITY * math.cos(self.grade)
                    #     force -= self.DECELERATION_SERVICE * self.mass
                    #  #if passenger ebrake or ebrake is on
                    # elif(not(self.sbrake) and (self.ebrake or self.passenger_ebrake)):
                    #     force = (power / temp_actual_speed)
                    #     force -= self.FRICTION_COE * (1.01605 * self.mass * 1000) * self.GRAVITY * math.cos(self.grade)
                    #     force -= self.DECELERATION_EMERGENCY * self.mass
                    if(force < 0):
                        force = 0


                # pprint("Force: ")
                # pprint(force)
                self.ui.grade_line.setText(str(round(force,1)))

                #ACCELERATION CALCULATION
                temp_acceleration = force/mass
                if(temp_acceleration > self.ACCELERATION_LIMIT):
                    temp_acceleration = self.ACCELERATION_LIMIT
                # elif(self.sbrake and not self.ebrake and not self.passenger_ebrake):
                #     self.acceleration = self.DECELERATION_SERVICE
                # elif(not self.sbrake and (self.ebrake or self.passenger_ebrake)):
                #     temp_acceleration = self.DECELERATION_EMERGENCY
                # elif(self.sbrake and (self.ebrake or self.passenger_ebrake)):
                #     temp_acceleration = self.DECELERATION_EMERGENCY
                
                
                #pprint(temp_acceleration)

                #VELOCITY CALCULATION

                # pprint(temp_acceleration)
                # pprint(prev_acceleration)
                temp_velocity = temp_actual_speed + ((sample_period/2) * (temp_acceleration + prev_acceleration))
                if(temp_velocity > self.VELOCITY_LIMIT):
                    temp_velocity = self.VELOCITY_LIMIT
                elif(temp_velocity < 0):
                    temp_velocity = 0

                #pprint(temp_velocity)

                #POSITION CALCULATION
                # temp_position = prev_position + (temp_velocity * sample_period)
                
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

                #convert metric to imperial
                #self.position = temp_position
                
                self.actual_speed = temp_velocity * 2.237
                if (self.actual_speed > self.VELOCITY_LIMIT):
                    self.actual_speed = self.VELOCITY_LIMIT
                #if (self.actual_speed > self.train_ctrl.real_train.get_commanded_speed()):
                #    self.actual_speed = self.train_ctrl.real_train.get_commanded_speed()
                    
                pprint("speed")
                pprint(self.actual_speed)
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

                pprint("Power: ")
                pprint(self.power)

                self.ui.power_line.setText(str(self.power))

                #signals.train_model_update.emit()

if __name__ == "__main__":
    TrainModel = Train()