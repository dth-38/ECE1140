import copy
from PLCCompiler import Token

class PLCCompiler:

    def __init__(self):
        #allows renaming of the program counter name
        self.program_counter = "pc"

        #dictionary storing program counter values using labels as keys
        self.jump_Table = {}
        #logic tokens
        self.logic = []
        #array of compiled python lines generated from logic tokens
        self.executable = []
        #tracks if a program has been successfully compiled
        self.status = False
    

    #allows setting the program counter name
    def set_PC(self, name):
        self.program_counter = name

    #compiles the plc logic, returning True if successful
    def compile_PLC(self, file):
        self.status = False

        if self.tokenize(file):

            if self.compile_Tokens():
                self.status = True
            
        return self.status

    #returns the exectuable python bytecode if it has been compiled
    def get_Executable(self):
        if self.status:
            return copy.copy(self.excutable)


    #tokenizes plc logic
    def tokenize(self, file):
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
                    self.jump_Table[label] = logic_Count
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
                    token.set_Opcode(2)

                    if not token.set_Var(1, var1) or not token.set_Var(2, var2) or not token.set_Var(3, var3):
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
                    token.set_Opcode(3)

                    if not token.set_Var(1, var1) or not token.set_Var(2, var2) or not token.set_Var(3, var3):
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
                    token.set_Opcode(0)

                    if (not token.set_Var(1, var1)) or (not token.set_Var(2, var2)):
                        print(var2 + "a")
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
                    token.set_Opcode(1)

                    if not token.set_Var(1, var1) or not token.set_Var(2, var2):
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
                    token.set_Opcode(4)
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
                    token.set_Opcode(5)
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
                    token.set_Opcode(6)
                    token.var1 = [var1]
                    token.var1_Type = "label"

                    if not token.set_Var(2, var2) or not token.set_Var(3, var3):
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
        return True

    #takes tokenized logic and converts it into compiled python lines
    def compile_Tokens(self):
        for token in self.logic:
            exec_String = ""

            match token.get_Opcode():
                #EQ: generates the format "var1 = var2"
                case 0:
                    if self.check_Output(token.get_Var_Type(1)):
                        print("Compilation failed: Input cannot be assigned to.")
                        return False
                    else:
                        exec_String += self.recreate_Variable(token, 1)

                    exec_String += " = "
                    exec_String += self.recreate_Variable(token, 2)

                #NOT: generates the format "var1 = not var2"
                case 1:
                    if self.check_Output(token.get_Var_Type(1)):
                        print("Compilation failed: Input cannot be assigned to.")
                        return False
                    else:
                        exec_String += self.recreate_Variable(token, 1)

                    exec_String += " = not "
                    exec_String += self.recreate_Variable(token, 2)

                #AND: generates the format "var1 = var2 and var3"
                case 2:
                    if self.check_Output(token.get_Var_Type(1)):
                        print("Compilation failed: Input cannot be assigned to.")
                        return False
                    else:
                        exec_String += self.recreate_Variable(token, 1)

                    exec_String += " = "
                    exec_String += self.recreate_Variable(token, 2)
                    exec_String += " and "
                    exec_String += self.recreate_Variable(token, 3)

                #OR: generates the format "var1 = var2 or var3"
                case 3:
                    if self.check_Output(token.get_Var_Type(1)):
                        print("Compilation failed: Input cannot be assigned to.")
                        return False
                    else:
                        exec_String += self.recreate_Variable(token, 1)

                    exec_String += " = "
                    exec_String += self.recreate_Variable(token, 2)
                    exec_String += " or "
                    exec_String += self.recreate_Variable(token, 3)

                #B: generates the format "pc = self.jump_Table[var1]"
                case 4:
                    exec_String += self.program_counter
                    exec_String += " = "
                    exec_String += str(self.jump_Table[token.get_Var(1)[0]])

                #BEQ: generates the format "if var2 == var3:\n\tpc = self.jump_Table[var1]"
                case 5:
                    exec_String += "if "
                    exec_String += self.recreate_Variable(token, 2)
                    exec_String += " == "
                    exec_String += self.recreate_Variable(token, 3)
                    exec_String += ":\n\t"
                    exec_String += self.program_counter
                    exec_String += " = "
                    exec_String += str(self.jump_Table[token.get_Var(1)[0]])
                
                #BNE: generates the format "if var2 != var3:\n\tpc = self.jump_Table[var1]"
                case 6:
                    exec_String += "if "
                    exec_String += self.recreate_Variable(token, 2)
                    exec_String += " != "
                    exec_String += self.recreate_Variable(token, 3)
                    exec_String += ":\n\t"
                    exec_String += self.program_counter
                    exec_String += " = "
                    exec_String += str(self.jump_Table[token.get_Var(1)[0]])

                case _:
                    print("Bad things have happened if you are seeing this.")
                    print("Tokenizer failed to get a valid opcode and didn't fail.")

            #compiles each line and adds it to the executable array
            print(exec_String)
            compiled_Line = compile(exec_String, "local", "exec")
            self.executable.append(compiled_Line)

        #returns true on success
        return True


    #builds the reference to the track variable in python's syntax from the tokenized variable
    def recreate_Variable(self, token, arg_Num):
        var_String = ""
        match token.get_Var_Type(arg_Num):
            case "temp":
                var_String += "t["
                var_String += str(token.get_Var(arg_Num)[0])
                var_String += "]"
            case "light":
                var_String += "self.next_Track_State[\""
                var_String += token.get_Var(arg_Num)[0]
                var_String += "\"].lights["
                var_String += str(token.get_Var(arg_Num)[1])
                var_String += "]["
                var_String += str(token.get_Var(arg_Num)[2])
                var_String += "]"
            case "gate":
                var_String += "self.next_Track_State[\""
                var_String += token.get_Var(arg_Num)[0]
                var_String += "\"].gates["
                var_String += str(token.get_Var(arg_Num)[1])
                var_String += "]"
            case "switch":
                var_String += "self.next_Track_State[\""
                var_String += token.get_Var(arg_Num)[0]
                var_String += "\"].switches["
                var_String += str(token.get_Var(arg_Num)[1])
                var_String += "]"
            case "occupied":
                var_String += "self.next_Track_State[\""
                var_String += token.get_Var(arg_Num)[0]
                var_String += "\"].occupied"
            case "failed":
                var_String += "self.next_Track_State[\""
                var_String += token.get_Var(arg_Num)[0]
                var_String += "\"].failed"
            case "closed":
                var_String += "self.next_Track_State[\""
                var_String += token.get_Var(arg_Num)[0]
                var_String += "\"].closed"
            case "label":
                var_String += token.get_Var(arg_Num)[0]
            case "constant":
                var_String += str(token.get_Var(arg_Num)[0])
            case _:
                print("Bad things have happened if you are seeing this.")
                print("Tokenizer got an invalid token type but didn't fail.")

        return var_String


    #returns False if the type is a track controller output
    def check_Output(self, type):
        if type != "temp" and type != "light" and type != "gate" and type != "switch":
            return True
        else:
            return False