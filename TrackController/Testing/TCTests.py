import unittest
import os
import pathlib
import sys

#needed to import TrackController
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from PyQt5.QtWidgets import QApplication
from TrackController import TrackController
from PLCInterpreter import PLCInterpreter
import Block

class TestTC(unittest.TestCase):
    @unittest.skip("Breaks shit.")
    def test_Tokenization(self):
        interpreter = PLCInterpreter.PLCInterpreter()

        current_path = str(pathlib.Path().absolute())
        gf = current_path + "/Test_Programs/should_pass.txt"

        good_File = open(gf)
        self.assertTrue(interpreter.tokenize(good_File))
        good_File.close()
        #checks that each token is fully correct
        self.assertEqual(interpreter.logic[0].getOpcode(), 2)
        self.assertEqual(interpreter.logic[0].get_Var_Type(1), "temp")
        self.assertEqual(interpreter.logic[0].get_Var_Type(2), "occupied")
        self.assertEqual(interpreter.logic[0].get_Var_Type(3), "failed")
        self.assertEqual(interpreter.logic[0].get_Var(1)[0], 0)
        self.assertEqual(interpreter.logic[0].get_Var(2)[0], "red_A_1")
        self.assertEqual(interpreter.logic[0].get_Var(3)[0], "red_A_1")
        self.assertEqual(interpreter.logic[1].getOpcode(), 3)
        self.assertEqual(interpreter.logic[1].get_Var_Type(1), "switch")
        self.assertEqual(interpreter.logic[1].get_Var_Type(2), "temp")
        self.assertEqual(interpreter.logic[1].get_Var_Type(3), "light")
        self.assertEqual(interpreter.logic[1].get_Var(1)[0], "red_A_1")
        self.assertEqual(interpreter.logic[1].get_Var(1)[1], 0)
        self.assertEqual(interpreter.logic[1].get_Var(2)[0], 0)
        self.assertEqual(interpreter.logic[1].get_Var(3)[0], "red_A_1")
        self.assertEqual(interpreter.logic[1].get_Var(3)[1], 0)
        self.assertEqual(interpreter.logic[1].get_Var(3)[2], "RED")
        self.assertEqual(interpreter.logic[2].getOpcode(), 0)
        self.assertEqual(interpreter.logic[2].get_Var_Type(1), "temp")
        self.assertEqual(interpreter.logic[2].get_Var_Type(2), "temp")
        self.assertEqual(interpreter.logic[2].get_Var(1)[0], 0)
        self.assertEqual(interpreter.logic[2].get_Var(2)[0], 1)
        self.assertEqual(interpreter.logic[3].getOpcode(), 1)
        self.assertEqual(interpreter.logic[3].get_Var_Type(1), "gate")
        self.assertEqual(interpreter.logic[3].get_Var_Type(2), "temp")
        self.assertEqual(interpreter.logic[3].get_Var(1)[0], "red_A_1")
        self.assertEqual(interpreter.logic[3].get_Var(1)[1], 0)
        self.assertEqual(interpreter.logic[3].get_Var(2)[0], 1)

    @unittest.skip("Might break shit.")
    def test_Tokenization_Fails(self):
        interpreter = PLCInterpreter.PLCInterpreter()
        track_Controller_App = QApplication([])
        controller = TrackController()
        controller.stop_Logic()


        #tests that an invalid DEFINE statement fails to tokenize
        current_path = str(pathlib.Path().absolute())
        baddef = current_path + "/Test_Programs/bad_define.txt"
        bad_Define = open(baddef)
        self.assertFalse(interpreter.tokenize(bad_Define))
        bad_Define.close()


        #tests that an invalid output variable fails to tokenize
        badout = current_path + "/Test_Programs/bad_output.txt"
        bad_Output = open(badout)
        self.assertFalse(interpreter.tokenize(bad_Output))
        bad_Output.close()

        #tests that an invalid input causes an error at runtime
        badinput = current_path + "/Test_Programs/bad_input.txt"
        controller.build_Track(badinput)
        controller.run_Logic()
        self.assertEqual(controller.run_PLC, False)

        track_Controller_App.exec()

    def test_Build_Track(self):
        track_Controller_App = QApplication([])
        controller = TrackController()
        #controller.stop_Logic()

        current_path = str(pathlib.Path().absolute())
        badblock = current_path + "/Test_Programs/bad_block.txt"

        #tests that an invalid track block causes there to be no track
        self.assertFalse(controller.build_Track(badblock))
        self.assertEqual(controller.current_Track_State, {})
        self.assertEqual(controller.next_Track_State, {})


        gf = current_path + "/Test_Programs/should_pass.txt"

        #tests that a valid track block generates the correct track
        self.assertTrue(controller.build_Track(gf))
        self.assertEqual(len(controller.current_Track_State["red_A_1"].switches), 1)
        self.assertEqual(len(controller.current_Track_State["red_A_1"].lights), 2)
        self.assertEqual(len(controller.current_Track_State["red_A_1"].gates), 1)
        self.assertEqual(controller.current_Track_State["red_A_1"].max_Speed, 30)

        track_Controller_App.exec()

    def test_Block(self):
        testBlock = Block.Block()

        #tests that lights colors are set properly
        testBlock.add_Light()
        self.assertEqual(len(testBlock.lights), 1)
        testBlock.set_Light(0, "YELLOW")
        self.assertEqual(testBlock.light_To_Str(0), "YELLOW")
        testBlock.set_Light(0, "GREEN")
        self.assertEqual(testBlock.light_To_Str(0), "GREEN")
        testBlock.set_Light(0, "RED")
        self.assertEqual(testBlock.light_To_Str(0), "RED")


    

if __name__ == '__main__':
    unittest.main()