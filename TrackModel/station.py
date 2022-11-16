class Station:
    def __init__(self):
        self.name = ""
        self.ticket_sales = 0
        self.train_occupancy = 0
        self.train_at_station = False

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def calculate_occupancy(self, p_on, p_off):
        self.train_occupancy = self.train_occupancy - p_off + p_on