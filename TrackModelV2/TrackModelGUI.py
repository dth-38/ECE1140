from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTabWidget, QVBoxLayout, QTableWidgetItem
from PyQt5.QtGui import QColor

HEIGHT = 1080
WIDTH = 1080
X_POS = 0
Y_POS = 0

class TrackModelGUI(QMainWindow):
    def __init__(self, gt):
        super().__init__()

        self.get_track = gt
        self.setup_gui()

    def setup_gui(self):
        self.main_layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.table_widgets = {}
        self.GREEN = QColor(0,128,0)
        self.RED = QColor(128,0,32)


        self.setGeometry(X_POS, Y_POS, WIDTH, HEIGHT)
        self.setWindowTitle("Track Model")
        self.setMinimumSize(WIDTH, HEIGHT)


    def initialize_lines(self):
        self.table_widgets.clear()
        self.tabs.clear()

        track = self.get_track()
        for line in track:
            new_line = QTableWidget()

            new_line.setColumnCount(9)
            col_headers = ["Section","Occupied","Authority","Commanded Spd.","Station","Beacon","Switch","Light","Gate"]
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
                if self.get_track[line][block].occupied != -1:
                    occ.setBackground(self.GREEN)
                else:
                    occ.setBackground(self.RED)

                new_line.setItem(block,1, occ)

                #create authority item
                new_line.setItem(block,2, QTableWidgetItem(str(track[line][block].authority)))

                #create commanded speed item
                new_line.setItem(block,3, QTableWidgetItem(str(track[line][block].commanded_speed)))

                #create Station item
                new_line.setItem(block,4, QTableWidgetItem(track[line][block].STATION))

                #create Beacon item
                new_line.setItem(block,5, QTableWidgetItem(track[line][block].STATION + ":" + str(track[line][block].BEACON)))

                #create switch item
                sw_pos = track[line][block].get_switch_to()
                if sw_pos != -1:
                    sw = QTableWidgetItem(str(sw_pos))
                else:
                    sw = QTableWidgetItem("NONE")
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
                    l = QTableWidgetItem("NONE")
                new_line.setItem(block,7, l)

                #create gate item
                if track[line][block].gate != []:
                    g = QTableWidgetItem(track[line][block].gate[0])
                else:
                    g = QTableWidgetItem("NONE")
                new_line.setItem(block,8, g)

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
            self.table_widgets[line].item(block,1).setBackground(self.RED)

    def update_authority(self, line, block):
        self.table_widgets[line].item(block,2).setText(str(self.get_track()[line][block].authority))

    def update_spd(self, line, block):
        self.table_widgets[line].item(block,3).setText(str(self.get_track()[line][block].commanded_speed))

    def update_switch(self, line, block):
        self.table_widgets[line].item(block,6).setText(str(self.get_track()[line][block].get_switch_to()))


    def update_light(self, line, block):
        if self.get_track()[line][block].light[0] == 1:
            self.table_widget[line].item(block,7).setText("GREEN")
            self.table_widget[line].item(block,7).setBackground(self.GREEN)
        else:
            self.table_widget[line].item(block,7).setText("RED")
            self.table_widget[line].item(block,7).setBackground(self.RED)

    def update_gate(self, line, block):
        if self.get_track()[line][block].gate[0] == 1:
            self.table_widgets[line].item(block,8).setText("CLOSED")
        else:
            self.table_widgets[line].item(block,8).setText("OPEN")
        