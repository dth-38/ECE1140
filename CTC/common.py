#TODO: GET CLASSES FROM OTHER MODULES
import math

class Train:
    def _init_(self, ID = 0, route = []):

        #train controller that controls this train
        #train_ctrl = TrainController

        #train id
        self.id = ID

        #dispatch information???
        #self.destination_block = destination_block
        #self.line = line

        #block list = array of blocks from starting block to destination block
        self.block_list = route

        #train runs until it reaches destination
        self.run_continuously = True

        #beacon info
        self.next_station = ""
        self.door_side = 0               #0 = closed, 1 = left, 2 = right, 3 = both

        #physical train info
        self.train_length = 105.6       #ft
        self.train_width = 11.2         #ft
        self.train_height = 9.7         #ft
        self.crew_count = 2
        self.passenger_count = 0
        self.mass = 40.25               #imperial tons

        #train movement info
        self.actual_speed = 0.0         #mph
        self.commanded_speed = 0.0      #mph
        self.grade = 0.0                #%ft risen per 100 ft
        self.power = 0.0                #watts
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
        self.MAX_FORCE = 18551.9333             #force
        self.GRAVITY = 9.8                      #m/s^2
        self.FRICTION_COE = .01
        self.ACCELERATION_LIMIT = .5            #m/s^2
        self.DECELERATION_SERVICE = -1.2        #m/s^2
        self.DECELERATION_EMERGENCY = -2.73     #m/s^2
        self.VELOCITY_LIMIT = 70                #kph
        self.POWER_LIMIT = 120000               #watts
        self.PASSENGER_LIMIT = 148

        #signals
        ##signals.train_model_dispatch_train.connect()
        #signals.train_model_transfer_lights.connect(self.train_model_transfer_lights)
        #signals.train_model_transfer_doors.connect(self.train_model_transfer_doors)
        #signals.train_model_transfer_announcement.connect(self.train_model_transfer_announcement)
        #signals.train_model_transfer_ads.connect(self.train_model_transfer_ads)
        #signals.train_model_transfer_temp(self.train_model_transfer_temp)
        #signals.train_model_transfer_service_brake(self.train_model_transfer_service_brake)
        #signals.train_model_transfer_emergency_brake(self.train_model_transfer_emergency_brake)
        #signals.train_model_transfer_passenger_ebrake(self.train_model_passenger_ebrake)
        #signals.train_model_transfer_power(self.train_model_transfer_power)
        #signals.train_model_transfer_grade(self.train_model_transfer_grade)
        #signals.train_model_update_authority(self.train_model_update_authority)
        #signals.train_model_update_command_speed(self.train_model_update_command_speed)
        #signals.train_model_update_passengers(self.train_model_update_passengers)
        #signals.train_model_update_beacon(self.train_model_update_beacon)
        #signals.train_model_transfer_brake_failure(self.transfer_brake_failure)
        #signals.train_model_transfer_engine_falure(self.transfer_engine_failure)
        #signals.train_model_transfer_signal_pickup_failure(self.transfere_signal_pickup_failure)
        #signals.train_model_fix_failure(self.train_model_fix_failure)
        #signals.train_model_transfer_circuit(self.train_model_transfer_circuit)
        #signals.train_model_transfer_horn(self.train_model_transfer_horn)

# ---------------------------------------------------------------------------------------------
# ----------------------------- Dispatch Train? ------------------------------------------------
# ---------------------------------------------------------------------------------------------

    #dont know if need dispatch function or train can be initialized with dispatch info

    #def dispatch_train(self,destination, blockroute):
        #self.route = blockroute
        #self.destination_block = destination

        #keep track of time? 
    
        # tell controller train has beend dispatched

# ---------------------------------------------------------------------------------------------
# ----------------------------- Train Controller Inputs ---------------------------------------
# ---------------------------------------------------------------------------------------------

    #sets train lights
    def train_model_transfer_lights(self, interior, exterior):
        if(interior == True):
            self.interior_light_cmd = True
        else:
            self.interior_light_cmd = False
        if(exterior == True):
            self.exterior_light_cmd = True
        else:
            self.exterior_light_cmd = False

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
    def train_model_transfer_announcement(self, announce):
        self.announcement_cmd = announce
        #signals.train_model_update.emit()

    #get horn from train controller
    def train_model_transfer_horn(self, horn):
        self.horn = horn
        #signals.train_model_update.emit()

    #get advertisement command from train controller
    def train_model_transfer_ads(self,adv):
        self.advertisement_cmd = adv
        #signals.train_model_update.emit()

    #get temperature from train controller
    def train_model_transfer_temp(self,temperature):
        self.ac_cmd = temperature
        #signals.train_model_update.emit()
    
    #get service brake from train controller
    def train_model_transfer_service_brake(self, service_brake):
        if(not self.brake_failure):
            self.sbrake = service_brake
        else:
            self.sbrake = False
        #signals.train_model_update.emit()

    #get emergency brake from train controller
    def train_model_transfer_emergency_brake(self, emergency_brake):
        self.ebrake = emergency_brake
        #signals.train_model_update.emit()

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

    
# ---------------------------------------------------------------------------------------------
# ----------------------------- Track Model Inputs --------------------------------------------
# ---------------------------------------------------------------------------------------------

    #transfer grade
    def train_model_transfer_grade(self, new_grade):
        self.grade = new_grade
        #signals.train_model_update.emit()        

    #update authority
    def train_model_update_authority(self, new_auth):
        if(self.signal_pickup_failure or self.destination_reached == True):
            self.authority = 0
        else:    
            self.authority = new_auth
        #signals.train_model_update.emit()

    #update commanded speed
    def train_model_update_command_speed(self, new_cmd_speed):
        if(self.signal_pickup_failure or self.destination_reached == True):
            self.commanded_speed = 0
        else:    
            self.commanded_speed = new_cmd_speed
        #signals.train_model_update.emit()

    #update passenger count and calculate new mass
    def train_model_update_passengers(self, pass_count):
        if(pass_count > self.PASSENGER_LIMIT):
            self.passenger_count = self.PASSENGER_LIMIT
        else:
            self.passenger_count = pass_count
        if(pass_count > 0):
            self.mass = 40.25 + (self.passenger_count * 0.0738155)
        #signals.train_model_update.emit()

    #sets beacon info
    def train_model_transfer_beacon(self, door_side, station):
        self.door_side = door_side
        self.next_station = station
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
        #signals.train_model_update.emit()

    #murphy sets failure
    def train_model_transfer_brake_failure(self, fail):
        self.brake_failure = fail
        #signals.train_model_update.emit()

    #murphy sets failure
    def train_model_transfer_engine_failure(self, fail):
        self.engine_failure = fail
        #signals.train_model_update.emit()

    #murphy sets failure
    def train_model_transfer_signal_pickup_failure(self, fail):
        self.signal_pickup_failure = fail
        #signals.train_model_update.emit()

# ---------------------------------------------------------------------------------------------
# ----------------------------- Passenger Inputs ----------------------------------------------
# ---------------------------------------------------------------------------------------------
 
    #get emergency brake from passenger
    def train_model_passenger_ebrake(self, emer_brake):
        self.passenger_ebrake = emer_brake
        #signals.train_model_update.emit() 

# ---------------------------------------------------------------------------------------------
# ----------------------------- Newtons laws calculation --------------------------------------
# ---------------------------------------------------------------------------------------------

    def train_model_transfer_power(self, new_power):
        if (self.run_continuously):

            if(self.failure_type == 1):
                new_power = 0
            
            if(new_power > self.POWER_LIMIT):
                new_power = self.POWER_LIMIT

            #convert imperial to metric
            #ft/s^2 to m/s^2
            prev_acceleration = self.acceleration / 3.28084
            sample_period = 1/5
            prev_position = self.position
            #mph to m/s
            temp_actual_speed = self.actual_speed / 2.237


            run = True
            #if there is a route, set current block and run
            if (len(self.block_list) > 0):
                #if theres block is not a station, run
                if (self.block_list[0].station == ""):
                    current_block = self.block_list[0]
                    current_block_length = current_block.block_length
                    self.grade = current_block.grade
                    run = True
                else:
                    #stop the train if block is a station
                    self.run_continuously = False
                    run = False
            else:
                #stop the train if route doesnt exist
                self.run_continuously = False
                run = False

            if (run):
                #FORCE CALCULATION
                if (self.sbrake or self.ebrake or self.passenger_ebrake or new_power == 0):
                    force = 0
                else:
                    if(temp_actual_speed == 0):
                        force = self.FRICTION_COE * (1.01605 * self.mass * 1000) * self.GRAVITY * math.cos(self.grade)
                    else:
                        force = (new_power / temp_actual_speed)
                        force -= self.FRICTION_COE * (1.01605 * self.mass * 1000) * self.GRAVITY * math.cos(self.grade)
                    
                    if(force < 0):
                        force = 0

                #ACCELERATION CALCULATION
                temp_acceleration = force/(1.01605 * self.mass * 1000)
                if(temp_acceleration > self.ACCELERATION_LIMIT and not self.sbrake and not self.ebrake and not self.passenger_ebrake):
                    temp_acceleration = self.ACCELERATION_LIMIT
                elif(self.sbrake and not self.ebrake and not self.passenger_ebrake):
                    self.acceleration = self.DECELERATION_SERVICE
                elif(not self.sbrake and (self.ebrake or self.passenger_ebrake)):
                    temp_acceleration = self.DECELERATION_EMERGENCY
                elif(self.sbrake and (self.ebrake or self.passenger_ebrake)):
                    temp_acceleration = self.DECELERATION_EMERGENCY
                
                #VELOCITY CALCULATION
                temp_velocity = temp_actual_speed + ((sample_period/2) * (temp_acceleration + prev_acceleration))
                if(temp_velocity > self.VELOCITY_LIMIT):
                    temp_velocity = self.VELOCITY_LIMIT
                elif(temp_velocity < 0):
                    temp_velocity = 0

                #POSITION CALCULATION
                temp_position = prev_position + (temp_velocity * sample_period)
                
                #if position length is greater than block length, move to next block
                if (temp_position > current_block_length):
                    #if at last block in route, at destnation, stop
                    if (len(self.block_list) <= 1):
                        self.block_list.pop(0)
                        temp_position = current_block_length
                        self.run_continuously = False
                    else:
                        #move to next block
                        temp_position -= current_block_length
                        #remove block that train has passed, update current block
                        self.block_list.pop(0)
                        self.current_block = self.block_list[0]
                        current_block = self.block_list[0]
                
                        #send block occupancy to track model
                        #signals.track_model_update_block_occupancy.emit(self.id, current_block)

                #convert metric to imperial
                self.position = temp_position
                self.power = new_power
                self.actual_speed = temp_velocity * 2.237
                self.acceleration = temp_acceleration * 3.28084

                # send to train controller

                #signals.train_model_update.emit()

class TrackModel:
    pass
class Station:
    pass
class Line:
    pass
