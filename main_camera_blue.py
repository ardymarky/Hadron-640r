#!/usr/bin/env python
# Hadron 640-R Master Script
# Arden Markin UA RSC
# 11/15/2023

# Import Libraries
import numpy as np
import cv2
import csv
import datetime
import time

# Init Default Variables
record = False
frame_rate = 8
minTemp = 44 # All values in Farenheit
maxTemp = 134
maskMinTemp = 100 
centerXPixel = 320
centerYPixel = 256
degreePerPixel = 0.05

# Convert Farenheit to Rankine
convertedMinTemp = (minTemp + 459.67) * 100 / 9 * 5
convertedMaxTemp = (maxTemp + 459.67) * 100 / 9 * 5
convertedMaskTemp = (255)/(maxTemp-minTemp) * (maskMinTemp-minTemp) 

# CSV formatting
header = ['time', 'loop time', 'object no.', 'azimuth', 'bearing']
f = open('hadron_data.csv', 'a', encoding='UTF8')
writer = csv.writer(f)
writer.writerow(header)

# Video Output
raw = cv2.VideoWriter('raw.avi', cv2.VideoWriter_fourcc(*'MJPG'), frame_rate, (640, 512))
final = cv2.VideoWriter('final.avi', cv2.VideoWriter_fourcc(*'MJPG'), frame_rate, (640, 512))

# Normalize Frame to gray8 0-255 range
def thermal_calibration(frame):
    global convertedMinTemp
    global convertedMaxTemp
    # awkward adjustments for better normalization
    frame[frame < convertedMinTemp] = convertedMinTemp
    frame[frame > convertedMaxTemp] = convertedMaxTemp
    frame[0][0] = convertedMinTemp
    frame[1][0] = convertedMaxTemp
    frame = cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    # Undistortion process (different values for each camera)
    h,w = frame.shape[:2]
    mtx= np.matrix([[1.19975668e+03, 0.00000000e+00, 2.90733126e+02],
            [0.00000000e+00, 1.20094533e+03, 2.45528429e+02],
            [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
    dist = np.array([[ 1.19948432e-01, -4.15188268e+00, -1.51634226e-03, -3.83780623e-03,      		2.28387360e+01]])
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    frame = cv2.undistort(frame, mtx, dist, None, newcameramtx)
    return frame

# Set capture parameters
cap = cv2.VideoCapture("/dev/video1")
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y','1','6',' '))
cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)
cap.set(cv2.CAP_PROP_FPS, frame_rate)

# Static Mask
grabbed, static_mask = cap.read()
static_mask = thermal_calibration(static_mask)
cv2.imshow('thermal tracker', static_mask)

# Find Current Frame Count and Time
frame_count = int((time.time() % 1) / (1./frame_rate))
prev_time = time.time()

while True: # record indefinitely (until user presses q)

    frame_count = (frame_count + 1) % frame_rate
    start_time=time.time() # Posix time

    # Get frame from camera
    (grabbed, thermal_frame) = cap.read()
    key = cv2.waitKey(1)

    # Normalize frame
    thermal_frame = thermal_calibration(thermal_frame)
    # Recalibrate static mask with 'c'
    if key == ord('c'):
        static_mask = thermal_frame;
        print("Got New Static Mask")



    # Refine Static and Thermal Mask
    new_static_mask = thermal_frame- static_mask + 5
    new_static_mask = 255 - cv2.inRange(new_static_mask, 0, 10)
    thermal_frame = np.uint8(thermal_frame)
    temp_mask = cv2.inRange(thermal_frame, convertedMaskTemp, 255)

    # Blob Detection
    params = cv2.SimpleBlobDetector_Params()
    params.minThreshold = 110
    params.maxThreshold = 150
    params.filterByArea = True
    params.filterByConvexity = False;
    params.filterByColor = False;
    params.filterByInertia = False;
    params.minArea = 10
    params.maxArea = 10000
    detector = cv2.SimpleBlobDetector_create(params)

    # Combine Masks and detect objects
    mask3 = (temp_mask * new_static_mask) * 255
    keypoints = detector.detect(mask3)
    endTime = time.time()

    # Graphical stuff
    thermal_frame = cv2.applyColorMap(thermal_frame, cv2.COLORMAP_JET)
    cv2.putText(thermal_frame, "Time: {0:.3f}".format(time.time()), (20,30), cv2.FONT_HERSHEY_PLAIN, 1.5, (255,255,255), 2)
    if record:
       raw.write(thermal_frame)
    cv2.putText(thermal_frame, "Obstacles detected over {0:.1f} F : {1:}".format(maskMinTemp, len(keypoints)), (20,60), cv2.FONT_HERSHEY_PLAIN, 1.5, (255,255,255), 2)
    thermal_frame = cv2.drawKeypoints(thermal_frame, keypoints, 0, (0,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    if record:
        final.write(thermal_frame)
        curr_time = time.time()
        row = [curr_time, endTime - start_time]
        # If objects detected and 'r' was pressed
        if len(keypoints) > 0:
            # Get current time
            # If 1 second has elapsed since last output
            for x in range(len(keypoints)):
                # Get bearing and azimuth angles
                width, height = keypoints[x].pt
                angleX = (width - centerXPixel)*degreePerPixel
                angleY = -(height - centerYPixel)*degreePerPixel
                # Write data to CSV
                row.extend([x+1, angleX, angleY])
        writer.writerow(row)

    # FPS Limiter
    temp_time = time.time()
    if frame_count == frame_rate - 1:
        time.sleep(int(time.time()+1) - time.time())
    elif temp_time - prev_time  < 1./frame_rate:
        time.sleep(1./frame_rate - temp_time + prev_time)
    # Log current time
    prev_time = time.time()

    # Display frame in window
    cv2.imshow("thermal tracker", thermal_frame)

    # Close program with 'q'
    if key == ord('q'):
        print("Closing...")
        break;

    # Begin or stop recording with 'r'
    if key == ord('r'):
        record = not record
        if record: 
            print("Recording...")
        else: print("Stopped Recording")
    
# Close all files and windows
cv2.destroyAllWindows()
f.close()
raw.release()
final.release()
