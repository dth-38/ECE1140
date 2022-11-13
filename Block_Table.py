from signals import signals

#TODO: GET BLOCK SWITCH POSITIONS FROM TRACK CONTROLLER TO SWITCH THEM AT THAT POSITION IN SET MAINTENANCE
class Block_Table: 
    def __init__(self):
        self.table = []
        self.maintenance_signal = False
        signals.update_switches.connect(self.get_switch_status)
        signals.update_states.connect(self.get_states)
    #TODO: GET STATES(BLOCK OCC, BLOCK FAILURE FROM TRACK CONTROLLER)
    def add_entry(self,blk,states):
        print("ADD BLOCK ENTRY!!!!!!")
        self.table.append([blk,states])
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
    


