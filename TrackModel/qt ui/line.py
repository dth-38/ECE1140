from block import *

class Line:
    def __init__(self, name):
        self.name = name
        self.blocks = []
        self.line_ticket_sales = 0

    def get_block(self, number):
        for i in range(len(self.blocks)):
            if (self.blocks[i].getNumber() == number):
                return self.blocks[i]