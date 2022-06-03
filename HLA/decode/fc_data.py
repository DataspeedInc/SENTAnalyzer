from enum import Enum, auto
import math

class ValueFormat(Enum):
    SIGNED   = auto()
    UNSIGNED = auto()

class FrameFormats(Enum):
    H_1  = auto()
    H_2  = auto()
    H_3  = auto()
    H_4  = auto()
    H_5  = auto()
    H_6  = auto()
    H_7  = auto()
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
    F3_3 = auto() # Not currently usable by the latest spec
    F3_4 = auto() # Not currently usable by the latest spec
    F3_5 = auto() # Not currently usable by the latest spec
    F4_1 = auto() # Not currently usable by the latest spec
    F4_2 = auto() # Not currently usable by the latest spec
    F4_3 = auto()
    F4_4 = auto()
    F4_5 = auto()
    F4_6 = auto() # Not currently usable by the latest spec
    F4_7 = auto() # Not currently usable by the latest spec
    F4_8 = auto()
    F4_9 = auto()

class TransferFunctions(Enum):
    LINEAR_PRESSURE            = auto()
    SPECIAL_LINEAR_TEMPERATURE = auto()
    DEFAULT_LINEAR_TEMPERATURE = auto()
    LINEAR_MAF                 = auto()
    SENSOR_SPECIFIC_MAF        = auto()
    LINEAR_HIGH_TEMPERATURE    = auto()
    LINEAR_POSITION_SENSOR     = auto()
    ANGLE_POSITION_SENSOR      = auto()
    RELATIVE_POSITION_SENSOR      = auto()
    RATIO_SENSING              = auto()

'''
( frame_format, (tf_ch1, tf_ch1, tf_supplementary) )
'''
sensor_definitions = {
    0x001: # P
        (FrameFormats.H_2,
        (TransferFunctions.LINEAR_PRESSURE, None) ),                                               
    0x002: # P/-
        (FrameFormats.H_5,
        (TransferFunctions.LINEAR_PRESSURE, None) ),                                               
    0x003: # P/S
        (FrameFormats.H_4,
        (TransferFunctions.LINEAR_PRESSURE, None) ),                                               
    0x004: # P/S/t
        (FrameFormats.H_4,
        (TransferFunctions.LINEAR_PRESSURE, None) ),                                               
    0x005: # P/S/t
        (FrameFormats.H_4,
        (TransferFunctions.LINEAR_PRESSURE, None, TransferFunctions.SPECIAL_LINEAR_TEMPERATURE) ), 
    0x006: # P/P
        (FrameFormats.H_1,
        (TransferFunctions.LINEAR_PRESSURE, TransferFunctions.LINEAR_PRESSURE) ),                  
    0x007: # P/T
        (FrameFormats.H_1,
        (TransferFunctions.LINEAR_PRESSURE, TransferFunctions.DEFAULT_LINEAR_TEMPERATURE) ),       
    0x008: # P/T
        (FrameFormats.H_1,
        (TransferFunctions.LINEAR_PRESSURE, TransferFunctions.SPECIAL_LINEAR_TEMPERATURE) ),       
    0x009: # P/P/t
        (FrameFormats.H_1,
        (TransferFunctions.LINEAR_PRESSURE, TransferFunctions.LINEAR_PRESSURE) ),                  
    0x00A: # P/P/t
        (FrameFormats.H_1,
        (TransferFunctions.LINEAR_PRESSURE, TransferFunctions.LINEAR_PRESSURE, TransferFunctions.SPECIAL_LINEAR_TEMPERATURE) ), 
    0x00B: # P/t
        (FrameFormats.H_2,
        (TransferFunctions.LINEAR_PRESSURE, None, TransferFunctions.SPECIAL_LINEAR_TEMPERATURE) ), 
    0x00C: # P/-/t
        (FrameFormats.H_1,
        (TransferFunctions.LINEAR_PRESSURE, None, TransferFunctions.SPECIAL_LINEAR_TEMPERATURE) ), 
    0x00D: # P (high speed)
        (FrameFormats.H_3,
        (TransferFunctions.LINEAR_PRESSURE, None) ),                                               
    0x00E: # P/t (high speed)
        (FrameFormats.H_3,
        (TransferFunctions.LINEAR_PRESSURE, None, TransferFunctions.SPECIAL_LINEAR_TEMPERATURE) ), 
    0x011: # MAF (hi-res, lin)
        (FrameFormats.H_7,
        (TransferFunctions.LINEAR_MAF, None) ),                                                    
    0x012: # MAF (hi-res, non-lin)
        (FrameFormats.H_7,
        (TransferFunctions.SENSOR_SPECIFIC_MAF, None) ),                                           
    0x013: # MAF (hi-res, lin) / Pressure
        (FrameFormats.H_7,
        (TransferFunctions.LINEAR_MAF, TransferFunctions.LINEAR_PRESSURE) ),                       
    0x014: # MAF (hi-res, non-lin) / Pressure
        (FrameFormats.H_7,
        (TransferFunctions.SENSOR_SPECIFIC_MAF, TransferFunctions.LINEAR_PRESSURE) ),              
    0x015: # MAF (lin) / Pressure (hi-res)
        (FrameFormats.H_6,
        (TransferFunctions.LINEAR_MAF, TransferFunctions.LINEAR_PRESSURE) ),                       
    0x016: # MAF (non-lin) / Pressure (hi-res)
        (FrameFormats.H_6,
        (TransferFunctions.SENSOR_SPECIFIC_MAF, TransferFunctions.LINEAR_PRESSURE) ),              
    0x017: # MAF (lin)
        (FrameFormats.H_6,
        (TransferFunctions.LINEAR_MAF, None) ),                                                    
    0x018: # MAF (non-lin)
        (FrameFormats.H_6,
        (TransferFunctions.SENSOR_SPECIFIC_MAF, None) ),                                           
    0x019: # MAF (lin) / Temperature
        (FrameFormats.H_6,
        (TransferFunctions.LINEAR_MAF, TransferFunctions.DEFAULT_LINEAR_TEMPERATURE) ),            
    0x01A: # MAF (non-lin) / Temperature
        (FrameFormats.H_6,
        (TransferFunctions.SENSOR_SPECIFIC_MAF, TransferFunctions.DEFAULT_LINEAR_TEMPERATURE) ),   
    0x01B: # MAF (hi-res, lin) / Temperature
        (FrameFormats.H_7,
        (TransferFunctions.LINEAR_MAF, TransferFunctions.DEFAULT_LINEAR_TEMPERATURE) ),            
    0x01C: # MAF (hi-res, non-lin) / Temperature
        (FrameFormats.H_7,
        (TransferFunctions.SENSOR_SPECIFIC_MAF, TransferFunctions.DEFAULT_LINEAR_TEMPERATURE) ),   
    0x01D: # MAF (low-res, non-lin)
        (FrameFormats.H_1,
        (TransferFunctions.SENSOR_SPECIFIC_MAF, None) ),                                           
    0x01E: # MAF (low-res, non-lin) / Pressure
        (FrameFormats.H_1,
        (TransferFunctions.SENSOR_SPECIFIC_MAF, TransferFunctions.LINEAR_PRESSURE) ),              
    0x01F: # MAF (low-res, non-lin) / Temperature
        (FrameFormats.H_1,
        (TransferFunctions.SENSOR_SPECIFIC_MAF, TransferFunctions.DEFAULT_LINEAR_TEMPERATURE) ),   
    0x041: # Temperature
        (FrameFormats.H_1,
        (TransferFunctions.DEFAULT_LINEAR_TEMPERATURE, None) ),                                    
    0x042: # Temperature / Secure Sensor
        (FrameFormats.H_4,
        (TransferFunctions.DEFAULT_LINEAR_TEMPERATURE, None) ),                                    
    0x043: # Temperature / Temperature
        (FrameFormats.H_1,
        (TransferFunctions.DEFAULT_LINEAR_TEMPERATURE, TransferFunctions.DEFAULT_LINEAR_TEMPERATURE) ), 
    0x044: # Temperature Sensor Cluster
        (FrameFormats.F1_5,
        (TransferFunctions.DEFAULT_LINEAR_TEMPERATURE, None) ),                                   
    0x045: # High Temperature
        (FrameFormats.H_1,
        (TransferFunctions.LINEAR_HIGH_TEMPERATURE, None) ),                                       
    0x046: # High Temperature / Secure Sensor
        (FrameFormats.H_4,
        (TransferFunctions.LINEAR_HIGH_TEMPERATURE, None) ),                                       
    0x047: # High Temperature / High Temperature
        (FrameFormats.H_1,
        (TransferFunctions.LINEAR_HIGH_TEMPERATURE, TransferFunctions.LINEAR_HIGH_TEMPERATURE) ),  
    0x048: # High Temperature Sensor Cluster
        (FrameFormats.F1_5,
        (TransferFunctions.LINEAR_HIGH_TEMPERATURE, None) ),                                      
    0x049: # Special Temperature
        (FrameFormats.H_1,
        (TransferFunctions.SPECIAL_LINEAR_TEMPERATURE, None) ),                                    
    0x04A: # Special Temperature / Secure Sensor
        (FrameFormats.H_4,
        (TransferFunctions.SPECIAL_LINEAR_TEMPERATURE, None) ),                                    
    0x04B: # Special Temperature / Special Temperature
        (FrameFormats.H_1, 
        (TransferFunctions.SPECIAL_LINEAR_TEMPERATURE, TransferFunctions.SPECIAL_LINEAR_TEMPERATURE, None) ), 
    0x04C: # Special Temperature Sensor Cluster
        (FrameFormats.F1_5,
        (TransferFunctions.SPECIAL_LINEAR_TEMPERATURE, None) ),                                   
    0x051: # Linear Position
        (FrameFormats.H_2,
        (TransferFunctions.LINEAR_POSITION_SENSOR, None) ),                                               
    0x052: # Linear Position
        (FrameFormats.H_1,
        (TransferFunctions.LINEAR_POSITION_SENSOR, None) ),                                               
    0x053: # Linear Position (high speed)
        (FrameFormats.H_3,
        (TransferFunctions.LINEAR_POSITION_SENSOR, None) ),                                               
    0x054: # Linear Position 1 / Linear Position 2
        (FrameFormats.H_1,
        (TransferFunctions.LINEAR_POSITION_SENSOR, TransferFunctions.LINEAR_POSITION_SENSOR) ),                  
    0x055: # Linear Position / Secure Sensor
        (FrameFormats.H_4,
        (TransferFunctions.LINEAR_POSITION_SENSOR, None) ),                                               
    0x056: # Linear Position / Temperature
        (FrameFormats.H_1,
        (TransferFunctions.LINEAR_POSITION_SENSOR, TransferFunctions.DEFAULT_LINEAR_TEMPERATURE) ),       
    0x057: # Linear Position / Ratio
        (FrameFormats.H_1,
        (TransferFunctions.LINEAR_POSITION_SENSOR, TransferFunctions.RATIO_SENSING) ),                    
    0x060: # Angle Position
        (FrameFormats.H_2,
        (TransferFunctions.ANGLE_POSITION_SENSOR, None) ),                                               
    0x061: # Angle Position
        (FrameFormats.H_1,
        (TransferFunctions.ANGLE_POSITION_SENSOR, None) ),                                               
    0x062: # Angle Position (high speed)
        (FrameFormats.H_3,
        (TransferFunctions.ANGLE_POSITION_SENSOR, None) ),                                               
    0x063: # Angle Position 1 / Angle Position 2
        (FrameFormats.H_1,
        (TransferFunctions.ANGLE_POSITION_SENSOR, TransferFunctions.ANGLE_POSITION_SENSOR) ),                  
    0x064: # Angle Position / Secure Sensor
        (FrameFormats.H_4,
        (TransferFunctions.ANGLE_POSITION_SENSOR, None) ),                                               
    0x065: # Angle Position Sensor / Temperature
        (FrameFormats.H_1,
        (TransferFunctions.ANGLE_POSITION_SENSOR, TransferFunctions.DEFAULT_LINEAR_TEMPERATURE) ),       
    0x070: # Relative Position
        (FrameFormats.H_2,
        (TransferFunctions.RELATIVE_POSITION_SENSOR, None) ),                                               
    0x071: # Relative Position
        (FrameFormats.H_1,
        (TransferFunctions.RELATIVE_POSITION_SENSOR, None) ),                                               
    0x072: # Relative Position (high speed)
        (FrameFormats.H_3,
        (TransferFunctions.RELATIVE_POSITION_SENSOR, None) ),                                               
    0x073: # Relative Position 1 / Relative Position 2
        (FrameFormats.H_1,
        (TransferFunctions.RELATIVE_POSITION_SENSOR, TransferFunctions.RELATIVE_POSITION_SENSOR) ),            
    0x074: # Relative Position / Secure Sensor
        (FrameFormats.H_4,
        (TransferFunctions.RELATIVE_POSITION_SENSOR, None) ),                                         
    0x075: # Relative Position / Temperature
        (FrameFormats.H_1,
        (TransferFunctions.RELATIVE_POSITION_SENSOR, TransferFunctions.DEFAULT_LINEAR_TEMPERATURE) ), 
    0x076: # Relative Position / Ratio
        (FrameFormats.H_1,
        (TransferFunctions.RELATIVE_POSITION_SENSOR, TransferFunctions.RATIO_SENSING) ),                    
    0x080: # Coded Position
        (FrameFormats.H_2,
        (None, None) ),                                                                            
    0x081: # Coded Position
        (FrameFormats.H_1,
        (None, None) ),                                                                            
    0x082: # Coded Position (high speed)
        (FrameFormats.H_3,
        (None, None) ),                                                                            
    0x083: # Coded Position 1 / Coded Position 2
        (FrameFormats.H_1,
        (None, None) ),                                                                            
    0x084: # Coded Position / Secure Sensor
        (FrameFormats.H_4,
        (None, None) ),                                                                            
    0x085: # Coded Position / Temperature
        (FrameFormats.H_1,
        (None, TransferFunctions.DEFAULT_LINEAR_TEMPERATURE) ),                                    
    0x0B1: # Ratio
        (FrameFormats.H_2,
        (TransferFunctions.RATIO_SENSING, None) ),                                                 
    0x0B2: # Ratio
        (FrameFormats.H_1,
        (TransferFunctions.RATIO_SENSING, None) ),                                                 
    0x0B3: # Ratio (high speed)
        (FrameFormats.H_3,
        (TransferFunctions.RATIO_SENSING, None) ),                                                 
    0x0B4: # Ratio 1 / Ratio 2
        (FrameFormats.H_1,
        (TransferFunctions.RATIO_SENSING, TransferFunctions.RATIO_SENSING) ),                      
    0x0B5: # Ratio / Secure Sensor
        (FrameFormats.H_4,
        (TransferFunctions.RATIO_SENSING, None) ),                                                 
    0x0B6: # Ratio / Temperature
        (FrameFormats.H_1,
        (TransferFunctions.RATIO_SENSING, TransferFunctions.DEFAULT_LINEAR_TEMPERATURE) ),         
    0x0B7: # Ratio / Pressure
        (FrameFormats.H_1,
        (TransferFunctions.RATIO_SENSING, TransferFunctions.LINEAR_PRESSURE) ),                    
}

def decode(sensor: int, data: tuple, x_vals_raw: tuple = None, y_vals: tuple = None):
    
    global sensor_definitions

    ff,     tf_info = sensor_definitions[sensor]
    ch1_tf, ch2_tf  = tf_info

    inorder_data = __nibbles_to_int(data, ff)

    ch1_n,    ch2_n    = inorder_data[0]
    ch1_data, ch2_data = inorder_data[1]

    ''' Obtain default y_vals if there were no y_vals provided from the caller '''
    if y_vals is None:
        yv = []

        yv.append( __default_y_vals(ch1_n) )

        if ch2_n is not None:
            yv.append( __default_y_vals(ch2_n) )
        
        y_vals = tuple(yv)

    toRet = []

    toRet.append( __channel_data_decode(ch1_data, ch1_tf, x_vals_raw[0], y_vals[0]) )

    if ch2_data is not None:
        toRet.append( __channel_data_decode(ch2_data, ch2_tf, x_vals_raw[1], y_vals[1]) )

    return tuple(toRet)

def __channel_data_decode(data: int, transfer_function: TransferFunctions, x_vals_raw: tuple, y_vals: tuple):
    '''
    Returns a tuple containing the transformed data as a number, and the unit as a string.
    
    Example: (1667.23, "kPa")
    '''
    
    tf = transfer_function

    nm, ne, xe_offset, m_format, e_format = None

    # if  tf == TransferFunctions.E_2:
    #     pass

    return (1337.69, "kPa")

def __nibbles_to_int(nibbles, frame_format):
    '''
    Determine the bit-width for the sensor being decoded +
    the in-order data nibbles for each channel, depending on the frame format.

    Returns a tuple containing: ( (ch1_n, ch2_n), (ch1_data, ch2_data) ).
    If the format doesn't contain a second channel, it will be assigned None.
    '''

    ff = frame_format
    data = nibbles

    ch1_n = None
    ch2_n = None
    
    ch1_data = None
    ch2_data = None

    if   ff == FrameFormats.H_1:
        ch1_n = 12
        ch2_n = 12
        ch1_data = (data[0] << 8) | (data[1] << 4) | (data[2])
        ch2_data = (data[3] << 8) | (data[4] << 4) | (data[5])
    elif ff == FrameFormats.H_2:
        ch1_n = 12
        ch1_data = (data[0] << 8) | (data[1] << 4) | (data[2])
    elif ff == FrameFormats.H_3:
        ch1_n = 12
        ch1_data = (data[0] << 9) | (data[1] << 6) | (data[2] << 3) | (data[3])
    elif ff == FrameFormats.H_4:
        ch1_n = 12
        ch1_data = (data[0] << 8) | (data[1] << 4) | (data[2])
    elif ff == FrameFormats.H_5:
        ch1_n = 12
        ch1_data = (data[0] << 8) | (data[1] << 4) | (data[2])
    elif ff == FrameFormats.H_6:
        ch1_n = 14
        ch2_n = 10
        # TODO: Confirm that H_6 is being properly decoded.
        ch1_data = (data[0] << 11) | (data[1] << 7) | (data[2] << 3) | (data[3])
        ch2_data = (data[5] << 6) | (data[4] << 2) | (data[3] & 0b0011)
    elif ff == FrameFormats.H_7:
        ch1_n = 16
        ch2_n = 8
        ch1_data = (data[0] << 12) | (data[1] << 8) | (data[2] << 4) | (data[3])
        ch2_data = (data[5] << 4) | (data[4])
    elif ff == FrameFormats.F1_1 or FrameFormats.F1_2 or FrameFormats.F1_3:
        ch1_n = 12
        ch1_data = (data[1] << 8) | (data[2] << 4) | (data[3])
    elif ff == FrameFormats.F1_4 or FrameFormats.F1_5 or FrameFormats.F1_6:
        ch1_n = 12
        ch1_data = (data[2] << 8) | (data[3] << 4) | (data[4])
    elif ff == FrameFormats.F2_1 or FrameFormats.F2_2 or FrameFormats.F2_3:
        ch1_n = 16
        ch1_data = (data[1] << 12) | (data[2] << 8) | (data[3] << 4) | (data[4])
    elif ff == FrameFormats.F2_4:
        ch1_n = 16
        ch1_data = (data[2] << 12) | (data[3] << 8) | (data[4] << 4) | (data[5])
    elif ff == FrameFormats.F3_1:
        ch1_n = 12
        ch2_n = 8
        ch1_data = (data[1] << 8) | (data[2] << 4) | (data[3])
        ch2_data = (data[5] << 4) | (data[4])
    elif ff == FrameFormats.F3_2:
        ch1_n = 10
        ch2_n = 10
        # TODO: Confirm that F3.2 is being properly decoded.
        ch1_data = (data[1] << 6) | (data[2] << 2) | (data[3] >> 2)
        ch2_data = (data[5] << 6) | (data[4] << 2) | (data[3] & 0b0011)
    else:
        raise NotImplementedError(f"Frame format {ff.name} is not yet implemented in this HLA.")

    return ( (ch1_n, ch2_n), (ch1_data, ch2_data) )

def __default_y_vals(bit_width: int):
    n = bit_width
    y1 = math.ceil( 0.047 * ( (2 ** n) - 8 ) )
    y2 = (2 ** n) - 7 - y1

    return (y1, y2)