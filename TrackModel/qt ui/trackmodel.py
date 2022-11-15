from line import *
from station import *
from heater import *
from trainloc import *
from track_info import *
from railwaycrossing import *

class TrackModel:
    def __init__(self):
        self.trains = []
        self.controllers = []
        self.lines = []
        self.stations = []
        self.train_locs = [len(self.trains)]
        self.heaters = []

    def load_model(self, red_table, green_table):
        ## Load the excel file, take in data
        file = TrackInfo(fp = 'track_layout.xlsx')
        file.load_excel_data(file.get_sheet(0), red_table)
        file.load_excel_data(file.get_sheet(1), green_table)

        ## Clean up track file
        file.set_dimensions()

        ## Set line names
        self.lines.append(Line("Red Line"))
        self.lines.append(Line("Green Line"))
        
        ## Get header labels from the file
        red_headers = []
        green_headers = []
        for y in range(9):
            red_headers.append(red_table.horizontalHeaderItem(y))
            green_headers.append(green_table.horizontalHeaderItem(y))

        ## Create block lists
        for x in range(red_table.rowCount()):
            section = ''
            number = 0
            length = 0
            grade = 0
            limit = 0
            elevation = 0
            new_block = Block(section, number)

            ## Get section, number, length, grade, speed limit, and elevation for new block
            for i in range(len(red_headers)):
                if red_headers[i] is not None:
                    if (red_headers[i].text() == "Section"):
                        new_block.section = file.get_cell_text(red_table, x, i)
                    elif (red_headers[i].text() == "Block Number"):
                        new_block.number = file.get_cell_text(red_table, x, i)
                    elif (red_headers[i].text() == "Block Length (m)"):
                        new_block.length = file.get_cell_text(red_table, x, i)
                    elif (red_headers[i].text() == "Block Grade (%)"):
                        new_block.grade = file.get_cell_text(red_table, x, i)
                    elif (red_headers[i].text() == "Speed Limit (Km/Hr)"):
                        new_block.commanded_speed = file.get_cell_text(red_table, x, i)
                    elif (red_headers[i].text() == "ELEVATION (M)"):
                        new_block.elevation = file.get_cell_text(red_table, x, i)
                    elif (red_headers[i].text() == "Infrastructure"):
                        self.load_infra_values(file, red_table, new_block, x, i)

            ## Add new block to block list for red line
            self.lines[0].blocks.append(new_block)

        for x in range(green_table.rowCount()):
            section = ''
            number = 0

            ## Get section and number for new block
            for i in range(len(green_headers)):
                if green_headers[i] is not None:
                    if (green_headers[i].text() == "Section"):
                        section = file.get_cell_text(green_table, x, i)
                    if (green_headers[i].text() == "Block Number"):
                        number = file.get_cell_text(green_table, x, i)

            ## Add new block to block list for green line
            new_block = Block(section, number)
            self.lines[1].blocks.append(new_block)

    def load_infra_values(self, file, table, block, row, col):
        ## Get station and other infrastructure information
        infra = file.get_cell_text(table, row, col)
        print(infra)

        ## Create rail crossing on corresponding block
        if (infra == "RAILWAY CROSSING"):
            rail = RailwayCrossing()
            block.set_rail_cross(rail)

        ## Create station, set beacon
        elif (infra.find("STATION") != -1):
            station = Station()
            block.set_station(station)
            

