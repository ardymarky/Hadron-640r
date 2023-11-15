#!/usr/bin/env python3.8
# Sync system time to current GPS time
# Arden Markin, Tuan Luong UA RSC
# 11/15/2023

# Import Libraries
from serial import Serial
from pyubx2 import UBXReader
import datetime
import time
import os

# Default port and baud
ins_port = '/dev/ttyUSB0'
ins_baud = 115200

# Init some flags
time_init = False
fix_stat = False

# Calculate UNIX time given GPS time
def calc_posix_time (gps_tow, gps_week, gps_leapS):
    return gps_tow/1000 + int(gps_week) * 604800 + 315964800 - gps_leapS

# Open serial port to Hadron 640-r  
stream = Serial(ins_port, ins_baud, timeout=3)
# Clear buffer
stream.reset_input_buffer()

# Get GPS data
ubr = UBXReader(stream)
(raw_data, parsed_data) = ubr.read()

# Run until GPStime is initialized
while not time_init:
    time.sleep (0.001) # Limit how fast the loop runs

    # Only sync if data is GPS Time
    if parsed_data.identity == "NAV-TIMEGPS":
        print("connected!")
        # Convert GPS time to UNIX time
        cur_posix_time = calc_posix_time(parsed_data.iTOW, parsed_data.week, parsed_data.leapS)
        # Set System Time 
        time.clock_settime(time.CLOCK_REALTIME, cur_posix_time)
        print ("Time synced to " + datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S UTC"))
        time_init = True

print("Success!")
                    

    
    

