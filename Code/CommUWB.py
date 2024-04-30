import serial
import time
from scipy.optimize import fsolve
from scipy.optimize import least_squares

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
    # This function will now use trilateration to calculate the tag's position
    def equations(p):
        x, y = p
        return (
            (x - anchor_positions[0][0])**2 + (y - anchor_positions[0][1])**2 - a1_range**2,
            (x - anchor_positions[1][0])**2 + (y - anchor_positions[1][1])**2 - a2_range**2,
            (x - anchor_positions[2][0])**2 + (y - anchor_positions[2][1])**2 - a3_range**2,
            (x - anchor_positions[3][0])**2 + (y - anchor_positions[3][1])**2 - a4_range**2,
        )

    # Initial guess for the positions (can be improved based on your setup)
    x0, y0 = 0, 0

    result = least_squares(equations, (x0, y0))

    # Extract the solution
    x, y = result.x

    return x, y
         

anchor_positions = [
    (-4.5, 4.5),  # A1710 position
    (4.5, 4.5),  # A1720 position
    (-4.5, -4.5),  # A30 position
    (4.5, -4.5)  # A40 position
]


avg_x,avg_y = 0,0
# if __name__ == '__main__':
def main():
    global avg_x,avg_y    
    ser = serial.Serial('/dev/tty.usbserial-02619786', 115200, timeout=1)

    n=20
    # try:
    A10_avg = [0] * n
    A20_avg = [0] * n
    A30_avg = [0] * n
    A40_avg = [0] * n
    i_Avg = 0

    A10_value=0
    A20_value=0
    A30_value=0
    A40_value=0

    

    while True:

            # Read and display the values received from Arduino
            if ser.in_waiting >= 0:
                received_data = ser.readline().decode('utf-8').rstrip()
                # print(received_data)
                
            process_line(received_data)
            # x,y=tag_pos_4_anchors(A10Range,A20Range,A30Range,A40Range,anchor_positions)


            
            i_Avg=i_Avg+1
            i_Avg= i_Avg%n

            if abs(A10Range) <=13 :
                A10_avg[i_Avg]=abs(A10Range)

            if abs(A20Range) <=13 :
                A20_avg[i_Avg]=abs(A20Range)

            if abs(A30Range) <=13 :
                A30_avg[i_Avg]=abs(A30Range)

            if abs(A40Range) <=13 :
                A40_avg[i_Avg]=abs(A40Range)

            A10_value =sum(A10_avg)/n 
            A20_value =sum(A20_avg)/n
            A30_value =sum(A30_avg)/n
            A40_value =sum(A40_avg)/n





            # print("-----------------")
            # print("A10Range",A10Range)
            # print("A20Range",A20Range)
            # print("A30Range",A30Range)
            # print("A40Range",A40Range)
            # print("x",x)
            # print("y",y)

            # print("---------avg--------")

            # print("A10_value",A10_value)
            # print("A20_value",A20_value)
            # print("A30_value",A30_value)
            # print("A40_value",A40_value)

          
            avg_x,avg_y=tag_pos_4_anchors(A10_value,A20_value,A30_value,A40_value,anchor_positions)
            # print("avg_x",avg_x)
            # print("avg_y",avg_y)
            
        
            # print("Extracted angle values:", angle_values)
                       
    # except KeyboardInterrupt:
    #     ser.write(b"0 0\r\n")
    #     print("Exiting program.")
    # finally:
    #     ser.write(b"0 0\r\n")
    #     ser.close()
        
        
# main()



    