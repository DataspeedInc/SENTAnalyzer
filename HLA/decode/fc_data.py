from enum import Enum, auto

class FrameFormats(Enum):
    H_1 = auto()
    H_2 = auto()
    H_3 = auto()
    H_4 = auto()
    H_5 = auto()
    H_6 = auto()
    H_7 = auto()
    # Multiplexed #
    F1_1 = auto()
    F1_2 = auto()
    F1_3 = auto()
    F1_4 = auto()
    F1_5 = auto()
    F1_6 = auto()
    F2_1 = auto()
    F2_2 = auto()
    F2_3 = auto()
    F2_4 = auto()
    F3_1 = auto()
    F3_2 = auto()
    F3_3 = auto()
    F3_4 = auto()
    F3_5 = auto()
    F4_1 = auto()
    F4_2 = auto()
    F4_3 = auto()
    F4_4 = auto()
    F4_5 = auto()
    F4_6 = auto()
    F4_7 = auto()
    F4_8 = auto()
    F4_9 = auto()

class TransferFunctions(Enum):
    E_2       = auto()
    E_2_1     = auto()
    E_2_1_1   = auto()
    E_2_1_2   = auto()
    E_2_1_3   = auto()
    E_2_1_4   = auto()
    E_2_1_5   = auto()
    E_2_2     = auto()
    E_2_2_1   = auto()
    E_2_2_2   = auto()
    E_2_2_3   = auto()
    E_2_2_4   = auto()
    E_2_3     = auto()
    E_2_4     = auto()
    E_2_4_1   = auto()
    E_2_4_1_1 = auto()
    E_2_4_1_2 = auto()
    E_2_5     = auto()
    E_2_6     = auto()

sensor_definitions = {
    0x001: (FrameFormats.H_2, TransferFunctions.E_2_4), # P
    0x002: (FrameFormats.H_5, TransferFunctions.E_2_4), # P/-
    0x003: (FrameFormats.H_4, TransferFunctions.E_2_4), # P/S
    0x004: (FrameFormats.H_4, TransferFunctions.E_2_4), # P/S/t
}

'''
A dict for looking up sensor channel bit-width to
default Y1 and Y2 values. (The returned tuples are
stored as (Y1, Y2) ).
'''
default_y_vals = {
    6 : (3   , 54),
    7 : (6   , 115),
    8 : (12  , 237),
    9 : (24  , 481),
    10: (48  , 969),
    11: (96  , 1945),
    12: (193 , 3896),
    13: (385 , 7800),
    14: (770 , 15607),
    15: (1540, 31221),
    16: (3080, 62449)
}

def decode(sensor: int, data: int, x_vals_raw: tuple(tuple(int, int), ...), y_vals: tuple(tuple(int, int), ...) = None):
    
    global sensor_definitions

    sensor = sensor_definitions[sensor]

    ch1_n = None
    ch2_n = None

    if   sensor[0] == FrameFormats.H_1:
        ch1_n = 12
        ch2_n = 12
    elif sensor[0] == FrameFormats.H_2:
        ch1_n = 12
    elif sensor[0] == FrameFormats.H_3:
        ch1_n = 12
    elif sensor[0] == FrameFormats.H_4:
        ch1_n = 12
    elif sensor[0] == FrameFormats.H_5:
        ch1_n = 12
    elif sensor[0] == FrameFormats.H_6:
        ch1_n = 14
        ch2_n = 10
    elif sensor[0] == FrameFormats.H_7:
        ch1_n = 16
        ch2_n = 8

    if y_vals is None:
        yv = []

        if ch1_n is not None:
            yv.append( default_y_vals[ch1_n] )
        if ch2_n is not None:
            yv.append( default_y_vals[ch2_n] )
        
        y_vals = tuple(yv)
    
    