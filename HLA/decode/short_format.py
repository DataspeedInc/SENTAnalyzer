from enum import Enum
import copy

class MessageTypes(Enum):
    AIR_TEMPERATURE_HIGH     = 0x0
    AIR_TEMPERATURE_LOW      = 0x1
    RELATIVE_HUMIDITY_HIGH   = 0x2
    RELATIVE_HUMIDITY_LOW    = 0x3
    BAROMETRIC_PRESSURE_HIGH = 0x4
    BAROMETRIC_PRESSURE_LOW  = 0x5
    RESERVED                 = 0x6#-0xE
    ERROR_CODES              = 0xF

    def correct(val: int):
        v = copy.deepcopy(val)
        
        # RESERVED correction
        if (0x6 < v <= 0xE):
            v = 0x6
        
        return v
    
    def convert(val: int):
        return MessageTypes( MessageTypes.correct(val) )

class ErrorCodes(Enum):
    AIR_TEMPERATURE_OOR_HIGH     = 0x0
    AIR_TEMPERATURE_OOR_LOW      = 0x1
    RELATIVE_HUMIDITY_OOR_HIGH   = 0x2
    RELATIVE_HUMIDITY_OOR_LOW    = 0x3
    BAROMETRIC_PRESSURE_OOR_HIGH = 0x4
    BAROMETRIC_PRESSURE_OOR_LOW  = 0x5
    RESERVED_0                   = 0x6
    RESERVED_1                   = 0x7

def decode(message_id: int, data: int):
    '''
    Decodes a short-format slow-channel message,
    returning a tuple which includes:
    - A string representation of the data.
    - An enum representing the message type.
    - (If applicable) A tuple of the applicable error codes.
    '''

    mt = MessageTypes.convert(message_id & 0xF)
    ec = []

    if mt == MessageTypes.ERROR_CODES:
        for i in range(8):
            if __bit_get(data, i):
                ec.append(ErrorCodes(i))

    str = __message_to_string(mt, ec, data)

    toRet = [str, mt]

    # If there were any error codes, append them as a tuple.
    if len(ec) > 0:
        toRet.append(tuple(ec))
    
    return tuple(toRet)

def __message_to_string(mt: MessageTypes, ec: list, data: int):

    toRet = ""

    if   mt == MessageTypes.AIR_TEMPERATURE_HIGH:
        toRet += "Air Temperature high-order byte"
    elif mt == MessageTypes.AIR_TEMPERATURE_LOW:
        toRet += "Air Temperature low-order byte"
    elif mt == MessageTypes.RELATIVE_HUMIDITY_HIGH:
        toRet += "Relative humidity high-order byte"
    elif mt == MessageTypes.RELATIVE_HUMIDITY_LOW:
        toRet += "Relative humidity low-order byte"
    elif mt == MessageTypes.BAROMETRIC_PRESSURE_HIGH:
        toRet += "Barometric pressure high-order byte"
    elif mt == MessageTypes.BAROMETRIC_PRESSURE_LOW:
        toRet += "Barometric pressure low-order byte"
    elif mt == MessageTypes.RESERVED:
        toRet += "Reserved message"
    elif mt == MessageTypes.ERROR_CODES:
        toRet += "Error codes"

    toRet += ": "

    if mt != MessageTypes.ERROR_CODES:
        toRet += '{0:08b} : 0x{0:02X} : {0}'.format(data)
    else:
        toRet += str(ec)

    return toRet

def __bit_get(val: int, bit: int):
    return (val >> bit) & 0x1