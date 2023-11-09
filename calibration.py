import numpy as np
import cv2
img_counter = 0
x_mouse = 0
y_mouse = 0

def mouse_events(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
    
        global x_mouse
        global y_mouse

    x_mouse = x
    y_mouse = y

cap = cv2.VideoCapture("/dev/video1")
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y','1','6',' '))
cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)
grabbed, frame_thermal = cap.read()
cv2.imshow('thermal tracker', frame_thermal)
cv2.setMouseCallback('thermal tracker', mouse_events)

while True:#record indefinitely (until user presses q), replace with "while True"

    (grabbed, thermal_frame) = cap.read()

#Normalize to gray8 0-255 range)
    thermal_frame = cv2.flip(thermal_frame, 0)
    thermal_frame = cv2.flip(thermal_frame, 1)

    minTemp = 50
    maxTemp = 110
    #Floor temp is roughy 68.5
    minTemp = 50
    maxTemp = 90

    convertedMinTemp = (minTemp + 459.67) * 100 / 9 * 5
    convertedMaxTemp = (maxTemp + 459.67) * 100 / 9 * 5
    temperature_pointer = thermal_frame[y_mouse, x_mouse]
    temperature_pointer = temperature_pointer / 100 * 9  / 5 - 459.67
    thermal_frame[thermal_frame < convertedMinTemp] = convertedMinTemp
    thermal_frame[thermal_frame > convertedMaxTemp] = convertedMaxTemp
    thermal_frame[0][0] = convertedMinTemp
    thermal_frame[1][0] = convertedMaxTemp
    thermal_frame = cv2.normalize(thermal_frame, thermal_frame, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    #thermal_frame = np.uint8(thermal_frame)

#Graphics stuff
    #thermal_frame = cv2.applyColorMap(thermal_frame, cv2.COLORMAP_JET)   
    cv2.putText(thermal_frame, "Temperature: {0:.1f} F".format(temperature_pointer), (30,30), cv2.FONT_HERSHEY_PLAIN, 1.5, (255,255,255), 2)


    cv2.imshow("thermal tracker", thermal_frame)

    k = cv2.waitKey(1)
    if k == ord('q'):
     	break;
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, thermal_frame)
        print("{} written!".format(img_name))
        img_counter += 1
        
cv2.destroyAllWindows()
print(convertedMinTemp)
print(convertedMaxTemp)
