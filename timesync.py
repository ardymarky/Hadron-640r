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
import csv

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
    # Only sync if data is GPS Time
    if parsed_data.identity == "NAV-TIMEGPS":
        print("connected!")
        # Convert GPS time to UNIX time
        cur_posix_time = calc_posix_time(parsed_data.iTOW, parsed_data.week, parsed_data.leapS)
        # Set System Time 
        time.clock_settime(time.CLOCK_REALTIME, cur_posix_time)
        print ("Time synced to " + datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S UTC"))
        time_init = True

    time.sleep (0.001) # Limit how fast the loop runs
    (raw_data, parsed_data) = ubr.read()


stream.reset_input_buffer()
ubr = UBXReader(stream)
(raw_data, parsed_data) = ubr.read()

while not fix_stat:
    if parsed_data.identity == "NAV-PVT":
        print("found location!")
       
        cur_position = [parsed_data.lon, parsed_data.lat, parsed_data.height, parsed_data.hMSL]
        f = open('hadron_data.csv', 'w', encoding='UTF8')
        writer = csv.writer(f)
        writer.writerow(["Longitude", "Latitude", "Height", "MSL"])
        writer.writerow(cur_position)
        writer.writerow([])
        fix_stat = True
        print(cur_position)
        if parsed_data.lon == 0:
            print("gps not fixed, wait and run again")
    (raw_data, parsed_data) = ubr.read()

print("Success!")
f.close()
    
    

