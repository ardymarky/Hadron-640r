# Hadron-640r
Object detection and 3d tracking using thermal cameras and python3

For recording calibration photos:

  1.  Run "python3 calibration.py".
  2.  Press spacebar to save image.
  3.  Take about 30-40 photos at different angles and locations

For lens undistortion:

  1. Add images to Image Folder
  2. Run "python3 camera_calib.py" and wait
  3. Record outputted matrix and dist arrays
  4. Plug into "master_script.py"


Update GPSD:

	sudo apt update
	sudo apt install -y scons libncurses-dev python-dev pps-tools git-core asciidoctor python3-matplotlib build-essential manpages-dev pkg-config python3-distutils
	wget http://download.savannah.gnu.org/releases/gpsd/gpsd-3.23.1.tar.gz
	tar -xzf gpsd-3.23.1.tar.gz
	cd gpsd-3.23.1
	sudo scons
	sudo scons install
	gpsd -V
