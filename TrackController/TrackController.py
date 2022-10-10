from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import pyqtSlot
from Block import Block
import TCGUI.DebugGUI, TCGUI.MaintenanceGUI, TCGUI.TextEditorGUI, TCGUI.DebugGUI
import sys

class TrackController(QMainWindow):
    #global variables used since they must be accessed and modified from signals in the GUI
    currentTrackState = {}#contains the current state of the track with all inputs and outputs, safe to get data from
    nextTrackState = {}   #contains the next state of the track being modified by PLC logic and sets from other modules, unsafe and should only be written to
    filename = ""
    program = 0
    inMaintenance = False
    runPLC = False


    def __init__(self):
        super().__init__()

        self.buildTrack()

        #Main Window setup 
        self.setGeometry(80, 80, 600, 600) #sets the window size
        self.setWindowTitle('Track Controller')

        #sets up central widget that the layout can be placed on
        mainWidget = QWidget()

        #message for uploaded PLC program
        message = ""
        if self.filename != "":
            message = self.filename + "is loaded."
        else:
            message = "No PLC program is loaded."
        self.statusBar().showMessage(message)

        #create widgets here
        uploadButton = QPushButton('Upload PLC Program', self)
        uploadButton.clicked.connect(self.uploadFile)

        editButton = QPushButton('Edit PLC Program', self)

        debugButton = QPushButton('Open Debug Menu', self)

        maintenanceButton = QPushButton('Open Maintenance Menu', self)


        tcLayout = QGridLayout()
        #add widgets to layout here
        tcLayout.addWidget(uploadButton, 1, 0)
        tcLayout.addWidget(editButton, 0, 0)
        tcLayout.addWidget(debugButton, 0, 1)
        tcLayout.addWidget(maintenanceButton, 1, 1)

        mainWidget.setLayout(tcLayout)
        self.setCentralWidget(mainWidget)

        self.show()
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
        tempTrack["red_A_1"].id = "red_A_1"
        tempTrack["red_A_2"].addGate()
        tempTrack["red_A_2"].id = "red_A_2"
        tempTrack["red_A_3"].addLight()
        tempTrack["red_A_3"].id = "red_A_3"

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
        if filenameTuple[0] != '':
            self.filename = filenameTuple[0]
            self.program = open(self.filename, "r")
            self.statusBar().showMessage(self.filename + " is loaded.")





#main for the whole Track Controller, simply creates an instance of TrackController
if __name__ == '__main__':
    #creates the application for Qt
    trackControllerApp = QApplication([])
    
    trackController = TrackController()
    #runs the app
    sys.exit(trackControllerApp.exec())

