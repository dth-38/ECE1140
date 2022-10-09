from PyQt5.QtWidgets import QApplication, QFileDialog
from multiprocessing import Process, Queue
import Block
from TCGUI import DebugGUI, MainGUI, MaintenanceGUI, TextEditorGUI

class TrackController:
    #global variables used since they must be accessed and modified from signals in the GUI
    currentTrackState = {}#contains the current state of the track with all inputs and outputs, safe to get data from
    nextTrackState = {}   #contains the next state of the track being modified by PLC logic and sets from other modules, unsafe and should only be written to
    filename = ""
    program = 0
    inMaintenance = False
    runPLC = True


    def __init__(self):
        self.buildTrack()

        #TODO: start main gui thread
        

        #run tick() on loop
        #doesn't need a timer since PLC should be running as fast as possible and all data transfers are event based
        while self.runPLC:
            #TODO: create thread to handle all reads since they can be safely done without locking data

            self.tick()


        #closes the plc program on exit if there was one loaded
        if self.filename != '':
            self.program.close()





    def buildTrack(self):
        #TODO:
        #probe track model for amount of blocks
        #generate blocks and add to trackState
        #probe track model for switches, gates, lights, possibly state of other block vars
        
        #BEGIN TEMPORARY SOLUTION FOR ITERATION 2
        tempTrack = {"red_A_1": Block(), "red_A_2": Block(), "red_A_3": Block()}
        tempTrack["red_A_1"].addSwitch()
        tempTrack["red_A_2"].addGate()
        tempTrack["red_A_3"].addLight('r')

        self.currentTrackState = tempTrack
        self.nextTrackState = tempTrack

        #END TEMPORARY SOLUTION FOR ITERATION 2


    def tick(self):
        #TODO: runs PLC logic modifying nextTrackState while also handling sets from other modules
        pass

    #opens windows explorer to select and open a new file
    #returns filename to display in GUI maybe idk
    def uploadFile(self):
        filenameTuple = QFileDialog.getOpenFileName(None, 'Choose PLC Program', 'C:\\', "Text Files (*.txt)")
        self.filename = filenameTuple[0]
        if self.filename != '':
            self.program = open(self.filename, "r")

        return self.filename




#main for the whole Track Controller, simply creates an instance of TrackController
if __name__ == '__main__':
    TrackController()

