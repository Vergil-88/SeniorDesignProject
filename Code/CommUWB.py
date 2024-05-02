import serial
import time

X=0
Y=0

def process_line(line):
    global X, Y
    # Split the line into parts by spaces
    parts = line.split()
    for part in parts:
        # Check for 'X=' and extract the value
        if "X=" in part:
            try:
                X = float(part.split("X=")[1])
            except ValueError:
                print("Error parsing X value")
        # Check for 'Y=' and extract the value
        elif "Y=" in part:
            try:
                Y = float(part.split("Y=")[1])
            except ValueError:
                print("Error parsing Y value")

def main():
    # Configure the serial connection
    ser = serial.Serial('/dev/tty.usbserial-02619786', 115200, timeout=1)
    while True:
        # Read a line from the serial port
        if ser.in_waiting > 0:
            received_data = ser.readline().decode('utf-8').strip()
            # print("Received:", received_data)
            # Process the received data to extract X and Y
            process_line(received_data)
            # Print the extracted values
            # print("X:",X)
            # print ("Y:",Y)

# if __name__ == '__main__':
#     # Global variables for storing the X and Y coordinates
#     X = 0
#     Y = 0
# main()
