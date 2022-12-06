#from typing import list

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

class Signals(QObject):

    #-----------------------------------------
    # Track Controller Signals
    #-----------------------------------------

    tc_update = pyqtSignal()

    #(str line, int block_num, int True/False)
    send_ctc_occupancy = pyqtSignal(str, int, int)
    #(str line, int block_num, int True/False)
    send_ctc_failure = pyqtSignal(str, int, int)

    #CTC sets tc exits

    #(str line, int block_num, int authority)
    send_track_authority = pyqtSignal(str, int, int)
    #(str, line, int block_num, int commanded_speed)
    send_track_speed = pyqtSignal(str, int, int)

    #(str line, int block_num, int next_block_num)
    broadcast_switch = pyqtSignal(str, int, int)
    #(str line, int block_num, str "GREEN"/"RED")
    broadcast_light = pyqtSignal(str, int, str)
    #(str line, int block_num, str "OPEN"/"CLOSED")
    broadcast_gate = pyqtSignal(str, int, str)    


    #---------------------------------------------
    # CTC SIGNALS
    #---------------------------------------------

    #FOR SIGNALS TO TRACK CONTROLLERS:
    #CONVERT line,block_num format TO line_section_block_num i.e.(green, 2 -> green_A_2)
    #USING TCTools convert_to_block function
    ctc_update = pyqtSignal()

    #(str line)
    send_tm_dispatch = pyqtSignal(str)

    #(str block, int authority)
    send_tc_authority = pyqtSignal(str, int)
    #(str block, int suggested_speed)
    send_tc_speed = pyqtSignal(str, int)
    #(str block, int True/False)
    send_tc_maintenance = pyqtSignal(str, int)
    #(str block, str next_block)
    set_tc_switch = pyqtSignal(str, str)

    #------------------------------------------
    # TRACK MODEL SIGNALS
    #------------------------------------------

    track_update = pyqtSignal()

    #(str line, int ticket_sales)
    send_ctc_ticket_sales = pyqtSignal(str, int)

    #(str block, int True/False)
    send_tc_occupancy = pyqtSignal(str, int)
    #(str block, int True/False)
    send_tc_failure = pyqtSignal(str, int)

    #(int id, int commanded speed)
    send_tm_commanded_speed = pyqtSignal(int, int)
    #(int id, int authority)
    send_tm_authority = pyqtSignal(int, int)
    #(int id, float grade)
    send_tm_grade = pyqtSignal(int, float)
    #(int id, int True/False)
    send_tm_failure = pyqtSignal(int, int)
    #(str station, int doorside)
    send_tm_beacon = pyqtSignal(str, int)
    #(int id, int passenger_count)
    send_tm_passenger_count = pyqtSignal(int, int)
    #(bool tunnel)
    send_tm_tunnel = pyqtSignal(int, bool)
    #(bool station)
    send_tm_station = pyqtSignal(int, bool)

    #-----------------------------------------
    # Train Model Signals
    #-----------------------------------------

    train_update = pyqtSignal()

    #(int id, float distance)
    send_tm_distance = pyqtSignal(int, float)

    #-----------------------------------------
    # Signals to open train controller/track model gui
    #-----------------------------------------

    #(int id)
    open_tm_gui = pyqtSignal(int)
    #(int id)
    open_tc_gui = pyqtSignal(int)

signals = Signals()