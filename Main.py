from time import sleep
import threading
import os
import TCPLink
import uwb


x=0
y=0

x_value=0
y_value=0

x_avg = [0] * 10
y_avg = [0] * 10
i_Avg = 0


my_thread = threading.Thread(target=uwb.main)
# Start the thread
my_thread.start()   

dx=0                 
dy=0

    
S=TCPLink.TCP_init()

while True:
    sleep(0.1)
    x=uwb.x
    y=uwb.y
    print(x,y)
    if x!=0 and y!=0 :
        

        
        if abs(x)<200 and abs(y)<200:
            print(x,y)
            i_Avg=i_Avg+1
            if i_Avg==10:
                i_Avg = 0
            
            x_avg[i_Avg]=x
            y_avg[i_Avg]=y         
            
            x_value =sum (x_avg)/10 
            y_value =sum (y_avg)/10 

        wx = 100 # waypoint x
        wy = 100 # waypoint y

        Mspeed = 50 #max speed prev 4000
        print("x=",x,"y=", y)
        print("x_value=",x_value,"y_value=",y_value)
        if abs(x)<200 and abs(y)<200:
            dx = ((wx - x)/400) * Mspeed
            dy = ((wy - y)/400) * Mspeed
        
            print("dx=",dx,"dy=",dy)

        TCPLink.send(S,0,dx)
        


    else:
        TCPLink.send(S,0,0)

        
    TCPLink.receive(S,False)


