import os
import subprocess

subprocess.Popen(["killall", "-9", "gpsd", "ntpd"])
subprocess.Popen(["gpsd", "-n", "/dev/ttyUSB"])
subprocess.Popen(["sleep", "2"])
subprocess.Popen(["ntpd", "-gN"])
subprocess.Popen(["sleep", "2"])
subprocess.Popen(["cgps"])


