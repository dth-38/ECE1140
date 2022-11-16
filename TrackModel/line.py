from block import *

class Line:
    def __init__(self, name):
        self.name = name
        self.blocks = []
        self.line_ticket_sales = 0
        self.total_length = 0

    ## Returns block object by calling the block number
    def get_block(self, number):
        return self.blocks[number]

    def get_name(self):
        return self.name

    ## Calculates the total track length of the line
    def calc_line_length(self):
        for b in self.blocks:
            self.total_length += b.get_length()