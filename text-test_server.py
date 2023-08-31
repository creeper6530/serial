import serial
from time import sleep
import platform

if platform.system() == "Windows":
    port = "COM5"
elif platform.system() == "Linux":
    port = "/dev/serial0"

BAUDRATES = (50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 19200, 38400, 57600, 115200)
brate = input("Enter baudrate (default: 9600): ")

if brate == "":
    brate = 9600
else:
    brate = int(brate)

if not brate in BAUDRATES:
    print("The baudrate you entered is non-standard.")
    print(f"Standart baudrates: {'; '.join(map(str, BAUDRATES))}")
    print("Errors are to be excepted.")

ser = serial.Serial(port=port, xonxoff=True, timeout=None, write_timeout=None, baudrate=brate)

print("Waiting for incoming data...")

while ser.in_waiting == 0:
    sleep(0.2)

print("Incoming data detected. Starting data reading and decoding...")

y = ser.read_until(expected="\x04".encode("utf-8")) #EOT (end of transfer) znak
ser.close()

z = y.decode("utf-8")[:-1]

print("Data decoded. Output: \n")

print(z)

input("\nPress Enter to exit...")