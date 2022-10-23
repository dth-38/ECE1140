#defines the token used to optimize the plc interpreter
#vars contain parsed variables
#opcodes: EQ=0, NOT=1, AND=2, OR=3, B=4, BEQ=5, BNE=6
#var types: Temporary register: "temp", Occupation: "occupied", Light: "light", 
#           Gate: "gate", Failure: "failed", Closed: "closed", Switch: "switch", label: "label", constant: "constant"

#for example:
#AND t[0], red_A_1:light[0].RED, red_A_2:occupied
#would be stored as: 
#opcode = 2, var1_Type = temp, var1 = [0], var2_Type = light, var2 = ["red_A_1", 0, 0], var2_Type = occ, var2 = ["red_A_2"]

class Token:

    def __init__(self):
        
        self.opcode = 0
        self.var1 = []
        self.var1_Type = ""
        self.var2 = []
        self.var2_Type = ""
        self.var3 = []
        self.var3_Type = ""


    def get_Opcode(self):
        return self.opcode

    def set_Opcode(self, code):
        self.opcode = code

    def get_Var_Type(self, num):
        match num:
            case 1:
                return self.var1_Type
            case 2:
                return self.var2_Type
            case 3:
                return self.var3_Type
            case _:
                pass

    def get_Var(self, num):
        match num:
            case 1:
                return self.var1
            case 2:
                return self.var2
            case 3:
                return self.var3
            case _:
                pass

    
    #parses a variable name to format it
    #returns true if successful, false otherwise
    #DO NOT PASS IT A BRANCH LABEL, IT WILL BREAK
    def set_Var(self, num, name):
        temp_Var = []
        temp_Type = ""
        i = 0
        j = 0


        if name[0] == "t":
            #temporary register
            reg = name[2]
            check = "t[" + reg + "]"
            if name != check:
                print("\nTokenizing failed: Invalid temporary register value.")
                return False 
            else:
                temp_Var.append(int(reg))
                temp_Type = "temp"
        elif name == "TRUE":
            temp_Type = "constant"
            temp_Var.append(True)
        elif name == "FALSE":
            temp_Type = "constant"
            temp_Var.append(False)
        else:
            #block variable
            
            #parses until a colon is reached
            block = ""
            for i in range(len(name)):
                if name[i] != ":":
                    block += name[i]
                else:
                    break


            i += 1
            #parses variable type
            for j in range(i, len(name)):
                if name[j] != "[":
                    temp_Type += name[j]
                else:
                    break

            #increments counter to make next parse easier
            j += 1

            #adds to temp_Var depending on variable type
            match temp_Type:
                case "occupied":
                    temp_Var.append(block)
                case "light":
                    #parses the light number
                    l_Num = ""
                    for i in range(j, len(name)):
                        if name[i] != "]":
                            l_Num += name[i]
                        else:
                            break

                    #tries to convert the light number to an int to check that it is valid
                    try:
                        l_real_Num = int(l_Num)
                    except:
                        print("\nTokenization failed: Array index not a number or formatted improperly.")
                        return False

                    #checks that there is a period after index (proper formatting)
                    try:
                        if name[i+1] != ".":
                            print("\nTokenization failed: Incorrect light variable formatting.")
                            return False
                    except:
                        print("\nTokenization failed: Invalid formatting.")
                        return False

                    #parses light color
                    color = ""
                    for j in range(i+2, len(name)):
                        color += name[j]

                    #checks that the light color is valid
                    match color:
                        case "RED":
                            color_Val = 0
                        case "YELLOW":
                            color_Val = 1
                        case "GREEN":
                            color_Val = 2
                        case _:
                            print("\nTokenization Failed: Invalid light color specification.")
                            return False

                    temp_Var.append(block)
                    temp_Var.append(l_real_Num)
                    temp_Var.append(color_Val)

                case "gate":
                    #parses the gate number
                    g_Num = ""

                    for i in range(j, len(name)):
                        if name[i] != "]":
                            g_Num += name[i]
                        else:
                            break

                    #tries to convert the gate number string to an integer
                    try:
                        g_real_Num = int(g_Num)
                    except:
                        print("\nTokenization failed: Array index not a number or formatted improperly.")
                        return False

                    temp_Var.append(block)
                    temp_Var.append(g_real_Num)

                case "switch":
                    #parses the switch number
                    s_Num = ""

                    for i in range(j, len(name)):
                        if name[i] != "]":
                            s_Num += name[i]
                        else:
                            break

                    #tries to convert the switch number to an integer
                    try:
                        s_real_Num = int(s_Num)
                    except:
                        print("\nTokenization failed: Array index not a number or formatted improperly.")
                        return False

                    temp_Var.append(block)
                    temp_Var.append(s_real_Num)

                case "closed":
                    temp_Var.append(block)
                case "failed":
                    temp_Var.append(block)
                case _:
                    print("\nTokenization failed: Invalid track variable")
                    return False

        
        #determines which var to assign to
        match num:
            case 1:
                self.var1 = temp_Var
                self.var1_Type = temp_Type
            case 2:
                self.var2 = temp_Var
                self.var2_Type = temp_Type
            case 3:
                self.var3 = temp_Var
                self.var3_Type = temp_Type
            case _:
                print("\nTokenizing failed: Internal variable numbering error.")
                return False

        return True

