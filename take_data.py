import    serial

# setting for device
SERIAL_NAME = "/dev/tty.usbserial-AL00EPTY"
PORT = "9600"

ser = serial.Serial(SERIAL_NAME, PORT, timeout=10)
while True:
    print ser.readline(),
