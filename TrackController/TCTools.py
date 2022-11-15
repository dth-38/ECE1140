#-------------------------------------------------------------------
# POSSIBLY USEFUL FUNCTIONS FOR INTERACTING WITH TRACK CONTROLLERS
#-------------------------------------------------------------------

#since the CTC and track controllers store block id differently
def convert_to_block(line, num):
    line.upper()
    tc_block = ""

    if line == "RED":
        pass
    elif line == "GREEN":
        if num < 4:
            tc_block = "green_A_" + str(num)
        elif num < 7:
            tc_block = "green_B_" + str(num)
        elif num < 13:
            tc_block = "green_C_" + str(num)
        elif num < 17:
            tc_block = "green_D_" + str(num)
        elif num < 21:
            tc_block = "green_E_" + str(num)
        elif num < 29:
            tc_block = "green_F_" + str(num)
        elif num < 33:
            tc_block = "green_G_" + str(num)
        elif num < 36:
            tc_block = "green_H_" + str(num)
        elif num < 58:
            tc_block = "green_I_" + str(num)
        elif num < 63:
            tc_block = "green_J_" + str(num)
        elif num < 69:
            tc_block = "green_K_" + str(num)
        elif num < 74:
            tc_block = "green_L_" + str(num)
        elif num < 77:
            tc_block = "green_M_" + str(num)
        elif num < 86:
            tc_block = "green_N_" + str(num)
        elif num < 89:
            tc_block = "green_O_" + str(num)
        elif num < 98:
            tc_block = "green_P_" + str(num)
        elif num < 101:
            tc_block = "green_Q_" + str(num)
        elif num < 102:
            tc_block = "green_R_" + str(num)
        elif num < 105:
            tc_block = "green_S_" + str(num)
        elif num < 110:
            tc_block = "green_T_" + str(num)
        elif num < 117:
            tc_block = "green_U_" + str(num)
        elif num < 122:
            tc_block = "green_V_" + str(num)
        elif num < 144:
            tc_block = "green_W_" + str(num)
        elif num < 147:
            tc_block = "green_X_" + str(num)
        elif num < 150:
            tc_block = "green_Y_" + str(num)
        else:
            tc_block = "green_Z_" + str(num)

    return tc_block

#use if you have block line, section, and number
def block_to_string(line, section, num):
    line.lower()
    section.upper()

    block = line + "_" + section + "_" + str(num)
    return block

#gets the controllers connected to a block
#returns an array of controllers since there can be more than one
#all track equipment is controlled by the first controller in the array
def get_controlling_controller(block):
    controller = -1

    if block[:3] == "red":
        line = "RED" 
    else:
        line = "GREEN"

    num_str = ""
    j = 0
    for i in range(len(block)):
        if block[i] == "_":
            if j < 2:
                j += 1
            else:
                num_str += block[i]

    num = int(num_str)

    if line == "RED":
        pass
    else:
        if num == 1 or num == 12 or num == 13:
            controller = 13
        elif num > 1 and num < 12:
            controller = 14
        elif (num > 13 and num < 31) or 150:
            controller = 12
        elif num > 30 and num < 36:
            controller = 11
        elif num > 35 and num < 59:
            controller = 10
        elif num > 58 and num < 62:
            controller = 0
        elif num > 61 and num < 69:
            controller = 1
        elif num > 68 and num < 76:
            controller = 2
        elif (num > 75 and num < 85) or num == 101:
            controller = 3
        elif num == 85 or num == 86 or num == 100:
            controller = 4
        elif num > 86 and num < 100:
            controller = 5
        elif num > 101 and num < 111:
            controller = 6
        elif num > 110 and num < 123:
            controller = 7
        elif num > 122 and num < 145:
            controller = 8
        else:
            controller = 9

    return controller