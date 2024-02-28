from time import sleep
import threading
import os
import TCPLink
# import uwb
import math
import Comm



S=TCPLink.TCP_init()


def calc_dis_ang(x1, y1, x2, y2): # Distance and angle USING THE BEACONS
    # Calculate distance
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    # Calculate angle in radians
    angle_radians = math.atan2(y2 - y1, x2 - x1)
    
    # Convert angle to degrees
    angle_degrees = math.degrees(angle_radians)
    
    return distance, angle_degrees
    
# my_thread = threading.Thread(target=uwb.main)
# # Start the thread
# my_thread.start()   

my_GY_thread = threading.Thread(target=Comm.main)
# Start the thread
my_GY_thread.start() 

TCPLink.send(S,0,0)
TCPLink.receive(S,False)
    

cntR_prev=TCPLink.cntR_int
cntL_prev=TCPLink.cntL_int

if cntR_prev > 4500:
    cntR_prev-=9000

if cntL_prev > 4500:
    cntL_prev-=9000



print("intial cntR_prev",cntR_prev)
print("intial cntL_prev",cntL_prev)





def encoder_calcs(cntR,cntL):
    global cntR_prev,cntL_prev,dTheta
    
    if (cntR-cntR_prev)>2000 or cntR>8000:
         cntR-=9000
         

    if (cntL-cntL_prev)>2000 or cntL>8000:
         cntL-=9000
         

    dR=cntR-cntR_prev
    dL=cntL-cntL_prev
    k=-0.5
    
    dTheta = k * (dR-dL)

    # dTheta=dTheta%360
    
    

    # print("cntR",cntR,"cntL",cntL)
    # print("cntR_prev",cntR_prev,"cntL_prev",cntL_prev)
    # print("dR",dR,"dL",dL)
    print("dTheta",dTheta)

    # cntL_prev=cntL
    # cntR_prev=cntR  



Distance=0 
Angle=0
gyro_Angle=0
X=0
Y=0


# sleep(20)

# X= uwb.x
# Y= uwb.y

cntR_int=0
cntL_int=0    

R_start=0
L_start=0
    
    
    

# Distance,Angle=calc_dis_ang(X,Y,20,30)

Distance=(Distance*9)/400

print("Distance",Distance)
print("Angle",Angle)
print(X,",",Y)
    
TCPLink.send(S,0,0)
while True:
    # print("Distance",Distance)
    # print("Angle",Angle)
    TCPLink.receive(S,True)     
    

    gyro_Angle=Comm.angle_values
    cntR_int=TCPLink.cntR_int
    cntL_int=TCPLink.cntL_int

    encoder_calcs(cntR_int,cntL_int)     
    
    
    
    meters=1
    margin=0.5
    # print(angle)
    # print(gyro_Angle)

    # R_start=cntR_int
    # L_start=cntL_int   
    Angle=90
    if  abs(dTheta)<=abs(Angle):
        if Angle < 0 and Angle != 0:
            
            TCPLink.send(S,0,-10)
        elif Angle != 0 :
            TCPLink.send(S,0,10)
        else:
            TCPLink.send(S,0,0)

        R_start=cntR_int
        L_start=cntL_int  

    
    
    # elif ((cntR_int-R_start)<=166*Distance and (cntL_int-L_start)<=166*Distance) :
        
    #     TCPLink.send(S,10,0)
    # else:
        
    #     TCPLink.send(S,0,0)
    #     break
