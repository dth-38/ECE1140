from line import *
from heater import *
from trainloc import *
from track_info import *

import pathlib

from PyQt5.QtCore import pyqtSlot
##from TrainModel import Train
##from Signals import signals

class TrackModel:
    def __init__(self):
        self.trains = []
        self.controllers = []
        self.lines = []
        self.heaters = []
        self.current = []

        ## Used to show the train moving correctly for Iteration #3 only
        self.prev_block = None
        self.curr_block = None
        self.next_block = None

    # ## Add new train to the map
    # def add_train(self, route):
    #     id = len(self.trains)
    #     t = Train(id, route)
    #     self.trains.append(t)

    ## Delete trains from the map
    def remove_train(self, id):
        self.trains.pop(id)

    ## Return train object based upon ID
    def get_train(self, id):
        return self.trains[id]

    def load_model(self, red_table, green_table):
        #walks up the file tree until ECE1140 directory is found
        destination = str(pathlib.Path().absolute())
        i = 0
        while destination[len(destination)-7:] != "ECE1140":
            i += 1
            destination = str(pathlib.Path(__file__).parents[i])
        #creates the expected text file based on the controller id
        destination += ("/TrackModel/track_layout.xlsx")

        ## Load the excel file, take in data
        file = TrackInfo(fp = destination)
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
                headers.append(red_table.horizontalHeaderItem(y).text())

        self.create_linked_block_list(file, red_table, headers)

        # ## Set up block lists for the red and green lines
        # self.create_blocks(file, self.lines[0], red_table, headers)
        # self.create_blocks(file, self.lines[1], green_table, headers)

        # ## Calculate total track length for green and red lines
        # self.lines[0].calc_line_length()
        # self.lines[1].calc_line_length()

    def create_linked_block_list(self, file, table, headers):
        # Set to red line, create new block for yard, append head node
        redline = self.lines[0]
        yard_head_node = Block(0,0)
        redline.blocks.append(yard_head_node)
        
        # Find node after/before yard to start the list
        section_col = headers.index("Section")
        number_col = headers.index("Block Number")
        infra_col = headers.index("Infrastructure")
        for x in range(table.rowCount()):
            # Get text value in the "Infrastructure" column
            text = file.get_cell_text(table, x, infra_col).lower()

            # Set section, number to the current table entry's values and 
            # create a new block, but don't add it to the list yet
            new_section = file.get_cell_text(table, x, section_col)
            new_number = int(file.get_cell_text(table, x, number_col))
            new_block = Block(new_section, new_number)

            # Only 1 block leads in/out of the yard
            if (text.find("to/from") != -1):
                # add block to linked list, next node is the new_block node
                redline.blocks.append(new_block)
                # set prev node to the new_block node also
                redline.blocks.head.prev = redline.blocks.head.next
            
            # Block only leads into the yard
            #elif (text.find(" to yard ") != -1):
                
        












    # def create_blocks(self, file, line, table, headers):
    #     ## Create block lists
    #     for x in range(table.rowCount()):
    #         section = ''
    #         number = 0
    #         new_block = Block(section, number)

    #         ## Get section, number, length, grade, speed limit, and elevation for new block
    #         for i in range(len(headers)):
    #             if headers[i] is not None:
    #                 if (headers[i].text() == "Section"):
    #                     new_block.section = file.get_cell_text(table, x, i)
    #                 elif (headers[i].text() == "Block Number"):
    #                     new_block.number = int(file.get_cell_text(table, x, i))
    #                 elif (headers[i].text() == "Block Length (m)"):
    #                     new_block.length = int(file.get_cell_text(table, x, i))
    #                 elif (headers[i].text() == "Block Grade (%)"):
    #                     new_block.grade = int(file.get_cell_text(table, x, i))
    #                 elif (headers[i].text() == "Speed Limit (Km/Hr)"):
    #                     new_block.commanded_speed = file.get_cell_text(table, x, i)
    #                 elif (headers[i].text() == "ELEVATION (M)"):
    #                     new_block.elevation = file.get_cell_text(table, x, i)
    #                 elif (headers[i].text() == "Infrastructure"):
    #                     self.load_infra_values(file, table, new_block, x, i)

    #         ## Add new block to block list for correct line
    #         line.blocks.append(new_block)

    #     ## Set beacon values for the blocks
    #     for j in range(table.rowCount()):
    #         self.set_beacon_values(line, line.get_block(j))

    # ## Load string values from the infrastructure section of the track information sheet
    # def load_infra_values(self, file, table, block, row, col):
    #     ## Get station and other infrastructure information
    #     infra = file.get_cell_text(table, row, col)

    #     ## Create rail crossing on corresponding block
    #     if (infra == "RAILWAY CROSSING"):
    #         rail = RailwayCrossing()
    #         block.set_rail_cross(rail)

    #     ## Create station, set beacon
    #     elif (infra.find("STATION") != -1):
    #         station = Station()
    #         block.set_station(station)

    #         ## Get station name
    #         #  infra[0:8] = "STATION: "
    #         semicolon = infra.find(";", 8)
    #         #  ex: STATION; PENN STATION; UNDERGROUND
    #         if (semicolon != -1):
    #             n = infra[8:semicolon]
    #             name = n.strip()
    #         #  ex: STATION; HERRON AVE
    #         else:
    #             n = infra[8:]
    #             name = n.strip()
            
    #         ## Set name to corresponding station
    #         block.get_station().set_name(name)

    # ## Call function after all blocks for each line are set
    # def set_beacon_values(self, line, block):
    #     station1 = ""
    #     station2 = ""
    #     side = ""

    #     ## Create new beacon for each block
    #     block.beacon = Beacon(station1, station2, side)

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
    #             if next_station is not None:
    #                 station2 = next_station
    #                 break

    #     ## Send previous and next station data to the corresponding block
    #     block.set_beacon(station1, station2, side)

    # ## Add light signals to the track model
    # def add_lights(self):
    #     # Light signals on the red line
    #     # forked to by switch
    #     line = self.lines[0]
    #     red_lights = [1, 13, 28, 76, 77, 85, 98, 150]
    #     for r in red_lights:
    #         line.get_block(r).set_light(Light())
    #     # at station block
    #     for y in range(len(line)):
    #         if line.get_block(y).get_station() is not None:
    #             line.get_block(r).set_light(Light())

    #     # Light signals on the green line
    #     line1 = self.lines[1]
    #     green_lights = [1, 15, 27, 32, 38, 43, 52, 66, 67, 71, 72, 76]
    #     for g in green_lights:
    #         line1.get_block(g).set_light(Light())
    #     # at station block
    #     for y in range(len(line)):
    #         if line.get_block(y).get_station() is not None:
    #             line.get_block(y).set_light(Light())

    ## Set up current block values table
    def curr_table_setup(self, current_table):
        # Create new array of QWidget Items
        for x in range(12):
            self.current.append(QTableWidgetItem())
        
        current_table.setColumnCount(1)
        current_table.setRowCount(12)
        current_table.setHorizontalHeaderLabels([''])
        current_table.setVerticalHeaderLabels(['Line', 'Section', 'Block #', 'Block Length',
                                                'Block Grade (%)', 'Commanded Speed (mph)', 'Authority (blocks)',
                                                'Elevation', 'Failure', 'Stop Signal', 'Beacon', 'Block Occupancy'])

    ## Fill in table with current values
    def set_current(self, line, block):
        # Set current values for the corresponding block
        self.current[0].setText(line.get_name())
        self.current[1].setText(block.get_section())
        self.current[2].setText(str(block.get_number()))
        self.current[3].setText(str(block.get_length()))
        self.current[4].setText(str(block.get_grade()))
        self.current[5].setText(str(block.get_commanded_speed()))
        self.current[6].setText(str(block.get_authority()))
        self.current[7].setText(str(block.get_elevation()))
        self.current[8].setText(str(block.get_failure_status()))
        self.current[9].setText(block.get_light_status())
        self.current[10].setText(block.get_beacon())
        self.current[11].setText(str(block.get_occupancy()))

    ## Print values to the main GUI
    def print_table(self, table):
        # self.set_current(self.lines[0], self.lines[0].get_block(13))
        # Iterate through current[] values list, print to GUI table
        for i in range(len(self.current)):
            table.setItem(0, i, self.current[i])

    # ## Return which line the block is on
    # def get_line(self, block):
    #     for l in self.lines:
    #         for b in l.blocks:
    #             if b == block:
    #                 return l
    #             else:
    #                 return None
        


    # ## SIGNAL SECTION
    # #  Initial set up of transmitted signals
    # def track_model_signals(self):
    #     # update signal
    #     signals.tm_update.connect(self.refresh_track)
        
    #     # signals sent to track model
    #     signals.send_track_authority.connect(self.refresh_authority)
    #     signals.send_track_speed.connect(self.refresh_speed)
        
    #     # signals broadcast to all modules
    #     signals.broadcast_switch.connect(self.refresh_switch)
    #     signals.broadcast_light.connect(self.refresh_light)
    #     signals.broadcast_gate.connect(self.refresh_gate)

    # #  Signal update functions
    # @pyqtSlot(str, int)
    # def signal_occupancy(self, block, occupancy):
    #     t = True; i = 0
    #     line = self.get_line(block)
    #     if line is not None:
    #         while(t):
    #             if (block == line.get_block(i)):
    #                 self.line.get_block(i).set_occupancy(occupancy)
    #                 t = False
    #                 break

    # # @pyqtSlot(str, int)
    # # def signal_failure(self, block, failure):

    # # @pyqtSlot(str, int)
    # # def signal_authority(self, block, authority):

    # # @pyqtSlot(str, int)
    # # def signal_grade(self, block, grade):

    # # @pyqtSlot(str, str, str, str)
    # # def signal_beacon(self, block, station1, station2, side):

    # # @pyqtSlot(str, int)
    # # def signal_passenger_count(self, station, passenger_count):