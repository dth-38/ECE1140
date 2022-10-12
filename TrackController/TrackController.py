import sys
import shutil
import pathlib
import os
import copy
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
from Block import Block
import TCGUI.TextEditorGUI, TCGUI.DebugGUI, TCGUI.MaintenanceGUI, TCGUI.ModifyGUI


class TrackController(QMainWindow):

    def __init__(self, tc_ID=0):
        self.current_Track_State = {}
        self.next_Track_State = {}
        self.id = tc_ID
        self.filename = ""
        self.program = 0
        self.in_Maintenance = False
        self.in_Debug = False
        self.run_PLC = True
        self.editor = None
        self.debug = None
        self.maintenance = None
        self.modify = None
        

        super().__init__()

        self.build_Track()

        self.load_Saved_Program()

        self.setup_Main_Window()

        self.show()



    def build_Track(self):
        #TODO:
        #probe track model for amount of blocks
        #generate blocks and add to trackState
        #probe track model for switches, gates, lights, possibly state of other block vars
        
        #BEGIN TEMPORARY SOLUTION FOR ITERATION 2
        block1 = Block()
        block2 = Block()
        block3 = Block()
        tempTrack = {"red_A_1": block1, "red_A_2": block2, "red_A_3": block3}
        tempTrack["red_A_1"].id = "red_A_1"
        tempTrack["red_A_2"].id = "red_A_2"
        tempTrack["red_A_3"].id = "red_A_3"
        tempTrack["red_A_1"].add_Switch()
        tempTrack["red_A_1"].add_Switch()
        tempTrack["red_A_1"].add_Switch()
        tempTrack["red_A_2"].add_Gate()
        tempTrack["red_A_3"].add_Light()


        self.current_Track_State = copy.deepcopy(tempTrack)
        self.next_Track_State = tempTrack

        #END TEMPORARY SOLUTION FOR ITERATION 2


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

            #enables PLC logic if a program is found
        else:
            message = "No PLC program is loaded."

        self.statusBar().setFont(QFont('Times', 13))
        self.statusBar().showMessage(message)


    #sets up main window GUI elements
    def setup_Main_Window(self):
        #Main Window setup 
        self.setGeometry(80, 80, 500, 400) #sets the window size
        self.setWindowTitle('Track Controller ' + str(self.id))
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
        editButton.clicked.connect(self.open_Editor)
        editButton.setMinimumHeight(160)
        editButton.setFont(buttonFont)

        debugButton = QPushButton('Open Debug Menu', self)
        debugButton.clicked.connect(self.open_Debug)
        debugButton.setMinimumHeight(160)
        debugButton.setFont(buttonFont)

        maintenanceButton = QPushButton('Open Maintenance Menu', self)
        maintenanceButton.clicked.connect(self.open_Maintenance)
        maintenanceButton.setMinimumHeight(160)
        maintenanceButton.setFont(buttonFont)

        modifyButton = QPushButton('Modify Track', self)
        modifyButton.clicked.connect(self.open_Modify)
        modifyButton.setMinimumHeight(80)
        modifyButton.setFont(buttonFont)


        tcLayout = QGridLayout()
        #add widgets to layout here
        tcLayout.addWidget(uploadButton, 0, 0)
        tcLayout.addWidget(editButton, 1, 0)
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

            #opens new file in editor if editor has been openend
            if self.editor is not None:
                self.editor.set_Filepath(self.filename)
                self.editor.open_File()


    #extracts the PLC filename from the filepath
    def extract_Name(self, filepath):
        temp = ''
        filepath_Pos = len(filepath)
        while temp != '/' and temp != '\\':
            filepath_Pos = filepath_Pos - 1
            temp = filepath[filepath_Pos]

        return filepath[filepath_Pos+1:len(filepath)]

    #opens Debug menu
    def open_Debug(self):
        if self.debug is None:
            self.debug = TCGUI.DebugGUI.DebugGUI(self.get_Track, self.set_Track, self.update_Sync_Track)
 
        self.debug.show()

    #opens text editor
    def open_Editor(self):
        #ensures the editor doesn't try to open a file that isn't there
        if self.filename != '':
            #disables the PLC from running when editing
            self.run_PLC = False

            #ensure the editor isn't already open
            if self.editor is None:

                #passes the enable_PLC function to allow the text editor
                #to reenable PLC logic on close
                self.editor = TCGUI.TextEditorGUI.TextEditorGUI(self.filename, self.enable_PLC, self.extract_Name)
            self.editor.show()

    #opens maintenance menu
    def open_Maintenance(self):
        if self.maintenance is None:
            self.maintenance = TCGUI.MaintenanceGUI.MaintenanceGUI(self.get_Track)

        self.maintenance.show()

    def open_Modify(self):
        if self.modify is None:
            self.modify = TCGUI.ModifyGUI.ModifyGUI(self.get_Next_Track)

        self.modify.show()

    #used to pass the track state to the debug and maintenance guis
    def get_Track(self):
        return self.current_Track_State

    #used to modify track blocks
    def get_Next_Track(self):
        return self.next_Track_State

    #updates a value in next_Track_State
    def set_Track(self, block, var, val):

        match var:
            case "spd":
                self.next_Track_State[block].suggested_Speed = copy.copy(val)
            case "fAuth":
                self.next_Track_State[block].forward_Authority = copy.copy(val)
            case "bAuth":
                self.next_Track_State[block].backward_Authority = copy.copy(val)
            case "occ":
                if val == 'Y':
                    val = True
                elif val == 'N':
                    val = False
                self.next_Track_State[block].occupied = copy.copy(val)
            case "cls":
                if val == 'Y':
                    val = True
                elif val == 'N':
                    val = False
                self.next_Track_State[block].closed = copy.copy(val)
            case "fail":
                if val == 'Y':
                    val = True
                elif val == 'N':
                    val = False
                self.next_Track_State[block].failed = copy.copy(val)
            case _:
                pass


    #runs PLC on next_Track_State and syncs current_Track_State
    def update_Sync_Track(self):
        if self.run_PLC:
            #TODO: run logic here

            #this might be changed later
            for block in self.next_Track_State:
                self.next_Track_State[block].commanded_Speed = copy.copy(self.next_Track_State[block].suggested_Speed)

            self.current_Track_State = copy.deepcopy(self.next_Track_State)


    #function for reenabling logic after editing a file
    def enable_PLC(self):
        self.run_PLC = True


#main for the whole Track Controller, simply creates an instance of TrackController
if __name__ == '__main__':
    #creates the application for Qt
    track_Controller_App = QApplication([])
    
    track_Controller = TrackController()
    #runs the app
    sys.exit(track_Controller_App.exec())

