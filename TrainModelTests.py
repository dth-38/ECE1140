import sys
from PyQt5 import QtCore, QtWidgets

from TrainModel.Train import Train

#test newton's laws calculated correctly. train is at rest, full power applied to train
def test_newtons_laws():
    train = Train()
    train.power = 12000
    train.train_model_update_speed()
    assert(round(train.acceleration,2) == .64), "acceleration incorrect"
    assert(round(train.force,0) == 8), "force incorrect"
    assert(round(train.actual_speed,2) == .22), "speed incorrect"
    print("newtons laws test complete")

#test that mass is updated correctly when passengers enter the train.
def test_passengers_update_mass():
    train = Train()
    train.train_model_update_passengers(0, 15)
    assert(train.passenger_count == 15), "passengers incorrect"
    assert(round(train.mass,0) == 41), "mass incorrect"
    print("passengers and mass test complete")

#test track circuit signal is sent to correct train. In this case train 1
def test_track_circuit():
    train = Train(1)
    train.train_model_update_authority(1, 117)
    train.train_model_update_command_speed(1,30)
    assert(train.authority == 117), "authority incorrect"
    assert(train.commanded_speed == 30), "commanded speed incorrect"
    print("track circuit test complete")

#test temperature begins to tick up when passenger sets higher temp. starts at room temp, ticks up 1 to 69 to get to 70
def test_temp():
    train = Train()
    train.ac_command = 70
    train.regulate_temp()
    assert(train.actual_temp == 69), "temperature incorrect"
    print("temperature test complete")

#test that lights turn on when train controller setse them to be on
def test_lights():
    train = Train()
    train.train_ctrl.real_train.set_internal_light("On")
    train.train_ctrl.real_train.set_external_light("On")
    train.interior_light_cmd = train.train_ctrl.real_train.get_internal_light()
    train.exterior_light_cmd = train.train_ctrl.real_train.get_external_light()
    assert(train.interior_light_cmd == "On"), "interior lights not on"
    assert(train.exterior_light_cmd == "On"), "exterior lights not on"
    print("lights test complete")

#test doors open to correct door side at a station.
def test_doors():
    train = Train()
    train.door_side = 0
    train.left_door_cmd = "Closed"
    train.left_door_cmd = "Closed"
    train.train_model_update_doors()

    assert(train.left_door_cmd == "Opened"), "Left door is not open when it should be"
    assert(train.right_door_cmd == "Closed"), "Right door is not closed when it should be"
    print("doors test complete")

#test that ebrake is pulled when passenger pulls it
def test_passenger_ebrake():
    train = Train()
    train.passenger_ebrake = True
    train.commanded_speed = 30
    train.authority = 100
    train.actual_speed = 25
    train.update_values()
    assert(round(train.acceleration,0) == -9), "emergency brake is not pulled"
    print("passenger ebrake test complete")

#test that engine failure causes the engine to shut off
def test_engine_failure():
    train = Train()
    train.power = 5000
    train.engine_failure == True
    train.update_values()
    assert(train.power == 0), "power incorrect"
    print("engien failure test complete")

def main():
    test_doors()
    test_engine_failure()
    test_lights()
    test_newtons_laws()
    test_passenger_ebrake()
    test_passengers_update_mass()
    test_temp()
    test_track_circuit()

    print("all tests complete")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    
    main()

    #sys.exit(app.exec_())