import os
import subprocess

subprocess.run(["killall", "-9", "gpsd", "ntpd"])
subprocess.run(["gpsd", "-n", "/dev/ttyUSB0"])
subprocess.run(["sleep", "2"])
subprocess.run(["ntpd", "-gN"])
subprocess.run(["sleep", "2"])
subprocess.run(["cgps"])


