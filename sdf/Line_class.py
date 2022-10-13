class Line:
    def __init__(self,label,sales=0):
        self.label = label
        self.ticket_sales = sales
        self.throughput = 0
    def get_label(self):
        return self.label
    def set_label(self,lab):
        self.label = lab
    def get_throughput(self):
        return self.throughput
    def get_ticket_sales(self):
        return self.ticket_sales
    def set_ticket_sales(self,s):
        self.ticket_sales = s
    def set_throughput(self,through):
        self.throughput = through
    def calc_throughput(self,hours):
        self.throughput = self.ticket_sales/hours
