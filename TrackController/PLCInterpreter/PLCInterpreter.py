from re import A
import time
from PLCInterpreter import Token

class PLCInterpreter:

    def __init__(self, env=0):
        #defines instruction constants
        self.CONST_EQ = 0
        self.CONST_NOT = 1
        self.CONST_AND = 2
        self.CONST_OR = 3
        self.CONST_B = 4
        self.CONST_BEQ = 5
        self.CONST_BNE = 6



        #dictionary storing program counter values using labels as keys
        self.jump_Table = {}
        #logic tokens
        self.logic = []
        #tracks if a program has been successfully tokenized
        self.status = False
        #program counter
        self.pc = 0
        #execution environment
        self.environment = env
        #temporary registers
        self.t = [0] * 10
    
    def set_Environment(self, env):
        self.environment = env

    #executes plc logic
    #env is the environment or track state to be modified
    def execute(self, timeout=0):
        self.pc = 0
        program_Length = len(self.logic)
        self.t = [0] * 10

        start_Time = time.perf_counter()

        while self.pc < program_Length:
            self.interpret(self.logic[self.pc])
            self.pc += 1

            elapsed_Time = time.perf_counter() - start_Time
            if elapsed_Time > timeout:
                return False

        return True

    #interprets a single token of logic using the environment
    def interpret(self, tok):
        opcode = tok.get_Opcode()
        is_Temp = tok.get_Var_Type(1) == "temp"

        #sets up track variable, index, and light color for block.set_Field call
        field = tok.get_Var_Type(1)
        index = 0
        color = 0
        if len(tok.get_Var(1)) > 1:
            index = tok.get_Var(1)[1]

        if len(tok.get_Var(1)) == 3:
            color = tok.get_Var(1)[2]

        #runs statements based on instruction opcode
        match opcode:
            case self.CONST_EQ:
                if is_Temp == True:
                    self.t[tok.get_Var(1)[0]] = self.get_Token_Val(tok, 2)
                else:
                    new_Val = self.get_Token_Val(tok, 2)
                    self.environment[tok.get_Var(1)[0]].set_Field(field, index, color, new_Val)
            case self.CONST_NOT:
                if is_Temp == True:
                    self.t[tok.get_Var(1)[0]] = not self.get_Token_Val(tok, 2)
                else:
                    new_Val = not self.get_Token_Val(tok, 2)
                    self.environment[tok.get_Var(1)[0]].set_Field(field, index, color, new_Val)
            case self.CONST_AND:
                if is_Temp == True:
                    self.t[tok.get_Var(1)[0]] = self.get_Token_Val(tok, 2) and self.get_Token_Val(tok, 3)
                else:
                    new_Val = self.get_Token_Val(tok, 2) and self.get_Token_Val(tok, 3)
                    self.environment[tok.get_Var(1)[0]].set_Field(field, index, color, new_Val)
            case self.CONST_OR:
                if is_Temp == True:
                    self.t[tok.get_Var(1)[0]] = self.get_Token_Val(tok, 2) or self.get_Token_Val(tok, 3)
                else:
                    new_Val = self.get_Token_Val(tok, 2) or self.get_Token_Val(tok, 3)
                    self.environment[tok.get_Var(1)[0]].set_Field(field, index, color, new_Val)
            case self.CONST_B:
                self.pc = self.jump_Table[tok.get_Var(1)[0]]
            case self.CONST_BEQ:
                if self.get_Token_Val(tok, 2) == self.get_Token_Val(tok, 3):
                    self.pc = self.jump_Table[tok.get_Var(1)[0]]
            case self.CONST_BNE:
                if self.get_Token_Val(tok, 2) != self.get_Token_Val(tok, 3):
                    self.pc = self.jump_Table[tok.get_Var(1)[0]]
            case _:
                pass


    #gets a variable's value from a token
    def get_Token_Val(self, tok, var_Num):
        val = 0
        var_type = tok.get_Var_Type(var_Num)

        match var_type:
            case "temp":
                val = self.t[tok.get_Var(var_Num)[0]]
            case "occupied":
                val = self.environment[tok.get_Var(var_Num)[0]].occupied
            case "light":
                val = self.environment[tok.get_Var(var_Num)[0]].lights[tok.get_Var(var_Num)[1]][tok.get_Var(var_Num)[2]]
            case "gate":
                val = self.environment[tok.get_Var(var_Num)[0]].gates[tok.get_Var(var_Num)[1]]
            case "failed":
                val = self.environment[tok.get_Var(var_Num)[0]].failed
            case "closed":
                val = self.environment[tok.get_Var(var_Num)[0]].closed
            case "switch":
                val = self.environment[tok.get_Var(var_Num)[0]].switches[tok.get_Var(var_Num)[1]]
            case "constant":
                val = tok.get_Var(var_Num)[0]
            case _:
                pass


        return val



    #tokenizes plc logic
    def tokenize(self, file):
        self.status = False
        logic_Count = 0
        line_Count = 1

        #gets the first line
        line = file.readline()

        #continues until the end of the file
        while line:
            add_Logic = True
            comm = ""
            i = 0
            j = 0

            #ignores leading whitespace
            while line[i] == " ":
                i += 1

            #gets the command by parsing until a space is found
            for j in range(i, len(line)):
                if line[j] != " ":
                    comm += line[j]
                else:
                    i = j
                    break

            #matches the command string and generates token
            token = Token.Token()
            var1 = ""
            var2 = ""
            var3 = ""

            j += 1
            #this switch block is ~350 lines, im sorry
            match comm:
                #adds a jump point to the table
                case "SET":
                    label = ""

                    #iterates through the current line starting from the end of the command
                    for i in range(j, len(line)):
                        #checks for the end of the label
                        if line[i] != " " and line[i] != "\n":
                            label += line[i]
                        else:
                            break

                    #adds position in logic array to dictionary with label as key
                    #offsets the logic_Count by one since the exeution loop is interpret then increment
                    self.jump_Table[label] = logic_Count - 1
                    add_Logic = False

                #command num = 2
                #format "AND var1, var2, var3"
                case "AND":

                    #iterates until a comma is found
                    for i in range(j, len(line)):
                        if line[i] != ",":
                            var1 += line[i]
                        else:
                            break

                    i += 1
                    #ignores whitespace
                    for j in range(i, len(line)):
                        if line[j] != " ":
                            break

                    #gets var2
                    for i in range(j, len(line)):
                        if line[i] != ",":
                            var2 += line[i]
                        else:
                            break

                    i += 1
                    #ignores whitespace
                    for j in range(i, len(line)):
                        if line[j] != " ":
                            break

                    #gets var3
                    for i in range(j, len(line)):
                        if line[i] != " " and line[i] != "\n":
                            var3 += line[i]
                        else:
                            break

                    i += 1
                    #ignores trailing whitespace and checks for improper formatting
                    for j in range(i, len(line)):
                        if line[j] != " " and line[j] != "\n":
                            print("\nTokenizing failed: Invalid formatting in line " + str(line_Count))
                            return False

                    #checks that 3 operands were found
                    if var1 == "" or var2 == "" or var3 == "":
                        print("\nTokenizing failed: Incorrect number of arguments in line " + str(line_Count))
                        return False


                    #creates token
                    token.set_Opcode(self.CONST_AND)

                    if not token.set_Var(1, var1) or not token.set_Var(2, var2) or not token.set_Var(3, var3):
                        return False

                    #ensures an input is not being assigned to
                    if self.check_Output(token.get_Var_Type(1)) == False:
                        print("\nTokenization failed: Cannot assign to an input.")
                        return False

                #command num = 3
                #format "OR var1, var2, var3"
                case "OR":

                    #iterates until a comma is found
                    for i in range(j, len(line)):
                        if line[i] != ",":
                            var1 += line[i]
                        else:
                            break

                    i += 1
                    #ignores whitespace
                    for j in range(i, len(line)):
                        if line[j] != " ":
                            break

                    #gets var2
                    for i in range(j, len(line)):
                        if line[i] != ",":
                            var2 += line[i]
                        else:
                            break

                    i += 1
                    #ignores whitespace
                    for j in range(i, len(line)):
                        if line[j] != " ":
                            break

                    #gets var3
                    for i in range(j, len(line)):
                        if line[i] != " " and line[i] != "\n":
                            var3 += line[i]
                        else:
                            break

                    i += 1
                    #ignores trailing whitespace and checks for improper formatting
                    for j in range(i, len(line)):
                        if line[j] != " " and line[j] != "\n":
                            print("\nTokenizing failed: Invalid formatting in line " + str(line_Count))
                            return False

                    #checks that 3 operands were found
                    if var1 == "" or var2 == "" or var3 == "":
                        print("\nTokenizing failed: Incorrect number of arguments in line " + str(line_Count))
                        return False

                    #creates token
                    token.set_Opcode(self.CONST_OR)

                    if not token.set_Var(1, var1) or not token.set_Var(2, var2) or not token.set_Var(3, var3):
                        return False

                    #ensures an input is not being assigned to
                    if self.check_Output(token.get_Var_Type(1)) == False:
                        print("\nTokenization failed: Cannot assign to an input.")
                        return False

                #command num = 0
                #format "EQ var1, var2"
                case "EQ":

                    #iterates until a comma is found
                    for i in range(j, len(line)):
                        if line[i] != ",":
                            var1 += line[i]
                        else:
                            break

                    i += 1
                    #ignores whitespace
                    for j in range(i, len(line)):
                        if line[j] != " ":
                            break

                    #gets var2
                    for i in range(j, len(line)):
                        if line[i] != " " and line[i] != "\n":
                            var2 += line[i]
                        else:
                            break

                    i += 1
                    #ignores trailing whitespace and checks for improper formatting
                    for j in range(i, len(line)):
                        if line[j] != " " and line[j] != "\n":
                            print("\nTokenizing failed: Invalid formatting in line " + str(line_Count))
                            return False

                    #checks that 2 operands were found
                    if var1 == "" or var2 == "":
                        print("\nTokenizing failed: Incorrect number of arguments in line " + str(line_Count))
                        return False

                    #creates token
                    token.set_Opcode(self.CONST_EQ)

                    if (not token.set_Var(1, var1)) or (not token.set_Var(2, var2)):
                        return False

                    #ensures an input is not being assigned to
                    if self.check_Output(token.get_Var_Type(1)) == False:
                        print("\nTokenization failed: Cannot assign to an input.")
                        return False

                    
                #command num = 1
                #format "NOT var1, var2"
                case "NOT":
                    
                    #iterates until a comma is found
                    for i in range(j, len(line)):
                        if line[i] != ",":
                            var1 += line[i]
                        else:
                            break

                    i += 1
                    #ignores whitespace
                    for j in range(i, len(line)):
                        if line[j] != " ":
                            break

                    #gets var2
                    for i in range(j, len(line)):
                        if line[i] != " " and line[i] != "\n":
                            var2 += line[i]
                        else:
                            break

                    i += 1
                    #ignores trailing whitespace and checks for improper formatting
                    for j in range(i, len(line)):
                        if line[j] != " " and line[j] != "\n":
                            print("\nTokenizing failed: Invalid formatting in line " + str(line_Count))
                            return False

                    #checks that 3 operands were found
                    if var1 == "" or var2 == "":
                        print("\nTokenizing failed: Incorrect number of arguments in line " + str(line_Count))
                        return False

                    #creates token
                    token.set_Opcode(self.CONST_NOT)

                    if not token.set_Var(1, var1) or not token.set_Var(2, var2):
                        return False

                    #ensures an input is not being assigned to
                    if self.check_Output(token.get_Var_Type(1)) == False:
                        print("\nTokenization failed: Cannot assign to an input.")
                        return False

                #command num = 4
                #format "B label"
                case "B":

                    #iterates until a space or endline to get the label to jump to
                    for i in range(j, len(line)):
                        if line[i] != " " and line[i] != "\n":
                            var1 += line[i]
                        else:
                            break
                    
                    #ignore trailing whitespace
                    for j in range(i+1, len(line)):
                        #if there is anything other than whitespace, the line is invalid
                        if line[j] != " " and line[j] != "\n":
                            print("\nTokenizing failed: Invalid formatting at line " + str(line_Count))
                            return False

                    #creates token
                    token.set_Opcode(self.CONST_B)
                    token.var1 = [label]
                    token.var1_Type = "label"

                #command num = 5
                #format "BEQ label, var1, var2"
                case "BEQ":

                    #iterates until a comma is found
                    for i in range(j, len(line)):
                        if line[i] != ",":
                            var1 += line[i]
                        else:
                            break

                    i += 1
                    #ignores whitespace
                    for j in range(i, len(line)):
                        if line[j] != " ":
                            break

                    #gets var2
                    for i in range(j, len(line)):
                        if line[i] != ",":
                            var2 += line[i]
                        else:
                            break

                    i += 1
                    #ignores whitespace
                    for j in range(i, len(line)):
                        if line[j] != " ":
                            break

                    #gets var3
                    for i in range(j, len(line)):
                        if line[i] != " " and line[i] != "\n":
                            var3 += line[i]
                        else:
                            break

                    i += 1
                    #ignores trailing whitespace and checks for improper formatting
                    for j in range(i, len(line)):
                        if line[j] != " " and line[j] != "\n":
                            print("\nTokenizing failed: Invalid formatting in line " + str(line_Count))
                            return False

                    #checks that 3 operands were found
                    if var1 == "" or var2 == "" or var3 == "":
                        print("\nTokenizing failed: Incorrect number of arguments in line " + str(line_Count))
                        return False

                    #creates token
                    token.set_Opcode(self.CONST_BEQ)
                    token.var1 = [var1]
                    token.var1_Type = "label"

                    if not token.set_Var(2, var2) or not token.set_Var(3, var3):
                        return False
                    

                #command num = 6
                #format "BNE label, var1, var2"
                case "BNE":

                    #iterates until a comma is found
                    for i in range(j, len(line)):
                        if line[i] != ",":
                            var1 += line[i]
                        else:
                            break

                    i += 1
                    #ignores whitespace
                    for j in range(i, len(line)):
                        if line[j] != " ":
                            break

                    #gets var2
                    for i in range(j, len(line)):
                        if line[i] != ",":
                            var2 += line[i]
                        else:
                            break

                    i += 1
                    #ignores whitespace
                    for j in range(i, len(line)):
                        if line[j] != " ":
                            break

                    #gets var3
                    for i in range(j, len(line)):
                        if line[i] != " " and line[i] != "\n":
                            var3 += line[i]
                        else:
                            break

                    i += 1
                    #ignores trailing whitespace and checks for improper formatting
                    for j in range(i, len(line)):
                        if line[j] != " " and line[j] != "\n":
                            print("\nTokenizing failed: Invalid formatting in line " + str(line_Count))
                            return False

                    #checks that 3 operands were found
                    if var1 == "" or var2 == "" or var3 == "":
                        print("\nTokenizing failed: Incorrect number of arguments in line " + str(line_Count))
                        return False

                    #creates token
                    token.set_Opcode(self.CONST_BNE)
                    token.var1 = [var1]
                    token.var1_Type = "label"

                    if not token.set_Var(2, var2) or not token.set_Var(3, var3):
                        self.status = False
                        return False

                case _:
                    #handles comments, invalid commands
                    if comm[0] != ";" and comm != "\n":
                        print("\nTokenizing failed: Invalid command at line " + str(line_Count))
                        return False
                    else:
                        add_Logic = False

            #checks if the token was generated (since SET command does not generate logic)
            if add_Logic:

                #adds the new token to the logic array and increments the count
                self.logic.append(token)
                logic_Count += 1

            #gets the next line
            line = file.readline()
            line_Count += 1

        #returns False if tokenizing failed at any point
        #returns True if tokenizing was successful
        self.status = True
        return True


    #returns False if the type is a track controller output
    def check_Output(self, type):
        if type != "temp" and type != "light" and type != "gate" and type != "switch":
            return False
        else:
            return True