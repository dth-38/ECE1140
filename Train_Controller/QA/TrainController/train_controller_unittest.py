import unittest
from train_prototype import Train_Controller

class test_train(unittest.TestCase):
    thomas = Train_Controller()

    def test_commanded_speed(self):
        self.thomas.set_speed_limit(60)
        self.thomas.set_commanded_speed(70)
        self.thomas.apply_change()
        self.assertEqual(self.thomas.get_speed_limit(), self.thomas.get_actual_speed())
        
    def test_normal_brake(self):
        self.thomas.set_actual_speed(50)
        temp = self.thomas.get_actual_speed()

        self.thomas.set_norm_deaccel_rate(10)
        self.thomas.press_norm_brake()
        self.assertEqual(temp - self.thomas.get_norm_deaccel_rate(), self.thomas.get_actual_speed())

    def test_left_door(self):
        self.thomas.set_left_door("On")
        self.thomas.apply_change()
        self.assertEqual(self.thomas.get_left_door(), self.thomas.get_commanded_left_door())


if __name__ == '__main__':
    unittest.main()


