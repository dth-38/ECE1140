

class Block:

    def __init__(self):
        self.id = ""
        self.forward_Authority = 0
        self.backward_Authority = 0
        self.suggested_Speed = 0
        self.commanded_Speed = 0
        self.occupied = False
        self.failed = False
        self.closed = False
        self.switches = []
        self.lights = []
        self.gates = []
        
        

    #adds a switch to the block
    def add_Switch(self):
        self.switches.append(0)

    #removes the last switch from the list
    def remove_Switch(self):
        if self.switches != []:
            self.switches.pop()

    #toggles the state of the specified switch
    def toggle_Switch(self, switchNum):
        self.switches[switchNum] = ~self.switches[switchNum]

    #adds a gate to the block
    def add_Gate(self):
        self.gates.append(0)

    #removes the last gate from the list
    def remove_Gate(self):
        if self.gates != []:
            self.gates.pop()

    #toggles the state of the specified gate
    def toggle_Gate(self, gateNum):
        self.gates[gateNum] = ~self.gates[gateNum]

    
    #adds a light to the block
    def add_Light(self):
        self.lights.append([1, 0, 0])

    #removes a light from the list
    def remove_Light(self):
        if self.lights != []:
            self.lights.pop()

    #possible colors are (r)ed, (y)ellow, or (g)reen
    #they are represented as an array of 3 bits, each bit corresponding to a color
    def set_Light(self, lightNum, color):
        if color == 'YELLOW':
            temp = [0, 1, 0]
        elif color == 'GREEN':
            temp = [0, 0, 1]
        else:
            temp = [1, 0, 0]

        self.lights[lightNum] = temp

    #gets a light's color as a string
    def light_To_Str(self, lightNum):
        light = self.lights[lightNum]

        if light == [1, 0, 0]:
            color = "RED"
        elif light == [0, 1, 0]:
            color = "YELLOW"
        elif light == [0, 0, 1]:
            color = "GREEN"
        else:
            color = "NONE"

        return color

    #gets a switch's position as a string
    def switch_To_Str(self, switchNum):
        switch = self.switches[switchNum]

        if switch:
            switch_Str = "ON"
        else:
            switch_Str = "OFF"

        return switch_Str

    #gets a gate's status as a string
    def gate_To_Str(self, gateNum):
        gate = self.gates[gateNum]

        if gate:
            gate_Str = "OPEN"
        else:
            gate_Str = "CLOSED"

        return gate_Str
