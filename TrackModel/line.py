from block import *
from linked_list import *

class Line:
    def __init__(self, name):
        self.name = name
        #self.blocks = doubly_linked_list()
        self.blocks = []
        self.line_ticket_sales = 0
        self.total_length = 0

    def propogate_line(self, max):
        for x in range(max):
            section = ''
            number = 0
            new_block = Block(section, number)

            ## Add new block to block list for correct line
            self.blocks.append(new_block)

    ## Returns block object by calling the block number
    def get_block(self, number):
        return self.blocks[number]

    def get_blocks(self):
        return self.blocks

    def get_name(self):
        return self.name

    ## Calculates the total track length of the line
    def calc_line_length(self):
        for b in self.blocks:
            self.total_length += b.get_length()
        
        ## Section that are passed over twice
        sections = []
        if (self.name == "Green Line"):
            sections = ['D', 'E', 'F', 'G']
        if (self.name == "Red Line"):
            sections = ['F', 'G', 'H', 'I', 'J']
        for section in sections:
            for b in self.blocks:
                if (b.get_section() == section):
                    self.total_length += b.get_length()