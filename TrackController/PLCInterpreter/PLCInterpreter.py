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
    def tokenize(self, filename):
        self.status = False
        line_Count = 1

        file = open(filename, "r")

        #gets the first line
        line = file.readline()

        #ignores anything after a logic block
        while len(line) != 0 and self.status == False:
            line = self.ignore_Whitespace(line)

            if line == "DEFINELOGIC":
                line = file.readline()
                line_Count += 1
                if len(line) == 0:
                    print("Tokenization failed: Reached EOF while parsing logic.")
                    file.close()
                    return False

                condensed_Line = self.ignore_Whitespace(line)

                while condensed_Line != "ENDLOGIC":
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

                    indicator = comm[0]
                    #only runs if not a comment or newline
                    if indicator != ";" and indicator != "\n":
                        #removes whitespace from line
                        line = self.ignore_Whitespace(line)
                        line = line[i:]


                        varNum = 1
                        #extracts operands from line
                        for i in range(len(line)):
                            if line[i] != ",":
                                match varNum:
                                    case 1:
                                        var1 += line[i]
                                    case 2:
                                        var2 += line[i]
                                    case 3:
                                        var3 += line[i]
                                    case _:
                                        print("\nTokenizing failed: Incorrect number of arguments in line " + str(line_Count))
                                        file.close()
                                        return False
                            else:
                                varNum += 1

                        #sets variables in token and tracks whether the operation was successful
                        set_Var1_Success = token.set_Var(1, var1)
                        set_Var2_Success = token.set_Var(2, var2)
                        set_Var3_Success = token.set_Var(3, var3)

                        if (set_Var1_Success and set_Var2_Success and set_Var3_Success) != True:
                            print("\nTokenizing failed: Unable to create token in line " + str(line_Count))
                            file.close()
                            return False

                        #ensures an input is not being assigned to
                        if self.check_Output(token.get_Var_Type(1)) == False:
                            print("\nTokenization failed: Cannot assign to input. line " + str(line_Count))
                            file.close()
                            return False


                        match comm:
                            #command num = 2
                            #format "AND var1, var2, var3"
                            case "AND":
                                #checks that 3 operands were found
                                if var1 == "" or var2 == "" or var3 == "":
                                    print("\nTokenizing failed: Incorrect number of arguments in line " + str(line_Count))
                                    file.close()
                                    return False

                                token.set_Opcode(self.CONST_AND)

                            #command num = 3
                            #format "OR var1, var2, var3"
                            case "OR":
                                #checks that 3 operands were found
                                if var1 == "" or var2 == "" or var3 == "":
                                    print("\nTokenizing failed: Incorrect number of arguments in line " + str(line_Count))
                                    file.close()
                                    return False

                                token.set_Opcode(self.CONST_OR)

                            #command num = 0
                            #format "EQ var1, var2"
                            case "EQ":
                                #checks that 2 operands were found
                                if var1 == "" or var2 == "":
                                    print("\nTokenizing failed: Incorrect number of arguments in line " + str(line_Count))
                                    file.close()
                                    return False

                                token.set_Opcode(self.CONST_EQ)
                            
                            #command num = 1
                            #format "NOT var1, var2"
                            case "NOT":
                                #checks that 3 operands were found
                                if var1 == "" or var2 == "":
                                    print("\nTokenizing failed: Incorrect number of arguments in line " + str(line_Count))
                                    file.close()
                                    return False

                                token.set_Opcode(self.CONST_NOT)

                            case _:
                                #handles invalid commands
                                print("\nTokenizing failed: Invalid command at line " + str(line_Count))
                                file.close()
                                return False

                        #adds the new token to the logic array and increments the count
                        self.logic.append(token)

                    #gets the next line
                    line = file.readline()
                    if len(line) == 0:
                        print("\nTokenizing failed: Reached EOF while parsing logic.")
                        file.close()
                        return False

                    condensed_Line = self.ignore_Whitespace(line)
                    line_Count += 1

                self.status = True
            line = file.readline()
            line_Count += 1

        file.close()

        #returns False if tokenizing failed at any point
        #returns True if tokenizing was successful
        return self.status


    #returns False if the type is a track controller output
    def check_Output(self, type):
        if type != "temp" and type != "light" and type != "gate" and type != "switch":
            return False
        else:
            return True

    #returns the string line with whitespace and newlines removed
    def ignore_Whitespace(self, line):
        newLine = ""
        for i in range(len(line)):
            if line[i] != " " and line[i] != "\n":
                newLine += line[i]

        return newLine