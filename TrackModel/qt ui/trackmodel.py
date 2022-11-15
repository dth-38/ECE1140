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
        file = TrackInfo(fp = "C:/Users/rachs/OneDrive/Documents/ECE1140/ECE1140/TrackModel/qt ui/track_layout.xlsx")
        file.load_excel_data(file.get_sheet(0), red_table)
        file.load_excel_data(file.get_sheet(1), green_table)

        ## Clean up track file
        file.set_dimensions()

        ## Set line names
        self.lines.append(Line("Red Line"))
        self.lines.append(Line("Green Line"))
        
        ## Get header labels from the file
        headers = []
        for y in range(9):
            if (red_table.horizontalHeaderItem(y).text() == green_table.horizontalHeaderItem(y).text()):
                headers.append(red_table.horizontalHeaderItem(y))

        ## Set up block lists for the red and green lines
        self.create_blocks(file, self.lines[0], red_table, headers)
        self.create_blocks(file, self.lines[1], green_table, headers)

        ## Check that blocks were created
        print(len(self.lines[0].blocks))
        print(self.lines[0].get_block(54).get_section())
        print(self.lines[0].blocks[54].get_section())

    def create_blocks(self, file, line, table, headers):
        ## Create block lists
        for x in range(table.rowCount()):
            section = ''
            number = 0
            new_block = Block(section, number)

            ## Get section, number, length, grade, speed limit, and elevation for new block
            for i in range(len(headers)):
                if headers[i] is not None:
                    if (headers[i].text() == "Section"):
                        new_block.section = file.get_cell_text(table, x, i)
                    elif (headers[i].text() == "Block Number"):
                        new_block.number = file.get_cell_text(table, x, i)
                    elif (headers[i].text() == "Block Length (m)"):
                        new_block.length = file.get_cell_text(table, x, i)
                    elif (headers[i].text() == "Block Grade (%)"):
                        new_block.grade = file.get_cell_text(table, x, i)
                    elif (headers[i].text() == "Speed Limit (Km/Hr)"):
                        new_block.commanded_speed = file.get_cell_text(table, x, i)
                    elif (headers[i].text() == "ELEVATION (M)"):
                        new_block.elevation = file.get_cell_text(table, x, i)
                    elif (headers[i].text() == "Infrastructure"):
                        self.load_infra_values(file, table, new_block, x, i)

            ## Add new block to block list for correct line
            line.blocks.append(new_block)

        # ## Set beacon values for the blocks
        # for j in range(table.rowCount()):
        #     self.set_beacon_values(line, line.get_block(j))

    def load_infra_values(self, file, table, block, row, col):
        ## Get station and other infrastructure information
        infra = file.get_cell_text(table, row, col)

        ## Create rail crossing on corresponding block
        if (infra == "RAILWAY CROSSING"):
            rail = RailwayCrossing()
            block.set_rail_cross(rail)

        ## Create station, set beacon
        elif (infra.find("STATION") != -1):
            station = Station()
            block.set_station(station)

            ## Get station name
            #  infra[0:8] = "STATION: "
            semicolon = infra.find(";", 8)
            #  ex: STATION; PENN STATION; UNDERGROUND
            if (semicolon != -1):
                n = infra[8:semicolon]
                name = n.strip()
            #  ex: STATION; HERRON AVE
            else:
                n = infra[8:]
                name = n.strip()
            
            ## Set name to corresponding station
            block.get_station().set_name(name)

    # ## Call function after all blocks for each line are set
    # def set_beacon_values(self, line, block):
    #     station1 = ""
    #     station2 = ""
    #     side = ""

    #     ## Set station to yard at first block for each line
    #     num = block.get_number()
    #     if (num == 1):
    #         block.set_station(Station())
    #         block.get_station().set_name("YARD")

    #     ## Get previous station
    #     n = num
    #     while (n > 1):
    #         ## Iterate through previous block until the most recent station is found
    #         n -= 1
    #         prev_station = line.get_block(n).get_station()
    #         if prev_station is not None:
    #             station1 = prev_station
    #             break

    #     ## Get upcoming station
    #     n = num
    #     while (n < (len(line.blocks) - 1)):
    #         ## Iterate through previous block until the most recent station is found
    #         n += 1
    #         if line.get_block(n) is not None:
    #             next_station = line.get_block(n).get_station()
    #             print(next_station.get_name())
    #             if next_station is not None:
    #                 station2 = next_station
    #                 break

    #     ## Send previous and next station data to the corresponding block
    #     block.set_beacon(station1, station2, side)
