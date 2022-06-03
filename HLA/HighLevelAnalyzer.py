from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting

import crc
import decode.short_format as decode_short
import decode.enhanced_format as decode_enhanced
import decode.fc_data as decode_fc

import math
import copy

# High level analyzers must subclass the HighLevelAnalyzer class.
class Hla(HighLevelAnalyzer):
    ### Settings ###
    attempt_fc_parsing = ChoicesSetting(choices=('Yes', 'No'))
    display = ChoicesSetting(choices=('Fast Channel Data', 'Slow Channel Data'))
    slow_channel_format = ChoicesSetting(choices=('Short', 'Enhanced'))

    ### Instance Variables ###
    frame_buffer = []
    sc_buffer = []
    using_spc = False
    #enhanced_sc = False

    # An optional list of types this analyzer produces, providing a way to customize the way frames are displayed in Logic 2.
    result_types = {
        'fc_data': {
            'format': 'FC Data: {{data.fc_data}}'
        },
        'short_frame': {
            'format': 'SF - {{data.slow_frame}}'
        },
        'enhanced_frame': {
            'format': 'EF - {{data.slow_frame}}'
        },
        'error': {
            'format': 'SC Frame Error: {{data.error}}'
        }
    }

    def __init__(self):
        '''
        Initialize HLA.

        Settings can be accessed using the same name used above.
        '''

    def __ints_bit_serialize(self, ints_list: list, n: int):
        '''
        Convert a list of integers (or numerical types) into a single integer by 
        taking the nth bit of every int in the list and recombining them into a single int type.
        
        (Note: n begins at 0, so a n of 0 would be the least significant bit.)
        '''
        
        toRet = 0

        for i in ints_list:
            toRet <<= 1
            toRet |= ( (i >> n) & 0x1 )

        return toRet

    def decode(self, frame: AnalyzerFrame):
        '''
        Process a frame from the input analyzer, and optionally return a single `AnalyzerFrame` or a list of `AnalyzerFrame`s.

        The type and data values in `frame` will depend on the input analyzer.
        '''

        toRet = None

        if frame.type == "mtp":
            self.using_spc = True
            # Commit frame buffer since we're this signal's "first pulse".
            toRet = self.end_frame()
        elif frame.type == "sync":
            # Commit frame buffer if we're this signal's "first pulse".
            if not self.using_spc:
                toRet = self.end_frame()
            
        self.frame_buffer.append(frame)

        return toRet

    def end_sc(self):
        fb  = self.frame_buffer
        fsb = self.sc_buffer
        sb  = []

        # Make sb only contain the sc_buffer's extracted status integer.
        for frame in fsb:
            sb.append(frame[0])

        toRet = None

        # If reading a short format.
        if self.slow_channel_format == "Short":

            # Extract the last 16 elements from the slow-channel buffer.
            slow_frame = sb[-16:]

            bit2s = self.__ints_bit_serialize(slow_frame, 2)

            crc_data   = (bit2s >> 4)  & 0xFFF
            computed_crc = crc.gen_crc_4(crc_data, 3)

            message_id = (bit2s >> 12) & 0xF
            data_byte  = (bit2s >> 4)  & 0xFF
            read_crc   = (bit2s)       & 0xF

            print(f"frame: {slow_frame}\n- - - -")

            print(
                f"Extracted frame info:\n"
                f"message_id:\t{'{0:04b}'.format(message_id)}\n"
                f"data_byte:\t{'{0:08b}'.format(data_byte)}\n"
                f"crc:\t\t{'{0:04b}'.format(read_crc)}\n"
                f"computed crc:\t{'{0:04b}'.format(computed_crc)}\n"
                f"raw bit2s:\t{'{0:016b}'.format(bit2s)}\n"
                f"----------------------------"
                )

            if read_crc != computed_crc:
                print(f"pre-short error- fsb: {fsb}")
                toRet = AnalyzerFrame('error', fsb[-1][1][0].start_time, fsb[-1][1][-1].end_time, {
                    'error': 'CRC Mismatch'
                    })
            else:
                decoded = decode_short.decode(message_id, data_byte)

                toRet = AnalyzerFrame('short_frame', fsb[-1][1][0].start_time, fsb[-1][1][-1].end_time, {
                    'slow_frame': str(decoded)
                    })

        # If reading an enhanced format.
        else:
            # Extract the last 18 elements from the slow-channel buffer.
            slow_frame = sb[-18:]

            ### Extract individual frame elements ###
            bit3s = self.__ints_bit_serialize(slow_frame, 3)
            bit2s = self.__ints_bit_serialize(slow_frame, 2)

            # Convert data bits into a 24-bit integer for the CRC check.
            combined_message = 0
            
            for i in range(12):
                combined_message <<= 1
                combined_message |= ( (bit2s >> 11 - i) & 0x1 )
                combined_message <<= 1
                combined_message |= ( (bit3s >> 11 - i) & 0x1 )

            computed_crc = crc.gen_crc_6(combined_message, 4)

            c           = (bit3s >> 10) & 0x1
            b3_nibble_1 = (bit3s >> 6)  & 0xF
            b3_nibble_2 = (bit3s >> 1)  & 0xF
            read_crc    = (bit2s >> 12) & 0x3F
            b2_data     = (bit2s)       & 0xFFF 

            print(
                f"Extracted frame info:\n"
                f"C bit:\t\t{c}\n"
                f"b3_nibble_1:\t{'{0:04b}'.format(b3_nibble_1)}\n"
                f"b3_nibble_2:\t{'{0:04b}'.format(b3_nibble_2)}\n"
                f"crc:\t\t{'{0:06b}'.format(read_crc)}\n"
                f"computed crc:\t{'{0:06b}'.format(computed_crc)}\n"
                f"b2_data:\t{'{0:012b}'.format(b2_data)}\n"
                f"raw bit3s:\t{'{0:018b}'.format(bit3s)}\n"
                f"raw bit2s:\t{'{0:018b}'.format(bit2s)}\n"
                f"combined data:\t{'{0:024b}'.format(combined_message)}\n"
                f"----------------------------"
                )

            if read_crc != computed_crc:
                toRet = AnalyzerFrame('error', fsb[-1][1][0].start_time, fsb[-1][1][-1].end_time, {
                    'error': 'CRC Mismatch'
                    })
            else:
                data = None
                decoded = None

                if c == 0:
                    message_id = (b3_nibble_1 << 4) | (b3_nibble_2)
                    data = b2_data
                    decoded = decode_enhanced.decode_8bit_id(message_id, data)
                else:
                    message_id = b3_nibble_1
                    data = (b3_nibble_2 << 12) | (b2_data)
                    decoded = decode_enhanced.decode_4bit_id(message_id, data)

                toRet = AnalyzerFrame('enhanced_frame', fsb[-1][1][0].start_time, fsb[-1][1][-1].end_time, {
                    'slow_frame': f'{decoded[0]}'
                    })

        self.sc_buffer.clear()

        return toRet

    def end_frame(self):
        # If the previous frame doesn't contain a passed crc check, return.
        if not list(filter(lambda x: (x.type == 'crc'), self.frame_buffer)):
            self.frame_buffer.clear()
            return
        
        toRet = None

        fb  = self.frame_buffer
        fsb = self.sc_buffer
        sb  = []

        # Make sb only contain the sc_buffer's extracted status integer.
        for frame in fsb:
            sb.append(frame[0])

        ### Extract the frame's data and status information. ###

        data_frames = list(filter(lambda x: (x.type == 'fc_data'), fb))
        
        data = []

        for f in data_frames:
            data.append(int.from_bytes(f.data['data'], 'little'))

        print(f"fc data: {data}")

        status = None

        # Catch an IndexError in the case that this frame is missing a status pulse.
        try:
            status = list(filter(lambda x: (x.type == 'status'), fb))[0]
            status = int.from_bytes(status.data['data'], 'little')
        except IndexError as e:
            return

        ### Store and parse the short channel information ###

        sc_output_frame = None

        # If we're attempting to parse a short message format for the slow channel.
        if self.slow_channel_format == 'Short':
            # If the beginning of a short channel frame is detected.
            if (status >> 3) & 0x1:
                if len(fsb) >= 16:
                    sc_output_frame = self.end_sc()
                else:
                    self.sc_buffer.clear()
        # If we're attempting to parse an enhanced message format for the slow channel.
        else:
            checks = ( len(sb) - 18 ) + 1

            if checks > 0:                
                status_bits = self.__ints_bit_serialize(sb, 3)

                # Iterate through our status bits and check if there's a pattern indicating
                # a finished enhanced frame.
                pattern = 0b111111100000100001
                match   = 0b111111000000000000

                if (status_bits & pattern) == match:
                    if len(fsb) >= 18:
                        sc_output_frame = self.end_sc()
                    else:
                        self.sc_buffer.clear()

        ### Specify which AnalyzerFrame to return ###

        if self.display == "Fast Channel Data":
            if len(data) > 0:
                ch1_data = (data[0] << 8) | (data[1] << 4) | (data[2])

                x1 = 5e3
                x2 = -120e3
                y1 = 193
                y2 = 3896

                phys = x1 + ( (x2 - x1) / (y2 - y1) ) * ( ch1_data - y1 )

                decoded = decode_fc.decode( 0x003, tuple(data), ((x1, x2),) )

                toRet = AnalyzerFrame('fc_data', fb[0].start_time, fb[-1].end_time, {
                    'fc_data': str(decoded)
                    })
        else:
            toRet = sc_output_frame

        ### Append / Clear buffers ###

        self.sc_buffer.append( (status, copy.copy(fb)) )

        self.frame_buffer.clear()

        return toRet