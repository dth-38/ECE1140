

class Block:
    id = ""
    forward_Authority = 0
    backward_Authority = 0
    suggested_Speed = 0
    commanded_Speed = 0
    occupied = False
    failed = False
    closed = False
    switches = []
    lights = []
    gates = []

    def __init__(self):
        pass

    #adds a switch to the block
    def add_Switch(self):
        self.switches.append(0)

    #toggles the state of the specified switch
    def toggle_Switch(self, switchNum):
        self.switches[switchNum] = ~self.switches[switchNum]
        return self.switches[switchNum]

    #adds a gate to the block
    def add_Gate(self):
        self.gates.append(0)

    #toggles the state of the specified gate
    def toggle_Gate(self, gateNum):
        self.gates[gateNum] = ~self.gates[gateNum]
        return self.gates[gateNum]
    

    #adds a light to the block
    def add_Light(self):
        self.lights.append([1, 0, 0])

    #possible colors are (r)ed, (y)ellow, or (g)reen
    #they are represented as an array of 3 bits, each bit corresponding to a color
    def set_Light(self, lightNum, color):
        if color == 'y':
            temp = [0, 1, 0]
        elif color == 'g':
            temp = [0, 0, 1]
        else:
            temp = [1, 0, 0]

        self.lights[lightNum] = temp
        return self.lights[lightNum]


