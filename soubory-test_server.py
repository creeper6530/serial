#!/usr/bin/python3
from time import sleep
import serial
import base64
import os
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

print("Waiting for incoming data...")

whole_filename = ser.readline().decode("utf-8")[:-1] #Odstraní newline znak na konci

if os.path.exists(whole_filename):
    i = 0
    split_file_name = whole_filename.split(".")
    extension = split_file_name.pop()
    filename = ".".join(split_file_name)
    del split_file_name

    while os.path.exists(whole_filename):
        i += 1
        whole_filename = f'{filename}({i}).{extension}'
        
print("Transmission started. Recieving data...")

sleep(2)

crc_supposed = ser.readline().decode("utf-8")[:-1] #Odstraní newline znak na konci
crc_supposed = int(crc_supposed, base=16)

data_encoded = ""
while True:
    while ser.in_waiting != 0:
        data_encoded += ser.read_all().decode("utf-8")
        sleep(0.2)

    if data_encoded[-1] == "\x04": #EOT (end of transfer) znak
        break

data_encoded = data_encoded.encode("utf-8")

print("Data received. Decoding and checking data...")

data = base64.b64decode(data_encoded)
del data_encoded

calculator = Calculator(Crc32.CRC32, optimized=True)
crc_actual = calculator.checksum(data)
if crc_actual != crc_supposed:
    print("Checksums do not match.")
    input("Press Enter to exit...")
    exit(1)
del calculator

f = open(whole_filename, "wb")
f.write(data)
f.close()

ser.close()

input("Done. Press Enter to exit...")