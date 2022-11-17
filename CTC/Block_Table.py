#from signals import signals

#TODO: GET BLOCK SWITCH POSITIONS FROM TRACK CONTROLLER TO SWITCH THEM AT THAT POSITION IN SET MAINTENANCE


class Block_Table: 
    def __init__(self):
        self.table = []
        self.maintenance_signal = False
        self.length = 0
        """"
        signals.update_switches.connect(self.get_switch_status)
        signals.update_states.connect(self.get_states)
        """
    #TODO: GET STATES(BLOCK OCC, BLOCK FAILURE FROM TRACK CONTROLLER)
    def add_entry(self,blk,states):
        print("ADD BLOCK ENTRY!!!!!!")
        self.table.append([blk,states])
        self.length += 1
    def add_occupancy(self,line,block_num,occ):
        self.table.append(["Occupancy",line,block_num,occ])
        self.length += 1
    def add_failure(self,line,block_num,failure):
        self.table.append(["Failure",line,block_num,failure])
        self.length += 1
    def add_switch(self,line,block_num,next_block_num):
        self.table.append(["Switch",line,block_num,next_block_num])
        self.length += 1
    def add_light(self,line,block_num,color):
        self.table.append(["Light",line,block_num,color])
        self.length += 1
    def add_gate(self,line,block_num,status):
        self.table.append([line,block_num,status])
        self.length += 1
    def set_maintenance(self,blk,section,line):
        print("MAINTENANCE SET!!!!!!")
        #TODO: CHANGE BLOCK SWITCH POSITIONS FROM TRACK CONTROLLER AND SWITCH THEM IF NEEDED FOR MAINTENANCE
        self.maintenance_signal = True
    def remove_entry(self):
        print("BLOCK ENTRY REMOVED!!!!!")
        self.table.pop(0)
    def get_entry(self,position):
        return self.table[position]
    def get_maintenance_signal(self):
        return self.maintenance_signal
    def get_table_length(self):
        return self.length

    


