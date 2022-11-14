import sys
import shutil
import pathlib
import os
import copy
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QGridLayout, QPushButton, QWidget, QLabel
from PyQt5.QtGui import QFont
from TrackController.Block import Block
import TrackController.TCGUI.TextEditorGUI, TrackController.TCGUI.DebugGUI
import TrackController.TCGUI.MaintenanceGUI, TrackController.TCGUI.ModifyGUI
from TrackController.PLCInterpreter.PLCInterpreter import PLCInterpreter



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
        #semaphore for track state access
        self.track_Lock = False
        #array for tracking which blocks were previously occupied
        #used for track failure checking
        self.previous_Occupations = []
        #tracks first and final blocks. speeds up safety logic
        self.first_Block = ""
        self.final_Block = ""
        #interpreter
        self.interpreter = PLCInterpreter()
        

        super().__init__()


        self.setup_Main_Window()
        self.load_Saved_Program()
        self.build_Track()

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
            if line[i] != " " and line[i] != "\n":
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
            self.debug = TCGUI.DebugGUI.DebugGUI(self.get_Track, self.set_Track, self.tick)
 
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
                self.editor = TCGUI.TextEditorGUI.TextEditorGUI(self.build_Track, self.filename)
            self.editor.show()

    #opens maintenance menu
    def open_Maintenance(self):
        if self.maintenance is None:
            self.maintenance = TCGUI.MaintenanceGUI.MaintenanceGUI(self.get_Track)
        
        self.in_Maintenance = True
        self.maintenance.show()


#---------------------------------------------------------------
# TRACK STATE ACCESSORS/MUTATORS
# !RETURNS NONE ON ACCESS FAILURE
#---------------------------------------------------------------
    #used to pass the track state to the debug and maintenance guis
    def get_Track_Block(self, block=""):
        #refuses access to the track if it is locked
        if self.track_Lock == False and block != "":
            return self.current_Track_State[block]
        else:
            return None

    def get_Track(self):
        if self.track_Lock == False:
            return self.current_Track_State
        else:
            return None

#-----------------------------------------------------------------
# DEPRECATED, ONLY HERE TO PREVENT DEBUG MENU FROM BREAKING
#-----------------------------------------------------------------
    #this is due for a refactor
    #updates a value in current_Track_State
    def set_Track(self, block, var, val):
        match var:
            case "spd":
                self.current_Track_State[block].suggested_Speed = copy.copy(val)
            case "auth":
                self.current_Track_State[block].forward_Authority = copy.copy(val)
            case "occ":
                if val == 'Y':
                    val = True
                elif val == 'N':
                    val = False
                self.current_Track_State[block].occupied = copy.copy(val)
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
            case _:
                pass

#-----------------------------------------------------------------
# MAIN FUNCTION TO RUN LOGIC AND UPDATE TRACK CONTROLLER
#-----------------------------------------------------------------
    #main plc loop continuously generating outputs using logic
    #is run on another thread?
    def tick(self):

        if self.run_Vitals == True:

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
                    self.interpreter.execute()

                except Exception as e:
                    print("FATAL PLC RUNTIME ERROR.")
                    print(e)    
                    print("Continuing to run vital logic.")
                
                    self.stop_PLC()


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
                #cannot determine if the first or last block has failed
                #since that is identical to a train entering the zone as far as the track controller can tell
                if self.next_Track_State[block].occupied == True:

                    #gets the next 2 and previous 2 blocks from an occupied one
                    #if the previous is the start or the next is the end, a train has entered the zone
                    previous = self.next_Track_State[block].get_Previous_Block()
                    if previous != "START":
                        previous_Second = self.next_Track_State[previous].get_Previous_Block()
                    else:
                        if previous not in self.previous_Occupations:
                            self.previous_Occupations.append(previous)
                    next_Bl = self.next_Track_State[block].get_Next_Block()
                    if next_Bl != "END":
                        next_Bl_Second = self.next_Track_State[next_Bl].get_Next_Block()
                    else:
                        if next_Bl not in self.previous_Occupations:
                            self.previous_Occupation.append(next_Bl)

                    #updates previously occupied blocks and checks for track failure
                    #if a currently occupied block does not have a previous in the list it has failed
                    previous_Block_Found = False
                    for prev_Occ in self.previous_Occupations:

                        #if a previous occupation is adjacent then we are all good
                        if prev_Occ == previous or prev_Occ == next_Bl:
                            previous_Block_Found = True
                            break

                        #if a previous occupation is currently occupied then it is no longer previously occupied
                        #this situation only really occurs and is handled due to block update order
                        elif prev_Occ == block:
                            self.previous_Occupations.remove(prev_Occ)
                            previous_Block_Found = True
                            break

                        #case for a train that has moved forward a space
                        #previously occupied must also move forward by one
                        elif prev_Occ == previous_Second and self.check_Occupancy(previous) == False:
                            self.previous_Occupations.remove(prev_Occ)
                            if previous not in self.previous_Occupations:
                                self.previous_Occupations.append(previous)
                            previous_Block_Found = True
                            break

                        #case for a train that has move backward a space
                        #previously occupied must also move backward by one
                        elif prev_Occ == next_Bl_Second and self.check_Occupancy(next_Bl) == False:
                            self.previous_Occupations.remove(prev_Occ)
                            if next_Bl not in self.previous_Occupations:
                                self.previous_Occupations.append(next_Bl)
                            previous_Block_Found = True
                            break
                        else:
                            pass

                    
                    if previous_Block_Found == False:
                        self.next_Track_State[block].failed = True

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


                #copies next track back to current track
                self.current_Track_State[block].commanded_Speed = copy.copy(self.next_Track_State[block].commanded_Speed)

                self.current_Track_State[block].authority = copy.copy(self.next_Track_State[block].authority)
                
                for switch in range(len(self.current_Track_State[block].switches)):
                    self.current_Track_State[block].switches[switch] = copy.copy(self.next_Track_State[block].switches[switch])
            
                for light in range(len(self.current_Track_State[block].lights)):
                    self.current_Track_State[block].lights[light] = copy.copy(self.next_Track_State[block].lights[light])

                for gate in range(len(self.current_Track_State[block].gates)):
                    self.current_Track_State[block].gates[gate] = copy.copy(self.next_Track_State[block].gates[gate])

            #longest track controller update period while ensured to properly detect trains is 1.6 seconds

            #goofy way to clean up previous occupancies once a train has left the track controller range
            #basically checks both the train's last position +1 and -1 are in the list
            #only works due to the jankyness of my previous position tracking system above
            start_Exists = False
            start_Plus2 = False
            end_Exists = False
            end_Minus2 = False
            for occ in self.previous_Occupations:
                if occ == "START":
                    start_Exists = True
                elif occ == "END":
                    end_Exists = True
                elif occ == self.next_Track_State[self.first_Block].get_Next_Block():
                    start_Plus2 = True
                elif occ == self.next_Track_State[self.final_Block].get_Previous_Block():
                    end_Minus2 = True
                
            if start_Exists == True and start_Plus2 == True and self.next_Track_State[self.first_Block].occupied == False:
                self.previous_Occupations.remove("START")
                self.previous_Occupations.remove(self.next_Track_State[self.first_Block].get_Next_Block())
            elif end_Exists == True and end_Minus2 == True and self.next_Track_State[self.final_Block].occupied == False:
                self.previous_Occupations.remove("END")
                self.previous_Occupations.remove(self.next_Track_State[self.final_Block].get_Previous_Block())


            #train padding check: creates a safety zone with all recently occupied blocks
            #this is done last so that previous occupancies have a chance to update
            for bl in self.previous_Occupations:
                if bl != "START" and bl != "END":
                    self.next_Track_State[bl].authority = 0

            #unlocks track state
            self.track_Lock = False

    #helper function to handle situations where a train is in two blocks at once
    #used in safety checks
    def check_Occupancy(self, block):
        val = True
        if block == "START" or block == "END":
            val = False
        else:
            val = self.next_Track_State[block].occupied

        return val


    #helper to update track state from ctc and track model
    def update_track(self):
        #stupid workaround to use these as pointers
        temp_speed = [1]
        temp_authority = [1]

        for block in self.current_Track_State:
            #use signal to call CTC get speed and authority
            #passing temp_speed[0] & temp_authority[0] to use a psuedo pointers
            self.current_Track_State[block].suggested_Speed = copy.copy(temp_speed[0])
            self.current_Track_State[block].authority = copy.copy(temp_authority[0])


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


#main for the whole Track Controller, simply creates an instance of TrackController
if __name__ == '__main__':
    #creates the application for Qt
    track_Controller_App = QApplication([])
    
    track_Controller = TrackController()
    #runs the app
    sys.exit(track_Controller_App.exec())

