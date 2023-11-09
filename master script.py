import numpy as np
import cv2

x_mouse = 0
y_mouse = 0

minTemp = 44
maxTemp = 134
maskMinTemp =100 #Farenheit
centerXPixel = 320
centerYPixel = 256
degreePerPixel = 0.05

convertedMinTemp = (minTemp + 459.67) * 100 / 9 * 5
convertedMaxTemp = (maxTemp + 459.67) * 100 / 9 * 5
convertedMaskTemp = (255)/(maxTemp-minTemp) * (maskMinTemp-minTemp) 

def mouse_events(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
    
        global x_mouse
        global y_mouse

    x_mouse = x
    y_mouse = y

#Normalize to gray8 0-255 range
def thermal_calibration(frame):
    global convertedMinTemp
    global convertedMaxTemp
    frame[frame < convertedMinTemp] = convertedMinTemp
    frame[frame > convertedMaxTemp] = convertedMaxTemp
    frame[0][0] = convertedMinTemp
    frame[1][0] = convertedMaxTemp
    frame = cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    h,w = frame.shape[:2]
    mtx = np.matrix([[1.15337497e+03, 0, 3.18136149e+02], 
           [0.00000000e+00, 1.15271799e+03, 2.59848723e+02], 
           [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
    dist = np.array([6.28685479e-02, -3.68503422e+00, -1.55064164e-03, -1.41925924e-03, 	             1.84969914e+01])

    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    frame = cv2.undistort(frame, mtx, dist, None, newcameramtx)
    return frame

cap = cv2.VideoCapture("/dev/video1")
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y','1','6',' '))
cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)

#Static Mask
grabbed, static_mask = cap.read()
static_mask = cv2.flip(static_mask, 0)
static_mask = cv2.flip(static_mask, 1)
static_mask = thermal_calibration(static_mask)
cv2.imshow('thermal tracker', static_mask)
cv2.setMouseCallback('thermal tracker', mouse_events)

while True: #record indefinitely (until user presses q)

    (grabbed, thermal_frame) = cap.read()
    key = cv2.waitKey(1)
    thermal_frame = cv2.flip(thermal_frame, 0)
    thermal_frame = cv2.flip(thermal_frame, 1)

#Mask 1 and Frame Conversions
    temperature_pointer = thermal_frame[y_mouse, x_mouse]
    temperature_pointer = temperature_pointer / 100 * 9  / 5 - 459.67
    thermal_frame = thermal_calibration(thermal_frame)
    if key == ord('c'):
        static_mask = thermal_frame;

    mask1 = thermal_frame- static_mask + 5
    mask1 = 255 - cv2.inRange(mask1, 0, 10)
    thermal_frame = np.uint8(thermal_frame)

# Blob Detection
    temp_mask = cv2.inRange(thermal_frame, convertedMaskTemp, 255)
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
    mask3 = (temp_mask * mask1) * 255
    keypoints = detector.detect(mask3)

#Graphics stuff
    thermal_frame = cv2.applyColorMap(thermal_frame, cv2.COLORMAP_JET)    
    thermal_frame = cv2.drawKeypoints(thermal_frame, keypoints, 0, (150,150,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.putText(thermal_frame, "Temperature: {0:.1f} F".format(temperature_pointer), (30,30), cv2.FONT_HERSHEY_PLAIN, 1.5, (255,255,255), 2)
    cv2.putText(thermal_frame, "Obstacles detected over {0:.1f} F : {1:}".format(maskMinTemp, len(keypoints)), (30,60), cv2.FONT_HERSHEY_PLAIN, 1.5, (255,255,255), 2)
    cv2.circle(thermal_frame, (centerXPixel, centerYPixel), 5, (255,0,0))



    if len(keypoints) > 0:
        for x in range(len(keypoints)):
            width, height = keypoints[x].pt
            angleX = (width - centerXPixel)*degreePerPixel
            angleY = (height - centerYPixel)*degreePerPixel
            print("Obstacle {} is at angle {}".format(x,(angleX,angleY)))


    cv2.imshow("thermal tracker", thermal_frame)
    if key == ord('q'):
        break;

cv2.destroyAllWindows()
