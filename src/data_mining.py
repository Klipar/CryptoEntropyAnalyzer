from collections import defaultdict
from Easy.animations import *
from Easy.massage import *
import struct
import sys
import os

def Read_bytes_bucket (file, bytes_per_value, value_count, format_char):
    try: # the function misses all checks to increase the reading speed
        bytes_data = file.read(bytes_per_value)
        if bytes_data:
            value = struct.unpack(format_char, bytes_data)[0]
            value_count[value] += 1
            return bytes_data, value
        return bytes_data, 0
    except Exception as e:
        failed (f"Error while reading file: \n{e}")

def get_format_char(num_bytes: int) -> str:
    """Determine the format character based on the number of bytes."""
    format_mapping = {
        1: 'B',  # 8-bit unsigned integer
        2: 'H',  # 16-bit unsigned integer
        4: 'I',  # 32-bit unsigned integer
        8: 'Q'   # 64-bit unsigned integer
    }
    
    if num_bytes in format_mapping:
        return format_mapping[num_bytes]
    else:
        raise ValueError(f"Unsupported number of bytes: {num_bytes}. Only 1, 2, 4, or 8 bytes are supported.")

def read_bytes_from_file(filename: str, format_char: str, num_bytes: int) -> dict:
    """_summary_

    Args:
        filename (str): name of the file to be scanned
        format_char (str): format char (use func get_format_char() to it)
        num_bytes (int): Number of bytes to be scanned must be in (1, 2, 4, 8)

    Raises:
        ValueError: The number of bytes must be at least 1!
        ValueError: Only 1, 2, 4, or 8 bytes are supported.

    Returns:
        dict: _description_
    """
    bytes_per_value = struct.calcsize(format_char)
    value_count = defaultdict(int) # a dictionary for counting meetings
    try:
        with open(filename, 'rb') as file:
            inform ("Show bar (it make proces slower)? (Yes/No): ", end = "")
            show_bat = input().lower()
            if (show_bat == "yes" or show_bat == 'y'):
                val = (int(os.path.getsize(filename))/num_bytes)
                bar = LineProgresBar (MaxLength = 50, text = "Scaning", maxWalue = val, isShowPersent = True,  isShowWalue = True)

                while True: # I used 2 cycles to speed up the processing of large files
                    bytes_data, value = Read_bytes_bucket (file, bytes_per_value, value_count, format_char)
                    bar.ShoveAndUpdate (isreturn = False)
                    print(f'  [{value:0{bytes_per_value * 8}b}]', end="\r") 
                    
                    if len(bytes_data) < bytes_per_value:
                        print()
                        break
            else:
                while True:
                    bytes_data, value = Read_bytes_bucket (file, bytes_per_value, value_count, format_char)

                    if len(bytes_data) < bytes_per_value:
                        break
            return value_count
    except:
        failed (f"could not open the file: {filename}")
        sys.exit (1)