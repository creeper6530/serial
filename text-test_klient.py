import serial
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

x = input("Enter data to send (multiline text isn't supported):\n")

print("\nEncoding and sending data...")

y = x.encode("utf-8")

ser = serial.Serial(port=port, xonxoff=True, baudrate=brate, timeout=None, write_timeout=None)

ser.write(y)
while ser.out_waiting != 0:
    print(f"{ser.out_waiting} bytes remaining.", end="\r")
ser.write("\x04".encode("utf-8")) #EOT (end of transfer) znak

ser.close()

input("Data sent. Press Enter to exit...")