import sys
import shutil
import pathlib
import os
import copy

from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QGridLayout, QPushButton, QWidget, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot

from TrackController.Block import Block, TO_NEXT, TO_PREV
from TrackController.TCGUI.DebugGUI import DebugGUI
from TrackController.TCGUI.MaintenanceGUI import MaintenanceGUI
from TrackController.TCGUI.TextEditorGUI import TextEditorGUI
from TrackController.PLCInterpreter.PLCInterpreter import PLCInterpreter

from TrackController.TCTools import decompose_block

from Signals import signals



class TrackController(QMainWindow):

    def __init__(self, tc_ID = 0, auto_Run = False):
        #track states
        self.track_Size = 0
        self.current_Track_State = {}
        self.next_Track_State = {}
        #id for when there are multiple track controllers
        self.id = tc_ID
        #name of saved plc file
        self.filename = ""
        #tracks which parts of tick() to run
        self.run_PLC = False
        self.run_Vitals = False
        #object for each menu
        self.editor = None
        self.debug = None
        self.maintenance = None
        #array for tracking which blocks were previously occupied
        #used for track failure checking
        self.previous_Occupations = []
        #tracks first and final blocks. speeds up safety logic
        self.first_Block = ""
        self.final_Block = ""
        #interpreter
        self.interpreter = PLCInterpreter()
        
        #array for tracking trains
        #each train is a list, with the format [movement_direction, occupied_block_1, occupied_block_2*]
        # *second occupied is -1 if there isnt one
        self.tracker = []

        super().__init__()


        self.setup_Main_Window()
        self.load_Saved_Program()
        self.build_Track()

        self.setup_signals()

        #allows the TC to be instantiated without opening the GUI
        if auto_Run == False:
            self.show()


#---------------------------------------------------------------
# FUNCTIONS TO BUILD TRACK
#---------------------------------------------------------------
    #builds the track_state dictionaries from the uploaded plc file or a specified one
    #returns True on success, False on failure
    def build_Track(self, fl = ""):
        self.stop_Vitals()
        self.stop_PLC()

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

            while len(line) != 0 and success == False:

                #parses each line looking for DEFINE TRACK
                define_Statement = self.ignore_Whitespace(line)

                if define_Statement == "DEFINETRACK":
                    #DEFINE TRACK has been found

                    #checks if a track section has already been parsed
                    if success == True:
                        print("Track initialization failed: Multiple track sections found.")
                        program.close()
                        success = False
                        self.default_Track()
                        return False
                        

                    line = program.readline()
                    block_Statement = self.ignore_Whitespace(line)

                    i = 0
                    #parses DEFINE TRACK section until an END TRACK is found
                    while block_Statement != "ENDTRACK":

                        #looks for a BLOCK statement
                        if block_Statement[0:5] == "BLOCK":
                            i += 1
                            #BLOCK statement has been found

                            #extracts block name and creates new block
                            block_Name = block_Statement[5:]
                            temp_Track[block_Name] = Block()

                            if i == 1:
                                b1 = block_Name
                            else:
                                b2 = block_Name

                            line = program.readline()
                            statement = self.ignore_Whitespace(line)

                            #section for parsing track equipment definitions in a block
                            while statement != "ENDBLOCK":

                                #try block here since the match substring or int typecasts could fail
                                try:
                                    match statement[0]:
                                        case "S":
                                            #format: S NEXT/PREV, off_Block, on_Block
                                            #gets blocks the switch sends to and whether they are previous or next
                                            direction = statement[1:5]
                                            off_Block = ""
                                            on_Block = ""
                                            for j in range(6, len(statement)):
                                                if statement[j] != ",":
                                                    off_Block += statement[j]
                                                else:
                                                    j += 1
                                                    break

                                            for k in range(j, len(statement)):
                                                on_Block += statement[k]

                                            temp_Track[block_Name].add_Switch(direction, off_Block, on_Block)

                                        case "G":
                                            for j in range(int(statement[1:])):
                                                temp_Track[block_Name].add_Gate()
                                        case "L":
                                            for j in range(int(statement[1:])):
                                                temp_Track[block_Name].add_Light()
                                        case "M":
                                            temp_Track[block_Name].max_Speed = int(statement[1:])
                                        case "P":
                                            temp_Track[block_Name].previous_Blocks.append(statement[1:])
                                        case "N":
                                            temp_Track[block_Name].next_Blocks.append(statement[1:])
                                        case ";":
                                            pass
                                        case _:
                                            raise Exception("Failed to intialize track: Invalid statement in block definition.")
                                except Exception as e:
                                    print(e)
                                    program.close()
                                    self.default_Track()
                                    return False

                                line = program.readline()
                                if len(line) == 0:
                                    print("Failed to initialize track: Reached EOF while parsing.")
                                    program.close()
                                    self.default_Track()
                                    return False
                                statement = self.ignore_Whitespace(line)
                        else:
                            if block_Statement != "":
                                #checks if the line is a comment and fails the function if it isnt
                                if block_Statement[0] != ";":
                                    print("Failed to initialize track: Invalid block definition statement.")
                                    program.close()
                                    self.default_Track()
                                    return False

                        line = program.readline()
                        if len(line) == 0:
                            print("Failed to initialize track: Reached EOF while parsing.")
                            program.close()
                            self.default_Track()
                            return False
                        block_Statement = self.ignore_Whitespace(line)


                    #if it makes it here a track has been successfully parsed
                    #continues iterating to ensure only one track is defined
                    success = True

                line = program.readline()

            program.close()


        #matches the track states to the newly created one if parsing is successful
        if success == True:
            self.track_Size = len(temp_Track)
            self.first_Block = b1
            self.final_Block = b2

            #copies temporary track into current and next
            self.current_Track_State = copy.deepcopy(temp_Track)
            self.next_Track_State = copy.deepcopy(temp_Track)

            #sets interpreter environement to the next track state
            self.interpreter.set_Environment(self.next_Track_State)

            #returns the program to the first line and calls the tokenizer
            tokenization_Success = self.interpreter.tokenize(self.filename)
            if tokenization_Success == True:
                self.start_PLC()

            self.start_Vitals()
        else:
            self.default_Track()

        return success

    #helper function to reset the track on track intitialization failure
    def default_Track(self):
        self.track_Size = 0
        self.first_Block = ""
        self.final_Block = ""
        self.current_Track_State.clear()
        self.next_Track_State.clear()
        self.statusBar().showMessage("No PLC program is loaded.")

    #returns the string line with whitespace and newlines removed
    def ignore_Whitespace(self, line):
        newLine = ""
        for i in range(len(line)):
            if line[i] != " " and line[i] != "\n" and line[i] != "\t":
                newLine += line[i]

        return newLine


#----------------------------------------------------------------
# HANDLES ALL MAIN WINDOW GUI ELEMENTS
#----------------------------------------------------------------
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


        self.plc_Label = QLabel("Logic: Stopped")
        self.plc_Label.setStyleSheet("color: red")
        self.plc_Label.setFont(QFont('Times', 12))
        self.plc_Label.setMaximumHeight(30)
        self.plc_Label.setMinimumHeight(30)

        self.vital_Label = QLabel("Vital: Stopped")
        self.vital_Label.setStyleSheet("color: red")
        self.vital_Label.setFont(QFont('Times', 12))
        self.vital_Label.setMaximumHeight(30)
        self.vital_Label.setMinimumHeight(30)

        tcLayout = QGridLayout()
        #add widgets to layout here
        tcLayout.addWidget(self.plc_Label, 0, 0)
        tcLayout.addWidget(self.vital_Label, 1, 0)
        tcLayout.addWidget(uploadButton, 2, 0)
        tcLayout.addWidget(editButton, 3, 0)
        tcLayout.addWidget(debugButton, 2, 1)
        tcLayout.addWidget(maintenanceButton, 3, 1)

        #applies the layout to the main widget and sets it as central
        mainWidget.setLayout(tcLayout)
        self.setCentralWidget(mainWidget)


#-----------------------------------------------------------------
# FUNCTIONS FOR LOADING SAVED/NEW PLC PROGRAMS
#-----------------------------------------------------------------
    #loads the saved PLC program if there is one
    #and displays loaded message
    def load_Saved_Program(self):
        #message for uploaded PLC program
        message = ""
        #walks up the file tree until ECE1140 directory is found
        destination = str(pathlib.Path().absolute())
        i = 0
        while destination[len(destination)-7:] != "ECE1140":
            i += 1
            destination = str(pathlib.Path(__file__).parents[i])
        #creates the expected text file based on the controller id
        destination += ("/plc_programs/plc_" + str(self.id) + ".txt")
        
        #checks if the file exists
        if os.path.isfile(destination):
            self.filename = destination
            message = self.extract_Name(self.filename) + " is loaded."
        else:
            message = "No PLC program is loaded."

        self.statusBar().setFont(QFont('Times', 13))
        self.statusBar().showMessage(message)


    #opens windows explorer to select and open a new file
    def upload_File(self):

        filename_Tuple = QFileDialog.getOpenFileName(None, 'Choose PLC Program', 'C:\\', "Text Files (*.txt)")

        #does nothing if the upload was canceled
        if filename_Tuple[0] != '':
            #creates a new name in the format plc_#.txt where # is the controller id
            new_Filename = "plc_" + str(self.id) + ".txt"
            #gets destination path by walking up the file tree until the ECE1140 directory is found
            destination = str(pathlib.Path().absolute())
            i = 0
            while destination[len(destination)-7:] != "ECE1140":
                i += 1
                destination = str(pathlib.Path(__file__).parents[i])

            destination += ('/plc_programs/' + new_Filename)
            if os.path.isfile(destination):
                os.remove(destination)

            self.filename = filename_Tuple[0]

            #saves the uploaded PLC program to local Program directory
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


#--------------------------------------------------------
# FUNCTIONS FOR OPENING OTHER MENUS
#--------------------------------------------------------
    #opens Debug menu
    def open_Debug(self):
        if self.debug is None:
            self.debug = DebugGUI(self.get_Track, self.set_Track, self.tick)
 
        self.in_Debug = True
        self.debug.show()

    #opens text editor
    def open_Editor(self):
        #ensures the editor doesn't try to open a file that isn't there
        if self.filename != '':
            #ensure the editor isn't already open
            if self.editor is None:

                #passes the build_Track function to allow the text editor
                #to refresh track on close
                self.editor = TextEditorGUI(self.build_Track, self.filename)
            self.editor.show()

    #opens maintenance menu
    def open_Maintenance(self):
        if self.maintenance is None:
            self.maintenance = MaintenanceGUI(self.get_Track)
        
        self.in_Maintenance = True
        self.maintenance.show()


#---------------------------------------------------------------
# TRACK STATE ACCESSORS/MUTATORS
# !RETURNS NONE ON ACCESS FAILURE
#---------------------------------------------------------------
    #used to pass the track state to the debug and maintenance guis
    def get_Track_Block(self, block=""):
        #refuses access to the track if it is locked
        return self.current_Track_State[block]

    def get_Track(self):
        return self.current_Track_State




#-----------------------------------------------------------------
# DEPRECATED, ONLY HERE TO PREVENT DEBUG MENU FROM BREAKING
#-----------------------------------------------------------------
    #this is due for a refactor
    #updates a value in current_Track_State
    def set_Track(self, block, var, val):

        d_block = decompose_block(block)

        match var:
            case "spd":
                self.current_Track_State[block].suggested_Speed = copy.copy(int(val))
            case "auth":
                self.current_Track_State[block].forward_Authority = copy.copy(int(val))
            case "occ":
                if val == 'Y':
                    val = True
                elif val == 'N':
                    val = False
                self.current_Track_State[block].occupied = copy.copy(val)
                signals.send_ctc_occupancy.emit(d_block[0], d_block[1], val)
            case "cls":
                if val == 'Y':
                    val = True
                elif val == 'N':
                    val = False
                self.current_Track_State[block].closed = copy.copy(val)
            case "fail":
                if val == 'Y':
                    val = True
                elif val == 'N':
                    val = False
                self.current_Track_State[block].failed = copy.copy(val)
                signals.send_ctc_failure.emit(d_block[0], d_block[1], val)
            case _:
                pass

#-----------------------------------------------------------------
# MAIN FUNCTION TO RUN LOGIC AND UPDATE TRACK CONTROLLER
#-----------------------------------------------------------------
    #main plc loop continuously generating outputs using logic
    #is run on another thread?
    @pyqtSlot()
    def tick(self):
        #immediately returns if vitals should not be run
        if self.run_Vitals == False:
            return 0

        #copies track state inputs to current_Track for comparison purposes
        for block in self.current_Track_State:
        #    self.next_Track_State[block].suggested_Speed = copy.copy(self.current_Track_State[block].suggested_Speed)
        #    self.current_Track_State[block].authority = copy.copy(self.next_Track_State[block].authority)
        #    self.current_Track_State[block].occupied = copy.copy(self.next_Track_State[block].occupied)
            self.current_Track_State[block].switches = copy.deepcopy(self.next_Track_State[block].switches)
        #    self.next_Track_State[block].failed = copy.copy(self.current_Track_State[block].failed)
        #    self.next_Track_State[block].closed = copy.copy(self.current_Track_State[block].closed)
            
        #runs logic
        if self.run_PLC == True:
            #try block to handle any undefined behavior in the plc program
            #for example a block name that the plc isnt connected to
            try:
                self.interpreter.execute()

            except Exception as e:
                print("FATAL PLC RUNTIME ERROR.")
                print(e)    
                print("Continuing to run vital logic.")
                
                self.stop_PLC()

        #TRAIN TRACKING LOGIC
        #iterate through trains to update train positions
        for train in self.tracker:
            blk1 = train[1]
            blk2 = train[2]
            dir = train[0]
            next_block = self.next_Track_State[blk1].get_Next_Block()
            prev_block = self.next_Track_State[blk1].get_Previous_Block()

            #train has moved since blk1 is no longer occupied
            if self.next_Track_State[blk1].occupied == False:
                train[1] = blk2
                train[2] = ""
                blk2 = ""
                blk1 = train[1]

                if blk1 != "":
                    next_block = self.next_Track_State[blk1].get_Next_Block()
                    prev_block = self.next_Track_State[blk1].get_Previous_Block()

            #checks to see if train has left the area and removes it from tracker if necessary
            if blk1 == "" and blk2 == "":
                self.tracker.remove(train)
                continue

            #checks to see if second occupied block must be updated
            if blk2 == "":
                #train moving forward, check next block
                if next_block != "END":
                    if dir == 1 and self.next_Track_State[next_block].occupied == True:
                        train[2] = next_block
                        blk2 = next_block
                #train moving backwards, check previous block
                if prev_block != "START":
                    if dir == 0 and self.next_Track_State[prev_block].occupied == True:
                        train[2] = prev_block
                        blk2 = prev_block


            #updates authority based on new train position
            if dir == 1 and prev_block != "START":
                self.next_Track_State[prev_block].authority = 0
                p_block = decompose_block(prev_block)
                signals.send_track_authority.emit(p_block[0], p_block[1], 0)
                
                p_prev_block = self.next_Track_State[prev_block].get_Previous_Block()
                if p_prev_block != "START":
                    p_p_block = decompose_block(p_prev_block)
                    signals.send_track_authority.emit(p_p_block[0], p_p_block[1], -1)
            elif dir == 0 and next_block != "END":
                self.next_Track_State[next_block].authority = 0
                n_block = decompose_block(next_block)
                signals.send_track_authority.emit(n_block[0], n_block[1], 0)

                n_next_block = self.next_Track_State[next_block].get_Next_Block()
                if n_next_block != "END":
                    n_n_block = decompose_block(n_next_block)
                    signals.send_track_authority.emit(n_n_block[0], n_n_block[1], -1)


        #runs vital safety logic then
        #copies newly generated outputs back to track state
        for block in self.current_Track_State:

            #speed safety check: commanded speed cannot exceed block maximum
            self.next_Track_State[block].commanded_Speed = copy.copy(self.next_Track_State[block].suggested_Speed)
            #if there is no commanded speed for a block, it is set to the maximum value
            if self.next_Track_State[block].commanded_Speed == 0:
                self.next_Track_State[block].commanded_Speed = copy.copy(self.next_Track_State[block].max_Speed)

            if self.next_Track_State[block].commanded_Speed > self.next_Track_State[block].max_Speed and self.next_Track_State[block].max_Speed != 0:
                self.next_Track_State[block].commanded_Speed = copy.copy(self.next_Track_State[block].max_Speed)


            #occupancy check for tracking purposes
            if self.next_Track_State[block].occupied == True:
                prev_block = self.next_Track_State[block].get_Previous_Block()
                next_block = self.next_Track_State[block].get_Next_Block()

                #attempts to find the train in the tracker associated with this occupancy
                train_found = False
                for train in self.tracker:
                    if train[1] == block or train[2] == block:
                        #train is still in an occupied block
                        train_found = True
                        break
                    
                #if a train isnt found and the block is an endpoint, a train start tracking a new train
                if next_block == "END" and train_found == False and block[len(block)-1:] != "0":
                    #creates a new train moving backwards through the blocks
                    new_train = [0, block, ""]
                    self.tracker.append(new_train)

                elif prev_block == "START" and train_found == False:
                    #creates a new train moving forwards through the blocks
                    new_train = [1, block, ""]
                    self.tracker.append(new_train)
                    

            #failures appear as occupations in the track controller
            if self.next_Track_State[block].failed == True:
                self.next_Track_State[block].occupied = True

            #failure/closure safety check: shuts down block if it has failed or is closed
            if self.next_Track_State[block].closed == True or self.next_Track_State[block].failed == True:
                self.next_Track_State[block].authority = 0
                for light in range(len(self.next_Track_State[block].lights)):
                    self.next_Track_State[block].set_Light(light, "RED")

            #switch interlock safety check: occupied blocks cannot change switch positions
            if self.next_Track_State[block].occupied == True:
                for switch in range(len(self.next_Track_State[block].switches)):
                    self.next_Track_State[block].switches[switch] = copy.copy(self.current_Track_State[block].switches[switch])


            #converts the block to line number form for other modules
            d_block = decompose_block(block)

            #signals only sent if there is a change of state
            if self.current_Track_State[block].commanded_Speed != self.next_Track_State[block].commanded_Speed:
                signals.send_track_speed.emit(d_block[0], d_block[1], self.next_Track_State[block].commanded_Speed)
                self.current_Track_State[block].commanded_Speed = copy.copy(self.next_Track_State[block].commanded_Speed)

            if self.current_Track_State[block].authority != self.next_Track_State[block].authority:
                signals.send_track_authority.emit(d_block[0], d_block[1], self.next_Track_State[block].authority)
                self.current_Track_State[block].authority = copy.copy(self.next_Track_State[block].authority)

                
            #probably shouldnt be able to run logic on switches when the block is closed
            if self.current_Track_State[block].closed == False:
                if self.current_Track_State[block].switches != []:
                    if self.current_Track_State[block].switches[0] != self.next_Track_State[block].switches[0]:
                        block_num = decompose_block(self.next_Track_State[block].get_switched_to())
                        signals.broadcast_switch.emit(d_block[0], d_block[1], block_num[1])
                        self.current_Track_State[block].switches[0] = copy.copy(self.next_Track_State[block].switches[0])

                        signals.send_track_authority.emit(block_num[0], block_num[1], -1)

                        #removes authority from blocks that are not being switched to if they are not already occupied
                        not_block = self.next_Track_State[block].get_not_switched_to()
                        n_blk = decompose_block(not_block)
                        if n_blk[1] != 0 and self.next_Track_State[not_block].occupied == False:
                            self.next_Track_State[not_block].authority = 0
                            signals.send_track_authority.emit(n_blk[0], n_blk[1], 0)
                            self.current_Track_State[not_block].authority = copy.copy(self.next_Track_State[not_block].authority)

            #check for light change and signal if so
            if self.current_Track_State[block].lights != []:
                if self.current_Track_State[block].lights[0] != self.next_Track_State[block].lights[0]:
                    signals.broadcast_light.emit(d_block[0], d_block[1], self.next_Track_State[block].light_To_Str())
                    self.current_Track_State[block].lights[0] = copy.copy(self.next_Track_State[block].lights[0])

            #check for gate change and signal if so
            if self.current_Track_State[block].gates != []:
                if self.current_Track_State[block].gates[0] != self.next_Track_State[block].gates[0]:
                    signals.broadcast_gate.emit(d_block[0], d_block[1], self.next_Track_State[block].gate_To_Str())
                    self.current_Track_State[block].gates[0] = copy.copy(self.next_Track_State[block].gates[0])


#-------------------------------------------------------------------
# FUNCTIONS THAT START/STOP CONTROLLER FUNCTIONALITY + UPDATE UI
#-------------------------------------------------------------------
    def start_PLC(self):
        self.run_PLC = True
        self.plc_Label.setText("Logic: Running")
        self.plc_Label.setStyleSheet("color: green")

    def stop_PLC(self):
        self.run_PLC = False
        self.plc_Label.setText("Logic: Stopped")
        self.plc_Label.setStyleSheet("color: red")

    def start_Vitals(self):
        self.run_Vitals = True
        self.vital_Label.setText("Vital: Running")
        self.vital_Label.setStyleSheet("color: green")

    def stop_Vitals(self):
        self.run_Vitals = False
        self.vital_Label.setText("Vital: Stopped")
        self.vital_Label.setStyleSheet("color: red")


#-------------------------------------------------------
# Signal handlers
#-------------------------------------------------------
    def setup_signals(self):
        signals.tc_update.connect(self.tick)
        signals.send_tc_authority.connect(self.handle_authority)
        signals.send_tc_speed.connect(self.handle_suggested_speed)
        signals.send_tc_maintenance.connect(self.handle_maintenance)
        signals.set_tc_switch.connect(self.handle_manual_switch)
        signals.send_tc_occupancy.connect(self.handle_occupancy)
        signals.send_tc_failure.connect(self.handle_failure)

    @pyqtSlot(str, int)
    def handle_authority(self, block, auth):
        for bl in self.current_Track_State:
            if block == bl:
                self.next_Track_State[bl].authority = auth
                break

    @pyqtSlot(str, int)
    def handle_suggested_speed(self, block, s_speed):
        for bl in self.current_Track_State:
            if block == bl:
                self.next_Track_State[bl].suggested_Speed = s_speed
                break

    @pyqtSlot(str, int)
    def handle_maintenance(self, block, maintenance):
        for bl in self.current_Track_State:
            if block == bl:
                self.next_Track_State[bl].closed = maintenance
                break

    @pyqtSlot(str, str)
    def handle_manual_switch(self, block, next_block):
        for bl in self.current_Track_State:
            if block == bl:
                if self.next_Track_State[bl].closed == True and self.next_Track_State[bl].switches != []:
                    if self.next_Track_State[bl].switch_to == TO_NEXT:
                        if self.next_Track_State[bl].next_blocks[0] == next_block:
                            self.next_Track_State[bl].switch[0] = False
                        elif self.next_Track_State[bl].next_blocks[1] == next_block:
                            self.next_Track_State[bl].switch[0] = True
                        else:
                            pass
                    elif self.next_Track_State[bl].switch_to == TO_PREV:
                        if self.next_Track_State[bl].next_blocks[0] == next_block:
                            self.next_Track_State[bl].switch[0] = False
                        elif self.next_Track_State[bl].next_blocks[1] == next_block:
                            self.next_Track_State[bl].switch[0] = True
                        else:
                            pass
            break

    @pyqtSlot(str, int)
    def handle_occupancy(self, block, occ):
        for bl in self.current_Track_State:
            if block == bl:
                #d_block = decompose_block(bl)

                self.next_Track_State[bl].occupied = copy.copy(occ)
                #signals.send_ctc_occupancy.emit(d_block[0], d_block[1], occ)
                break

    @pyqtSlot(str, int)
    def handle_failure(self, block, fail):
        for bl in self.current_Track_State:
            if block == bl:
                self.next_Track_State[bl].failed = fail
                break




#main for the whole Track Controller, simply creates an instance of TrackController
if __name__ == '__main__':
    #creates the application for Qt
    track_Controller_App = QApplication([])
    
    track_Controller = TrackController()
    #runs the app
    sys.exit(track_Controller_App.exec())

