import sys
import shutil
import pathlib
import os
import copy
import time
import threading
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QGridLayout, QPushButton, QWidget, QLabel
from PyQt5.QtGui import QFont
from Block import Block
import TCGUI.TextEditorGUI, TCGUI.DebugGUI, TCGUI.MaintenanceGUI, TCGUI.ModifyGUI
from PLCInterpreter import PLCInterpreter


#TODO:
#modify gui elements to disable run_Vitals not run_PLC
#execute logic on debug test
#write track building function (depends on track model so idk yet)

class TrackController(QMainWindow):

    def __init__(self, tc_ID = 0, auto_Run = False):
        #track states
        self.current_Track_State = {}
        self.next_Track_State = {}
        #id for when there are multiple track controllers
        self.id = tc_ID
        #name of saved plc file
        self.filename = ""
        #tracks what menus are open
        self.in_Debug = False
        self.in_Maintenance = False
        self.in_Modify = False
        #tracks which parts of the logic thread to run
        self.run_PLC = False
        self.run_Vital = True
        #object for each menu
        self.editor = None
        self.debug = None
        self.maintenance = None
        #self.modify = None
        #semaphore for track state access
        self.track_Lock = False
        #target fps = 1/target_Time
        self.target_Time = 0.5
        #thread object for running logic in background
        self.logic_Thread = threading.Thread(target=self.run_Logic)
        
        #interpreter
        self.interpreter = PLCInterpreter.PLCInterpreter()
        
        

        super().__init__()

        self.build_Track()

        self.load_Saved_Program()

        self.setup_Main_Window()

        if auto_Run == True:
            self.start_Logic()
        else:
            self.show()



    def build_Track(self):
        #TODO:
        #probe track model for blocks
        #probe track model for switche, gate, and light amounts

        #for testing
        tempBlock = Block("red_A_1")
        tempBlock.add_Switch()
        tempBlock.add_Light()
        tempBlock.add_Gate()
        self.current_Track_State["red_A_1"] = copy.deepcopy(tempBlock)

        tempBlock = Block("red_A_2")
        tempBlock.add_Switch()
        tempBlock.add_Light()
        tempBlock.add_Gate()
        self.current_Track_State["red_A_2"] = copy.deepcopy(tempBlock)

        tempBlock = Block("red_A_3")
        tempBlock.add_Switch()
        tempBlock.add_Light()
        tempBlock.add_Gate()
        self.current_Track_State["red_A_3"] = copy.deepcopy(tempBlock)

        tempBlock = Block("red_A_4")
        tempBlock.add_Switch()
        tempBlock.add_Light()
        tempBlock.add_Gate()
        self.current_Track_State["red_A_4"] = copy.deepcopy(tempBlock)

        tempBlock = Block("red_A_5")
        tempBlock.add_Switch()
        tempBlock.add_Light()
        tempBlock.add_Gate()
        self.current_Track_State["red_A_5"] = copy.deepcopy(tempBlock)

        tempBlock = Block("red_A_6")
        tempBlock.add_Switch()
        tempBlock.add_Light()
        tempBlock.add_Gate()
        self.current_Track_State["red_A_6"] = copy.deepcopy(tempBlock)

        tempBlock = Block("red_A_7")
        tempBlock.add_Switch()
        tempBlock.add_Light()
        tempBlock.add_Gate()
        self.current_Track_State["red_A_7"] = copy.deepcopy(tempBlock)

        tempBlock = Block("red_A_8")
        tempBlock.add_Switch()
        tempBlock.add_Light()
        tempBlock.add_Gate()
        self.current_Track_State["red_A_8"] = copy.deepcopy(tempBlock)

        tempBlock = Block("red_A_9")
        tempBlock.add_Switch()
        tempBlock.add_Light()
        tempBlock.add_Gate()
        self.current_Track_State["red_A_9"] = copy.deepcopy(tempBlock)

        tempBlock = Block("red_A_10")
        tempBlock.add_Switch()
        tempBlock.add_Light()
        tempBlock.add_Gate()
        self.current_Track_State["red_A_10"] = copy.deepcopy(tempBlock)

        self.next_Track_State = copy.deepcopy(self.current_Track_State)
        



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
        self.setGeometry(80, 80, 500, 450) #sets the window size
        self.setWindowTitle('Track Controller ' + str(self.id))
        self.setMinimumSize(500, 450)

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

        #modifyButton = QPushButton('Modify Track', self)
        #modifyButton.clicked.connect(self.open_Modify)
        #modifyButton.setMinimumHeight(60)
        #modifyButton.setFont(buttonFont)

        self.run_Button = QPushButton('RUN PLC', self)
        self.run_Button.clicked.connect(self.start_Logic)
        self.run_Button.setMinimumHeight(60)
        self.run_Button.setFont(buttonFont)
        self.run_Button.setCheckable(True)
        self.run_Button.setEnabled(True)
        self.run_Button.setStyleSheet("background-color: green")


        self.stop_Button = QPushButton('STOP PLC', self)
        self.stop_Button.clicked.connect(self.stop_Logic)
        self.stop_Button.setMinimumHeight(60)
        self.stop_Button.setFont(buttonFont)
        self.stop_Button.setCheckable(True)
        self.stop_Button.setEnabled(False)
        self.stop_Button.setStyleSheet("background-color: gray")

        self.vitals_Label = QLabel("Vitals: Stopped")
        self.vitals_Label.setFont(QFont('Times', 12))
        self.vitals_Label.setMaximumHeight(30)
        self.vitals_Label.setMinimumHeight(30)
        
        self.plc_Label = QLabel("Logic: Stopped")
        self.plc_Label.setFont(QFont('Times', 12))
        self.plc_Label.setMaximumHeight(30)
        self.plc_Label.setMinimumHeight(30)



        tcLayout = QGridLayout()
        #add widgets to layout here
        #tcLayout.addWidget(modifyButton, 0, 0)
        tcLayout.addWidget(self.run_Button, 0, 0)
        tcLayout.addWidget(self.stop_Button, 0, 1)
        tcLayout.addWidget(self.vitals_Label, 1, 0)
        tcLayout.addWidget(self.plc_Label, 2, 0)
        tcLayout.addWidget(uploadButton, 3, 0)
        tcLayout.addWidget(editButton, 4, 0)
        tcLayout.addWidget(debugButton, 3, 1)
        tcLayout.addWidget(maintenanceButton, 4, 1)

        #applies the layout to the main widget and sets it as central
        mainWidget.setLayout(tcLayout)
        self.setCentralWidget(mainWidget)


    #opens windows explorer to select and open a new file
    def upload_File(self):
        #kills thread running run_Logic
        self.stop_Logic()

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
            self.statusBar().showMessage(self.extract_Name(self.filename) + " is loaded.")

            #opens new file in editor if editor has been opened
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
            self.debug = TCGUI.DebugGUI.DebugGUI(self.get_Track, self.set_Track, self.update_Sync_Track, self.leave_Debug)
 
        if self.in_Modify is False:
            self.in_Debug = True
            self.debug.show()

    #opens text editor
    def open_Editor(self):
        #ensures the editor doesn't try to open a file that isn't there
        if self.filename != '':
            #disables the PLC from running when editing
            self.run_Vital = False

            #ensure the editor isn't already open
            if self.editor is None:

                #passes the enable_Vitals function to allow the text editor
                #to reenable PLC logic on close
                self.editor = TCGUI.TextEditorGUI.TextEditorGUI(self.enable_Vitals, self.filename)
            self.editor.show()

    #opens maintenance menu
    def open_Maintenance(self):
        if self.maintenance is None:
            self.maintenance = TCGUI.MaintenanceGUI.MaintenanceGUI(self.get_Track, self.leave_Maintenance)

        if self.in_Modify is False:
            self.in_Maintenance = True
            self.maintenance.show()

    #opens modify menu
    #def open_Modify(self):
    #    if self.modify is None:
    #        self.modify = TCGUI.ModifyGUI.ModifyGUI(self.get_Next_Track, self.update_Sync_Track, self.leave_Modify)
    #
    #    if self.in_Debug is False and self.in_Maintenance is False:
    #        self.in_Modify = True
    #        self.modify.show()

    #used to pass the track state to the debug and maintenance guis
    def get_Track(self):
        #refuses access to the track if it is locked
        if self.track_Lock == False:
            return self.current_Track_State

    #used to modify track blocks
    def get_Next_Track(self):
        return self.next_Track_State

    #updates a value in next_Track_State
    def set_Track(self, block, var, val):

        match var:
            case "spd":
                self.next_Track_State[block].suggested_Speed = copy.copy(val)
            case "auth":
                self.next_Track_State[block].forward_Authority = copy.copy(val)
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
        #this might be changed later
        for block in self.next_Track_State:
            self.next_Track_State[block].commanded_Speed = copy.copy(self.next_Track_State[block].suggested_Speed)

        self.current_Track_State = copy.deepcopy(self.next_Track_State)


    #main plc loop continuously generating outputs using logic
    #is run on another thread
    def run_Logic(self):
        self.run_Vital = True
        self.interpreter.set_Environment(self.next_Track_State)

        if self.filename != "":
            #opens plc file
            logic_File = open(self.filename, 'r')
            self.run_PLC = self.interpreter.tokenize(logic_File)
            logic_File.close()
        else:
            self.run_PLC = False


        self.vitals_Label.setText("Vitals: Running")
        self.stop_Button.setStyleSheet("background-color: red")
        self.run_Button.setStyleSheet("background-color: gray")
        if self.run_PLC == True:
            self.plc_Label.setText("Logic: Running")


        while self.run_Vital == True:
            #starts timer for fps control
            start_Time = time.perf_counter()

            #locks track state before copying
            self.track_Lock = True
            #copies track state inputs to next state
            for block in self.current_Track_State:
                self.next_Track_State[block].suggested_Speed = copy.copy(self.current_Track_State[block].suggested_Speed)
                self.next_Track_State[block].authority = copy.copy(self.current_Track_State[block].authority)
                self.next_Track_State[block].occupied = copy.copy(self.current_Track_State[block].occupied)
                self.next_Track_State[block].failed = copy.copy(self.current_Track_State[block].failed)
                self.next_Track_State[block].closed = copy.copy(self.current_Track_State[block].closed)
            #unlocks track state so other modules can modify inputs/read outputs
            self.track_Lock = False
            
            #runs logic
            if self.run_PLC == True:
                #try block to handle any undefined behavior in the plc program
                #for example a block name that the plc isnt connected to
                try:
                    success = self.interpreter.execute(self.target_Time)
                    if success == False:
                        raise Exception("PLC timeout during execution.")

                except Exception as e:
                    print("FATAL PLC RUNTIME ERROR.")
                    print(e)    
                    print("Continuing to run vital logic.")
                
                    self.run_PLC = False

            #maybe put some safety logic here idk

            #locks track state before updating
            self.track_Lock = True
            #copies newly generated outputs back to track state
            for block in self.current_Track_State:
                self.current_Track_State[block].authority = copy.copy(self.next_Track_State[block].authority)
                
                for switch in range(len(self.current_Track_State[block].switches)):
                    self.current_Track_State[block].switches[switch] = copy.copy(self.next_Track_State[block].switches[switch])
                
                for light in range(len(self.current_Track_State[block].lights)):
                    self.current_Track_State[block].lights[light] = copy.copy(self.next_Track_State[block].lights[light])

                for gate in range(len(self.current_Track_State[block].gates)):
                    self.current_Track_State[block].gates[gate] = copy.copy(self.next_Track_State[block].gates[gate])
            #unlocks track state
            self.track_Lock = False

            #calculates the amount of time to sleep to achieve target fps
            time_Diff = time.perf_counter() - start_Time
            wait_Time = self.target_Time - time_Diff
            time.sleep(wait_Time)


    #function for reenabling logic after editing a file
    def enable_Vitals(self):
        self.run_Vital = True

    #resets the in_Debug flag when the menu is closed
    def leave_Debug(self):
        self.in_Debug = False

    #resets the in_Maintenance flag when the menu is closed
    def leave_Maintenance(self):
        self.in_Maintenance = False

    #resets the in_Modify flag when the menu is closed
    def leave_Modify(self):
        self.in_Modify = False
        self.update_Sync_Track()
        if self.maintenance is not None:
            self.maintenance.parse_Blocks()
        if self.debug is not None:
            self.debug.parse_Track_Blocks()

    #starts logic thread
    def start_Logic(self):
        self.run_Button.setEnabled(False)
        self.stop_Button.setEnabled(True)

        if self.logic_Thread.is_alive() == False:
            self.logic_Thread.start()

    #stops logic thread
    def stop_Logic(self):
        self.run_Vital = False
        self.run_PLC = False
        #consider a timeout for join and a force abort if join fails
        self.logic_Thread.join()
        self.vitals_Label.setText("Vitals: Stopped")
        self.plc_Label.setText("Logic: Stopped")

        self.run_Button.setEnabled(True)
        self.run_Button.setStyleSheet("background-color: green")
        self.stop_Button.setEnabled(False)
        self.stop_Button.setStyleSheet("background-color: gray")

#main for the whole Track Controller, simply creates an instance of TrackController
if __name__ == '__main__':
    #creates the application for Qt
    track_Controller_App = QApplication([])
    
    track_Controller = TrackController()
    #runs the app
    sys.exit(track_Controller_App.exec())

