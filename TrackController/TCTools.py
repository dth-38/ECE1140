#-------------------------------------------------------------------
# POSSIBLY USEFUL FUNCTIONS FOR INTERACTING WITH TRACK CONTROLLERS
#-------------------------------------------------------------------

#since the CTC and track controllers store block id differently
def convert_to_block(line, num):
    line = line.upper()
    tc_block = ""

    if line == "RED":
        if num == 0:
            tc_block = "red___0"
        elif num < 4:
            tc_block = "red_A_" + str(num)
        elif num < 7:
            tc_block = "red_B_" + str(num)
        elif num < 10:
            tc_block = "red_C_" + str(num)
        elif num < 13:
            tc_block = "red_D_" + str(num)
        elif num < 16:
            tc_block = "red_E_" + str(num)
        elif num < 21:
            tc_block = "red_F_" + str(num)
        elif num < 24:
            tc_block = "red_G_" + str(num)
        elif num < 46:
            tc_block = "red_H_" + str(num)
        elif num < 49:
            tc_block = "red_I_" + str(num)
        elif num < 55:
            tc_block = "red_J_" + str(num)
        elif num < 58:
            tc_block = "red_K_" + str(num)
        elif num < 61:
            tc_block = "red_L_" + str(num)
        elif num < 64:
            tc_block = "red_M_" + str(num)
        elif num < 67:
            tc_block = "red_N_" + str(num)
        elif num < 68:
            tc_block = "red_O_" + str(num)
        elif num < 71:
            tc_block = "red_P_" + str(num)
        elif num < 72:
            tc_block = "red_Q_" + str(num)
        elif num < 73:
            tc_block = "red_R_" + str(num)
        elif num < 76:
            tc_block = "red_S_" + str(num)
        else:
            tc_block = "red_T_" + str(num)

    elif line == "GREEN":
        if num == 0:
            tc_block = "green___0"
        elif num < 4:
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

#this does no error checking/handling, use carefully
def decompose_block(block):
    d_block = []

    l = block[:3]

    if l == "red":
        d_block.append(l.upper())
        #red_A_1
        n = block[6:]
        d_block.append(int(n))
    else:
        d_block.append("GREEN")
        #green_A_1
        n = block[8:]
        d_block.append(int(n))

    return d_block