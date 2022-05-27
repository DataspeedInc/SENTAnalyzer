import math

CRC_4 = [
    0, 13, 7, 10, 14, 3, 9, 4, 1, 12, 6, 11, 15, 2, 8, 5
]

CRC_6 = [
    0, 25, 50, 43, 61, 36, 15, 22, 35, 58, 17, 8, 30, 7, 44, 53,
    31, 6, 45, 52, 34, 59, 16, 9, 60, 37, 14, 23, 1, 24, 51, 42,
    62, 39, 12, 21, 3, 26, 49, 40, 29, 4, 47, 54, 32, 57, 18, 11,
    33, 56, 19, 10, 28, 5, 46, 55, 2, 27, 48, 41, 63, 38, 13, 20
]

def gen_crc_4():

    pass

def gen_crc_6(input: int, n: int):
    checksum_64 = 21

    for i in range(n):
        nibble = __extract_nibble(input, 6, (n-1) - i)
        checksum_64 = nibble ^ CRC_6[checksum_64]

    checksum_64 = 0 ^ CRC_6[checksum_64]

    return checksum_64

def __extract_nibble(input: int, len: int, n: int):
    '''
    Extracts the nth nibble of length len from the input.
    (In LSB order-- n of 0 is the least significant nibble)
    '''

    return ( input >> (n * len) ) & (2 ** len) - 1