from enum import Enum
import copy

class MessageTypes(Enum):
    AIR_TEMPERATURE_HIGH     = 0x0
    AIR_TEMPERATURE_LOW      = 0x1
    RELATIVE_HUMIDITY_HIGH   = 0x2
    RELATIVE_HUMIDITY_LOW    = 0x3
    BAROMETRIC_PRESSURE_HIGH = 0x4
    BAROMETRIC_PRESSURE_LOW  = 0x5
    RESERVED                 = 0x6
    ERROR_CODES              = 0xF

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

    id = copy.deepcopy(message_id)

    # If the message id is in the reserved range, set the id to
    # be the single numerical value of the reserved enum value.
    if 0x6 <= id <= 0xE:
        id = 0x6

    mt = MessageTypes(id & 0xF)
    ec = []

    if mt == MessageTypes.ERROR_CODES:
        for i in range(8):
            if __bit_get(data, i):
                ec.append(ErrorCodes(i))

    str = __message_to_string(mt, ec, data)

    retval = [str, mt]

    # If there were any error codes, append them as a tuple.
    if len(ec) > 0:
        retval.append(tuple(ec))
    
    return tuple(retval)

def __message_to_string(mt: MessageTypes, ec: list, data: int):

    retval = ""

    if   mt == MessageTypes.AIR_TEMPERATURE_HIGH:
        retval += "Air Temperature high-order byte"
    elif mt == MessageTypes.AIR_TEMPERATURE_LOW:
        retval += "Air Temperature low-order byte"
    elif mt == MessageTypes.RELATIVE_HUMIDITY_HIGH:
        retval += "Relative humidity high-order byte"
    elif mt == MessageTypes.RELATIVE_HUMIDITY_LOW:
        retval += "Relative humidity low-order byte"
    elif mt == MessageTypes.BAROMETRIC_PRESSURE_HIGH:
        retval += "Barometric pressure high-order byte"
    elif mt == MessageTypes.BAROMETRIC_PRESSURE_LOW:
        retval += "Barometric pressure low-order byte"
    elif mt == MessageTypes.RESERVED:
        retval += "Reserved message"
    elif mt == MessageTypes.ERROR_CODES:
        retval += "Error codes"

    retval += ": "

    if mt != MessageTypes.ERROR_CODES:
        retval += f"{'{0:08b}'.format(data)} - {data}"
    else:
        retval += str(ec)

    return retval

def __bit_get(val: int, bit: int):
    return (val >> bit) & 0x1