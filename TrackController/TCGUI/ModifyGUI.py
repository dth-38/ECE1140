from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QComboBox
from PyQt5.QtGui import QFont
from Block import Block

class ModifyGUI(QWidget):
    
    def __init__(self, track, update, leave_Modify):
        #function for modifying the track in TrackController
        self.track = track
        self.drawn = False
        self.update_Track = update
        self.leave_Modify = leave_Modify

        super().__init__()

        #sets window properties
        self.setGeometry(580, 80, 500, 400)
        self.setWindowTitle('Track Modifier')


        self.grid = QGridLayout()
        self.setup_Interaction()
        self.setLayout(self.grid)

    #sets up widgets for interacting with blocks
    def setup_Interaction(self):
        #block name input
        self.add_Block_Name_Line = QLineEdit()
        self.add_Block_Name_Line.setMaximumWidth(50)
        self.grid.addWidget(self.add_Block_Name_Line, 0, 0)
        
        self.add_Block_Name_Sect = QLineEdit()
        self.add_Block_Name_Sect.setMaxLength(1)
        self.add_Block_Name_Sect.setMaximumWidth(30)
        self.grid.addWidget(self.add_Block_Name_Sect, 0, 1)

        self.add_Block_Name_Num = QLineEdit()
        self.add_Block_Name_Num.setMaxLength(2)
        self.add_Block_Name_Num.setMaximumWidth(40)
        self.grid.addWidget(self.add_Block_Name_Num, 0, 2)

        #add block button
        self.add_Block_Button = QPushButton()
        self.add_Block_Button.setText('ADD BLOCK')
        self.add_Block_Button.setFont(QFont('Times', 16))
        self.add_Block_Button.setMinimumWidth(80)
        self.add_Block_Button.setMinimumHeight(50)
        self.add_Block_Button.clicked.connect(self.add_Block)
        self.grid.addWidget(self.add_Block_Button, 0, 3)


        #Block label + dropdown
        self.block_Label = QLabel('Block:')
        self.block_Label.setFont(QFont('Times', 14))
        self.grid.addWidget(self.block_Label, 1, 0)
    
        self.block_Drop = QComboBox()
        self.block_Drop.setEditable(True)
        self.block_Drop.setMinimumWidth(70)
        self.block_Drop.currentTextChanged.connect(self.update_Info)
        self.grid.addWidget(self.block_Drop, 1, 1)

        #remove block button
        self.remove_Block_Button = QPushButton()
        self.remove_Block_Button.setText('REMOVE BLOCK')
        self.remove_Block_Button.setFont(QFont('Times', 14))
        self.remove_Block_Button.clicked.connect(self.remove_Block)
        self.grid.addWidget(self.remove_Block_Button, 1, 3)

        #Switch amount and add/subtract
        self.switch_Num = QLabel()
        self.switch_Num.setText('Switches:')
        self.switch_Num.setFont(QFont('Times', 12))
        self.grid.addWidget(self.switch_Num, 2, 0)

        self.switch_Add = QPushButton()
        self.switch_Add.setText('ADD')
        self.switch_Add.setFont(QFont('Times', 12))
        self.switch_Add.clicked.connect(lambda: self.mod_Switch(1))
        self.grid.addWidget(self.switch_Add, 2, 2)

        self.switch_Remove = QPushButton()
        self.switch_Remove.setText('REMOVE')
        self.switch_Remove.setFont(QFont('Times', 12))
        self.switch_Remove.clicked.connect(lambda: self.mod_Switch(0))
        self.grid.addWidget(self.switch_Remove, 2, 3)

        #Light amount and add/subtract
        self.light_Num = QLabel()
        self.light_Num.setText('Lights:')
        self.light_Num.setFont(QFont('Times', 12))
        self.grid.addWidget(self.light_Num, 3, 0)

        self.light_Add = QPushButton()
        self.light_Add.setText('ADD')
        self.light_Add.setFont(QFont('Times', 12))
        self.light_Add.clicked.connect(lambda: self.mod_Light(1))
        self.grid.addWidget(self.light_Add, 3, 2)
        
        self.light_Remove = QPushButton()
        self.light_Remove.setText('REMOVE')
        self.light_Remove.setFont(QFont('Times', 12))
        self.light_Remove.clicked.connect(lambda: self.mod_Light(0))
        self.grid.addWidget(self.light_Remove, 3, 3)

        #Gate amount and add/subtract
        self.gate_Num = QLabel()
        self.gate_Num.setText('Gates:')
        self.gate_Num.setFont(QFont('Times', 12))
        self.grid.addWidget(self.gate_Num, 4, 0)

        self.gate_Add = QPushButton()
        self.gate_Add.setText('ADD')
        self.gate_Add.setFont(QFont('Times', 12))
        self.gate_Add.clicked.connect(lambda: self.mod_Gate(1))
        self.grid.addWidget(self.gate_Add, 4, 2)
        
        self.gate_Remove = QPushButton()
        self.gate_Remove.setText('REMOVE')
        self.gate_Remove.setFont(QFont('Times', 12))
        self.gate_Remove.clicked.connect(lambda: self.mod_Gate(0))
        self.grid.addWidget(self.gate_Remove, 4, 3)
        
        self.update_Blocks()
        self.update_Info()


    #adds or removes a switch based on mod then updates amount
    def mod_Switch(self, mod):
        if mod == 1:
            self.track()[self.block_Drop.currentText()].add_Switch()
        else:
            self.track()[self.block_Drop.currentText()].remove_Switch()

        self.switch_Num.setText('Switches: ' + str(len(self.track()[self.block_Drop.currentText()].switches)))


    #adds or removes a gate based on mod then updates amount
    def mod_Gate(self, mod):
        if mod == 1:
            self.track()[self.block_Drop.currentText()].add_Gate()
        else:
            self.track()[self.block_Drop.currentText()].remove_Gate()
    
        self.gate_Num.setText('Gates: ' + str(len(self.track()[self.block_Drop.currentText()].gates)))


    #adds or removes a light based on mod then updates amount
    def mod_Light(self, mod):
        if mod == 1:
            self.track()[self.block_Drop.currentText()].add_Light()
        else:
            self.track()[self.block_Drop.currentText()].remove_Light()

        self.light_Num.setText('Lights: ' + str(len(self.track()[self.block_Drop.currentText()].lights)))


    #updates switch, light, and gate amounts
    def update_Info(self):
        if self.block_Drop.currentText() != '':
            self.switch_Num.setText('Switches: ' + str(len(self.track()[self.block_Drop.currentText()].switches)))
            self.gate_Num.setText('Gates: ' + str(len(self.track()[self.block_Drop.currentText()].gates)))
            self.light_Num.setText('Lights: ' + str(len(self.track()[self.block_Drop.currentText()].lights)))

        

    #refreshes the list of blocks in the dropdown
    #hides interactivity if track has no blocks
    def update_Blocks(self):
        self.block_Drop.blockSignals(True)
        self.block_Drop.clear()

        if self.track() == {}:
            self.block_Drop.addItem("")
            self.switch_Add.blockSignals(True)
            self.switch_Remove.blockSignals(True)
            self.remove_Block_Button.blockSignals(True)
            self.block_Drop.blockSignals(True)
            self.light_Add.blockSignals(True)
            self.light_Remove.blockSignals(True)
            self.gate_Add.blockSignals(True)
            self.gate_Remove.blockSignals(True)
        else:
            self.block_Drop.addItems(self.track().keys())
            self.remove_Block_Button.blockSignals(False)
            self.block_Drop.blockSignals(False)
            self.switch_Add.blockSignals(False)
            self.switch_Remove.blockSignals(False)
            self.light_Add.blockSignals(False)
            self.light_Remove.blockSignals(False)
            self.gate_Add.blockSignals(False)
            self.gate_Remove.blockSignals(False)

        self.block_Drop.blockSignals(False)


    #attempts to add a block to the track
    #based on the lineedits in the menu
    def add_Block(self):
        #generates block name from line/section/number
        name = self.add_Block_Name_Line.text() + "_"
        name += self.add_Block_Name_Sect.text()
        name += "_"
        name += self.add_Block_Name_Num.text()

        #checks that it doesnt already exist
        found = False
        if self.track() != {}:
            for key in self.track().keys():
                if key == name:
                    found = True

            if found == False:
                self.track()[name] = Block()
        else:     
            self.track()[name] = Block()

        #calls update_Info to ensure info on screen is up to date
        self.update_Blocks()
        self.update_Track()

    #removes a block selected from the drop down from the track
    def remove_Block(self):
        if self.block_Drop.currentText() != '':
            self.track().pop(self.block_Drop.currentText())
            self.update_Blocks()
            self.update_Info()
            self.update_Track()

    
    def closeEvent(self, event):
        self.leave_Modify()
        self.hide()
