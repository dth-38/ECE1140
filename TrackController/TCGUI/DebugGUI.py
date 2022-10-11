from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtWidgets import QComboBox, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QFont

class DebugGUI(QWidget):

    def __init__(self, get_Track, set_Track, update_Track):
        super().__init__()

        #creates local get_Track function
        #so it can be used in other functions
        self.get_Track = get_Track
        self.set_Track = set_Track
        self.update_Track = update_Track

        self.setGeometry(580, 80, 500, 400)
        self.setWindowTitle("Debug Menu")

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


        self.setLayout(self.grid_Layout)
        self.parse_Track_Blocks()

    #handles creating the block drop down menu
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
        self.grid_Layout.addWidget(self.blocks_Dropdown, 1, 0)

        #Combobox for selecting block outputs to view
        self.out_Blocks_Dd = QComboBox()
        self.out_Blocks_Dd.addItems(block_List)
        self.update_Outputs(self.out_Blocks_Dd.currentText())
        self.out_Blocks_Dd.currentTextChanged.connect(lambda: self.update_Outputs(self.out_Blocks_Dd.currentText()))
        self.out_Blocks_Dd.setMaximumWidth(100)
        self.grid_Layout.addWidget(self.out_Blocks_Dd, 1, 1)

        #Push button to run plc and update outputs
        self.update_Button = QPushButton()
        self.update_Button.setText("Test")
        self.update_Button.setFont(QFont('Times', 13))
        self.update_Button.clicked.connect(lambda: self.update_Track_Outputs())
        self.grid_Layout.addWidget(self.update_Button, 7, 1)


    #creates input UI based on block
    def update_Inputs(self, block):
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
        speed_Line.returnPressed.connect(lambda: self.set_Track(block, "speed", speed_Line.text()))
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
        occ.currentTextChanged.connect(lambda: self.set_Track(block, "occ", [occ.currentText()]))
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
        

    def update_Outputs(self, block):
        #Commanded speed label
        #switches Labels
        #lights labels
        #gates labels
        pass


    def update_Track_Outputs(self):
        self.update_Track()
        self.update_Outputs(self.out_Blocks_Dd.currentText())
