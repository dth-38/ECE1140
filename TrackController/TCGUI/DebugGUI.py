from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtWidgets import QFontComboBox, QLabel, QLineEdit
from PyQt5.QtGui import QFont

class DebugGUI(QWidget):

    def __init__(self, get_Track, set_Track, update_Track):
        super().__init__()

        #creates local get_Track function
        #so it can be used in other functions
        self.getTrack = get_Track
        self.setTrack = set_Track
        self.update_Track = update_Track

        self.setGeometry(580, 80, 500, 400)
        self.setWindowTitle("Debug Menu")

        #creates a layout and adds labels to top
        self.grid_Layout = QGridLayout()
        self.grid_Layout.addWidget(QLabel("Inputs"), 0, 0)
        self.grid_Layout.addWidget(QLabel("Outputs"), 0, 2)

        self.setLayout(self.grid_Layout)

    #handles creating the block drop down menu
    def parse_Track_Blocks(self):
        #gets the track state from the main TrackController
        current_Track = self.get_Track()

        #iterates through the track dictionary for each block
        #and adds it to a list
        block_List = []
        for block in current_Track:
            block_List.append(block)

        self.blocks_Dropdown = QFontComboBox()

        self.blocks_Dropdown.setEditable(True)
        self.blocks_Dropdown.addItems(block_List)
        self.blocks_Dropdown.currentTextChanged.connect(self.update_Inputs)
        self.grid_Layout.addWidget(self.blocks_Dropdown, 1, 0)

    #creates input UI based on block
    def update_Inputs(self, block):
        #creates input labels
        self.grid_Layout.addWidget(QLabel("Speed(mph):"), 1, 0)
        self.grid_Layout.addWidget(QLabel("Forward Authority(blocks):"), 2, 0)
        self.grid_Layout.addWidget(QLabel("Backward Authority(blocks):"), 3, 0)
        self.grid_Layout.addWidget(QLabel("Occupied:"), 4, 0)
        self.grid_Layout.addWidget(QLabel("Closed:"), 5, 0)
        self.grid_Layout.addWidget(QLabel("Failed:"), 6, 0)

        #speed QLineEdit
        speed_Line = QLineEdit()
        speed_Line.setMaxLength(3)
        #this might not work
        speed_Line.returnPressed(lambda: self.setTrack(block, "speed", speed_Line.text()))
        self.grid_Layout.addWidget(speed_Line, 1, 1)

        #forward authority QLineEdit
        f_Auth = QLineEdit()
        f_Auth.setMaxLength(2)
        f_Auth.returnPressed(lambda: self.setTrack(block, "fAuth", f_Auth.text()))
        self.grid_Layout.addWidget(f_Auth, 2, 1)

        #backward authority QLineEdit
        b_Auth = QLineEdit()
        b_Auth.setMaxLength(2)
        b_Auth.returnPressed(lambda: self.setTrack(block, "bAuth", b_Auth.text()))
        self.grid_Layout.addWidget(b_Auth, 3, 1)

        #Occupied QFontComboBox




