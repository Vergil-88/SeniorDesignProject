from time import sleep
import threading
import TCPLink
import math
import Comm
# import uwb
import time

# my_thread = threading.Thread(target=uwb.main)
# # Start the thread
# my_thread.start()  

# sleep(30)

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


avgDis, Encdr_angle,timeDis,dx,dy, prv_time, Encdr_Distance, Desired_Angle, gyro_Angle, cntR_int, cntL_int, R_start, L_start , cntR_prev2 , cntL_prev2 = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

# sleep(20)

# X= uwb.x
# Y= uwb.y

def postion_xy(angle , distance):
    angle = (math.pi*angle) / 180
    dx = distance * math.cos(angle)
    dy = distance * math.sin(angle)
    return dx, dy




def encoder_Acalcs(cntR,cntL):
    
    if (cntR-cntR_prev)>4500 or cntR>8000:
         cntR-=9000
         

    if (cntL-cntL_prev)>4500 or cntL>8000:
         cntL-=9000
         

    dR=cntR-cntR_prev
    dL=cntL-cntL_prev
    
    k=-0.5
    
    Encdr_angle = k * (dR-dL)

    return Encdr_angle


def encoder_Dcalcs(cntR,cntL,cntR_prev,cntL_prev):
    
    if (cntR-cntR_prev)>4500 or cntR>8000:
         cntR-=9000
         

    if (cntL-cntL_prev)>4500 or cntL>8000:
         cntL-=9000
         

    dR=cntR-cntR_prev
    dL=cntL-cntL_prev

    



    dAvg = (dR+dL)/2


    
    Encdr_Distance = dAvg/166
    return Encdr_Distance




def calc_dis_ang(x1, y1, x2, y2): # Distance and angle USING THE BEACONS
    # Calculate distance
    distance = math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
    
    # Calculate angle in radians
    angle_radians = math.atan2(y2 - y1, x2 - x1)
    
    # Convert angle to degrees
    angle_degrees = math.degrees(angle_radians)
    
    return distance, angle_degrees


TCPLink.send(S,0,0)


encoderDis=0

while True:



    new_time=time.time()

    dT=new_time-prv_time

    prv_time = new_time

    TCPLink.receive(S,False)     

    gyro_Angle=Comm.angle_values

    cntR_int=TCPLink.cntR_int
    cntL_int=TCPLink.cntL_int
    Distance, Angle = calc_dis_ang(0, 0, 2, 1)

    Encdr_angle = encoder_Acalcs(cntR_int,cntL_int)     
    
    timeAngle = ((time.time() - start_time) * 360) / 50 #calculate current angle using time
    avrgTheta = (Encdr_angle + gyro_Angle) / 2

    


    print("G    ",gyro_Angle)
    print("EN   ",Encdr_angle)
    print("|||||||||||||||||||||")
   

    if  abs(avrgTheta)<=abs(Angle):
        if Angle < 0 and Angle != 0:
            Encdr_angle = encoder_Acalcs(cntR_int,cntL_int)  
            TCPLink.send(S,0,-10)
        elif Angle != 0 :
            TCPLink.send(S,0,10)
            # break
        else:
            TCPLink.send(S,0,0)

      
    # print(avrgTheta)
    # print("|||||||||||||||||||||")


    
    elif ((avgDis)<=Distance) :
        
        TCPLink.send(S,10,0)

        dx, dy = postion_xy(avrgTheta , encoderDis)

        Encdr_Distance = encoder_Dcalcs(cntR_int,cntL_int,cntR_prev2,cntL_prev2)

        encoderDis += Encdr_Distance

        timeDis += 0.10*dT

        avgDis = (encoderDis + timeDis)/2

        cntR_prev2 = cntR_int
        cntL_prev2 = cntL_int

        if cntR_prev2 > 4500:
            cntR_prev2-=9000

        if cntL_prev2 > 4500:
            cntL_prev2-=9000

    else:
        
        TCPLink.send(S,0,0)
        break
    
    
    
    print("timeDis",timeDis)
    print("X= ",dx," Y= ",dy)
    print("ED= ",Encdr_Distance)
    print("encoderDis", encoderDis)
    print("avgDis= ",avgDis)


    

# print("X: %d|| Y: %d",uwb.x ,uwb.y)
