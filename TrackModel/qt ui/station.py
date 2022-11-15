class Station:
    def __init__(self, line, block):
        self.ticket_sales = 0
        self.line = line
        self.block = block
        self.train_occupancy = 0
        self.train_at_station = FALSE

    def calculate_occupancy(self, p_on, p_off):
        self.train_occupancy = self.train_occupancy - p_off + p_on