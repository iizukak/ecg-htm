import serial
import time
from datetime import datetime

# setting for device
SERIAL_NAME = "/dev/tty.usbserial-AL00EPTY"
PORT = "9600"

ser = serial.Serial(SERIAL_NAME, PORT, timeout=10)
while True:
    print datetime.now(), ",", ser.readline(),
