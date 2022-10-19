import sys
import shutil
import pathlib
import os
import copy
import time
import threading
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
from Block import Block
import TCGUI.TextEditorGUI, TCGUI.DebugGUI, TCGUI.MaintenanceGUI, TCGUI.ModifyGUI
from Token import Token


class TrackController(QMainWindow):

    def __init__(self, tc_ID=0):
        self.current_Track_State = {}
        self.next_Track_State = {}
        self.id = tc_ID
        self.filename = ""
        self.program = 0
        self.in_Debug = False
        self.in_Maintenance = False
        self.in_Modify = False
        self.run_PLC = False
        self.run_Vital = True
        self.editor = None
        self.debug = None
        self.maintenance = None
        self.modify = None
        self.track_Lock = False
        self.target_Time = 0.5
        self.jump_Table = {}
        self.logic = []
        self.logic_Thread = 0
        

        super().__init__()

        self.build_Track()

        self.load_Saved_Program()

        self.setup_Main_Window()

        self.logic_Thread = threading.Thread(target=self.run_Logic)
        self.logic_Thread.start()

        self.show()



    def build_Track(self):
        #TODO:
        #probe track model for amount of blocks
        #generate blocks and add to trackState
        #probe track model for switches, gates, lights, possibly state of other block vars
        
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

        modifyButton = QPushButton('Modify Track', self)
        modifyButton.clicked.connect(self.open_Modify)
        modifyButton.setMinimumHeight(60)
        modifyButton.setFont(buttonFont)


        tcLayout = QGridLayout()
        #add widgets to layout here
        tcLayout.addWidget(modifyButton, 0, 0)
        tcLayout.addWidget(uploadButton, 1, 0)
        tcLayout.addWidget(editButton, 2, 0)
        tcLayout.addWidget(debugButton, 1, 1)
        tcLayout.addWidget(maintenanceButton, 2, 1)

        #applies the layout to the main widget and sets it as central
        mainWidget.setLayout(tcLayout)
        self.setCentralWidget(mainWidget)


    #opens windows explorer to select and open a new file
    def upload_File(self):
        #kills thread running run_Logic
        self.run_Vital = False
        self.run_PLC = False
        self.logic_Thread.join()

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

            #opens new file in editor if editor has been opened
            if self.editor is not None:
                self.editor.set_Filepath(self.filename)
                self.editor.open_File()

            #restarts thread running run_Logic
            self.logic_Thread = threading.Thread(target=self.run_Logic)



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
            self.maintenance = TCGUI.MaintenanceGUI.MaintenanceGUI(self.get_Track, self.leave_Maintenance)

        if self.in_Modify is False:
            self.in_Maintenance = True
            self.maintenance.show()

    def open_Modify(self):
        if self.modify is None:
            self.modify = TCGUI.ModifyGUI.ModifyGUI(self.get_Next_Track, self.update_Sync_Track, self.leave_Modify)

        if self.in_Debug is False and self.in_Maintenance is False:
            self.in_Modify = True
            self.modify.show()

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
    #should be run on another thread
    def run_Logic(self):
        if self.filename != "":
            #opens plc file
            logic_File = open(self.filename, 'r')

            t1 = time.perf_counter()
            self.run_PLC = self.tokenize(logic_File)
            tdiff = time.perf_counter() - t1
            print("Time to tokenize: " + str(tdiff))
            logic_File.close()

            self.run_Vital = self.run_PLC
        else:
            self.run_PLC = False


        while self.run_Vital:
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
            if self.run_PLC:
                pass

                

                #god help me
            

            #maybe put some safety logic here idk

            #locks track state before updating
            self.track_Lock = True
            #copies newly generated outputs back to track state
            for block in self.current_Track_State:
                self.current_Track_State.commanded_Authority = copy.copy(self.next_Track_State[block].commanded_Authority)
                
                for switch in self.current_Track_State[block].switches:
                    self.current_Track_State[block].switches[switch] = copy.copy(self.next_Track_State[block].switches[switch])
                
                for light in self.current_Track_State[block].lights:
                    self.current_Track_State[block].lights[light] = copy.copy(self.next_Track_State[block].lights[light])

                for gate in self.current_Track_State[block].gates:
                    self.current_Track_State[block].gates[gate] = copy.copy(self.next_Track_State[block].gates[gate])
            #unlocks track state
            self.track_Lock = False

            #calculates the amount of time to sleep to achieve target fps
            time_Diff = time.perf_counter() - start_Time
            wait_Time = self.target_Time - time_Diff
            time.sleep(wait_Time)


    #tokenizes plc logic to make runtime interpretation faster
    def tokenize(self, file):
        logic_Count = 0
        line_Count = 1

        #gets the first line
        line = file.readline()

        #continues until the end of the file
        while line:
            add_Logic = True
            comm = ""
            i = 0
            j = 0

            #ignores leading whitespace
            while line[i] == " ":
                i += 1

            #gets the command by parsing until a space is found
            for j in range(i, len(line)):
                if line[j] != " ":
                    comm += line[j]
                else:
                    i = j
                    break

            #matches the command string and generates token
            token = Token()
            var1 = ""
            var2 = ""
            var3 = ""

            j += 1
            #this switch block is ~350 lines, im sorry
            match comm:
                #adds a jump point to the table
                case "SET":
                    label = ""

                    #iterates through the current line starting from the end of the command
                    for i in range(j, len(line)):
                        #checks for the end of the label
                        if line[i] != " " and line[i] != "\n":
                            label += line[i]
                        else:
                            break

                    #adds position in logic array to dictionary with label as key
                    self.jump_Table[label] = logic_Count
                    add_Logic = False

                #command num = 2
                #format "AND var1, var2, var3"
                case "AND":

                    #iterates until a comma is found
                    for i in range(j+1, len(line)):
                        if line[i] != ",":
                            var1 += line[i]
                        else:
                            break

                    i += 1
                    #ignores whitespace
                    for j in range(i, len(line)):
                        if line[j] != " ":
                            break

                    #gets var2
                    for i in range(j, len(line)):
                        if line[i] != ",":
                            var2 += line[i]
                        else:
                            break

                    i += 1
                    #ignores whitespace
                    for j in range(i, len(line)):
                        if line[j] != " ":
                            break

                    #gets var3
                    for i in range(j, len(line)):
                        if line[i] != " " and line[i] != "\n":
                            var3 += line[i]
                        else:
                            break

                    i += 1
                    #ignores trailing whitespace and checks for improper formatting
                    for j in range(i, len(line)):
                        if line[j] != " " and line[j] != "\n":
                            print("\nTokenizing failed: Invalid formatting in line " + str(line_Count))
                            return False

                    #checks that 3 operands were found
                    if var1 == "" or var2 == "" or var3 == "":
                        print("\nTokenizing failed: Incorrect number of arguments in line " + str(line_Count))
                        return False

                    #creates token
                    token.set_Opcode(2)

                    if not token.set_Var(1, var1) or not token.set_Var(2, var2) or not token.set_Var(3, var3):
                        return False

                #command num = 3
                #format "OR var1, var2, var3"
                case "OR":

                    #iterates until a comma is found
                    for i in range(j, len(line)):
                        if line[i] != ",":
                            var1 += line[i]
                        else:
                            break

                    i += 1
                    #ignores whitespace
                    for j in range(i, len(line)):
                        if line[j] != " ":
                            break

                    #gets var2
                    for i in range(j, len(line)):
                        if line[i] != ",":
                            var2 += line[i]
                        else:
                            break

                    i += 1
                    #ignores whitespace
                    for j in range(i, len(line)):
                        if line[j] != " ":
                            break

                    #gets var3
                    for i in range(j, len(line)):
                        if line[i] != " " and line[i] != "\n":
                            var3 += line[i]
                        else:
                            break

                    i += 1
                    #ignores trailing whitespace and checks for improper formatting
                    for j in range(i, len(line)):
                        if line[j] != " " and line[j] != "\n":
                            print("\nTokenizing failed: Invalid formatting in line " + str(line_Count))
                            return False

                    #checks that 3 operands were found
                    if var1 == "" or var2 == "" or var3 == "":
                        print("\nTokenizing failed: Incorrect number of arguments in line " + str(line_Count))
                        return False

                    #creates token
                    token.set_Opcode(3)

                    if not token.set_Var(1, var1) or not token.set_Var(2, var2) or not token.set_Var(3, var3):
                        return False

                #command num = 0
                #format "EQ var1, var2"
                case "EQ":

                    #iterates until a comma is found
                    for i in range(j, len(line)):
                        if line[i] != ",":
                            var1 += line[i]
                        else:
                            break

                    i += 1
                    #ignores whitespace
                    for j in range(i, len(line)):
                        if line[j] != " ":
                            break

                    #gets var2
                    for i in range(j, len(line)):
                        if line[i] != " " and line[i] != "\n":
                            var2 += line[i]
                        else:
                            break

                    i += 1
                    #ignores trailing whitespace and checks for improper formatting
                    for j in range(i, len(line)):
                        if line[j] != " " and line[j] != "\n":
                            print("\nTokenizing failed: Invalid formatting in line " + str(line_Count))
                            return False

                    #checks that 2 operands were found
                    if var1 == "" or var2 == "":
                        print("\nTokenizing failed: Incorrect number of arguments in line " + str(line_Count))
                        return False

                    #creates token
                    token.set_Opcode(0)

                    if (not token.set_Var(1, var1)) or (not token.set_Var(2, var2)):
                        print(var2 + "a")
                        return False

                    
                #command num = 1
                #format "NOT var1, var2"
                case "NOT":
                    
                    #iterates until a comma is found
                    for i in range(j, len(line)):
                        if line[i] != ",":
                            var1 += line[i]
                        else:
                            break

                    i += 1
                    #ignores whitespace
                    for j in range(i, len(line)):
                        if line[j] != " ":
                            break

                    #gets var2
                    for i in range(j, len(line)):
                        if line[i] != " " and line[i] != "\n":
                            var2 += line[i]
                        else:
                            break

                    i += 1
                    #ignores trailing whitespace and checks for improper formatting
                    for j in range(i, len(line)):
                        if line[j] != " " and line[j] != "\n":
                            print("\nTokenizing failed: Invalid formatting in line " + str(line_Count))
                            return False

                    #checks that 3 operands were found
                    if var1 == "" or var2 == "":
                        print("\nTokenizing failed: Incorrect number of arguments in line " + str(line_Count))
                        return False

                    #creates token
                    token.set_Opcode(1)

                    if not token.set_Var(1, var1) or not token.set_Var(2, var2):
                        return False

                #command num = 4
                #format "B label"
                case "B":

                    #iterates until a space or endline to get the label to jump to
                    for i in range(j, len(line)):
                        if line[i] != " " and line[i] != "\n":
                            var1 += line[i]
                        else:
                            break
                    
                    #ignore trailing whitespace
                    for j in range(i+1, len(line)):
                        #if there is anything other than whitespace, the line is invalid
                        if line[j] != " " and line[j] != "\n":
                            print("\nTokenizing failed: Invalid formatting at line " + str(line_Count))
                            return False

                    #creates token
                    token.set_Opcode(4)
                    token.var1 = [label]
                    token.var1_Type = "label"

                #command num = 5
                #format "BEQ label, var1, var2"
                case "BEQ":

                    #iterates until a comma is found
                    for i in range(j, len(line)):
                        if line[i] != ",":
                            var1 += line[i]
                        else:
                            break

                    i += 1
                    #ignores whitespace
                    for j in range(i, len(line)):
                        if line[j] != " ":
                            break

                    #gets var2
                    for i in range(j, len(line)):
                        if line[i] != ",":
                            var2 += line[i]
                        else:
                            break

                    i += 1
                    #ignores whitespace
                    for j in range(i, len(line)):
                        if line[j] != " ":
                            break

                    #gets var3
                    for i in range(j, len(line)):
                        if line[i] != " " and line[i] != "\n":
                            var3 += line[i]
                        else:
                            break

                    i += 1
                    #ignores trailing whitespace and checks for improper formatting
                    for j in range(i, len(line)):
                        if line[j] != " " and line[j] != "\n":
                            print("\nTokenizing failed: Invalid formatting in line " + str(line_Count))
                            return False

                    #checks that 3 operands were found
                    if var1 == "" or var2 == "" or var3 == "":
                        print("\nTokenizing failed: Incorrect number of arguments in line " + str(line_Count))
                        return False

                    #creates token
                    token.set_Opcode(5)
                    token.var1 = [var1]
                    token.var1_Type = "label"

                    if not token.set_Var(2, var2) or not token.set_Var(3, var3):
                        return False
                    

                #command num = 6
                #format "BNE label, var1, var2"
                case "BNE":

                    #iterates until a comma is found
                    for i in range(j, len(line)):
                        if line[i] != ",":
                            var1 += line[i]
                        else:
                            break

                    i += 1
                    #ignores whitespace
                    for j in range(i, len(line)):
                        if line[j] != " ":
                            break

                    #gets var2
                    for i in range(j, len(line)):
                        if line[i] != ",":
                            var2 += line[i]
                        else:
                            break

                    i += 1
                    #ignores whitespace
                    for j in range(i, len(line)):
                        if line[j] != " ":
                            break

                    #gets var3
                    for i in range(j, len(line)):
                        if line[i] != " " and line[i] != "\n":
                            var3 += line[i]
                        else:
                            break

                    i += 1
                    #ignores trailing whitespace and checks for improper formatting
                    for j in range(i, len(line)):
                        if line[j] != " " and line[j] != "\n":
                            print("\nTokenizing failed: Invalid formatting in line " + str(line_Count))
                            return False

                    #checks that 3 operands were found
                    if var1 == "" or var2 == "" or var3 == "":
                        print("\nTokenizing failed: Incorrect number of arguments in line " + str(line_Count))
                        return False

                    #creates token
                    token.set_Opcode(6)
                    token.var1 = [var1]
                    token.var1_Type = "label"

                    if not token.set_Var(2, var2) or not token.set_Var(3, var3):
                        return False

                case _:
                    #handles comments, invalid commands
                    if comm[0] != ";" and comm != "\n":
                        print("\nTokenizing failed: Invalid command at line " + str(line_Count))
                        return False
                    else:
                        add_Logic = False

            #checks if the token was generated (since SET command does not generate logic)
            if add_Logic:

                #adds the new token to the logic array and increments the count
                self.logic.append(token)
                logic_Count += 1

            #gets the next line
            line = file.readline()
            line_Count += 1

        #returns False if tokenizing failed at any point
        #returns True if tokenizing was successful
        return True
        


    #function for reenabling logic after editing a file
    def enable_PLC(self):
        self.run_PLC = True

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


#main for the whole Track Controller, simply creates an instance of TrackController
if __name__ == '__main__':
    #creates the application for Qt
    track_Controller_App = QApplication([])
    
    track_Controller = TrackController()
    #runs the app
    sys.exit(track_Controller_App.exec())

