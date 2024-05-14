import serial
import time

# Variable to store the latest angle value
latest_angle_value = None

def process_line(line):
    global latest_angle_value
    try:
        # Convert the received line to a float and store it as the latest angle value
        latest_angle_value = float(line.strip())
    except ValueError:
        # Handle cases where the conversion to float fails
        print(f"Could not convert angle value to float: '{line}'")

def main():    
    # Initialize serial connection
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

    while True:
        try:
            # Check if there is data waiting in the serial buffer
            if ser.in_waiting > 0:
                received_data = ser.readline().decode('utf-8')
                process_line(received_data)
                # print("Current angle value:", latest_angle_value)
        except KeyboardInterrupt:
            # print("Exiting program.")
            break

if __name__ == '__main__':
    main()
