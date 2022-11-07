class Block:

    def __init__(self,name, station, block_length, grade):
        self.name = name                    #name of block
        self.station = station              #name of station, "" if no station
        self.block_length = block_length    #length of block, meters
        self.grade = grade                  #percentage. float