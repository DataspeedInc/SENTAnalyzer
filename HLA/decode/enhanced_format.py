from enum import Enum
import copy

class MessageTypes4Bit(Enum):
    AIR_TEMPERATURE     = 0x0
    UNDEFINED           = 0x1
    HUMIDITY            = 0x2
    # UNDEFINED         = 0x3
    BAROMETRIC_PRESSURE = 0x4
    # UNDEFINED         = 0x5 - 0xF

class MessageTypes8Bit(Enum):
    NOT_ASSIGNED                              = 0x00
    ERROR_AND_STATUS                          = 0x01
    RESERVED                                  = 0x02
    CHANNEL_1_2_SENSOR_TYPE                   = 0x03
    CONFIGURATION_CODE                        = 0x04
    MANUFACTURER_CODE                         = 0x05
    PROTOCOL_STD_REVISION                     = 0x06
    FC_1_CHARACTERISTIC_X1                    = 0x07
    FC_1_CHARACTERISTIC_X2                    = 0x08
    FC_1_CHARACTERISTIC_Y1                    = 0x09
    FC_1_CHARACTERISTIC_Y2                    = 0x0A
    FC_2_CHARACTERISTIC_X1                    = 0x0B
    FC_2_CHARACTERISTIC_X2                    = 0x0C
    FC_2_CHARACTERISTIC_Y1                    = 0x0D
    FC_2_CHARACTERISTIC_Y2                    = 0x0E
    # NOT_ASSIGNED                            = 0x0F
    SUPPLEMENTARY_DATA_CH_1_1                 = 0x10
    SUPPLEMENTARY_DATA_CH_1_2                 = 0x11
    SUPPLEMENTARY_DATA_CH_1_CHARACTERISTIC_X1 = 0x12
    SUPPLEMENTARY_DATA_CH_1_CHARACTERISTIC_X2 = 0x13
    SUPPLEMENTARY_DATA_CH_1_CHARACTERISTIC_Y1 = 0x14
    SUPPLEMENTARY_DATA_CH_1_CHARACTERISTIC_Y2 = 0x15
    SUPPLEMENTARY_DATA_CH_2_1                 = 0x16
    SUPPLEMENTARY_DATA_CH_2_2                 = 0x17
    SUPPLEMENTARY_DATA_CH_2_CHARACTERISTIC_X1 = 0x18
    SUPPLEMENTARY_DATA_CH_2_CHARACTERISTIC_X2 = 0x19
    SUPPLEMENTARY_DATA_CH_2_CHARACTERISTIC_Y1 = 0x1A
    SUPPLEMENTARY_DATA_CH_2_CHARACTERISTIC_Y2 = 0x1B
    SUPPLEMENTARY_DATA_CH_3_1                 = 0x1C
    SUPPLEMENTARY_DATA_CH_3_2                 = 0x1D
    SUPPLEMENTARY_DATA_CH_3_CHARACTERISTIC_X1 = 0x1E
    # RESERVED                                = 0x1F
    SUPPLEMENTARY_DATA_CH_3_CHARACTERISTIC_X2 = 0x20
    SUPPLEMENTARY_DATA_CH_3_CHARACTERISTIC_Y1 = 0x21
    SUPPLEMENTARY_DATA_CH_3_CHARACTERISTIC_Y2 = 0x22
    SUPPLEMENTARY_DATA_CH_4_1                 = 0x23
    SUPPLEMENTARY_DATA_CH_4_2                 = 0x24
    SUPPLEMENTARY_DATA_CH_4_CHARACTERISTIC_X1 = 0x25
    SUPPLEMENTARY_DATA_CH_4_CHARACTERISTIC_X2 = 0x26
    SUPPLEMENTARY_DATA_CH_4_CHARACTERISTIC_Y1 = 0x27
    SUPPLEMENTARY_DATA_CH_4_CHARACTERISTIC_Y2 = 0x28
    SENSOR_ID_1                               = 0x29
    SENSOR_ID_2                               = 0x2A
    SENSOR_ID_3                               = 0x2B
    SENSOR_ID_4                               = 0x2C
    # RESERVED                                = 0x2D - 0x7F
    OEM_DEFINED                               = 0x80#- 0x8F
    ASCII_OEM_CODES                           = 0x90#- 0x97
    # OEM_DEFINED                             = 0x98 - 0xFF

class ErrorCodes(Enum):
    NO_ERROR                                    = 0x000
    CH_1_OOR_HIGH                               = 0x001
    CH_1_OOR_LOW                                = 0x002
    CH_1_INIT_ERROR                             = 0x003
    CH_2_OOR_HIGH                               = 0x004
    CH_2_OOR_LOW                                = 0x005
    CH_2_INIT_ERROR                             = 0x006
    CH_1_AND_2_RATIONALITY_ERROR                = 0x007
    FAST_CHANNEL_STATUS                         = 0x008#- 0x01F
    UNDERVOLTAGE_STATUS                         = 0x020
    OVERVOLTAGE_STATUS                          = 0x021
    OVERTEMPERATURE_STATUS                      = 0x022
    SENSOR_ERROR_AND_STATUS                     = 0x023#- 0x02F
    RESERVED                                    = 0x030#- 0x100
    # FC Multiplexing #
    # FC 0
    MULTIPLEXED_1ST_FC_FRAME_0_OOR_HIGH         = 0x101
    MULTIPLEXED_1ST_FC_FRAME_0_OOR_LOW          = 0x102
    MULTIPLEXED_1ST_FC_FRAME_0_INIT_ERROR       = 0x103
    MULTIPLEXED_2ND_FC_FRAME_0_OOR_HIGH         = 0x104
    MULTIPLEXED_2ND_FC_FRAME_0_OOR_LOW          = 0x105
    MULTIPLEXED_2ND_FC_FRAME_0_INIT_ERROR       = 0x106
    MULTIPLEXED_1_2_FRAME_0_RATIONALITY_ERROR   = 0x107
    MULTIPLEXED_FC_FRAME_0_STATUS               = 0x108#- 0x10F
    # FC 1
    MULTIPLEXED_1ST_FC_FRAME_1_OOR_HIGH         = 0x111
    MULTIPLEXED_1ST_FC_FRAME_1_OOR_LOW          = 0x112
    MULTIPLEXED_1ST_FC_FRAME_1_INIT_ERROR       = 0x113
    MULTIPLEXED_2ND_FC_FRAME_1_OOR_HIGH         = 0x114
    MULTIPLEXED_2ND_FC_FRAME_1_OOR_LOW          = 0x115
    MULTIPLEXED_2ND_FC_FRAME_1_INIT_ERROR       = 0x116
    MULTIPLEXED_1_2_FRAME_1_RATIONALITY_ERROR   = 0x117
    MULTIPLEXED_FC_FRAME_1_STATUS               = 0x118#- 0x11F
    # FC 2
    MULTIPLEXED_1ST_FC_FRAME_2_OOR_HIGH         = 0x121
    MULTIPLEXED_1ST_FC_FRAME_2_OOR_LOW          = 0x122
    MULTIPLEXED_1ST_FC_FRAME_2_INIT_ERROR       = 0x123
    MULTIPLEXED_2ND_FC_FRAME_2_OOR_HIGH         = 0x124
    MULTIPLEXED_2ND_FC_FRAME_2_OOR_LOW          = 0x125
    MULTIPLEXED_2ND_FC_FRAME_2_INIT_ERROR       = 0x126
    MULTIPLEXED_1_2_FRAME_2_RATIONALITY_ERROR   = 0x127
    MULTIPLEXED_FC_FRAME_2_STATUS               = 0x128#- 0x12F
    # FC 3
    MULTIPLEXED_1ST_FC_FRAME_3_OOR_HIGH         = 0x131
    MULTIPLEXED_1ST_FC_FRAME_3_OOR_LOW          = 0x132
    MULTIPLEXED_1ST_FC_FRAME_3_INIT_ERROR       = 0x133
    MULTIPLEXED_2ND_FC_FRAME_3_OOR_HIGH         = 0x134
    MULTIPLEXED_2ND_FC_FRAME_3_OOR_LOW          = 0x135
    MULTIPLEXED_2ND_FC_FRAME_3_INIT_ERROR       = 0x136
    MULTIPLEXED_1_2_FRAME_3_RATIONALITY_ERROR   = 0x137
    MULTIPLEXED_FC_FRAME_3_STATUS               = 0x138#- 0x13F
    # FC 4
    MULTIPLEXED_1ST_FC_FRAME_4_OOR_HIGH         = 0x141
    MULTIPLEXED_1ST_FC_FRAME_4_OOR_LOW          = 0x142
    MULTIPLEXED_1ST_FC_FRAME_4_INIT_ERROR       = 0x143
    MULTIPLEXED_2ND_FC_FRAME_4_OOR_HIGH         = 0x144
    MULTIPLEXED_2ND_FC_FRAME_4_OOR_LOW          = 0x145
    MULTIPLEXED_2ND_FC_FRAME_4_INIT_ERROR       = 0x146
    MULTIPLEXED_1_2_FRAME_4_RATIONALITY_ERROR   = 0x147
    MULTIPLEXED_FC_FRAME_4_STATUS               = 0x148#- 0x14F
    # FC 5
    MULTIPLEXED_1ST_FC_FRAME_5_OOR_HIGH         = 0x151
    MULTIPLEXED_1ST_FC_FRAME_5_OOR_LOW          = 0x152
    MULTIPLEXED_1ST_FC_FRAME_5_INIT_ERROR       = 0x153
    MULTIPLEXED_2ND_FC_FRAME_5_OOR_HIGH         = 0x154
    MULTIPLEXED_2ND_FC_FRAME_5_OOR_LOW          = 0x155
    MULTIPLEXED_2ND_FC_FRAME_5_INIT_ERROR       = 0x156
    MULTIPLEXED_1_2_FRAME_5_RATIONALITY_ERROR   = 0x157
    MULTIPLEXED_FC_FRAME_5_STATUS               = 0x158#- 0x15F
    # FC 6
    MULTIPLEXED_1ST_FC_FRAME_6_OOR_HIGH         = 0x161
    MULTIPLEXED_1ST_FC_FRAME_6_OOR_LOW          = 0x162
    MULTIPLEXED_1ST_FC_FRAME_6_INIT_ERROR       = 0x163
    MULTIPLEXED_2ND_FC_FRAME_6_OOR_HIGH         = 0x164
    MULTIPLEXED_2ND_FC_FRAME_6_OOR_LOW          = 0x165
    MULTIPLEXED_2ND_FC_FRAME_6_INIT_ERROR       = 0x166
    MULTIPLEXED_1_2_FRAME_6_RATIONALITY_ERROR   = 0x167
    MULTIPLEXED_FC_FRAME_6_STATUS               = 0x168#- 0x16F
    # FC 7
    MULTIPLEXED_1ST_FC_FRAME_7_OOR_HIGH         = 0x171
    MULTIPLEXED_1ST_FC_FRAME_7_OOR_LOW          = 0x172
    MULTIPLEXED_1ST_FC_FRAME_7_INIT_ERROR       = 0x173
    MULTIPLEXED_2ND_FC_FRAME_7_OOR_HIGH         = 0x174
    MULTIPLEXED_2ND_FC_FRAME_7_OOR_LOW          = 0x175
    MULTIPLEXED_2ND_FC_FRAME_7_INIT_ERROR       = 0x176
    MULTIPLEXED_1_2_FRAME_7_RATIONALITY_ERROR   = 0x177
    MULTIPLEXED_FC_FRAME_7_STATUS               = 0x178#- 0x17F
    # FC 8
    MULTIPLEXED_1ST_FC_FRAME_8_OOR_HIGH         = 0x181
    MULTIPLEXED_1ST_FC_FRAME_8_OOR_LOW          = 0x182
    MULTIPLEXED_1ST_FC_FRAME_8_INIT_ERROR       = 0x183
    MULTIPLEXED_2ND_FC_FRAME_8_OOR_HIGH         = 0x184
    MULTIPLEXED_2ND_FC_FRAME_8_OOR_LOW          = 0x185
    MULTIPLEXED_2ND_FC_FRAME_8_INIT_ERROR       = 0x186
    MULTIPLEXED_1_2_FRAME_8_RATIONALITY_ERROR   = 0x187
    MULTIPLEXED_FC_FRAME_8_STATUS               = 0x188#- 0x18F
    # FC 9
    MULTIPLEXED_1ST_FC_FRAME_9_OOR_HIGH         = 0x191
    MULTIPLEXED_1ST_FC_FRAME_9_OOR_LOW          = 0x192
    MULTIPLEXED_1ST_FC_FRAME_9_INIT_ERROR       = 0x193
    MULTIPLEXED_2ND_FC_FRAME_9_OOR_HIGH         = 0x194
    MULTIPLEXED_2ND_FC_FRAME_9_OOR_LOW          = 0x195
    MULTIPLEXED_2ND_FC_FRAME_9_INIT_ERROR       = 0x196
    MULTIPLEXED_1_2_FRAME_9_RATIONALITY_ERROR   = 0x197
    MULTIPLEXED_FC_FRAME_9_STATUS               = 0x198#- 0x19F
    # FC 10
    MULTIPLEXED_1ST_FC_FRAME_10_OOR_HIGH        = 0x1A1
    MULTIPLEXED_1ST_FC_FRAME_10_OOR_LOW         = 0x1A2
    MULTIPLEXED_1ST_FC_FRAME_10_INIT_ERROR      = 0x1A3
    MULTIPLEXED_2ND_FC_FRAME_10_OOR_HIGH        = 0x1A4
    MULTIPLEXED_2ND_FC_FRAME_10_OOR_LOW         = 0x1A5
    MULTIPLEXED_2ND_FC_FRAME_10_INIT_ERROR      = 0x1A6
    MULTIPLEXED_1_2_FRAME_10_RATIONALITY_ERROR  = 0x1A7
    MULTIPLEXED_FC_FRAME_10_STATUS              = 0x1A8#- 0x1AF
    # FC 11
    MULTIPLEXED_1ST_FC_FRAME_11_OOR_HIGH        = 0x1B1
    MULTIPLEXED_1ST_FC_FRAME_11_OOR_LOW         = 0x1B2
    MULTIPLEXED_1ST_FC_FRAME_11_INIT_ERROR      = 0x1B3
    MULTIPLEXED_2ND_FC_FRAME_11_OOR_HIGH        = 0x1B4
    MULTIPLEXED_2ND_FC_FRAME_11_OOR_LOW         = 0x1B5
    MULTIPLEXED_2ND_FC_FRAME_11_INIT_ERROR      = 0x1B6
    MULTIPLEXED_1_2_FRAME_11_RATIONALITY_ERROR  = 0x1B7
    MULTIPLEXED_FC_FRAME_11_STATUS              = 0x1B8#- 0x1BF
    # FC 12
    MULTIPLEXED_1ST_FC_FRAME_12_OOR_HIGH        = 0x1C1
    MULTIPLEXED_1ST_FC_FRAME_12_OOR_LOW         = 0x1C2
    MULTIPLEXED_1ST_FC_FRAME_12_INIT_ERROR      = 0x1C3
    MULTIPLEXED_2ND_FC_FRAME_12_OOR_HIGH        = 0x1C4
    MULTIPLEXED_2ND_FC_FRAME_12_OOR_LOW         = 0x1C5
    MULTIPLEXED_2ND_FC_FRAME_12_INIT_ERROR      = 0x1C6
    MULTIPLEXED_1_2_FRAME_12_RATIONALITY_ERROR  = 0x1C7
    MULTIPLEXED_FC_FRAME_12_STATUS              = 0x1C8#- 0x1CF
    # FC 13
    MULTIPLEXED_1ST_FC_FRAME_13_OOR_HIGH        = 0x1D1
    MULTIPLEXED_1ST_FC_FRAME_13_OOR_LOW         = 0x1D2
    MULTIPLEXED_1ST_FC_FRAME_13_INIT_ERROR      = 0x1D3
    MULTIPLEXED_2ND_FC_FRAME_13_OOR_HIGH        = 0x1D4
    MULTIPLEXED_2ND_FC_FRAME_13_OOR_LOW         = 0x1D5
    MULTIPLEXED_2ND_FC_FRAME_13_INIT_ERROR      = 0x1D6
    MULTIPLEXED_1_2_FRAME_13_RATIONALITY_ERROR  = 0x1D7
    MULTIPLEXED_FC_FRAME_13_STATUS              = 0x1D8#- 0x1DF
    # FC 14
    MULTIPLEXED_1ST_FC_FRAME_14_OOR_HIGH        = 0x1E1
    MULTIPLEXED_1ST_FC_FRAME_14_OOR_LOW         = 0x1E2
    MULTIPLEXED_1ST_FC_FRAME_14_INIT_ERROR      = 0x1E3
    MULTIPLEXED_2ND_FC_FRAME_14_OOR_HIGH        = 0x1E4
    MULTIPLEXED_2ND_FC_FRAME_14_OOR_LOW         = 0x1E5
    MULTIPLEXED_2ND_FC_FRAME_14_INIT_ERROR      = 0x1E6
    MULTIPLEXED_1_2_FRAME_14_RATIONALITY_ERROR  = 0x1E7
    MULTIPLEXED_FC_FRAME_14_STATUS              = 0x1E8#- 0x1EF
    # FC 15
    MULTIPLEXED_1ST_FC_FRAME_15_OOR_HIGH        = 0x1F1
    MULTIPLEXED_1ST_FC_FRAME_15_OOR_LOW         = 0x1F2
    MULTIPLEXED_1ST_FC_FRAME_15_INIT_ERROR      = 0x1F3
    MULTIPLEXED_2ND_FC_FRAME_15_OOR_HIGH        = 0x1F4
    MULTIPLEXED_2ND_FC_FRAME_15_OOR_LOW         = 0x1F5
    MULTIPLEXED_2ND_FC_FRAME_15_INIT_ERROR      = 0x1F6
    MULTIPLEXED_1_2_FRAME_15_RATIONALITY_ERROR  = 0x1F7
    MULTIPLEXED_FC_FRAME_15_STATUS              = 0x1F8#- 0x1FF
    # RESERVED                                  = 0x200 - 0x400
    SUPPLEMENTARY_DATA_CH_1_1_OOR_HIGH          = 0x401
    SUPPLEMENTARY_DATA_CH_1_1_OOR_LOW           = 0x402
    SUPPLEMENTARY_DATA_CH_1_1_SIGNAL_INIT_ERROR = 0x403
    SUPPLEMENTARY_DATA_CH_2_1_OOR_HIGH          = 0x404
    SUPPLEMENTARY_DATA_CH_2_1_OOR_LOW           = 0x405
    SUPPLEMENTARY_DATA_CH_2_1_SIGNAL_INIT_ERROR = 0x406
    SUPPLEMENTARY_DATA_CH_3_1_OOR_HIGH          = 0x407
    SUPPLEMENTARY_DATA_CH_3_1_OOR_LOW           = 0x408
    SUPPLEMENTARY_DATA_CH_3_1_SIGNAL_INIT_ERROR = 0x409
    SUPPLEMENTARY_DATA_CH_4_1_OOR_HIGH          = 0x40A
    SUPPLEMENTARY_DATA_CH_4_1_OOR_LOW           = 0x40B
    SUPPLEMENTARY_DATA_CH_4_1_SIGNAL_INIT_ERROR = 0x40C
    SUPPLEMENTARY_DATA_CH_1_2_OOR_HIGH          = 0x40D
    SUPPLEMENTARY_DATA_CH_1_2_OOR_LOW           = 0x40E
    SUPPLEMENTARY_DATA_CH_1_2_SIGNAL_INIT_ERROR = 0x40F
    SUPPLEMENTARY_DATA_CH_2_2_OOR_HIGH          = 0x410
    SUPPLEMENTARY_DATA_CH_2_2_OOR_LOW           = 0x411
    SUPPLEMENTARY_DATA_CH_2_2_SIGNAL_INIT_ERROR = 0x412
    SUPPLEMENTARY_DATA_CH_3_2_OOR_HIGH          = 0x413
    SUPPLEMENTARY_DATA_CH_3_2_OOR_LOW           = 0x414
    SUPPLEMENTARY_DATA_CH_3_2_SIGNAL_INIT_ERROR = 0x415
    SUPPLEMENTARY_DATA_CH_4_2_OOR_HIGH          = 0x416
    SUPPLEMENTARY_DATA_CH_4_2_OOR_LOW           = 0x417
    SUPPLEMENTARY_DATA_CH_4_2_SIGNAL_INIT_ERROR = 0x418
    SUPPLEMENTARY_DATA_CH_ERROR_AND_STATUS      = 0x419#- 0x41F
    # RESERVED                                  = 0x420 - 0x7FF
    OEM_DEFINED                                 = 0x800#- 0xFFF

def decode_8bit_id(message_id: int, data: int):
    '''
    Decodes an enhanced-format slow-channel message with an 8bit ID,
    returning a tuple which includes:
    - A string representation of the data.
    - An enum representing the message type.
    - (If applicable) An error code.
    '''

    # Apply corrections to message IDs that are in undefined ranges, as to
    # have them be compatible with a MessageTypes8Bit enum.
    mid = copy.deepcopy(message_id)

    # NOT_ASSIGNED correction
    if mid == 0x0F:
        mid = 0x00
    # RESERVED correction
    if (mid == 0x1F) or (0x2D <= mid <= 0x7F):
        mid = 0x02
    # OEM_DEFINED correction
    if (0x81 <= mid <= 0x8F) or (0x98 <= mid <= 0xFF):
        mid = 0x80
    # ASCII_OEM_CODES correction
    if (0x91 <= mid <= 0x97):
        mid = 0x90

    mt = MessageTypes8Bit(mid)

    # Apply corrections to error codes that are in undefined ranges, as to
    # have them be compatible with a ErrorCodes enum.
    ec = None

    if mt == MessageTypes8Bit.ERROR_AND_STATUS:

        eid = copy.deepcopy(message_id)

        # FAST_CHANNEL_STATUS correction
        if (0x008 < eid <= 0x01F):
            eid = 0x008
        # SENSOR_ERROR_AND_STATUS correction
        if (0x023 < eid <= 0x02F):
            eid = 0x023
        # RESERVED correction
        if (0x030 < eid <= 0x100) or (0x200 <= eid <= 0x400) or (0x420 <= eid <= 0x7FF):
            eid = 0x30
        # MULTIPLEXED_FC_FRAME_0_STATUS correction
        if (0x108 < eid <= 0x10F):
            eid = 0x108
        # MULTIPLEXED_FC_FRAME_1_STATUS correction
        if (0x118 < eid <= 0x11F):
            eid = 0x118
        # MULTIPLEXED_FC_FRAME_2_STATUS correction
        if (0x128 < eid <= 0x12F):
            eid = 0x128
        # MULTIPLEXED_FC_FRAME_3_STATUS correction
        if (0x138 < eid <= 0x13F):
            eid = 0x138
        # MULTIPLEXED_FC_FRAME_4_STATUS correction
        if (0x148 < eid <= 0x14F):
            eid = 0x148
        # MULTIPLEXED_FC_FRAME_5_STATUS correction
        if (0x158 < eid <= 0x15F):
            eid = 0x158
        # MULTIPLEXED_FC_FRAME_6_STATUS correction
        if (0x168 < eid <= 0x16F):
            eid = 0x168
        # MULTIPLEXED_FC_FRAME_7_STATUS correction
        if (0x178 < eid <= 0x17F):
            eid = 0x178
        # MULTIPLEXED_FC_FRAME_8_STATUS correction
        if (0x188 < eid <= 0x18F):
            eid = 0x188
        # MULTIPLEXED_FC_FRAME_9_STATUS correction
        if (0x198 < eid <= 0x19F):
            eid = 0x198
        # MULTIPLEXED_FC_FRAME_10_STATUS correction
        if (0x1A8 < eid <= 0x1AF):
            eid = 0x1A8
        # MULTIPLEXED_FC_FRAME_11_STATUS correction
        if (0x1B8 < eid <= 0x1BF):
            eid = 0x1B8
        # MULTIPLEXED_FC_FRAME_12_STATUS correction
        if (0x1C8 < eid <= 0x1CF):
            eid = 0x1C8
        # MULTIPLEXED_FC_FRAME_13_STATUS correction
        if (0x1D8 < eid <= 0x1DF):
            eid = 0x1D8
        # MULTIPLEXED_FC_FRAME_14_STATUS correction
        if (0x1E8 < eid <= 0x1EF):
            eid = 0x1E8
        # MULTIPLEXED_FC_FRAME_15_STATUS correction
        if (0x1F8 < eid <= 0x1FF):
            eid = 0x1F8
        # SUPPLEMENTARY_DATA_CH_ERROR_AND_STATUS correction
        if (0x419 < eid <= 0x41F):
            eid = 0x419
        # OEM_DEFINED correction
        if (0x800 < eid <= 0xFFF):
            eid = 0x800

        ec = ErrorCodes(eid)
    
    toRet = ["-string rep-", mt]

    if ec is not None:
        toRet.append(ec)

    return tuple(toRet)


def decode_4bit_id(message_id: int, data: int):
    '''
    Decodes an enhanced-format slow-channel message with a 4bit ID,
    returning a tuple which includes:
    - A string representation of the data.
    - An enum representing the message type.
    - (If applicable) A tuple of the applicable error codes.
    '''

    # Apply corrections to message IDs that are in undefined ranges, as to
    # have them be compatible with a MessageTypes8Bit enum.
    id = copy.deepcopy(message_id)

    # UNDEFINED correction
    if (id == 0x3) or (0x5 <= id <= 0xF):
        id = 0x1

    mt = MessageTypes4Bit(id)