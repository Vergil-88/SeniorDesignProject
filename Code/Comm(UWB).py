import serial
import time

A10Range =0
A20Range =0
A30Range =0
A40Range =0

def process_line(line):
    global A10Range,A20Range,A30Range,A40Range
    # Check if the line contains the angle value
    if "from: 1710" in line:
        try:
        # Extract the angle value after the "Angle:" string
            # Split the line by colon and strip to remove any leading/trailing spaces
            A10Range = line.split("Range:")[1].strip()
            A10Range = A10Range.split('m')[0].strip()
            # Convert the extracted value to a float and store it
            A10Range=(float(A10Range))
            # print(A10Range)
        except:
            pass            
    elif "from: 1720" in line:
        try:
        # Extract the angle value after the "Angle:" string
            # Split the line by colon and strip to remove any leading/trailing spaces
            A20Range = line.split("Range:")[1].strip()
            A20Range = A20Range.split('m')[0].strip()
            # Convert the extracted value to a float and store it
            A20Range=(float(A20Range))
            # print(A20Range) 
        except:
            pass

    elif "from: 30" in line:
        try:
        # Extract the angle value after the "Angle:" string
            # Split the line by colon and strip to remove any leading/trailing spaces
            A30Range = line.split("Range:")[1].strip()
            A30Range = A30Range.split('m')[0].strip()
            # Convert the extracted value to a float and store it
            A30Range=(float(A30Range))
            # print(A30Range)
        except:
            pass
    elif "from: 40" in line:
        # Extract the angle value after the "Angle:" string
        try:
            # Split the line by colon and strip to remove any leading/trailing spaces
            A40Range = line.split("Range:")[1].strip()
            A40Range = A40Range.split('m')[0].strip()
            # Convert the extracted value to a float and store it
            A40Range=(float(A40Range))
            # print(A40Range)
        except:
            pass

x,y=0,0
def tag_pos_4_anchors(a1_range, a2_range, a3_range, a4_range, anchor_positions):
    global x,y
    # This function will now use trilateration to calculate the tag's position
    def equations(p):
        x, y = p
        return (
            (x - anchor_positions[0][0])**2 + (y - anchor_positions[0][1])**2 - a1_range**2,
            (x - anchor_positions[1][0])**2 + (y - anchor_positions[1][1])**2 - a2_range**2,
            (x - anchor_positions[2][0])**2 + (y - anchor_positions[2][1])**2 - a3_range**2,
            (x - anchor_positions[3][0])**2 + (y - anchor_positions[3][1])**2 - a4_range**2,
        )
         

anchor_positions = [
    (-4, 4),  # A1710 position
    (4, 4),  # A1720 position
    (-4, -4),  # A30 position
    (4, -4)  # A40 position
]



# if __name__ == '__main__':
def main():    
    ser = serial.Serial('COM8', 115200, timeout=1)


    # try:
    while True:

            # Read and display the values received from Arduino
            if ser.in_waiting >= 0:
                received_data = ser.readline().decode('utf-8').rstrip()
                # print(received_data)
                
            process_line(received_data)
            x,y=tag_pos_4_anchors(A10Range,A20Range,A30Range,A40Range,)
            print("-----------------")
            print("A10Range",A10Range)
            print("A20Range",A20Range)
            print("A30Range",A30Range)
            print("A40Range",A40Range)   
            
        
            # print("Extracted angle values:", angle_values)
                       
    # except KeyboardInterrupt:
    #     ser.write(b"0 0\r\n")
    #     print("Exiting program.")
    # finally:
    #     ser.write(b"0 0\r\n")
    #     ser.close()
        
        
main()



    