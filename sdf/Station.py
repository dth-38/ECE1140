from re import L


class Station:
    def __init__(self,label,dwell_time,ticket_sales):
        self.label = label 
        self.dwell_time = dwell_time
        self.ticket_sales = ticket_sales
    def get_dwell_time(self):
        return self.dwell_time
    def set_dwell_time(self,time):
        self.dwell_time = time
    def get_ticket_sales(self):
        return self.ticket_sales
    def set_ticket_sales(self,sales):
        self.ticket_sales = sales
    def get_label(self):
        return self.label
    def set_label(self,location):
        self.label = location
