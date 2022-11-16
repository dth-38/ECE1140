
#block constants for switches
TO_NONE = 0
TO_NEXT = 1
TO_PREV = 2

class Block:

    def __init__(self, id = ""):
        #constants for if the switch is connected to next blocks or previous blocks

        self.id = id
        self.authority = 0
        self.suggested_Speed = 0
        self.commanded_Speed = 0
        self.max_Speed = 0
        self.previous_Blocks = []
        self.next_Blocks = []
        self.occupied = False
        self.failed = False
        self.closed = False
        self.is_Exit = False
        self.switch_To = TO_NONE
        self.switches = []
        self.lights = []
        self.gates = []
        
#------------------------------------------------
# ONLY TO BE USED BY TOKENIZER/INTERPRETER
#------------------------------------------------
    def set_Field(self, field, index=0, color=0, val=0):
        match field:
            case "occupied":
                self.occupied = val
            case "light":
                self.lights[index][color] = val
            case "gate":
                self.gates[index] = val
            case "failed":
                self.failed = val
            case "closed":
                self.closed = val
            case "switch":
                self.switches[index] = val
            case _:
                return False

        return True
    
    def get_Field(self, field, index=0, color=0):
        val = 0

        match field:
            case "occupied":
                val = self.occupied
            case "light":
                val = self.lights[index][color]
            case "gate":
                val = self.gates[index]
            case "failed":
                val = self.failed
            case "closed":
                val = self.closed
            case "switch":
                val = self.switches[index]
            case "exit":
                val = self.is_Exit
            case _:
                pass

        return val

#---------------------------------------------------------
# MUTATORS & ACCESSORS FOR SWITCHES
#---------------------------------------------------------
    #adds a switch to the block
    def add_Switch(self, dir, off, on):
        self.switches.append(0)
        if dir == "NEXT":
            self.switch_To = TO_NEXT
            self.next_Blocks.append(off)
            self.next_Blocks.append(on)
        else:
            self.switch_To = TO_PREV
            self.previous_Blocks.append(off)
            self.previous_Blocks.append(on)


    #removes the last switch from the list
    def remove_Switch(self):
        if self.switches != []:
            self.switches.pop()

    #toggles the state of the specified switch
    def toggle_Switch(self, switchNum):
        self.switches[switchNum] = ~self.switches[switchNum]

    def set_Switch(self, switchNum=0, state=False):
        self.switches[switchNum] = state

    def get_Switch(self, switchNum=0):
        return self.switches[switchNum]

    #gets a switch's position as a string
    def switch_To_Str(self, switchNum=0):
        switch = self.switches[switchNum]

        if switch == True:
            switch_Str = "ON"
        else:
            switch_Str = "OFF"

        return switch_Str

    def get_switched_to(self, switchNum=0):
        block = ""

        if self.switch_To == TO_PREV:
            if self.switches[switchNum] == True:
                block = self.previous_Blocks[1]
            else:
                block = self.previous_Blocks[0]
        elif self.switch_To == TO_NEXT:
            if self.switches[switchNum] == True:
                block = self.next_Blocks[1]
            else:
                block = self.next_Blocks[0]
        else:
            pass

        return block

            

#---------------------------------------------------------
# MUTATORS & ACCESSORS FOR GATES
#---------------------------------------------------------
    #adds a gate to the block
    def add_Gate(self):
        self.gates.append(0)

    #removes the last gate from the list
    def remove_Gate(self):
        if self.gates != []:
            self.gates.pop()

    #toggles the state of the specified gate
    def toggle_Gate(self, gateNum=0):
        self.gates[gateNum] = ~self.gates[gateNum]

    def set_Gate(self, gateNum=0, state=False):
        self.gates[gateNum] = state

    def get_Gate(self, gateNum=0):
        return self.gates[gateNum]

    #gets a gate's status as a string
    def gate_To_Str(self, gateNum=0):
        gate = self.gates[gateNum]

        if gate == True:
            gate_Str = "OPEN"
        else:
            gate_Str = "CLOSED"

        return gate_Str

#--------------------------------------------------------
# MUTATORS & ACCESSORS FOR LIGHTS
#--------------------------------------------------------

    #adds a light to the block
    def add_Light(self):
        self.lights.append([1, 0])

    #removes a light from the list
    def remove_Light(self):
        if self.lights != []:
            self.lights.pop()

    #possible colors are red, yellow, or green
    #they are represented as an array of 3 bits, each bit corresponding to a color
    def set_Light(self, lightNum=0, color="RED"):
        color.upper()

        match color:
            case 'GREEN':
                temp = [0, 1]
            case _:
                temp = [1, 0]

        self.lights[lightNum] = temp

    #gets a light's color as a string
    def light_To_Str(self, lightNum=0):
        light = self.lights[lightNum]

        if light == [1, 0]:
            color = "RED"
        elif light == [0, 1]:
            color = "GREEN"
        else:
            color = "NONE"

        return color


#--------------------------------------------------------------------
# ACCESSORS FOR NEXT/PREVIOUS BLOCKS SINCE THEY HAVE CUSTOM LOGIC
#--------------------------------------------------------------------
    def get_Next_Block(self):
        if self.switch_To == TO_NEXT:
            val = int(self.switches[0])
        else:
            val = 0

        return self.next_Blocks[val]

    def get_Previous_Block(self):
        if self.switch_To == TO_PREV:
            val = int(self.switches[0])
        else:
            val = 0
        
        return self.previous_Blocks[val]