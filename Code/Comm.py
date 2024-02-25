import serial
import time

angle_values = 0

def process_line(line):
    global angle_values
    # Check if the line contains the angle value
    if "Angle:" in line:
        # Extract the angle value after the "Angle:" string
        try:
            # Split the line by colon and strip to remove any leading/trailing spaces
            angle_value = line.split("Angle:")[1].strip()
            # Convert the extracted value to a float and store it
            angle_values=(float(angle_value))
        except ValueError:
            # Handle cases where the conversion to float fails
            print(f"Could not convert angle value to float: '{line}'")






# if __name__ == '__main__':
def main():    
    ser = serial.Serial('/dev/tty.usbmodem1301', 115200, timeout=1)


    # try:
    while True:

            # Read and display the values received from Arduino
            if ser.in_waiting >= 0:
                received_data = ser.readline().decode('utf-8').rstrip()
                # print(received_data)
                
            process_line(received_data)   
        
            # print("Extracted angle values:", angle_values)
                       
    # except KeyboardInterrupt:
    #     ser.write(b"0 0\r\n")
    #     print("Exiting program.")
    # finally:
    #     ser.write(b"0 0\r\n")
    #     ser.close()
        
        
        


    