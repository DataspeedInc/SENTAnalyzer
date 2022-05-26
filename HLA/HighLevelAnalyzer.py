# High Level Analyzer
# For more information and documentation, please go to https://support.saleae.com/extensions/high-level-analyzer-extensions

from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting

import math

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
        'status': {
            'format': 'Status: {{data.status}}'
        }
    }

    def __init__(self):
        '''
        Initialize HLA.

        Settings can be accessed using the same name used above.
        '''

    def decode(self, frame: AnalyzerFrame):
        '''
        Process a frame from the input analyzer, and optionally return a single `AnalyzerFrame` or a list of `AnalyzerFrame`s.

        The type and data values in `frame` will depend on the input analyzer.
        '''

        def end_sc():
            fb = self.frame_buffer
            sb = self.sc_buffer

            toRet = None

            # If reading a short format.
            if self.slow_channel_format == "Short":
                toRet = AnalyzerFrame('status', fb[0].start_time, fb[len(fb)-1].end_time, {
                    'status': 'endd'
                    })
            # If reading an enhanced format.
            else:
                # Extract the last 18 elements from the slow-channel buffer.
                slow_frame = sb[-18:]

                print(f"Extracted enhanced frame: {slow_frame}")

            sb.clear()
            
            return toRet

        def end_frame():
            # If the previous frame doesn't contain a passed crc check, return.
            if not list(filter(lambda x: (x.type == 'crc'), self.frame_buffer)):
                self.frame_buffer.clear()
                return
            
            toRet = None

            fb = self.frame_buffer
            sb = self.sc_buffer

            ### Extract the frame's data and status information. ###

            data = list(filter(lambda x: (x.type == 'fc_data'), fb))

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
                    sc_output_frame = end_sc()
            # If we're attempting to parse an enhanced message format for the slow channel.
            else:
                checks = ( len(sb) - 18 ) + 1

                if checks > 0:                
                    status_bits = 0
                    
                    # Convert our status buffer's current bit 3s into an integer for bitwise comparisons.
                    for i in sb:
                        status_bits <<= 1
                        status_bits |= ( (i >> 3) & 0x1 )

                    # Get the amount of bits needed to represent status_bits
                    status_bits_len = math.floor(math.log2(status_bits)) + 1

                    # Iterate through our status bits and check if there's a pattern indicating
                    # a finished enhanced frame.
                    pattern = 0b111111100000100001
                    match =   0b111111000000000000

                    if (status_bits & pattern) == match:
                        sc_output_frame = end_sc()

            ### Specify which AnalyzerFrame to return ###

            if self.display == "Fast Channel Data":
                if len(data) > 0:
                    toRet = AnalyzerFrame('fc_data', data[0].start_time, data[len(data)-1].end_time, {
                        'fc_data': 'deeta'
                        })
            else:
                toRet = sc_output_frame

            ### Append / Clear buffers ###

            self.sc_buffer.append(status)

            self.frame_buffer.clear()

            return toRet

        toRet = None

        if frame.type == "mtp":
            self.using_spc = True
            # Commit frame buffer since we're this signal's "first pulse".
            toRet = end_frame()
        elif frame.type == "sync":
            # Commit frame buffer if we're this signal's "first pulse".
            if not self.using_spc:
                toRet = end_frame()
            
        self.frame_buffer.append(frame)

        return toRet
