from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtWidgets import QComboBox, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QFont

class DebugGUI(QWidget):

    def __init__(self, get_Track, set_Track, update_Track):
        self.inputs_Drawn = 0
        self.outputs_Drawn = 0


        super().__init__()

        #creates local Track functions
        #so they can be used in other functions
        self.get_Track = get_Track
        self.set_Track = set_Track
        self.update_Track = update_Track

        self.setGeometry(580, 80, 500, 400)
        self.setWindowTitle("Debug Menu")

        self.setup_Labels()

        self.setLayout(self.grid_Layout)
        self.parse_Track_Blocks()

    #handles creating the block drop down menus and test button
    def parse_Track_Blocks(self):
        #gets the track state from the main TrackController
        current_Track = self.get_Track()

        #iterates through the track dictionary for each block
        #and adds it to a list
        block_List = []
        for block in current_Track:
            block_List.append(block)

        #Combobox for selecting input block
        self.blocks_Dropdown = QComboBox()

        self.blocks_Dropdown.setEditable(True)
        self.blocks_Dropdown.addItems(block_List)
        self.update_Inputs(self.blocks_Dropdown.currentText())
        self.blocks_Dropdown.currentTextChanged.connect(lambda: self.update_Inputs(self.blocks_Dropdown.currentText()))
        self.blocks_Dropdown.setMaximumWidth(100)
        self.grid_Layout.addWidget(self.blocks_Dropdown, 1, 1)

        #Combobox for selecting block outputs to view
        self.out_Blocks_Dd = QComboBox()
        self.out_Blocks_Dd.setEditable(True)
        self.out_Blocks_Dd.addItems(block_List)
        self.update_Outputs(self.out_Blocks_Dd.currentText())
        self.out_Blocks_Dd.currentTextChanged.connect(lambda: self.update_Outputs(self.out_Blocks_Dd.currentText()))
        self.out_Blocks_Dd.setMaximumWidth(100)
        self.grid_Layout.addWidget(self.out_Blocks_Dd, 1, 3)


    def setup_Labels(self):
        #creates a layout and adds labels to top
        self.grid_Layout = QGridLayout()
        inputs = QLabel("Inputs")
        inputs.setFont(QFont('Times', 16))
        inputs.setMaximumHeight(30)
        outputs = QLabel("Outputs")
        outputs.setFont(QFont('Times', 16))
        outputs.setMaximumHeight(30)
        self.grid_Layout.addWidget(inputs, 0, 0)
        self.grid_Layout.addWidget(outputs, 0, 2)

        block_Label = QLabel("Block:")
        block_Label2 = QLabel("Block:")
        self.grid_Layout.addWidget(block_Label, 1, 0)
        self.grid_Layout.addWidget(block_Label2, 1, 2)

        #Push button to run plc and update outputs
        self.update_Button = QPushButton()
        self.update_Button.setText("Test")
        self.update_Button.setFont(QFont('Times', 13))
        self.update_Button.setMaximumWidth(100)
        self.update_Button.clicked.connect(lambda: self.update_Track_Outputs())
        self.grid_Layout.addWidget(self.update_Button, 8, 0)


    #creates input UI based on block
    def update_Inputs(self, block):
        #deletes old widgets before drawing new ones
        if self.inputs_Drawn:
            for i in range(2, 8):
                temp_Widget1 = self.grid_Layout.itemAtPosition(i, 0).widget()
                temp_Widget2 = self.grid_Layout.itemAtPosition(i, 1).widget()
                self.grid_Layout.removeWidget(temp_Widget1)
                self.grid_Layout.removeWidget(temp_Widget2)
                temp_Widget1.deleteLater()
                temp_Widget2.deleteLater()
        else:
            self.inputs_Drawn = True

        #creates input labels
        self.grid_Layout.addWidget(QLabel("Speed(mph):"), 2, 0)
        self.grid_Layout.addWidget(QLabel("Forward Authority(blocks):"), 3, 0)
        self.grid_Layout.addWidget(QLabel("Backward Authority(blocks):"), 4, 0)
        self.grid_Layout.addWidget(QLabel("Occupied:"), 5, 0)
        self.grid_Layout.addWidget(QLabel("Closed:"), 6, 0)
        self.grid_Layout.addWidget(QLabel("Failed:"), 7, 0)

        #speed QLineEdit
        speed_Line = QLineEdit()
        speed_Line.setMaxLength(3)
        speed_Line.setMaximumWidth(40)
        speed_Line.setText(str(self.get_Track()[block].suggested_Speed))
        speed_Line.returnPressed.connect(lambda: self.set_Track(block, "spd", speed_Line.text()))
        self.grid_Layout.addWidget(speed_Line, 2, 1)

        #forward authority QLineEdit
        f_Auth = QLineEdit()
        f_Auth.setMaxLength(2)
        f_Auth.setMaximumWidth(40)
        f_Auth.setText(str(self.get_Track()[block].forward_Authority))
        f_Auth.returnPressed.connect(lambda: self.set_Track(block, "fAuth", f_Auth.text()))
        self.grid_Layout.addWidget(f_Auth, 3, 1)

        #backward authority QLineEdit
        b_Auth = QLineEdit()
        b_Auth.setMaxLength(2)
        b_Auth.setMaximumWidth(40)
        b_Auth.setText(str(self.get_Track()[block].backward_Authority))
        b_Auth.returnPressed.connect(lambda: self.set_Track(block, "bAuth", b_Auth.text()))
        self.grid_Layout.addWidget(b_Auth, 4, 1)

        #Occupied QFontComboBox
        occ = QComboBox()
        occ.setEditable(True)
        occ.setMaximumWidth(40)
        occ.addItems(['N', 'Y'])
        if self.get_Track()[block].occupied == True:
            occ.setCurrentText('Y')
        occ.currentTextChanged.connect(lambda: self.set_Track(block, "occ", occ.currentText()))
        self.grid_Layout.addWidget(occ, 5, 1)

        #Closed QFontComboBox
        cls = QComboBox()
        cls.setEditable(True)
        cls.setMaximumWidth(40)
        cls.addItems(['N', 'Y'])
        if self.get_Track()[block].closed == True:
            cls.setCurrentText('Y')
        cls.currentTextChanged.connect(lambda: self.set_Track(block, "cls", cls.currentText()))
        self.grid_Layout.addWidget(cls, 6, 1)

        #Failed QFontComboBox
        fail = QComboBox()
        fail.setEditable(True)
        fail.setMaximumWidth(40)
        fail.addItems(['N', 'Y'])
        if self.get_Track()[block].failed == True:
            fail.setCurrentText('Y')
        fail.currentTextChanged.connect(lambda: self.set_Track(block, "fail", fail.currentText()))
        self.grid_Layout.addWidget(fail, 7, 1)
        

    #updates output GUI elements from current track state
    #does not run PLC
    def update_Outputs(self, block):
        #deletes old widgets before drawing new ones
        if self.outputs_Drawn:
            for i in range(2, self.grid_Layout.rowCount()):
                #checks that there is a widget there since row amount is variable
                if self.grid_Layout.itemAtPosition(i, 2) is not None:
                    temp_Widget1 = self.grid_Layout.itemAtPosition(i, 2).widget()
                    temp_Widget2 = self.grid_Layout.itemAtPosition(i, 3).widget()
                    self.grid_Layout.removeWidget(temp_Widget1)
                    self.grid_Layout.removeWidget(temp_Widget2)
                    temp_Widget1.deleteLater()
                    temp_Widget2.deleteLater()
        else:
            self.outputs_Drawn = True

        #Commanded speed label
        com_Speed_Label = QLabel("Commanded Speed:")
        com_Speed = QLabel(str(self.get_Track()[block].commanded_Speed))
        self.grid_Layout.addWidget(com_Speed_Label, 2, 2)
        self.grid_Layout.addWidget(com_Speed, 2, 3)

        #switches Labels
        #absolute_Row_Pos handles tracking rows for adding widgets
        absolute_Row_Pos = 2
        for i in range(len(self.get_Track()[block].switches)):
            absolute_Row_Pos = absolute_Row_Pos + 1
            sw_Label = QLabel("Switch #" + str(i) + ":")
            sw_State = QLabel(self.get_Track()[block].switch_To_Str(i))
            self.grid_Layout.addWidget(sw_Label, absolute_Row_Pos, 2)
            self.grid_Layout.addWidget(sw_State, absolute_Row_Pos, 3)
            
        #lights labels
        for i in range(len(self.get_Track()[block].lights)):
            absolute_Row_Pos = absolute_Row_Pos + 1
            light_Label = QLabel("Light #" + str(i) + ":")
            light_State = QLabel(self.get_Track()[block].light_To_Str(i))
            self.grid_Layout.addWidget(light_Label, absolute_Row_Pos, 2)
            self.grid_Layout.addWidget(light_State, absolute_Row_Pos, 3)

        #gates labels
        for i in range(len(self.get_Track()[block].gates)):
            absolute_Row_Pos = absolute_Row_Pos + 1
            gate_Label = QLabel("Gate #" + str(i) + ":")
            gate_State = QLabel(self.get_Track()[block].gate_To_Str(i))
            self.grid_Layout.addWidget(gate_Label, absolute_Row_Pos, 2)
            self.grid_Layout.addWidget(gate_State, absolute_Row_Pos, 3)
        

    #runs PLC then updates output GUI elements using update_Outputs
    def update_Track_Outputs(self):
        self.update_Track()
        self.update_Inputs(self.blocks_Dropdown.currentText())
        self.update_Outputs(self.out_Blocks_Dd.currentText())

