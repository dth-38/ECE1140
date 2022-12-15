import unittest
import sys
from CTC.CTC_Scheduler import CTC_Scheduler
from CTC.Block_Table import Block_Table
class testCTC(unittest.TestCase):
    def test_dispatch(self):
        self.schedule = CTC_Scheduler()
        self.time = (0,4,10)
        self.schedule.manual_dispatch_train(self.time,0,"Red",["South Hills Junction"])
        self.train = self.schedule.train_table.get_entry(0)
        assert(self.train[1] == 0), "Train is not dispatched"
        print("Dispatch passed")
    def maintenance_test(self):
        self.maintenance = Block_Table()
        self.maintenance.set_maintenance(9,"A","Red")
        assert(self.maintenance.get_maintenance_signal() == True), "Maintenance not set"
        print("Maintenance passed")
    def throughput_test(self):
        self.schedule = CTC_Scheduler()
        self.schedule.calc_throughput("Red",100,10)
        assert(self.schedule.get_throughput("Red") == 10), "Throughput is wrong"
        print("Throughput passed")
    def schedule_test(self):
        self.schedule = CTC_Scheduler()
        red_schedule, green_scheduele = self.schedule.upload_schedule("./CTC/Schedule_v2.xlsx")
        assert(len(red_schedule) > 0), "Red line didn't read"
        assert(len(green_scheduele) > 0), "Green line didn't read"
        print("Schedule passed")
    def authority_speed_test(self):
        self.schedule = CTC_Scheduler()
        authority = self.schedule.calc_authority(0,"Red","Shadyside",0)
        assert(authority > 0), "Authority not working"
        speed = self.schedule.calc_suggested_speed("Red",1)
        assert(speed > 0), "Speed not working"
        print("Authority and speed passed")
    def switch_test(self):
        self.block_table = Block_Table()
        self.block_table.add_switch("Red",9,0)
        assert(self.block_table.get_switch_length() > 0), "Switch not added"
        print("Switch passed")
    



if __name__ == '__main__':
    test = testCTC()
    test.test_dispatch()
    test.maintenance_test()
    test.throughput_test()
    test.schedule_test()
    test.authority_speed_test()
    test.switch_test()
    