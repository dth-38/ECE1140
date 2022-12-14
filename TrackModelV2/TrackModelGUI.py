from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTabWidget, QGridLayout, QTableWidgetItem
from PyQt5.QtWidgets import QComboBox, QLabel, QPushButton
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt
from Signals import signals
from TrackController.TCTools import convert_to_block

HEIGHT = 1000
WIDTH = 1000
X_POS = 0
Y_POS = 0

class TrackModelGUI(QMainWindow):
    def __init__(self, gt):
        super().__init__()

        self.get_track = gt
        self.lines = []
        self.blocks = {}
        self.setup_gui()

    def setup_gui(self):
        #self.main_layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.table_widgets = {}
        self.GREEN = QColor(0,128,0)
        self.RED = QColor(128,0,32)
        self.WHITE = QColor(255,255,255)
        self.text_font = QFont('Times', 14)


        self.setGeometry(X_POS, Y_POS, WIDTH, HEIGHT)
        self.setWindowTitle("Track Model")
        self.setMinimumSize(WIDTH, HEIGHT)

        #self.main_layout.addWidget(self.tabs)
        self.setCentralWidget(self.tabs)

        self.failure_tab = QWidget()
        self.failure_layout = QGridLayout()
        self.failure_layout.setAlignment(Qt.AlignTop)

        self.failure_tab.setLayout(self.failure_layout)

        self.lines_dropdown = QComboBox()
        self.lines_dropdown.setEditable(True)
        self.lines_dropdown.currentTextChanged.connect(self.update_blocks)
        self.lines_dropdown.setFont(self.text_font)

        self.blocks_dropdown = QComboBox()
        self.lines_dropdown.setEditable(True)
        self.blocks_dropdown.currentTextChanged.connect(self.check_label)
        self.blocks_dropdown.setFont(self.text_font)

        self.failure_label = QLabel()
        self.failure_label.setFont(self.text_font)

        self.failure_toggle = QPushButton("Toggle Failure")
        self.failure_toggle.clicked.connect(self.toggle_failure)
        self.failure_toggle.setFont(self.text_font)

        self.failure_layout.addWidget(self.lines_dropdown, 0, 0)
        self.failure_layout.addWidget(self.blocks_dropdown, 0, 1)
        self.failure_layout.addWidget(self.failure_label, 0, 2)
        self.failure_layout.addWidget(self.failure_toggle, 0, 3)



    def initialize_lines(self):
        self.lines_dropdown.clear()
        self.lines_dropdown.addItems(self.get_track().keys())

        self.table_widgets.clear()
        self.tabs.clear()

        track = self.get_track()
        for line in track:
            new_line = QTableWidget()
            new_line.setFont(self.text_font)

            new_line.setColumnCount(13)
            col_headers = ["Section","Occupied","Authority (Blocks)","Commanded Spd. (mph)","Station","Beacon","Switch","Light","Gate","Length (ft)","Grade","Underground","Max Speed"]
            new_line.setHorizontalHeaderLabels(col_headers)

            row_headers = []
            for block in track[line]:
                #adds a row
                new_line.insertRow(block)
                
                #creates a headers for the row
                if block == 0:
                    row_headers.append("YARD")
                else:
                    row_headers.append(str(block))

                #sets the section for the block
                sect = QTableWidgetItem(track[line][block].SECTION)
                sect.setFont(self.text_font)
                new_line.setItem(block,0, sect)

                #create occupancy item
                occ_val = track[line][block].occupied
                if occ_val == -1:
                    occ = QTableWidgetItem("")
                else:
                    occ = QTableWidgetItem(str(occ_val))
                if self.get_track()[line][block].occupied != -1:
                    occ.setBackground(self.GREEN)

                occ.setFont(self.text_font)
                new_line.setItem(block,1, occ)

                #create authority item
                auth = track[line][block].authority
                if auth == -1:
                    auth_item = QTableWidgetItem("")
                else:
                    auth_item = QTableWidgetItem(str(auth))

                auth_item.setFont(self.text_font)
                new_line.setItem(block,2, auth_item)

                #create commanded speed item
                spd_item = QTableWidgetItem(str(track[line][block].commanded_speed))
                spd_item.setFont(self.text_font)
                new_line.setItem(block,3, spd_item)

                #create Station item
                station_item = QTableWidgetItem(track[line][block].STATION)
                station_item.setFont(self.text_font)
                new_line.setItem(block,4, station_item)

                #create Beacon item
                if track[line][block].BEACON[0] != "":
                    beac = QTableWidgetItem(track[line][block].BEACON[0] + ":" + track[line][block].BEACON[1])
                else:
                    beac = QTableWidgetItem("")

                beac.setFont(self.text_font)
                new_line.setItem(block,5, beac)

                #create switch item
                sw_pos = track[line][block].get_switch_to()
                if sw_pos != -1:
                    if sw_pos == 0:
                        sw = QTableWidgetItem("YARD")
                    else:
                        sw = QTableWidgetItem(str(sw_pos))
                else:
                    sw = QTableWidgetItem()

                sw.setFont(self.text_font)
                new_line.setItem(block,6, sw)

                #create light item
                if track[line][block].light != []:
                    if track[line][block].light[0] == 1:
                        l = QTableWidgetItem("GREEN")
                        l.setBackground(self.GREEN)
                    else:
                        l = QTableWidgetItem("RED")
                        l.setBackground(self.RED)
                else:
                    l = QTableWidgetItem()

                l.setFont(self.text_font)
                new_line.setItem(block,7, l)

                #create gate item
                if track[line][block].gate != []:
                    g = QTableWidgetItem(track[line][block].gate[0])
                else:
                    g = QTableWidgetItem()

                g.setFont(self.text_font)
                new_line.setItem(block,8, g)

                #create length item
                l_b = QTableWidgetItem(str(round(track[line][block].LENGTH / 0.3408, 2)))
                l_b.setFont(self.text_font)
                new_line.setItem(block,9,l_b)

                #create grade item
                g_b = QTableWidgetItem(str(track[line][block].GRADE))
                g_b.setFont(self.text_font)
                new_line.setItem(block,10,g_b)

                #create undergound item
                if track[line][block].UNDERGROUND == True:
                    u_b = QTableWidgetItem("Y")
                else:
                    u_b = QTableWidgetItem("N")
                u_b.setFont(self.text_font)
                new_line.setItem(block,11,u_b)

                #create max speed item
                ms_b = QTableWidgetItem(str(track[line][block].MAX_SPEED))
                ms_b.setFont(self.text_font)
                new_line.setItem(block,12,ms_b)

            #set newly generated headers
            new_line.setVerticalHeaderLabels(row_headers)

            #adds the table to the array for modifying and tabs for displaying
            self.table_widgets[line] = new_line
            self.tabs.addTab(new_line, line)

        
        self.tabs.addTab(self.failure_tab, "Failures")

    def update_occupancy(self, line, block):
        occ = self.get_track()[line][block].occupied
        self.table_widgets[line].item(block,1).setText(str(occ))
        if occ != -1:
            self.table_widgets[line].item(block,1).setBackground(self.GREEN)
            self.table_widgets[line].item(block,1).setText(str(occ))
        else:
            self.table_widgets[line].item(block,1).setBackground(self.WHITE)
            self.table_widgets[line].item(block,1).setText("")

    def update_authority(self, line, block):
        auth = self.get_track()[line][block].authority
        if auth == -1:
            self.table_widgets[line].item(block,2).setText("")
        else:
            self.table_widgets[line].item(block,2).setText(str(auth))

    def update_spd(self, line, block):
        self.table_widgets[line].item(block,3).setText(str(self.get_track()[line][block].commanded_speed))

    def update_switch(self, line, block):
        sw = self.get_track()[line][block].get_switch_to()
        if sw == 0:
            sw_str = "YARD"
        else:
            sw_str = str(sw)
        self.table_widgets[line].item(block,6).setText(sw_str)


    def update_light(self, line, block):
        #TODO: check that excel is being parsed right
        if self.get_track()[line][block].light == []:
            return 0

        if self.get_track()[line][block].light[0] == 1:
            self.table_widgets[line].item(block,7).setText("GREEN")
            self.table_widgets[line].item(block,7).setBackground(self.GREEN)
        else:
            self.table_widgets[line].item(block,7).setText("RED")
            self.table_widgets[line].item(block,7).setBackground(self.RED)

    def update_gate(self, line, block):
        if self.get_track()[line][block].gate[0] == 1:
            self.table_widgets[line].item(block,8).setText("CLOSED")
        else:
            self.table_widgets[line].item(block,8).setText("OPEN")

    def show_incident(self, line, block):
        self.table_widgets[line].item(block,1).setBackground(self.RED)

    def update_blocks(self):
        line = self.lines_dropdown.currentText()
        
        blocks = list(self.get_track()[line].keys())

        for i in range(len(blocks)):
            blocks[i] = str(blocks[i])

        self.blocks_dropdown.clear()
        self.blocks_dropdown.addItems(blocks)


    def toggle_failure(self):
        line = self.lines_dropdown.currentText()
        block = self.blocks_dropdown.currentText()

        try:
            block = int(block)

            self.get_track()[line][block].failed = not self.get_track()[line][block].failed

            tc_block = convert_to_block(line, block)
            signals.send_tc_failure.emit(tc_block, self.get_track()[line][block].failed)

            if self.get_track()[line][block].failed == True:
                self.table_widgets[line].item(block, 0).setBackground(self.RED)
            else:
                self.table_widgets[line].item(block, 0).setBackground(self.WHITE)

            self.check_label()

        except:
            print("Conversion error in track model failure tab")

    def check_label(self):
        line = self.lines_dropdown.currentText()
        block = self.blocks_dropdown.currentText()
        try:
            block = int(block)

            if self.get_track()[line][block].failed == True:
                self.failure_label.setText("Failed: True")
                self.failure_label.setStyleSheet("color: red")
            else:
                self.failure_label.setText("Failed: False")
                self.failure_label.setStyleSheet("color: green")
        except:
            print("Conversion error in track model failure tab.")

        