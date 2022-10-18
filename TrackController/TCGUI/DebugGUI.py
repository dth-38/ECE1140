from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtWidgets import QComboBox, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QFont

class DebugGUI(QWidget):

    def __init__(self, get_Track, set_Track, update_Track, leave_Debug):
        self.inputs_Drawn = 0
        self.outputs_Drawn = 0


        super().__init__()

        #creates local Track functions
        #so they can be used in other functions
        self.get_Track = get_Track
        self.set_Track = set_Track
        self.update_Track = update_Track
        self.leave_Debug = leave_Debug

        self.setGeometry(580, 80, 500, 400)
        self.setWindowTitle("Debug Menu")

        self.setup_Labels()

    #handles creating the block drop down menus and test button
    def parse_Track_Blocks(self):
        self.blocks_Dropdown.blockSignals(True)
        self.out_Blocks_Dd.blockSignals(True)
        self.blocks_Dropdown.clear()
        self.out_Blocks_Dd.clear()

        if self.get_Track() != {}:
            self.blocks_Dropdown.addItems(self.get_Track().keys())
            self.out_Blocks_Dd.addItems(self.get_Track().keys())
            self.update_Inputs(self.blocks_Dropdown.currentText())
            self.update_Outputs(self.out_Blocks_Dd.currentText())
        else:
            self.update_Inputs(self.blocks_Dropdown.currentText(), False)
            self.update_Outputs(self.out_Blocks_Dd.currentText(), False)
        

        self.blocks_Dropdown.blockSignals(False)
        self.out_Blocks_Dd.blockSignals(False)


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
        self.grid_Layout.addWidget(self.update_Button, 7, 0)

        #Combobox for selecting input block
        self.blocks_Dropdown = QComboBox()
        self.blocks_Dropdown.setEditable(True)
        self.blocks_Dropdown.currentTextChanged.connect(lambda: self.update_Inputs(self.blocks_Dropdown.currentText()))
        self.blocks_Dropdown.setMaximumWidth(100)
        self.grid_Layout.addWidget(self.blocks_Dropdown, 1, 1)

        #Combobox for selecting block outputs to view
        self.out_Blocks_Dd = QComboBox()
        self.out_Blocks_Dd.setEditable(True)
        self.out_Blocks_Dd.currentTextChanged.connect(lambda: self.update_Outputs(self.out_Blocks_Dd.currentText()))
        self.out_Blocks_Dd.setMaximumWidth(100)
        self.grid_Layout.addWidget(self.out_Blocks_Dd, 1, 3)

        self.setLayout(self.grid_Layout)

        self.parse_Track_Blocks()


    #creates input UI based on block
    def update_Inputs(self, block, redraw=True):
        #deletes old widgets before drawing new ones
        if self.inputs_Drawn:
            for i in range(2, 7):
                temp_Widget1 = self.grid_Layout.itemAtPosition(i, 0).widget()
                temp_Widget2 = self.grid_Layout.itemAtPosition(i, 1).widget()
                self.grid_Layout.removeWidget(temp_Widget1)
                self.grid_Layout.removeWidget(temp_Widget2)
                temp_Widget1.deleteLater()
                temp_Widget2.deleteLater()

            self.inputs_Drawn = False

        if redraw is True:
            self.inputs_Drawn = True

            #creates input labels
            self.grid_Layout.addWidget(QLabel("Speed(mph):"), 2, 0)
            self.grid_Layout.addWidget(QLabel("Authority(blocks):"), 3, 0)
            self.grid_Layout.addWidget(QLabel("Occupied:"), 4, 0)
            self.grid_Layout.addWidget(QLabel("Closed:"), 5, 0)
            self.grid_Layout.addWidget(QLabel("Failed:"), 6, 0)

            #speed QLineEdit
            speed_Line = QLineEdit()
            speed_Line.setMaxLength(3)
            speed_Line.setMaximumWidth(40)
            speed_Line.setText(str(self.get_Track()[block].suggested_Speed))
            speed_Line.returnPressed.connect(lambda: self.set_Track(block, "spd", speed_Line.text()))
            self.grid_Layout.addWidget(speed_Line, 2, 1)

            #forward authority QLineEdit
            auth = QLineEdit()
            auth.setMaxLength(2)
            auth.setMaximumWidth(40)
            auth.setText(str(self.get_Track()[block].authority))
            auth.returnPressed.connect(lambda: self.set_Track(block, "auth", auth.text()))
            self.grid_Layout.addWidget(auth, 3, 1)


            #Occupied QFontComboBox
            occ = QComboBox()
            occ.setEditable(True)
            occ.setMaximumWidth(40)
            occ.addItems(['N', 'Y'])
            if self.get_Track()[block].occupied == True:
                occ.setCurrentText('Y')
            occ.currentTextChanged.connect(lambda: self.set_Track(block, "occ", occ.currentText()))
            self.grid_Layout.addWidget(occ, 4, 1)

            #Closed QFontComboBox
            cls = QComboBox()
            cls.setEditable(True)
            cls.setMaximumWidth(40)
            cls.addItems(['N', 'Y'])
            if self.get_Track()[block].closed == True:
                cls.setCurrentText('Y')
            cls.currentTextChanged.connect(lambda: self.set_Track(block, "cls", cls.currentText()))
            self.grid_Layout.addWidget(cls, 5, 1)

            #Failed QFontComboBox
            fail = QComboBox()
            fail.setEditable(True)
            fail.setMaximumWidth(40)
            fail.addItems(['N', 'Y'])
            if self.get_Track()[block].failed == True:
                fail.setCurrentText('Y')
            fail.currentTextChanged.connect(lambda: self.set_Track(block, "fail", fail.currentText()))
            self.grid_Layout.addWidget(fail, 6, 1)
        

    #updates output GUI elements from current track state
    #does not run PLC
    def update_Outputs(self, block, redraw=True):
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

            self.outputs_Drawn = False

        if redraw is True:
            self.outputs_Drawn = True

            #Commanded speed label
            com_Speed_Label = QLabel("Commanded Speed(mph):")
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
        if self.get_Track() != {}:
            self.update_Inputs(self.blocks_Dropdown.currentText())
            self.update_Outputs(self.out_Blocks_Dd.currentText())

    def closeEvent(self, event):
        self.leave_Debug()
        self.hide()

