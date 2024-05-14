import serial
import time

# Variables to store the latest values for left, middle, and right
left = None
middle = None
right = None

def process_line(line):
    global left, middle, right
    try:
        # Split the line into components based on commas and strip any whitespace
        values = line.strip().split(',')
        # Assign each value to the respective variable after converting to float
        if len(values) == 3:
            left = float(values[2])
            middle = float(values[1])
            right = float(values[0])
        else:
            print(f"Received line does not have three elements: '{line}'")
    except ValueError:
        # Handle cases where the conversion to float fails
        print(f"Could not convert angle values to float: '{line}'")

def main():    
    # Initialize serial connection
    ser = serial.Serial('/dev/ttyACM1', 115200, timeout=1)

    while True:
        try:
            # Check if there is data waiting in the serial buffer
            if ser.in_waiting > 0:
                received_data = ser.readline().decode('utf-8')
                process_line(received_data)
                # Print the current values of left, middle, and right
                print("Current values - Left:", left, "Middle:", middle, "Right:", right)
        except KeyboardInterrupt:
            # Gracefully exit if there's a keyboard interrupt
            print("Exiting program.")
            break

if __name__ == '__main__':
    main()
