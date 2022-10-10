import sys
import shutil
import pathlib
import os
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
from Block import Block
import TCGUI.MaintenanceGUI, TCGUI.TextEditorGUI, TCGUI.DebugGUI


class TrackController(QMainWindow):
    #track states separated to make things threadsafe probably
    current_Track_State = {}
    next_Track_State = {}
    filename = ""
    program = 0
    in_Maintenance = False
    run_PLC = False


    def __init__(self):
        super().__init__()

        self.build_Track()

        self.load_Saved_Program()

        self.setup_Main_Window()

        self.show()
        

        #run tick() on loop
        #doesn't need a timer since PLC should be running as fast as possible and all data transfers are event based
        while self.run_PLC:
            #TODO: create thread to handle all reads since they can be safely done without locking data

            self.tick()


        #closes the plc program on exit if there was one loaded
        if self.program != 0:
            self.program.close()



    def build_Track(self):
        #TODO:
        #probe track model for amount of blocks
        #generate blocks and add to trackState
        #probe track model for switches, gates, lights, possibly state of other block vars
        
        #BEGIN TEMPORARY SOLUTION FOR ITERATION 2
        tempTrack = {"red_A_1": Block(), "red_A_2": Block(), "red_A_3": Block()}
        tempTrack["red_A_1"].add_Switch()
        tempTrack["red_A_1"].id = "red_A_1"
        tempTrack["red_A_2"].add_Gate()
        tempTrack["red_A_2"].id = "red_A_2"
        tempTrack["red_A_3"].add_Light()
        tempTrack["red_A_3"].id = "red_A_3"

        self.current_Track_State = tempTrack
        self.next_Track_State = tempTrack

        #END TEMPORARY SOLUTION FOR ITERATION 2


    def tick(self):
        #TODO: runs PLC logic modifying nextTrackState while also handling sets from other modules
        pass


    #loads the saved PLC program if there is one
    #and displays loaded message
    def load_Saved_Program(self):
        #message for uploaded PLC program
        message = ""
        #complicated buts gets all path to .txt files in Program folder
        file_Array = sorted(pathlib.Path(str(pathlib.Path().absolute()) + '/Program/').glob('*.txt'))
        #gets the first .txt file in Program folder
        if len(file_Array) != 0:
            filepath = file_Array[0]
        
            #sets filename from filepath and displays PLC message
            self.filename = str(filepath)
            message = self.extract_Name(self.filename) + " is loaded."
        else:
            message = "No PLC program is loaded."

        self.statusBar().setFont(QFont('Times', 13))
        self.statusBar().showMessage(message)


    #sets up main window GUI elements
    def setup_Main_Window(self):
        #Main Window setup 
        self.setGeometry(80, 80, 500, 400) #sets the window size
        self.setWindowTitle('Track Controller')
        self.setMinimumSize(400, 400)

        #sets up central widget that the layout will be placed on
        mainWidget = QWidget()

        #creates the font used in buttons
        buttonFont = QFont('Times', 16)

        #create main window buttons here and add functionality
        uploadButton = QPushButton('Upload PLC Program', self)
        uploadButton.clicked.connect(self.upload_File)
        uploadButton.setMinimumHeight(160)
        uploadButton.setFont(buttonFont)

        editButton = QPushButton('Edit PLC Program', self)
        editButton.setMinimumHeight(160)
        editButton.setFont(buttonFont)

        debugButton = QPushButton('Open Debug Menu', self)
        debugButton.setMinimumHeight(160)
        debugButton.setFont(buttonFont)

        maintenanceButton = QPushButton('Open Maintenance Menu', self)
        maintenanceButton.setMinimumHeight(160)
        maintenanceButton.setFont(buttonFont)

        tcLayout = QGridLayout()
        #add widgets to layout here
        tcLayout.addWidget(uploadButton, 1, 0)
        tcLayout.addWidget(editButton, 0, 0)
        tcLayout.addWidget(debugButton, 0, 1)
        tcLayout.addWidget(maintenanceButton, 1, 1)

        #applies the layout to the main widget and sets it as central
        mainWidget.setLayout(tcLayout)
        self.setCentralWidget(mainWidget)


    #opens windows explorer to select and open a new file
    def upload_File(self):
        filename_Tuple = QFileDialog.getOpenFileName(None, 'Choose PLC Program', 'C:\\', "Text Files (*.txt)")

        #does nothing if the upload was canceled
        if filename_Tuple[0] != '':
            #complicated buts gets path to all .txt files in Program folder
            file_Array = sorted(pathlib.Path(str(pathlib.Path().absolute()) + '/Program/').glob('*.txt'))
            if len(file_Array) != 0:
                os.remove(str(file_Array[0]))

            self.filename = filename_Tuple[0]

            #saves the uploaded PLC program to local Program directory
            destination = str(pathlib.Path().absolute()) + '/Program/' + self.extract_Name(self.filename) 
            shutil.copyfile(self.filename, destination)
            #ensures that the local copy of the PLC program is opened
            self.filename = destination

            #opens new PLC program and shows message stating so
            #self.program = open(self.filename, "r")
            self.statusBar().showMessage(self.extract_Name(self.filename) + " is loaded.")


    #extracts the PLC filename from the filepath
    def extract_Name(self, filepath):
        temp = ''
        filepath_Pos = len(filepath)
        while temp != '/' and temp != '\\':
            filepath_Pos = filepath_Pos - 1
            temp = filepath[filepath_Pos]

        return filepath[filepath_Pos+1:len(filepath)]


    def open_Debug(self):
        pass

    def open_Editor(self):
        #disables the PLC from running when editing
        self.run_PLC = False

        #passes the enable_PLC function to allow the text editor 
        #to reenable the PLC on close (I PRAY THIS WORKS)
        editor = TCGUI.TextEditorGUI(self.filename, self.enable_PLC)
        editor.show()

    def open_Maintenance(self):
        pass


    def enable_PLC(self):
        self.run_PLC = True

#main for the whole Track Controller, simply creates an instance of TrackController
if __name__ == '__main__':
    #creates the application for Qt
    track_Controller_App = QApplication([])
    
    track_Controller = TrackController()
    #runs the app
    sys.exit(track_Controller_App.exec())

