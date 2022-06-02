from enum import Enum
import copy

class MessageTypes4Bit(Enum):
    AIR_TEMPERATURE     = 0x0
    UNDEFINED           = 0x1
    HUMIDITY            = 0x2
    # UNDEFINED         = 0x3
    BAROMETRIC_PRESSURE = 0x4
    # UNDEFINED         = 0x5 - 0xF

    def correct(val: int):

        # Apply corrections to message IDs that are in undefined ranges, as to
        # have them be compatible with a MessageTypes8Bit enum.
        v = copy.deepcopy(val)

        # UNDEFINED correction
        if (v == 0x3) or (0x5 <= v <= 0xF):
            v = 0x1
        
        return v
    
    def convert(val: int):
        return MessageTypes4Bit( MessageTypes4Bit.correct(val) )

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

    def correct(val: int):

        # Apply corrections to message IDs that are in undefined ranges, as to
        # have them be compatible with a MessageTypes8Bit enum.
        v = copy.deepcopy(val)

        # NOT_ASSIGNED correction
        if v == 0x0F:
            v = 0x00
        # RESERVED correction
        elif (v == 0x1F) or (0x2D <= v <= 0x7F):
            v = 0x02
        # OEM_DEFINED correction
        elif (0x81 <= v <= 0x8F) or (0x98 <= v <= 0xFF):
            v = 0x80
        # ASCII_OEM_CODES correction
        elif (0x91 <= v <= 0x97):
            v = 0x90
        
        return v
    
    def convert(val: int):
        return MessageTypes8Bit( MessageTypes8Bit.correct(val) )

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
    MULTIPLEXED_1ST_FC_FRAME_0_OOR_HIGH         = 0x101
    MULTIPLEXED_1ST_FC_FRAME_0_OOR_LOW          = 0x102
    MULTIPLEXED_1ST_FC_FRAME_0_INIT_ERROR       = 0x103
    MULTIPLEXED_2ND_FC_FRAME_0_OOR_HIGH         = 0x104
    MULTIPLEXED_2ND_FC_FRAME_0_OOR_LOW          = 0x105
    MULTIPLEXED_2ND_FC_FRAME_0_INIT_ERROR       = 0x106
    MULTIPLEXED_1_2_FRAME_0_RATIONALITY_ERROR   = 0x107
    MULTIPLEXED_FC_FRAME_0_STATUS               = 0x108#- 0x10F
    MULTIPLEXED_1ST_FC_FRAME_1_OOR_HIGH         = 0x111
    MULTIPLEXED_1ST_FC_FRAME_1_OOR_LOW          = 0x112
    MULTIPLEXED_1ST_FC_FRAME_1_INIT_ERROR       = 0x113
    MULTIPLEXED_2ND_FC_FRAME_1_OOR_HIGH         = 0x114
    MULTIPLEXED_2ND_FC_FRAME_1_OOR_LOW          = 0x115
    MULTIPLEXED_2ND_FC_FRAME_1_INIT_ERROR       = 0x116
    MULTIPLEXED_1_2_FRAME_1_RATIONALITY_ERROR   = 0x117
    MULTIPLEXED_FC_FRAME_1_STATUS               = 0x118#- 0x11F
    MULTIPLEXED_1ST_FC_FRAME_2_OOR_HIGH         = 0x121
    MULTIPLEXED_1ST_FC_FRAME_2_OOR_LOW          = 0x122
    MULTIPLEXED_1ST_FC_FRAME_2_INIT_ERROR       = 0x123
    MULTIPLEXED_2ND_FC_FRAME_2_OOR_HIGH         = 0x124
    MULTIPLEXED_2ND_FC_FRAME_2_OOR_LOW          = 0x125
    MULTIPLEXED_2ND_FC_FRAME_2_INIT_ERROR       = 0x126
    MULTIPLEXED_1_2_FRAME_2_RATIONALITY_ERROR   = 0x127
    MULTIPLEXED_FC_FRAME_2_STATUS               = 0x128#- 0x12F
    MULTIPLEXED_1ST_FC_FRAME_3_OOR_HIGH         = 0x131
    MULTIPLEXED_1ST_FC_FRAME_3_OOR_LOW          = 0x132
    MULTIPLEXED_1ST_FC_FRAME_3_INIT_ERROR       = 0x133
    MULTIPLEXED_2ND_FC_FRAME_3_OOR_HIGH         = 0x134
    MULTIPLEXED_2ND_FC_FRAME_3_OOR_LOW          = 0x135
    MULTIPLEXED_2ND_FC_FRAME_3_INIT_ERROR       = 0x136
    MULTIPLEXED_1_2_FRAME_3_RATIONALITY_ERROR   = 0x137
    MULTIPLEXED_FC_FRAME_3_STATUS               = 0x138#- 0x13F
    MULTIPLEXED_1ST_FC_FRAME_4_OOR_HIGH         = 0x141
    MULTIPLEXED_1ST_FC_FRAME_4_OOR_LOW          = 0x142
    MULTIPLEXED_1ST_FC_FRAME_4_INIT_ERROR       = 0x143
    MULTIPLEXED_2ND_FC_FRAME_4_OOR_HIGH         = 0x144
    MULTIPLEXED_2ND_FC_FRAME_4_OOR_LOW          = 0x145
    MULTIPLEXED_2ND_FC_FRAME_4_INIT_ERROR       = 0x146
    MULTIPLEXED_1_2_FRAME_4_RATIONALITY_ERROR   = 0x147
    MULTIPLEXED_FC_FRAME_4_STATUS               = 0x148#- 0x14F
    MULTIPLEXED_1ST_FC_FRAME_5_OOR_HIGH         = 0x151
    MULTIPLEXED_1ST_FC_FRAME_5_OOR_LOW          = 0x152
    MULTIPLEXED_1ST_FC_FRAME_5_INIT_ERROR       = 0x153
    MULTIPLEXED_2ND_FC_FRAME_5_OOR_HIGH         = 0x154
    MULTIPLEXED_2ND_FC_FRAME_5_OOR_LOW          = 0x155
    MULTIPLEXED_2ND_FC_FRAME_5_INIT_ERROR       = 0x156
    MULTIPLEXED_1_2_FRAME_5_RATIONALITY_ERROR   = 0x157
    MULTIPLEXED_FC_FRAME_5_STATUS               = 0x158#- 0x15F
    MULTIPLEXED_1ST_FC_FRAME_6_OOR_HIGH         = 0x161
    MULTIPLEXED_1ST_FC_FRAME_6_OOR_LOW          = 0x162
    MULTIPLEXED_1ST_FC_FRAME_6_INIT_ERROR       = 0x163
    MULTIPLEXED_2ND_FC_FRAME_6_OOR_HIGH         = 0x164
    MULTIPLEXED_2ND_FC_FRAME_6_OOR_LOW          = 0x165
    MULTIPLEXED_2ND_FC_FRAME_6_INIT_ERROR       = 0x166
    MULTIPLEXED_1_2_FRAME_6_RATIONALITY_ERROR   = 0x167
    MULTIPLEXED_FC_FRAME_6_STATUS               = 0x168#- 0x16F
    MULTIPLEXED_1ST_FC_FRAME_7_OOR_HIGH         = 0x171
    MULTIPLEXED_1ST_FC_FRAME_7_OOR_LOW          = 0x172
    MULTIPLEXED_1ST_FC_FRAME_7_INIT_ERROR       = 0x173
    MULTIPLEXED_2ND_FC_FRAME_7_OOR_HIGH         = 0x174
    MULTIPLEXED_2ND_FC_FRAME_7_OOR_LOW          = 0x175
    MULTIPLEXED_2ND_FC_FRAME_7_INIT_ERROR       = 0x176
    MULTIPLEXED_1_2_FRAME_7_RATIONALITY_ERROR   = 0x177
    MULTIPLEXED_FC_FRAME_7_STATUS               = 0x178#- 0x17F
    MULTIPLEXED_1ST_FC_FRAME_8_OOR_HIGH         = 0x181
    MULTIPLEXED_1ST_FC_FRAME_8_OOR_LOW          = 0x182
    MULTIPLEXED_1ST_FC_FRAME_8_INIT_ERROR       = 0x183
    MULTIPLEXED_2ND_FC_FRAME_8_OOR_HIGH         = 0x184
    MULTIPLEXED_2ND_FC_FRAME_8_OOR_LOW          = 0x185
    MULTIPLEXED_2ND_FC_FRAME_8_INIT_ERROR       = 0x186
    MULTIPLEXED_1_2_FRAME_8_RATIONALITY_ERROR   = 0x187
    MULTIPLEXED_FC_FRAME_8_STATUS               = 0x188#- 0x18F
    MULTIPLEXED_1ST_FC_FRAME_9_OOR_HIGH         = 0x191
    MULTIPLEXED_1ST_FC_FRAME_9_OOR_LOW          = 0x192
    MULTIPLEXED_1ST_FC_FRAME_9_INIT_ERROR       = 0x193
    MULTIPLEXED_2ND_FC_FRAME_9_OOR_HIGH         = 0x194
    MULTIPLEXED_2ND_FC_FRAME_9_OOR_LOW          = 0x195
    MULTIPLEXED_2ND_FC_FRAME_9_INIT_ERROR       = 0x196
    MULTIPLEXED_1_2_FRAME_9_RATIONALITY_ERROR   = 0x197
    MULTIPLEXED_FC_FRAME_9_STATUS               = 0x198#- 0x19F
    MULTIPLEXED_1ST_FC_FRAME_10_OOR_HIGH        = 0x1A1
    MULTIPLEXED_1ST_FC_FRAME_10_OOR_LOW         = 0x1A2
    MULTIPLEXED_1ST_FC_FRAME_10_INIT_ERROR      = 0x1A3
    MULTIPLEXED_2ND_FC_FRAME_10_OOR_HIGH        = 0x1A4
    MULTIPLEXED_2ND_FC_FRAME_10_OOR_LOW         = 0x1A5
    MULTIPLEXED_2ND_FC_FRAME_10_INIT_ERROR      = 0x1A6
    MULTIPLEXED_1_2_FRAME_10_RATIONALITY_ERROR  = 0x1A7
    MULTIPLEXED_FC_FRAME_10_STATUS              = 0x1A8#- 0x1AF
    MULTIPLEXED_1ST_FC_FRAME_11_OOR_HIGH        = 0x1B1
    MULTIPLEXED_1ST_FC_FRAME_11_OOR_LOW         = 0x1B2
    MULTIPLEXED_1ST_FC_FRAME_11_INIT_ERROR      = 0x1B3
    MULTIPLEXED_2ND_FC_FRAME_11_OOR_HIGH        = 0x1B4
    MULTIPLEXED_2ND_FC_FRAME_11_OOR_LOW         = 0x1B5
    MULTIPLEXED_2ND_FC_FRAME_11_INIT_ERROR      = 0x1B6
    MULTIPLEXED_1_2_FRAME_11_RATIONALITY_ERROR  = 0x1B7
    MULTIPLEXED_FC_FRAME_11_STATUS              = 0x1B8#- 0x1BF
    MULTIPLEXED_1ST_FC_FRAME_12_OOR_HIGH        = 0x1C1
    MULTIPLEXED_1ST_FC_FRAME_12_OOR_LOW         = 0x1C2
    MULTIPLEXED_1ST_FC_FRAME_12_INIT_ERROR      = 0x1C3
    MULTIPLEXED_2ND_FC_FRAME_12_OOR_HIGH        = 0x1C4
    MULTIPLEXED_2ND_FC_FRAME_12_OOR_LOW         = 0x1C5
    MULTIPLEXED_2ND_FC_FRAME_12_INIT_ERROR      = 0x1C6
    MULTIPLEXED_1_2_FRAME_12_RATIONALITY_ERROR  = 0x1C7
    MULTIPLEXED_FC_FRAME_12_STATUS              = 0x1C8#- 0x1CF
    MULTIPLEXED_1ST_FC_FRAME_13_OOR_HIGH        = 0x1D1
    MULTIPLEXED_1ST_FC_FRAME_13_OOR_LOW         = 0x1D2
    MULTIPLEXED_1ST_FC_FRAME_13_INIT_ERROR      = 0x1D3
    MULTIPLEXED_2ND_FC_FRAME_13_OOR_HIGH        = 0x1D4
    MULTIPLEXED_2ND_FC_FRAME_13_OOR_LOW         = 0x1D5
    MULTIPLEXED_2ND_FC_FRAME_13_INIT_ERROR      = 0x1D6
    MULTIPLEXED_1_2_FRAME_13_RATIONALITY_ERROR  = 0x1D7
    MULTIPLEXED_FC_FRAME_13_STATUS              = 0x1D8#- 0x1DF
    MULTIPLEXED_1ST_FC_FRAME_14_OOR_HIGH        = 0x1E1
    MULTIPLEXED_1ST_FC_FRAME_14_OOR_LOW         = 0x1E2
    MULTIPLEXED_1ST_FC_FRAME_14_INIT_ERROR      = 0x1E3
    MULTIPLEXED_2ND_FC_FRAME_14_OOR_HIGH        = 0x1E4
    MULTIPLEXED_2ND_FC_FRAME_14_OOR_LOW         = 0x1E5
    MULTIPLEXED_2ND_FC_FRAME_14_INIT_ERROR      = 0x1E6
    MULTIPLEXED_1_2_FRAME_14_RATIONALITY_ERROR  = 0x1E7
    MULTIPLEXED_FC_FRAME_14_STATUS              = 0x1E8#- 0x1EF
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

    def correct(val: int):

        # Apply corrections to message IDs that are in undefined ranges, as to
        # have them be compatible with a MessageTypes8Bit enum.
        v = copy.deepcopy(val)

        # FAST_CHANNEL_STATUS correction
        if (0x008 < v <= 0x01F):
            v = 0x008
        # SENSOR_ERROR_AND_STATUS correction
        elif (0x023 < v <= 0x02F):
            v = 0x023
        # RESERVED correction
        elif (0x030 < v <= 0x100) or (0x200 <= v <= 0x400) or (0x420 <= v <= 0x7FF):
            v = 0x30
        # MULTIPLEXED_FC_FRAME_0_STATUS correction
        elif (0x108 < v <= 0x10F):
            v = 0x108
        # MULTIPLEXED_FC_FRAME_1_STATUS correction
        elif (0x118 < v <= 0x11F):
            v = 0x118
        # MULTIPLEXED_FC_FRAME_2_STATUS correction
        elif (0x128 < v <= 0x12F):
            v = 0x128
        # MULTIPLEXED_FC_FRAME_3_STATUS correction
        elif (0x138 < v <= 0x13F):
            v = 0x138
        # MULTIPLEXED_FC_FRAME_4_STATUS correction
        elif (0x148 < v <= 0x14F):
            v = 0x148
        # MULTIPLEXED_FC_FRAME_5_STATUS correction
        elif (0x158 < v <= 0x15F):
            v = 0x158
        # MULTIPLEXED_FC_FRAME_6_STATUS correction
        elif (0x168 < v <= 0x16F):
            v = 0x168
        # MULTIPLEXED_FC_FRAME_7_STATUS correction
        elif (0x178 < v <= 0x17F):
            v = 0x178
        # MULTIPLEXED_FC_FRAME_8_STATUS correction
        elif (0x188 < v <= 0x18F):
            v = 0x188
        # MULTIPLEXED_FC_FRAME_9_STATUS correction
        elif (0x198 < v <= 0x19F):
            v = 0x198
        # MULTIPLEXED_FC_FRAME_10_STATUS correction
        elif (0x1A8 < v <= 0x1AF):
            v = 0x1A8
        # MULTIPLEXED_FC_FRAME_11_STATUS correction
        elif (0x1B8 < v <= 0x1BF):
            v = 0x1B8
        # MULTIPLEXED_FC_FRAME_12_STATUS correction
        elif (0x1C8 < v <= 0x1CF):
            v = 0x1C8
        # MULTIPLEXED_FC_FRAME_13_STATUS correction
        elif (0x1D8 < v <= 0x1DF):
            v = 0x1D8
        # MULTIPLEXED_FC_FRAME_14_STATUS correction
        elif (0x1E8 < v <= 0x1EF):
            v = 0x1E8
        # MULTIPLEXED_FC_FRAME_15_STATUS correction
        elif (0x1F8 < v <= 0x1FF):
            v = 0x1F8
        # SUPPLEMENTARY_DATA_CH_ERROR_AND_STATUS correction
        elif (0x419 < v <= 0x41F):
            v = 0x419
        # OEM_DEFINED correction
        elif (0x800 < v <= 0xFFF):
            v = 0x800
        
        return v
    
    def convert(val: int):
        return ErrorCodes( ErrorCodes.correct(val) )

class ManufacturerCodes(Enum):
    NOT_SPECIFIED                   = 0x000
    BOSCH                           = 0x001
    HITACHI                         = 0x002
    CONTINENTAL                     = 0x003
    INFINEON                        = 0x004
    SENSATA                         = 0x005
    MELEXIS                         = 0x006
    MICRONAS                        = 0x007
    AUSTRIA_MICRO_SYSTEMS           = 0x008
    DENSO                           = 0x009
    # BOSCH                         = 0x010
    STONERIDGE_INC                  = 0x012
    SIEMENSVDO                      = 0x020
    I2S_INTELLIGENTE_SENSORSSYSTEME = 0x032
    AUTOLIV                         = 0x040
    # AUTOLIV                       = 0x041
    # BOSCH                         = 0x042
    # CONTINENTAL                   = 0x043
    ELMOS                           = 0x045
    FREESCALE                       = 0x046
    HELLA                           = 0x048
    # INFINEON                      = 0x049
    NXP_SEMICONDUCTORS              = 0x04E
    ONSEMI                          = 0x04F
    STMICROELECTRONICS              = 0x053
    TRW                             = 0x054
    VALEO                           = 0x056
    ZMDI                            = 0x05A
    IHR                             = 0x069
    SESKION                         = 0x073
    # CONTINENTAL                   = 0x080
    # NOT_SPECIFIED                 = 0x0FF - 0xFFF

    def correct(val: int):

        # Apply corrections to message IDs that are in undefined ranges, as to
        # have them be compatible with a MessageTypes8Bit enum.
        v = copy.deepcopy(val)

        # BOSCH correction
        if   (v == 0x010) or (v == 0x042):
            v = 0x001
        # AUTOLIV correction
        elif (v == 0x041):
            v = 0x040
        # CONTINENTAL correction
        elif (v == 0x043) or (v == 0x080):
            v = 0x003
        # INFINEON correction
        elif (v == 0x049):
            v = 0x004
        # NOT_SPECIFIED correction
        elif (0x0FF <= v <= 0xFFF):
            v = 0x000
        
        return v
    
    def convert(val: int):
        return ManufacturerCodes( ManufacturerCodes.correct(val) )

class SENTRevisionCodes(Enum):
    NOT_SPECIFIED = 0x000
    J2716_FEB2007_SENT_REV_1 = 0x000
    J2716_FEB2008_SENT_REV_2 = 0x001
    J2716_JAN2010_SENT_REV_3 = 0x002
    J2716_APR2016_SENT_REV_4 = 0x003
    RESERVED = 0x005#- 0xFFF

    def correct(val: int):

        # Apply corrections to message IDs that are in undefined ranges, as to
        # have them be compatible with a MessageTypes8Bit enum.
        v = copy.deepcopy(val)

        # RESERVED correction
        if (0x005 < v <= 0xFFF):
            v = 0x005
        
        return v
    
    def convert(val: int):
        return SENTRevisionCodes( SENTRevisionCodes.correct(val) )

# 'Global' variable to be set by calling modules.
attempt_data_parsing = True

def decode_8bit_id(message_id: int, data: int):
    '''
    Decodes an enhanced-format slow-channel message with an 8bit ID,
    returning a tuple which includes:
    - A string representation of the data.
    - An enum representing the message type.
    - (If applicable) An error code.
    '''

    mt = MessageTypes8Bit.convert(message_id)

    toRet = [mt]

    # Apply corrections to error codes that are in undefined ranges, as to
    # have them be compatible with a ErrorCodes enum.

    if   mt == MessageTypes8Bit.ERROR_AND_STATUS:
        toRet.append( ErrorCodes.convert(data) )
    elif mt == MessageTypes8Bit.MANUFACTURER_CODE:
        toRet.append( ManufacturerCodes.convert(data) )
    elif mt == MessageTypes8Bit.PROTOCOL_STD_REVISION:
        toRet.append( SENTRevisionCodes.convert(data) )

    toRet.insert(0, __message_to_string_8bit(toRet, data))

    return tuple(toRet)

def decode_4bit_id(message_id: int, data: int):
    '''
    Decodes an enhanced-format slow-channel message with a 4bit ID,
    returning a tuple which includes:
    - A string representation of the data.
    - An enum representing the message type.
    - (If applicable) A tuple of the applicable error codes.
    '''

    mt = MessageTypes4Bit.convert(message_id)

    return (__message_to_string_4bit(mt, data), mt)

def __message_to_string_4bit(mt: MessageTypes4Bit, data: int):
    
    toRet = ""

    if mt == MessageTypes4Bit.AIR_TEMPERATURE:
        toRet += "Air Temperature"
    if mt == MessageTypes4Bit.UNDEFINED:
        toRet += "Undefined Message ID"
    if mt == MessageTypes4Bit.HUMIDITY:
        toRet += "Humidity"
    if mt == MessageTypes4Bit.BAROMETRIC_PRESSURE:
        toRet += "Barometric Pressure"

    toRet += '{0:016b} : 0x{0:04X} : {0}'.format(data)

    return toRet

def __message_to_string_8bit(message: list, data: int):

    toRet = ""

    mt = message[0]

    if   mt == MessageTypes8Bit.ERROR_AND_STATUS:
        toRet += f"Error: {message[1].name}"
    elif mt == MessageTypes8Bit.MANUFACTURER_CODE:
        toRet += f"Manufacturer Code: {message[1].name}"
    elif mt == MessageTypes8Bit.PROTOCOL_STD_REVISION:
        toRet += f"SENT Protocol: {message[1].name}"
    else:
        toRet += f"{mt.name}: {'{0:012b} : 0x{0:03X} : {0}'.format(data)}"

    return toRet
    