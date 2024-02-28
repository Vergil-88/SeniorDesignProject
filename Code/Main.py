from time import sleep
import threading
import os
import time
import TCPLink
# import uwb
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
    
# my_thread = threading.Thread(target=uwb.main)
# # Start the thread
# my_thread.start()   

my_GY_thread = threading.Thread(target=Comm.main)
# Start the thread
my_GY_thread.start() 

# TCPLink.send(S,0,0)
# TCPLink.receive(S,False)

    

# cntR_prev=TCPLink.cntR_int
# cntL_prev=TCPLink.cntL_int

# if cntR_prev > 4500:
#     cntR_prev-=9000

# if cntL_prev > 4500:
#     cntL_prev-=9000

# dTheta = 0



# print("intial cntR_prev",cntR_prev)
# print("intial cntL_prev",cntL_prev)

# print("intial cntR",TCPLink.cntR_int)
# print("intial cntL",TCPLink.cntL_int)





def encoder_calcs(cntR,cntL):
    global cntR_prev,cntL_prev,dTheta
    
    if (cntR-cntR_prev)>4500 or cntR>8000:
         cntR-=9000
         

    if (cntL-cntL_prev)>4500 or cntL>8000:
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

execute_once = True

S=TCPLink.TCP_init()
TCPLink.send(S,0,0)

start_time = time.time()

while True:
    # print("Distance",Distance)
    # print("Angle",Angle)
    TCPLink.receive(S,True)     
    

    gyro_Angle=Comm.angle_values
    cntR_int=TCPLink.cntR_int
    cntL_int=TCPLink.cntL_int

    if execute_once:
        # The line of code you want to execute only once
        cntR_prev=cntR_int
        cntL_prev=cntL_int

        if cntR_prev > 4500:
            cntR_prev-=9000

        if cntL_prev > 4500:
            cntL_prev-=9000

        dTheta = 0



        print("intial cntR_prev",cntR_prev)
        print("intial cntL_prev",cntL_prev)

        print("intial cntR",TCPLink.cntR_int)
        print("intial cntL",TCPLink.cntL_int)

        
        # Set the flag to False so this block doesn't execute again
        execute_once = False
    

    # print("current cntR",TCPLink.cntR_int)
    # print("current cntL",TCPLink.cntL_int)

    encoder_calcs(cntR_int,cntL_int)     
    
    
    
    meters=1
    margin=0.5
    # print(angle)
    print("gyro_Angle",gyro_Angle)

    # R_start=cntR_int
    # L_start=cntL_int   
    Angle=90

    timeAngle = ((time.time() - start_time)*360)/50 #calcolate current angle using time

    print("timeAngle",timeAngle)

    avrgTheta = (dTheta + gyro_Angle+timeAngle)/3
    print("avrgTheta",avrgTheta)
     
    if  abs(avrgTheta)<=abs(Angle)   :

        
        if Angle <0 and Angle != 0:
            
            TCPLink.send(S,0,-10)
        elif Angle != 0 :
            TCPLink.send(S,0,10)
            # break
        else:
            TCPLink.send(S,0,0)

        R_start=cntR_int
        L_start=cntL_int  

    
    
    # elif ((cntR_int-R_start)<=166*Distance and (cntL_int-L_start)<=166*Distance) :
        
    #     TCPLink.send(S,10,0)
    # else:
        
    #     TCPLink.send(S,0,0)
    #     break

       
     
    
    
    

    


