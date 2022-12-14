import functools
from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtWidgets import QComboBox, QLabel
from PyQt5.QtGui import QFont

class MaintenanceGUI(QWidget):

    def __init__(self, get_Track, set_switch, set_light, set_gate):
        self.is_Drawn = False
        self.get_Track = get_Track
        self.set_switch = set_switch
        self.set_light = set_light
        self.set_gate = set_gate

        self.text_font = QFont('Times', 13)

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
        block_Label.setFont(QFont('Times', 16))
        self.grid.addWidget(block_Label, 0, 0)

        #creates block dropdown and adds it
        self.block_Dd = QComboBox()
        self.block_Dd.setFont(QFont('Times', 16))
        self.block_Dd.setEditable(True)
        self.block_Dd.currentTextChanged.connect(lambda: self.open_Block(self.block_Dd.currentText()))
        self.block_Dd.setMaximumWidth(150)
        self.grid.addWidget(self.block_Dd, 0, 1)

        self.parse_Blocks()


    #parses blocks to add to dropdown
    #and prevents issues if there are no blocks in the track
    def parse_Blocks(self):
        self.block_Dd.blockSignals(True)
        self.block_Dd.clear()

        if self.get_Track() == {}:
            self.open_Block(self.block_Dd.currentText(), False)
        else:
            self.block_Dd.addItems(self.get_Track().keys())
            self.open_Block(self.block_Dd.currentText())

        self.block_Dd.blockSignals(False)

    #creates widgets for block output interactivity
    def open_Block(self, block, redraw=True):
        #removes old widgets before drawing new ones
        if self.is_Drawn is True:
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

            self.is_Drawn = False


        if redraw is True:
            self.is_Drawn = True

            #Functools.partial is used as a workaround
            #to be able to send the current loop index to the connect function
            #as a parameter.
            #For lights this is combined with a lambda that passes the 
            #early bound loop index with the runtime bound text.

            #shows switches
            #row_Pos handles tracking row for adding widgets
            row_Pos = 1
            for i in range(len(self.get_Track()[block].switches)):
                row_Pos = row_Pos + 1
                sw_Label = QLabel("Switch #" + str(i) + ":")
                sw_Label.setFont(self.text_font)
                sw_State = QComboBox()
                sw_State.setFont(self.text_font)
                sw_State.setEditable(True)
                sw_State.addItems(['OFF', 'ON'])
                sw_State.setCurrentText(self.get_Track()[block].switch_To_Str(i))
                sw_State.currentTextChanged.connect(functools.partial(self.update_switch, block, i))
                sw_State.setMaximumWidth(100)
                self.grid.addWidget(sw_Label, row_Pos, 0)
                self.grid.addWidget(sw_State, row_Pos, 1)

            #shows lights
            for i in range(len(self.get_Track()[block].lights)):
                #light_Lambdas.append(lambda: self.get_Track()[block].set_Light(i, l_State.currentText()))
                row_Pos = row_Pos + 1
                l_Label = QLabel("Light #" + str(i) + ":")
                l_Label.setFont(self.text_font)
                l_State = QComboBox()
                l_State.setFont(self.text_font)
                l_State.setEditable(True)
                l_State.addItems(["RED", "GREEN"])
                l_State.setCurrentText(self.get_Track()[block].light_To_Str(i))
                set_Light_Part = functools.partial(self.get_Track()[block].set_Light, i)
                l_State.currentTextChanged.connect(lambda: set_Light_Part(l_State.currentText()))
                l_State.currentTextChanged.connect(functools.partial(self.update_light, block))
                l_State.setMaximumWidth(100)
                self.grid.addWidget(l_Label, row_Pos, 0)
                self.grid.addWidget(l_State, row_Pos, 1)

            #shows gates
            for i in range(len(self.get_Track()[block].gates)):
                row_Pos = row_Pos + 1
                g_Label = QLabel("Gate #" + str(i) + ":")
                g_Label.setFont(self.text_font)
                g_State = QComboBox()
                g_State.setFont(self.text_font)
                g_State.setEditable(True)
                g_State.addItems(["CLOSED", "OPEN"])
                g_State.setCurrentText(self.get_Track()[block].gate_To_Str(i))
                g_State.currentTextChanged.connect(functools.partial(self.update_gate, block, i))
                g_State.setMaximumWidth(80)
                self.grid.addWidget(g_Label, row_Pos, 0)
                self.grid.addWidget(g_State, row_Pos, 1)

    def update_switch(self, block, switch_num):
        self.get_Track()[block].toggle_Switch(switch_num)

        self.set_switch(block)

    def update_light(self, block):
        #self.get_Track()[block].set_Light(color)

        self.set_light(block)

    def update_gate(self, block, switch_num):
        self.get_Track()[block].toggle_Gate(switch_num)

        self.set_gate(block)
        

    def closeEvent(self, event):
        self.hide()