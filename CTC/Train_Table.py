

class Train_Table:
    def __init__(self):
        self.table = []
        self.destinations_count = 1
    def add_entry(self,id,position,states,destinations,authority,line,arrival_time):
        print("ADD TRAIN ENTRY!!!!!")
        #create instance of the train
        #a_train = new trainmodel()
        self.table.append([id,position,states,destinations,authority,line,arrival_time])
    def remove_entry(self):
        print("REMOVE TRAIN ENTRY!!!!")
        #Remove first entry from table
        self.table.pop(0)
    def get_next_destination(self,position):
        destinations = self.table[position][3]
        self.destinations_count += 1
        return destinations[self.destinations_count - 1]
    def get_train_destinations(self,position):
        return self.table[position][3]
    def get_train_id(self,position):
        return self.table[position][0]
    def get_position(self,position):
        return self.table[position][1]
    def get_line(self,position):
        return self.table[position][5]
    def get_authority(self,position):
        return self.table[position][4]
    def get_train_states(self,position):
        return self.table[position][2]
    def get_entry(self,position):
        return self.table[position]
    def get_table_length(self):
        return len(self.table)
    def change_authority(self,position,authority):
        if len(self.table) > 0:
            #print("authority: " + str(authority))
            self.table[position][4] = authority
    def change_position(self,position,location):
        if len(self.table) > 0:
            #print("location:" + str(location))
            self.table[position][1] = location
