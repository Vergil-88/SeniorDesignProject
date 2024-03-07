from time import sleep
import threading
import TCPLink
import math
import Comm
import uwb
import time

my_thread = threading.Thread(target=uwb.main)
# Start the thread
my_thread.start()  

sleep(30)

S=TCPLink.TCP_init()
TCPLink.send(S,0,0)
TCPLink.receive(S,False)

## ENCODER INIT (IN A FUNCTION)
cntR_prev=TCPLink.cntR_int
cntL_prev=TCPLink.cntL_int
if cntR_prev > 4500:
    cntR_prev-=9000

if cntL_prev > 4500:
    cntL_prev-=9000
###############


my_GY_thread = threading.Thread(target=Comm.main)
my_GY_thread.start() 

start_time = time.time()

Encdr_angle, Encdr_Distance, Desired_Angle, gyro_Angle, cntR_int, cntL_int, R_start, L_start = 0,0,0,0,0,0,0,0

# sleep(20)

# X= uwb.x
# Y= uwb.y

Encdr_Distance = (Encdr_Distance*9)/400



def encoder_calcs(cntR,cntL):
    
    if (cntR-cntR_prev)>4500 or cntR>8000:
         cntR-=9000
         

    if (cntL-cntL_prev)>4500 or cntL>8000:
         cntL-=9000
         

    dR=cntR-cntR_prev
    dL=cntL-cntL_prev
    k=-0.5
    
    Encdr_angle = k * (dR-dL)

    return Encdr_angle



def calc_dis_ang(x1, y1, x2, y2): # Distance and angle USING THE BEACONS
    # Calculate distance
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    # Calculate angle in radians
    angle_radians = math.atan2(y2 - y1, x2 - x1)
    
    # Convert angle to degrees
    angle_degrees = math.degrees(angle_radians)
    
    return distance, angle_degrees


cntR_int=TCPLink.cntR_int
cntL_int=TCPLink.cntL_int
TCPLink.send(S,0,0)



while True:

    TCPLink.receive(S,True)     

    gyro_Angle=Comm.angle_values

    Distance, Angle = calc_dis_ang(uwb.x, uwb.y, 2, 2)

    Encdr_angle = encoder_calcs(cntR_int,cntL_int)     
    
    timeAngle = ((time.time() - start_time) * 360) / 50 #calculate current angle using time
    avrgTheta = (Encdr_angle + gyro_Angle) / 2


    print("G    ",gyro_Angle)
    print("EN   ",Encdr_angle)
    print("|||||||||||||||||||||")


    if  abs(avrgTheta)<=abs(Angle):
        if Angle < 0 and Angle != 0:
            
            TCPLink.send(S,0,-10)
        elif Angle != 0 :
            TCPLink.send(S,0,10)
            # break
        else:
            TCPLink.send(S,0,0)

        R_start=cntR_int
        L_start=cntL_int
    # print(avrgTheta)
    # print("|||||||||||||||||||||")


    
    if ((cntR_int-R_start)<=166*Distance and (cntL_int-L_start)<=166*Distance) :
        
        TCPLink.send(S,10,0)
    else:
        
        TCPLink.send(S,0,0)
        break


    

print("X: %d|| Y: %d",uwb.x ,uwb.y)
