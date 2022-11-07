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
#FIX logic jankyness, getting there...
#add initial logic block search to PLCInterpreter
#execute logic on debug test
#add next_Block field to block
#add edge case to safety logic for changing track controllers
#might still need a start_PLC function idk look into it
#make room for update function calls to other modules maybe???

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
        #tracks which parts of the logic thread to run
        self.run_PLC = False
        self.run_Vitals = False
        #object for each menu
        self.editor = None
        self.debug = None
        self.maintenance = None
        #semaphore for track state access
        self.track_Lock = False
        #target fps = 1/target_Time
        self.target_Time = 0.5

        #array for tracking which blocks were previously occupied
        #used for track failure checking
        self.previous_Occupations = []

        #CHANGING STUFF WITH THREADING
        #use run_Logic as a standalone function that acts as the system timer if there is no integration
        #thread object for running logic in background
        #self.logic_Thread = threading.Thread(target=self.run_Logic)
        
        #interpreter
        self.interpreter = PLCInterpreter.PLCInterpreter()
        

        super().__init__()

        self.load_Saved_Program()

        self.build_Track()

        self.setup_Main_Window()

        if auto_Run == True:
            self.run_PLC = True
        else:
            self.show()


    #builds the track_state dictionaries from the uploaded plc file or a specified one
    #returns True on success, False on failure
    def build_Track(self, fl = ""):
        self.run_Vitals = False

        success = False
        temp_Track = {}

        #allows a plc program to be directly parsed, mainly for testing purposes
        if fl != "":
            self.filename = fl
            self.statusBar().showMessage(self.extract_Name(self.filename) + " is loaded.")


        #checks that there is a plc program loaded
        if self.filename != "":
            program = open(self.filename, "r")

            line = program.readline()

            while line:

                #parses each line looking for DEFINE TRACK
                define_Statement = self.ignore_Whitespace(line)

                if define_Statement == "DEFINETRACK":
                    #DEFINE TRACK has been found

                    #checks if a track section has already been parsed
                    if success == True:
                        print("Track initialization failed: Multiple track sections found.")
                        success = False
                        return False
                        

                    line = program.readline()
                    block_Statement = self.ignore_Whitespace(line)

                    #parses DEFINE TRACK section until an END TRACK is found
                    while block_Statement != "ENDTRACK":

                        #looks for a BLOCK statement
                        if block_Statement[0:5] == "BLOCK":
                            #BLOCK statement has been found

                            #extracts block name and creates new block
                            block_Name = block_Statement[5:]
                            temp_Track[block_Name] = Block()

                            line = program.readline()
                            statement = self.ignore_Whitespace(line)

                            #section for parsing track equipment definitions in a block
                            while statement != "ENDBLOCK":
                                
                                #try block here since the match substring or int typecasts could fail
                                try:
                                    match statement[:1]:
                                        case "S":
                                            for j in range(int(statement[1:])):
                                                temp_Track[block_Name].add_Switch()
                                        case "G":
                                            for j in range(int(statement[1:])):
                                                temp_Track[block_Name].add_Gate()
                                        case "L":
                                            for j in range(int(statement[1:])):
                                                temp_Track[block_Name].add_Light()
                                        case "M":
                                            temp_Track[block_Name].max_Speed = int(statement[1:])
                                        case "P":
                                            temp_Track[block_Name].previous_Block = statement[1:]
                                        case _:
                                            if statement[0] != ";":
                                                raise Exception("Failed to intialize track: Invalid statement in block definition.")
                                except Exception as e:
                                    print(e)
                                    program.close()
                                    return False

                                line = program.readline()
                                statement = self.ignore_Whitespace(line)
                        else:
                            #checks if the line is a comment and fails the function if it isnt
                            if block_Statement[0] != ";":
                                print("Failed to initialize track: Invalid block definition statement.")
                                program.close()
                                return False

                        line = program.readline()
                        block_Statement = self.ignore_Whitespace(line)

                    #if it makes it here a track has been successfully parsed
                    #continues iterating to ensure only one track is defined
                    success = True

            line = program.readline()


        #matches the track states to the newly created one if parsing is successful
        if success == True:
            #copies temporary track into current and next
            self.current_Track_State = copy.deepcopy(temp_Track)
            self.next_Track_State = copy.deepcopy(temp_Track)

            #sets interpreter environement to the next track state
            self.interpreter.set_Environment(self.next_Track_State)

            #returns the program to the first line and calls the tokenizer

            self.run_PLC = self.interpreter.tokenize(program)

            self.run_Vitals = True

        return success

    #returns the string line with whitespace and newlines removed
    def ignore_Whitespace(self, line):
        newLine = ""
        for i in range(len(line)):
            if line[i] != " " and line[i] != "\n":
                newLine += line[i]

        return newLine


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

        self.run_Button = QPushButton('RUN PLC', self)
        self.run_Button.clicked.connect(self.run_Logic)
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

        self.plc_Label = QLabel("Logic: Stopped")
        self.plc_Label.setFont(QFont('Times', 12))
        self.plc_Label.setMaximumHeight(30)
        self.plc_Label.setMinimumHeight(30)



        tcLayout = QGridLayout()
        #add widgets to layout here
        tcLayout.addWidget(self.run_Button, 0, 0)
        tcLayout.addWidget(self.stop_Button, 0, 1)
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
        #stops logic from running
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

            self.build_Track()



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

        
        self.in_Maintenance = True
        self.maintenance.show()


    #used to pass the track state to the debug and maintenance guis
    def get_Track(self):
        #refuses access to the track if it is locked
        if self.track_Lock == False:
            return self.current_Track_State

    #used to modify track blocks
    def get_Next_Track(self):
        return self.next_Track_State

    #this is due for a refactor
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

    #also due for a refactor
    #runs PLC on next_Track_State and syncs current_Track_State
    def update_Sync_Track(self):
        #this might be changed later
        for block in self.next_Track_State:
            self.next_Track_State[block].commanded_Speed = copy.copy(self.next_Track_State[block].suggested_Speed)

        self.current_Track_State = copy.deepcopy(self.next_Track_State)


    #main plc loop continuously generating outputs using logic
    #is run on another thread
    def tick(self):

        if self.filename != "":
            #opens plc file
            logic_File = open(self.filename, 'r')
            self.run_PLC = self.interpreter.tokenize(logic_File)
            logic_File.close()
        else:
            self.run_PLC = False

        self.update_Run_UI(True)

        if self.run_Vital == True:

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


            #locks track state before updating
            self.track_Lock = True

            #runs vital safety logic then
            #copies newly generated outputs back to track state
            for block in self.current_Track_State:

                #speed safety check: commanded speed cannot exceed block maximum
                self.next_Track_State[block].commanded_Speed = copy.copy(self.next_Track_State[block].suggested_Speed)
                if self.next_Track_State[block].commanded_Speed > self.next_Track_State[block].max_Speed:
                    self.next_Track_State[block].commanded_Speed = copy.copy(self.next_Track_State[block].max_Speed)

                #track failure check
                #cannot determine if a block connected to a yard has failed
                #since that is identical to dispatching as far as the track controller can tell
                if self.next_Track_State[block].occupied == True:
                    previous = self.next_Track_State[block].previous_Block
                    if previous != "yard":
                        previous_Second = self.next_Track_State[previous].previous_Block
                    else:
                        self.previous_Occupations.append(previous)
                    next_Bl = self.next_Track_State[block].next_Block
                    next_Bl_Second = self.next_Track_State[next_Bl].next_Block

                    #updates previously occupied blocks and checks for track failure
                    #if a currently occupied block does not have a previous in the list it has failed
                    previous_Block_Found = False
                    for prev_Occ in self.previous_Occupations:
                        if prev_Occ == previous or prev_Occ == next_Bl or prev_Occ == block:
                            previous_Block_Found = True
                            break
                        elif prev_Occ == previous_Second:
                            self.previous_Occupations.remove(prev_Occ)
                            self.previous_Occupations.append(previous)
                            previous_Block_Found = True
                            break
                        elif prev_Occ == next_Bl_Second:
                            self.previous_Occupations.remove(prev_Occ)
                            self.previous_Occupations.append(next_Bl)
                            previous_Block_Found = True
                            break
                        else:
                            pass

                    if previous_Block_Found == False:
                        self.next_Track_State[block].failed = True


                #failure/closure safety check: shuts down block if it has failed or is closed
                if self.next_Track_State[block].closed == True or self.next_Track_State[block].failed == True:
                    self.next_Track_State[block].authority = 0
                    for light in range(len(self.next_Track_State[block].lights)):
                        self.next_Track_State[block].set_Light(light, "RED")

                #switch interlock safety check: occupied blocks cannot change switch positions
                if self.next_Track_State[block].occupied == True:
                    for switch in range(len(self.next_Track_State[block].switches)):
                        self.next_Track_State[block].switches[switch] = copy.copy(self.current_Track_State[block].switches[switch])

                #train padding check: creates a safety zone with all recently occupied block
                for bl in self.previous_Occupations:
                    if bl != "yard":
                        self.next_Track_State[bl].authority = 0

                #copies next track back to current track
                self.current_Track_State[block].commanded_Speed = copy.copy(self.next_Track_State[block].commanded_Speed)

                self.current_Track_State[block].authority = copy.copy(self.next_Track_State[block].authority)
                
                for switch in range(len(self.current_Track_State[block].switches)):
                    self.current_Track_State[block].switches[switch] = copy.copy(self.next_Track_State[block].switches[switch])
            
                for light in range(len(self.current_Track_State[block].lights)):
                    self.current_Track_State[block].lights[light] = copy.copy(self.next_Track_State[block].lights[light])

                for gate in range(len(self.current_Track_State[block].gates)):
                    self.current_Track_State[block].gates[gate] = copy.copy(self.next_Track_State[block].gates[gate])

            #longest track controller update period while properly detecting trains is 1.6 seconds


            #unlocks track state
            self.track_Lock = False



    #resets the in_Debug flag when the menu is closed
    def leave_Debug(self):
        self.in_Debug = False

    #resets the in_Maintenance flag when the menu is closed
    def leave_Maintenance(self):
        self.in_Maintenance = False


    #stops logic thread
    def stop_Logic(self):
        self.run_PLC = False
        #consider a timeout for join and a force abort if join fails
        #self.logic_Thread.join()
        self.plc_Label.setText("Logic: Stopped")

        self.update_Run_UI(False)

    #updates the state of the run/stop buttons and status lines
    #based on the whether the logic is starting or stopping
    #and if the vital or nonvital logic is running
    def update_Run_UI(self, start):
        if start == True:
            self.run_Button.setEnabled(False)
            self.stop_Button.setEnabled(True)
            if self.run_PLC == True:
                self.plc_Label.setText("Logic: Running")
            else:
                self.plc_Label.setText("Logic: Stopped")
            if self.run_Vitals == True:
                self.vitals_Label.setText("Vitals: Running")
                self.stop_Button.setStyleSheet("background-color: red")
                self.run_Button.setStyleSheet("background-color: gray")
            else:
                self.vitals_Label.setText("Vitals: Stopped")
                self.stop_Button.setStyleSheet("background-color: gray")
                self.run_Button.setStyleSheet("background-color: green")
        else:
            self.run_Button.setEnabled(True)
            self.stop_Button.setEnabled(False)
            self.stop_Button.setStyleSheet("background-color: gray")
            self.run_Button.setStyleSheet("background-color: green")

            



#main for the whole Track Controller, simply creates an instance of TrackController
if __name__ == '__main__':
    #creates the application for Qt
    track_Controller_App = QApplication([])
    
    track_Controller = TrackController()
    #runs the app
    sys.exit(track_Controller_App.exec())

