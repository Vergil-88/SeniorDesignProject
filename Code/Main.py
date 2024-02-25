from time import sleep
import threading
import os
import TCPLink
import uwb
import math
import Comm

def calc_dis_ang(x1, y1, x2, y2):
    # Calculate distance
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    # Calculate angle in radians
    angle_radians = math.atan2(y2 - y1, x2 - x1)
    
    # Convert angle to degrees
    angle_degrees = math.degrees(angle_radians)
    
    return distance, angle_degrees
    
my_thread = threading.Thread(target=uwb.main)
# Start the thread
my_thread.start()   

my_GY_thread = threading.Thread(target=Comm.main)
# Start the thread
my_GY_thread.start() 

  



Distance=0 
Angle=0
gyro_Angle=0
X=0
Y=0


sleep(20)

X= uwb.x
Y= uwb.y

cntR_int=0
cntL_int=0    
    
    
    
    

Distance,Angle=calc_dis_ang(X,Y,100,100)

Distance=(Distance*9)/400

print("Distance",Distance)
print("Angle",Angle)
    
S=TCPLink.TCP_init()
while True:
    
    
    gyro_Angle=Comm.angle_values
    cntR_int=TCPLink.cntR_int
    cntL_int=TCPLink.cntL_int

    
    
    meters=1
    margin=0.5
    # print(angle)
    
    if  gyro_Angle<=Angle  :
    
        TCPLink.send(S,0,10)
        R_start=cntR_int
        L_start=cntL_int   
    
    elif ((cntR_int-R_start)<=166*Distance and (cntL_int-L_start)<=166*Distance):
        TCPLink.send(S,10,0)
    else:
        
        TCPLink.send(S,0,0)

       
    TCPLink.receive(S,True)  
    
    
    

    


