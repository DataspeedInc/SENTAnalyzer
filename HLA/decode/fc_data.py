from enum import Enum, auto
import math
import copy

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
    #SENSOR_SPECIFIC_MAF        = auto()
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
        (None, None) ),                                           
    0x013: # MAF (hi-res, lin) / Pressure
        (FrameFormats.H_7,
        (TransferFunctions.LINEAR_MAF, TransferFunctions.LINEAR_PRESSURE) ),                       
    0x014: # MAF (hi-res, non-lin) / Pressure
        (FrameFormats.H_7,
        (None, TransferFunctions.LINEAR_PRESSURE) ),              
    0x015: # MAF (lin) / Pressure (hi-res)
        (FrameFormats.H_6,
        (TransferFunctions.LINEAR_MAF, TransferFunctions.LINEAR_PRESSURE) ),                       
    0x016: # MAF (non-lin) / Pressure (hi-res)
        (FrameFormats.H_6,
        (None, TransferFunctions.LINEAR_PRESSURE) ),              
    0x017: # MAF (lin)
        (FrameFormats.H_6,
        (TransferFunctions.LINEAR_MAF, None) ),                                                    
    0x018: # MAF (non-lin)
        (FrameFormats.H_6,
        (None, None) ),                                           
    0x019: # MAF (lin) / Temperature
        (FrameFormats.H_6,
        (TransferFunctions.LINEAR_MAF, TransferFunctions.DEFAULT_LINEAR_TEMPERATURE) ),            
    0x01A: # MAF (non-lin) / Temperature
        (FrameFormats.H_6,
        (None, TransferFunctions.DEFAULT_LINEAR_TEMPERATURE) ),   
    0x01B: # MAF (hi-res, lin) / Temperature
        (FrameFormats.H_7,
        (TransferFunctions.LINEAR_MAF, TransferFunctions.DEFAULT_LINEAR_TEMPERATURE) ),            
    0x01C: # MAF (hi-res, non-lin) / Temperature
        (FrameFormats.H_7,
        (None, TransferFunctions.DEFAULT_LINEAR_TEMPERATURE) ),   
    0x01D: # MAF (low-res, non-lin)
        (FrameFormats.H_1,
        (None, None) ),                                           
    0x01E: # MAF (low-res, non-lin) / Pressure
        (FrameFormats.H_1,
        (None, TransferFunctions.LINEAR_PRESSURE) ),              
    0x01F: # MAF (low-res, non-lin) / Temperature
        (FrameFormats.H_1,
        (None, TransferFunctions.DEFAULT_LINEAR_TEMPERATURE) ),   
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

def decode(sensor: int, data: tuple, x_vals_raw: tuple = ((None, None), (None, None)), y_vals: tuple = ((None, None), (None, None))):
    '''
    Expects assigned values for sensor and data at minimum.

    Returns a tuple of tuples, with each sub-tuple containing the converted value + unit pair for each channel.

    Example Return:
    ( (123.45, 'K'), (324.33, 'Pa') )

    If one of the channels doesn't exist, or cannot be converted, the sub-tuple for that channel will be None.
    '''
    
    global sensor_definitions

    # Copy parameters from the caller. #
    sensor     = copy.deepcopy(sensor)
    data       = copy.deepcopy(data)
    x_vals_raw = copy.deepcopy(x_vals_raw)
    y_vals     = list(copy.deepcopy(y_vals))

    ff,     tf_info = sensor_definitions[sensor]
    ch1_tf, ch2_tf  = tf_info

    inorder_data = __nibbles_to_int(data, ff)

    ch1_n,    ch2_n    = inorder_data[0]
    ch1_data, ch2_data = inorder_data[1]

    ''' Obtain default y_vals if there were no y_vals provided from the caller '''
    # Check / correct Ch 1. y Vals #
    if ch1_n is not None and (y_vals[0][0] is None or y_vals[0][1] is None):
        y_vals[0] = __default_y_vals(ch1_n)

    # Check / correct Ch 2. y Vals #
    if ch2_n is not None and (y_vals[1][0] is None or y_vals[1][1] is None):
        y_vals[1] = __default_y_vals(ch2_n)

    toRet = []

    toRet.append( __channel_data_decode(ch1_data, ch1_n, ch1_tf, x_vals_raw[0], tuple(y_vals[0])) )

    toRet.append( __channel_data_decode(ch2_data, ch2_n, ch2_tf, x_vals_raw[1], tuple(y_vals[1])) )

    return tuple(toRet)

def __channel_data_decode(data: int, bit_width:int, transfer_function: TransferFunctions, x_vals_raw: tuple, y_vals: tuple):
    '''
    If the data can be decoded with the information provided,
    this returns a tuple containing the transformed data as a number, and the unit as a string.
    
    Example: (1667.23, "kPa")

    Otherwise, None is returned.
    '''
    
    class TFType(Enum):
        LINEAR         = auto()
        DEFAULT_LINEAR = auto()
        RATIO          = auto()

    tf_type = None

    tf = transfer_function

    default_linear_lsb_per = None
    default_linear_offset = None

    nm = ne = xe_offset = m_format = e_format = None
    
    unit = ""

    '''
    Set the decoding variables necessary for the calculation 
    depending on the transfer function.
    '''
    if   tf == TransferFunctions.LINEAR_PRESSURE:
        tf_type = TFType.LINEAR
        unit = 'Pa'
        nm = 9
        m_format = ValueFormat.SIGNED
        ne = 3
        e_format = ValueFormat.UNSIGNED
        xe_offset = 0
    elif tf == TransferFunctions.SPECIAL_LINEAR_TEMPERATURE:
        tf_type = TFType.LINEAR
        unit = 'K'
        nm = 11
        m_format = ValueFormat.UNSIGNED
        ne = 1
        e_format = ValueFormat.SIGNED
        xe_offset = 0
    elif tf == TransferFunctions.DEFAULT_LINEAR_TEMPERATURE:
        tf_type = TFType.DEFAULT_LINEAR
        unit = 'K'
        char = {
            12: (8, 200),
            10: (4, 220),
            8:  (1, 220),
        }
        
        is_default_linear      = True
        default_linear_lsb_per = char[bit_width][0]
        default_linear_offset  = char[bit_width][1]
    elif tf == TransferFunctions.LINEAR_MAF:
        tf_type = TFType.LINEAR
        unit = 'kg/h'
        nm = 10
        m_format = ValueFormat.SIGNED
        ne = 2
        e_format = ValueFormat.UNSIGNED
        xe_offset = 0
    elif tf == TransferFunctions.LINEAR_HIGH_TEMPERATURE:
        tf_type = TFType.DEFAULT_LINEAR
        unit = 'K'
        is_default_linear      = True
        default_linear_lsb_per = 3
        default_linear_offset  = 200
    elif tf == TransferFunctions.LINEAR_POSITION_SENSOR:
        tf_type = TFType.LINEAR
        unit = 'm'
        nm = 9
        m_format = ValueFormat.SIGNED
        ne = 3
        e_format = ValueFormat.UNSIGNED
        xe_offset = -6
    elif tf == TransferFunctions.ANGLE_POSITION_SENSOR:
        tf_type = TFType.LINEAR
        unit = '°'
        nm = 9
        m_format = ValueFormat.SIGNED
        ne = 3
        e_format = ValueFormat.UNSIGNED
        xe_offset = -3
    elif tf == TransferFunctions.RELATIVE_POSITION_SENSOR:
        tf_type = TFType.LINEAR
        unit = 'm'
        nm = 9
        m_format = ValueFormat.SIGNED
        ne = 3
        e_format = ValueFormat.UNSIGNED
        xe_offset = -3
    elif tf == TransferFunctions.RATIO_SENSING:
        unit = '%'
        tf_type = TFType.RATIO

    ''' Calculate the unit. '''

    value = None

    if   tf_type == TFType.LINEAR:
        def x_val_parsing(x_val: int):
            m_corrected = e_corrected = None

            if m_format == ValueFormat.SIGNED:
                m_corrected = __tc_correction(x_val >> ne, nm)
            else:
                m_corrected = ( x_val >> ne ) & (2 ** nm - 1)

            if e_format == ValueFormat.SIGNED:
                e_corrected = __tc_correction(x_val, ne)
            else:
                e_corrected = ( x_val ) & (2 ** ne - 1)\

            print(f"m_corrected: {m_corrected}, e_corrected: {e_corrected}")

            return m_corrected * ( 10 ** ( e_corrected + xe_offset ) )
        
        x1_raw, x2_raw = x_vals_raw

        if x1_raw is not None and x2_raw is not None:
            x1 = x_val_parsing(x1_raw)
            x2 = x_val_parsing(x2_raw)

            y1, y2 = y_vals

            value = x1 + ( (x2 - x1) / (y2 - y1) * (data - y1) )
        else:
            # Assign the value to be returned as none, since the custom linear data
            # cannot be properly decoded without provided x values.
            value = None
    elif tf_type == TFType.DEFAULT_LINEAR:
        value = (data * default_linear_lsb_per) + default_linear_offset
    elif tf_type == TFType.RATIO:
        value = (data - 444) / 32

    if value is not None:
        return (value, unit)
    else:
        return None

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

def __tc_correction(val: int, width: int):
    '''
    Interprets val to be an integer with a bit-width of width as a 2's compliment number.

    Returns a python int representing that corrected number.
    '''

    mask = ( 2 ** width ) - 1

    # Copy and mask off the value to the given width.
    v = copy.deepcopy(val) & mask

    twos_neg = ( v >> (width - 1) ) & 0x1

    if twos_neg:
        # Convert the twos negative value to it's unsigned version, and multiply it by -1.
        v ^= mask
        v += 1

        v *= -1

    return v