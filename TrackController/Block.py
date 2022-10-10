

class Block:
    id = ""
    forwardAuthority = 0
    backwardAuthority = 0
    suggestedSpeed = 0
    commandedSpeed = 0
    occupied = False
    failed = False
    closed = False
    switches = []
    lights = []
    gates = []

    def __init__(self):
        pass

    #adds a switch to the block
    def addSwitch(self):
        self.switches.append(0)

    #toggles the state of the specified switch
    def toggleSwitch(self, switchNum):
        self.switches[switchNum] = ~self.switches[switchNum]
        return self.switches[switchNum]

    #adds a gate to the block
    def addGate(self):
        self.gates.append(0)

    #toggles the state of the specified gate
    def toggleGate(self, gateNum):
        self.gates[gateNum] = ~self.gates[gateNum]
        return self.gates[gateNum]
    

    #adds a light to the block
    def addLight(self):
        self.lights.append([1, 0, 0])

    #possible colors are (r)ed, (y)ellow, or (g)reen
    #they are represented as an array of 3 bits, each bit corresponding to a color
    def setLight(self, lightNum, color):
        if color == 'y':
            temp = [0, 1, 0]
        elif color == 'g':
            temp = [0, 0, 1]
        else:
            temp = [1, 0, 0]

        self.lights[lightNum] = temp
        return self.lights[lightNum]


