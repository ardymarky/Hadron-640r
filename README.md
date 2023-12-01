# Hadron-640r

Object detection and 3d tracking using thermal cameras and OpenCV

Proces 1 (Timesync):

  1. Plug in GPS to Avermedia board
  2. Wait 30 seconds
  3. Run "sudo python3.8 timesync.py"

Process 2 (Recording Data):

  1. Run "sudo main_camera_*.py"

  Commands:
     "R" - record/stop
     "C" - reset static mask
     "Q" - quit


----------------------------------------------------------------------
For recording calibration photos:

  1.  Run "python3 calibration.py".
  2.  Press spacebar to save image.
  3.  Cool thermal checkerboard in fridge
  3.  Take about 30-40 photos of checkerboard attached to a posterboard at different locations

To correct for lens distortion:

  1. Add captured images to Image Folder
  2. Inside image folder, run "python3 ../camera_calib.py" and wait
  3. Record outputted matrix and dist arrays
  4. Plug matrixs into "main_camera_*.py"

----------------------------------------------------------------------

Beam distance is 62 inches
Bracket piece is 55mm 
Distance between two cameras is 1.5198 meters or 1519.8 millimeters
The lens is 76mm along the beam and 16mmn forward of the gnss receiver

Camera 1 (Red power cable):
    mtx = np.matrix([[1.15337497e+03, 0, 3.18136149e+02], 
           [0.00000000e+00, 1.15271799e+03, 2.59848723e+02], 
           [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
    dist = np.array([6.28685479e-02, -3.68503422e+00, -1.55064164e-03, -1.41925924e-03, 	             1.84969914e+01])

Camera 2 (Blue power cable):
    mtx= np.matrix([[1.19975668e+03, 0.00000000e+00, 2.90733126e+02],
            [0.00000000e+00, 1.20094533e+03, 2.45528429e+02],
            [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
    dist = np.array([[ 1.19948432e-01, -4.15188268e+00, -1.51634226e-03, -3.83780623e-03,      2.28387360e+01]])


