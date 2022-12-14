from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTabWidget, QVBoxLayout, QTableWidgetItem
from PyQt5.QtGui import QColor
from Signals import signals

HEIGHT = 1000
WIDTH = 1000
X_POS = 0
Y_POS = 0

class TrackModelGUI(QMainWindow):
    def __init__(self, gt):
        super().__init__()

        self.get_track = gt
        self.setup_gui()

    def setup_gui(self):
        #self.main_layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.table_widgets = {}
        self.GREEN = QColor(0,128,0)
        self.RED = QColor(128,0,32)
        self.WHITE = QColor(255,255,255)


        self.setGeometry(X_POS, Y_POS, WIDTH, HEIGHT)
        self.setWindowTitle("Track Model")
        self.setMinimumSize(WIDTH, HEIGHT)

        #self.main_layout.addWidget(self.tabs)
        self.setCentralWidget(self.tabs)


    def initialize_lines(self):
        self.table_widgets.clear()
        self.tabs.clear()

        track = self.get_track()
        for line in track:
            new_line = QTableWidget()

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
                new_line.setItem(block,0, QTableWidgetItem(track[line][block].SECTION))

                #create occupancy item
                occ = QTableWidgetItem(str(track[line][block].occupied))
                if self.get_track()[line][block].occupied != -1:
                    occ.setBackground(self.GREEN)

                new_line.setItem(block,1, occ)

                #create authority item
                auth = track[line][block].authority
                if auth == -1:
                    new_line.setItem(block,2, QTableWidgetItem(""))
                else:
                    new_line.setItem(block,2, QTableWidgetItem(str(auth)))

                #create commanded speed item
                new_line.setItem(block,3, QTableWidgetItem(str(track[line][block].commanded_speed)))

                #create Station item
                new_line.setItem(block,4, QTableWidgetItem(track[line][block].STATION))

                #create Beacon item
                if track[line][block].BEACON[0] != "":
                    new_line.setItem(block,5, QTableWidgetItem(track[line][block].BEACON[0] + ":" + track[line][block].BEACON[1]))
                else:
                    new_line.setItem(block,5,QTableWidgetItem())

                #create switch item
                sw_pos = track[line][block].get_switch_to()
                if sw_pos != -1:
                    if sw_pos == 0:
                        sw = QTableWidgetItem("YARD")
                    else:
                        sw = QTableWidgetItem(str(sw_pos))
                else:
                    sw = QTableWidgetItem()
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
                new_line.setItem(block,7, l)

                #create gate item
                if track[line][block].gate != []:
                    g = QTableWidgetItem(track[line][block].gate[0])
                else:
                    g = QTableWidgetItem()
                new_line.setItem(block,8, g)

                #create length item
                l_b = QTableWidgetItem(str(round(track[line][block].LENGTH / 0.3408, 2)))
                new_line.setItem(block,9,l_b)

                #create grade item
                g_b = QTableWidgetItem(str(track[line][block].GRADE))
                new_line.setItem(block,10,g_b)

                #create undergound item
                if track[line][block].UNDERGROUND == True:
                    u_b = QTableWidgetItem("Y")
                else:
                    u_b = QTableWidgetItem("N")
                new_line.setItem(block,11,u_b)

                #create max speed item
                ms_b = QTableWidgetItem(str(track[line][block].MAX_SPEED))
                new_line.setItem(block,12,ms_b)

            #set newly generated headers
            new_line.setVerticalHeaderLabels(row_headers)

            #adds the table to the array for modifying and tabs for displaying
            self.table_widgets[line] = new_line
            self.tabs.addTab(new_line, line)

    def update_occupancy(self, line, block):
        occ = self.get_track()[line][block].occupied
        self.table_widgets[line].item(block,1).setText(str(occ))
        if occ != -1:
            self.table_widgets[line].item(block,1).setBackground(self.GREEN)
        else:
            self.table_widgets[line].item(block,1).setBackground(self.WHITE)

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
        