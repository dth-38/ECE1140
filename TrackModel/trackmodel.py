from TrackModel.line import *
from TrackModel.heater import *
from TrackModel.trainloc import *
from TrackModel.track_info import *
from TrainModel.Train import Train
from Signals import signals

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

        # Track layout file
        self.file = TrackInfo(fp = "C:/Users/rachs/OneDrive/Documents/ECE1140/ECE1140/TrackModel/track_layout_2.0.xlsx") 

        # Used to show the train moving correctly for Iteration #3 only
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

    ## Get position of train, change block occupancy
    def get_position(self, train):
        return train.position

    ## Current distance traveled --> block number
    def get_train_block_position(self, line, train):
        # after yard
        start_block = line.get_block(63)

        # distance <= 5412
        before_Nswitch = 0
        for b in range(63, 101):
            before_Nswitch = before_Nswitch + line.get_block(b).get_length()
        print(before_Nswitch)

        # 5412 < distance <= 7812 
        n = 0
        for b in range(77, 86):
            n = n + line.get_block(b).get_length()
        print(n)

        # 7812 < distance <= 11143
        after_N = 0
        for b in range(101, 150):
            after_N = after_N + line.get_block(b).get_length()
        print(after_N)

        # 11143 < distance <= 18424
        after_Z = 0
        for b in range(0, 29):
            after_Z = after_Z + line.get_block(b).get_length()
        print(after_Z)

        # 18424 < distance <= 21174
        fed = 0
        for b in range(13, 29):
            fed = fed + line.get_block(b).get_length()
        print(fed)

        # 21174 < distance <= 22574
        ghi = 0
        for b in range(29, 58):
            ghi = ghi + line.get_block(b).get_length()
        print(ghi)

        j = 0
        for b in range(58, 63):
            j = j + line.get_block(b).get_length()
        print(j)

        end = self.get_position(train)
        temp = end
        if (end <= before_Nswitch):
            for i in range(100, 62, -1):
                temp = temp - line.blocks(i).get_length()
                s = self.get_end_block_pos(line, line.get_block(i), 63)
                if (temp < s):
                    train_block = line.get_block(i)

        return train_block

    def get_end_block_pos(line, block, start):
        s = 0
        for i in range(start, block):
            s = s + line.get_block(i).get_length()
        return s


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
        self.file.set_dimensions()

        ## Set line names
        self.lines.append(Line("Red Line"))
        self.lines.append(Line("Green Line"))
        
        ## Get header labels from the file
        headers = []
        for y in range(9):
            if (red_table.horizontalHeaderItem(y).text() == green_table.horizontalHeaderItem(y).text()):
                headers.append(red_table.horizontalHeaderItem(y).text())

        self.create_blocks_list(self.file, self.lines[0], red_table, headers)
        self.create_blocks_list(self.file, self.lines[1], green_table, headers)

        self.get_train_block_position(self.lines[1])

        # self.start_linked_block_list(red_table, headers, self.lines[0])
        # self.start_linked_block_list(green_table, headers, self.lines[1])

        # #self.finish_linked_block_list(red_table, headers, self.lines[0])
        # self.finish_linked_block_list(green_table, headers, self.lines[1])

        # self.lines[0].blocks.tracklistprint(self.lines[0].blocks.head)
        # self.lines[1].blocks.tracklistprint(self.lines[1].blocks.head)

        # ## Set up block lists for the red and green lines
        # self.create_blocks(file, self.lines[0], red_table, headers)
        # self.create_blocks(file, self.lines[1], green_table, headers)

        # ## Calculate total track length for green and red lines
        # self.lines[0].calc_line_length()
        # self.lines[1].calc_line_length()

    def start_linked_block_list(self, table, headers, line):
        # Set to red line, create new block for yard, append head node
        yard_head_node = line.blocks_list[0]
        line.blocks.append(yard_head_node)
        
        # Find node after/before yard to start the list
        section_col = headers.index("Section")
        number_col = headers.index("Block Number")
        infra_col = headers.index("Infrastructure")
        for x in range(table.rowCount()):
            # Get text value in the "Infrastructure" column
            text = self.file.get_cell_text(table, x, infra_col).lower()

            # Set section, number to the current table entry's values and 
            # create a new block, but don't add it to the list yet
            new_section = self.file.get_cell_text(table, x, section_col)
            new_number = self.file.get_cell_text(table, x, number_col)
            new_block = line.blocks_list[int(new_number)]

            # Only 1 block leads in/out of the yard
            if (text.find("to/from") != -1):
                # get block number from switch direction (if different from current
                # table block number)
                i = text.find("(") + 1
                j = text.find("-")
                new_number = text[i:j]
                new_block = line.blocks_list[int(new_number)]
                # add block to linked list, next node is set to the new_block node
                line.blocks.append(new_block)
                # set prev node to the new_block node also
                line.blocks.head.prev = line.blocks.head.next
            
            # Block only leads into the yard
            elif (text.find(" to yard ") != -1):
                # get block number from switch direction (if different from current
                # table block number)
                i = text.find("(") + 1
                j = text.find("-")
                new_number = text[i:j]
                new_block = line.blocks_list[int(new_number)]
                # create new_block node, set prev node of head node to the
                # new_block node (yard is still head)
                new_block_node = Node(new_block)
                line.blocks.head.prev = new_block_node

            # Block only leads out of the yard
            elif (text.find(" from yard ") != -1):
                # get block number from switch direction (if different from current
                # table block number)
                i = text.find(")")
                j = text.find("-") + 1
                new_number = text[j:i]
                new_block = line.blocks_list[int(new_number)]
                # add block to linked list, next node is set to the new_block node
                line.blocks.append(new_block)



    def set_block_stops(self, block_stops, switches):
        # get next block number
        # switches[switch[pair1[i,j], pair2[i,j]]]
        for switch in switches:
            for pair in switch:
                for block in pair:
                    block_stops.append(block)

    def parse_switch_text(self, switch):
        # parse out block numbers from infrastructure text
        n = []; first_pair = []; second_pair = []
        first = switch[switch.find("(") : (switch.find(";") + 1)]
        second = switch[switch.find(";") : (switch.find(")") + 1)]

        string_nums = []
        for i in range(0, 150):
            s = str(i)
            string_nums.append(s)

        found1 = []; found2 = []
        for num in string_nums:
            ff = int(num) in found1
            sf = int(num) in found2
            p1 = first.find(num)
            p2 = second.find(num)

            # get correct value, not just all ints in the string, and add it
            # to the corresponding switch pairs
            if (p1 != -1) and (not ff):
                f1 = first[p1 : (p1 + 2)] in string_nums
                f2 = first[p1 : (p1 + 3)] in string_nums
                if (f1) and (not f2):
                    first_pair.append(int(first[p1 : (p1 + 2)]))
                    found1.append(int(first[p1 : (p1 + 2)]))
                elif (f2):
                    first_pair.append(int(first[p1 : (p1 + 3)]))
                    found1.append(int(first[p1 : (p1 + 3)]))

            if (p2 != -1) and (not sf):
                s1 = second[p2 : (p2 + 2)] in string_nums
                s2 = second[p2 : (p2 + 3)] in string_nums
                if (s1) and (not s2):
                    if (not (int(second[p2 : (p2 + 2)]) in found2)):
                        second_pair.append(int(second[p2 : (p2 + 2)]))
                        found2.append(int(second[p2 : (p2 + 2)]))
                elif (s2):
                    if (not (int(second[p2 : (p2 + 3)]) in found2)):
                        second_pair.append(int(second[p2 : (p2 + 3)]))
                        found2.append(int(second[p2 : (p2 + 3)]))

        # add block numbers in pairs (corresponding switches) to n[]
        n.append(first_pair)
        n.append(second_pair)

        return n

    def switch_add_nodes(self, number, switches):
        print("switch node time")
        new_number = 0

        # get next block number
        # switches[switch[pair1[i,j], pair2[i,j]]]
        for switch in switches:
            for pair in switch:
                if (number in pair):
                    for block in pair:
                        if (number != block):
                            print(block)
                            new_number = block

        return new_number


    def create_blocks_list(self, file, line, table, headers):
        ## Add yard as the first block to blocks_list (at index 0)
        line.blocks.append(Block(0,0))

        ## Create block lists
        for x in range(table.rowCount()):
            section = ''
            number = 0
            new_block = Block(section, number)

            ## Get section, number, length, grade, speed limit, and elevation for new block
            for i in range(len(headers)):
                if headers[i] is not None:
                    if (headers[i] == "Section"):
                        new_block.section = file.get_cell_text(table, x, i)
                    elif (headers[i] == "Block Number"):
                        new_block.number = int(file.get_cell_text(table, x, i))
                    elif (headers[i] == "Block Length (m)"):
                        new_block.length = int(file.get_cell_text(table, x, i))
                    elif (headers[i] == "Block Grade (%)"):
                        new_block.grade = int(file.get_cell_text(table, x, i))
                    elif (headers[i] == "Speed Limit (Km/Hr)"):
                        new_block.commanded_speed = file.get_cell_text(table, x, i)
                    elif (headers[i] == "ELEVATION (M)"):
                        new_block.elevation = file.get_cell_text(table, x, i)
                    elif (headers[i] == "Infrastructure"):
                        self.load_infra_values(file, table, new_block, x, i)

            ## Add new block to block list for correct line
            line.blocks.append(new_block)
            print(str(x) + ": ", end="")
            print(line.blocks[x].get_number())

    ## Load string values from the infrastructure section of the track information sheet
    def load_infra_values(self, file, table, block, row, col):
        ## Get station and other infrastructure information
        infra = file.get_cell_text(table, row, col)
        block.set_infra(infra)

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

    ## Add light signals to the track model
    def add_lights(self):
        # Light signals on the red line
        # forked to by switch
        line = self.lines[0]
        red_lights = [1, 13, 28, 76, 77, 85, 98, 150]
        for r in red_lights:
            line.get_block(r).set_light(Light())
        # at station block
        for y in range(len(line)):
            if line.get_block(y).get_station() is not None:
                line.get_block(r).set_light(Light())

        # Light signals on the green line
        line1 = self.lines[1]
        green_lights = [1, 15, 27, 32, 38, 43, 52, 66, 67, 71, 72, 76]
        for g in green_lights:
            line1.get_block(g).set_light(Light())
        # at station block
        for y in range(len(line)):
            if line.get_block(y).get_station() is not None:
                line.get_block(y).set_light(Light())

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



    @pyqtSlot()
    def setup_signals(self):
        signals.tm_update.connect(self.tick)
        signals.send_track_authority.connect(self.handle_authority)
        signals.send_track_speed.connect(self.handle_speed)
        signals.broadcast_switch.connect(self.handle_switch)
        signals.broadcast_light.connect(self.handle_light)
        signals.broadcast_gate.connect(self.handle_gate)
        signals.send_tm_distance.connect(self.handle_distance)

    @pyqtSlot(str, int, int)
    def handle_speed(self, line, block_num, speed):
        pass   

    @pyqtSlot(str, int, int)
    def handle_switch(self, line, block_num, next_block_num):
        pass

    @pyqtSlot(str, int, str)
    def handle_light(self, line, block_num, color):
        pass

    @pyqtSlot(str, int, str)
    def handle_gate(self, line, block_num, position):
        pass

    @pyqtSlot(int, float)
    def handle_distance(self, train_id, distance):
        pass

    #update for the whole track model
    @pyqtSlot()
    def tick(self):
        pass

    @pyqtSlot(str, int, int)
    def handle_authority(self, line, block_num, authority):
        pass

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


    # #  Refresh track function
    # @pyqtSlot()
    # def refresh_track():


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

    # @pyqtSlot(str, int)
    # def signal_failure(self, block, failure):

    # @pyqtSlot(str, int)
    # def signal_authority(self, block, authority):

    # @pyqtSlot(str, int)
    # def signal_grade(self, block, grade):

    # @pyqtSlot(str, str, str, str)
    # def signal_beacon(self, block, station1, station2, side):

    # @pyqtSlot(str, int)
    # def signal_passenger_count(self, station, passenger_count):












    def finish_linked_block_list(self, table, headers, line):
        # list to hold switch numbers
        switches = []
        block_stops = []

        # Second node in the current linked list, i.e. the first block of track the
        # train goes on after the yard
        head_node = line.blocks.head
        second_node = head_node.next
        first_block_number = second_node.get_block_number()
        
        # Find next node to add to the linked list
        section_col = headers.index("Section")
        number_col = headers.index("Block Number")
        infra_col = headers.index("Infrastructure")
        x = first_block_number
        x_before_switch = -1
        while(x < 121):
            # Set section, number to the current table entry's values and 
            # create a new block, but don't add it to the list yet
            new_number = x
            print(x)
            new_block = line.blocks_list[int(x)]

            # Get text value in the "Infrastructure" column
            text = new_block.infra_text.lower()

            # Block has a switch
            if (text.find("switch (") != -1):
                # get block numbers (4 total) for the switch, save in n[]
                i = text.find("(")
                j = text.find(")") + 1
                s = self.parse_switch_text(text[i:j])
                switches.append(s)
                self.set_block_stops(block_stops, switches)

            # If current block is at a switch, call switch function to add nodes
            # Add block node to linked list
            line.blocks.append(new_block)
            x1 = -1
            if (int(new_number) in block_stops):
                x_before_switch = x
                #if ()
                x1 = self.switch_add_nodes(new_number, switches)
                line.blocks.append(line.blocks_list[int(x1)])

        # end_index = first_block_number - 1
        # for x in range(0, end_index):
        #     # Get text value in the "Infrastructure" column
        #     text = self.file.get_cell_text(table, x, infra_col).lower()

        #     # Set section, number to the current table entry's values and 
        #     # create a new block, but don't add it to the list yet
        #     new_section = self.file.get_cell_text(table, x, section_col)
        #     new_number = self.file.get_cell_text(table, x, number_col)
        #     new_block = line.blocks_list[int(new_number)]

        #     # Add block to linked list
        #     line.blocks.append(new_block)

                # get highest block number, add it to block_stops[] list
                # m = 0
                # for i in range(2):
                #     if (max(s[i]) > m):
                #         m = max(s[i])
                # block_stops.append(m)
            
            # Go backwards through already traversed block if switched
            if (x1 != -1):
                x = x1
            if (x < x_before_switch):
                x = x - 1
            else:
                x = x + 1

            # # Nothing listed in infrastructure column, normal node
            # else:
            #     # add block to linked list, next node is set to the new_block node
            #     line.blocks.append(new_block)

        print(switches)
        print(block_stops)