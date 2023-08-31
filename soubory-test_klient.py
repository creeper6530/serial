#!/usr/bin/python3
import serial
import base64
import platform
from crc import Calculator, Crc32

if platform.system() == "Windows":
    port = "COM5"
elif platform.system() == "Linux":
    port = "/dev/serial0"

BAUDRATES = (50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 19200, 38400, 57600, 115200)
brate = input("Enter baudrate (default: 115200): ")

if brate == "":
    brate = 115200
else:
    brate = int(brate)

if not brate in BAUDRATES:
    print("The baudrate you entered is non-standard.")
    print(f"Standart baudrates: {'; '.join(map(str, BAUDRATES))}")
    print("Errors are to be excepted.")

try: ser = serial.Serial(port, xonxoff=True, timeout=None, write_timeout=None, baudrate=brate)
except serial.SerialException: input("Could not open port. Did you enter correct port name/number?\nPress Enter to exit..."); exit(1)
del port

file = input("Enter name of the file with extension to send (both relative and absolute path supported): ")
try: f = open(file, "rb")
except FileNotFoundError: input("File not found. Press Enter to exit..."); exit(1)

data = f.read()
f.close()
del f

calculator = Calculator(Crc32.CRC32, optimized=True)
crc = calculator.checksum(data)
crc = hex(crc)
del calculator

data_encoded = base64.b64encode(data)
del data

whole_filename = file.split("\\")
del file

filename = "".join(whole_filename.pop())
del whole_filename

ser.write(f"{filename}\n".encode('utf-8'))
del filename

ser.write(f"{crc}\n".encode('utf-8'))

ser.write(data_encoded)

print("Sending data...")
while ser.out_waiting != 0:
    print(f"{ser.out_waiting} bytes remaining.", end="\r")
ser.write("\x04".encode("utf-8")) #EOT (end of transfer) znak

del data_encoded
ser.close()

input("Data sent. Press Enter to exit...")