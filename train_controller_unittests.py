import unittest
from Train_Controller.train_controller_main import train_status

class test_train(unittest.TestCase):

    #1st test
    def test_commanded_speed(self):
        self.thomas = train_status()
        self.thomas.set_speed_limit(60)
        self.thomas.set_commanded_speed(70)
        self.thomas.apply_change()
        self.assertEqual(self.thomas.get_speed_limit(), self.thomas.get_speed())
    
    #2nd test
    def test_normal_brake(self):
        self.thomas = train_status()
        self.thomas.set_speed(50)
        temp = self.thomas.get_speed()

        self.thomas.set_norm_deaccel_rate(10)
        self.thomas.press_norm_brake()
        self.assertEqual(temp - self.thomas.get_norm_deaccel_rate(), self.thomas.get_speed())

    #3rd test
    def test_left_door(self):
        self.thomas = train_status()
        self.thomas.set_left_door("On")
        self.thomas.apply_change()
        self.assertEqual(self.thomas.get_left_door(), self.thomas.get_commanded_left_door())


    #4th test
    def test_tunnel_state(self):
        self.thomas = train_status()
        self.thomas.set_commanded_external_light("Off")
        self.thomas.set_tunnel_state(True)
        self.thomas.apply_change()
        self.assertEqual(self.thomas.get_external_train_light(), "On")

    #5th test
    def test_train_auto_brake(self):
        self.thomas = train_status()
        self.thomas.set_speed(20)
        temp = self.thomas.get_speed()
        self.thomas.set_speed_limit(30)
        self.thomas.set_authority(0)
        self.thomas.set_norm_deaccel_rate(10)
        self.thomas.apply_change()
        self.thomas.press_norm_brake()
        self.assertEqual(self.thomas.get_norm_brake_state(), True)
        self.assertEqual(self.thomas.get_speed(), temp - self.thomas.get_norm_deaccel_rate())

    #6th test
    def test_train_departure(self):
        self.thomas = train_status()
        self.thomas.set_left_door("On")
        self.thomas.set_right_door("On")
        self.thomas.set_authority(10)
        self.thomas.apply_change()
        self.assertEqual(self.thomas.get_left_door(), self.thomas.get_commanded_left_door())
        self.assertEqual(self.thomas.get_right_door(), self.thomas.get_commanded_right_door())


if __name__ == '__main__':
    unittest.main()
