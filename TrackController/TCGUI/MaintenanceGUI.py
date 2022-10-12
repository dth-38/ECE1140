from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtWidgets import QComboBox, QLabel

class MaintenanceGUI(QWidget):

    def __init__(self, get_Track):
        self.is_Drawn = False
        self.get_Track = get_Track

        #initializes QWidget
        super().__init__()

        #sets window properties
        self.setGeometry(580, 480, 400, 400)
        self.setWindowTitle("Test Equipment")

        #creates grid layout and sets up block dropdown
        self.grid = QGridLayout()
        self.setup_Block_Menu()
        self.setLayout(self.grid)


    #creates block label and block selecting dropdown
    #calls the open_Block function to show interactivity
    def setup_Block_Menu(self):
        #creates block label and adds it
        block_Label = QLabel("Block:")
        self.grid.addWidget(block_Label, 0, 0)

        #generates list of blocks to add to the dropdown
        block_List = []
        current_Track = self.get_Track()
        for block in current_Track:
            block_List.append(block)

        #creates block dropdown and adds it
        self.block_Dd = QComboBox()
        self.block_Dd.setEditable(True)
        self.block_Dd.addItems(block_List)
        self.open_Block(self.block_Dd.currentText())
        self.block_Dd.currentTextChanged.connect(lambda: self.open_Block(self.block_Dd.currentText()))
        self.block_Dd.setMaximumWidth(100)
        self.grid.addWidget(self.block_Dd, 0, 1)


    #TODO: fix lambdas, passing i only passes last value of i used in loop
    #rather than the current i in loop

    #creates widgets for block output interactivity
    def open_Block(self, block):
        #removes old widgets before drawing new ones
        if self.is_Drawn:
            #checks each row
            for i in range(1, self.grid.rowCount()):
                #checks if there is a widget
                if self.grid.itemAtPosition(i, 0) is not None:
                    widg1 = self.grid.itemAtPosition(i, 0).widget()
                    widg2 = self.grid.itemAtPosition(i, 1).widget()
                    self.grid.removeWidget(widg1)
                    self.grid.removeWidget(widg2)
                    widg1.deleteLater()
                    widg2.deleteLater()
        else:
            self.is_Drawn = True

        #shows switches
        #row_Pos handles tracking row for adding widgets
        row_Pos = 1
        for i in range(len(self.get_Track()[block].switches)):
            row_Pos = row_Pos + 1
            sw_Label = QLabel("Switch #" + str(i) + ":")
            sw_State = QComboBox()
            sw_State.setEditable(True)
            sw_State.addItems(['OFF', 'ON'])
            sw_State.setCurrentText(self.get_Track()[block].switch_To_Str(i))
            sw_State.currentTextChanged.connect(lambda: self.get_Track()[block].toggle_Switch(i))
            sw_State.setMaximumWidth(50)
            self.grid.addWidget(sw_Label, row_Pos, 0)
            self.grid.addWidget(sw_State, row_Pos, 1)

        #shows lights
        for i in range(len(self.get_Track()[block].lights)):
            row_Pos = row_Pos + 1
            l_Label = QLabel("Light #" + str(i) + ":")
            l_State = QComboBox()
            l_State.setEditable(True)
            l_State.addItems(["RED", "YELLOW", "GREEN"])
            l_State.setCurrentText(self.get_Track()[block].light_To_Str(i))
            l_State.currentTextChanged.connect(lambda: self.get_Track()[block].set_Light(i, l_State.currentText()))
            l_State.setMaximumWidth(80)
            self.grid.addWidget(l_Label, row_Pos, 0)
            self.grid.addWidget(l_State, row_Pos, 1)

        #shows gates
        for i in range(len(self.get_Track()[block].gates)):
            row_Pos = row_Pos + 1
            g_Label = QLabel("Gate #" + str(i) + ":")
            g_State = QComboBox()
            g_State.setEditable(True)
            g_State.addItems(["CLOSED", "OPEN"])
            g_State.setCurrentText(self.get_Track()[block].gate_To_Str(i))
            g_State.currentTextChanged.connect(lambda: self.get_Track()[block].toggle_Gate(i))
            g_State.setMaximumWidth(80)
            self.grid.addWidget(g_Label, row_Pos, 0)
            self.grid.addWidget(g_State, row_Pos, 1)
        

