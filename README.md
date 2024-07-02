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

## LAN Network ##

[Guide 1](https://www.digitalocean.com/community/tutorials/how-to-enable-remote-desktop-protocol-using-xrdp-on-ubuntu-22-04)
[Guide 2](https://phoenixnap.com/kb/ubuntu-remote-desktop-from-windows)

To remote into each jetson nano from a laptop, it is recommended to use xrdp and Windows Remote Desktop. Make sure to use a grapical desktop interface like xfce4 (included in first guide).
An optional additional step is to disable the "thinclient_drives" mounted drive. This is done by including `EnableFuseMount=false` in the `/etc/xrdp/sesman.ini` file.

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

Camera 3 (White):
    mtx= np.matrix([[1.11467677e+03, 0.00000000e+00, 3.25094199e+02],
            [0.00000000e+00, 1.11898652e+03, 2.57595640e+02],
            [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
    dist = np.array([ 2.33737757e-03, -1.88523229e+00,  1.27303159e-03, -2.99893824e-03, 4.57368528e+00])

