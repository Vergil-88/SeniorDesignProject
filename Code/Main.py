from time import sleep
import threading
import TCPLink
import math
import Comm
import CommUWB
import time
import Astar
import ultrasonicOne


my_thread = threading.Thread(target=CommUWB.main)
# Start the thread
my_thread.start()  

my_GY_thread = threading.Thread(target=Comm.main)
my_GY_thread.start() 


start_time = time.time()




sleep(5)

i = 0
S=TCPLink.TCP_init()

# TCP_thred=threading.Thread(TCPLink.receive(S,False))
# TCP_thred.start()

while i<10 :
   
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
    i+=1


    
avgDis,avgX,avgY,uwbX_prev,uwbY_prev ,Encdr_angle,timeDis,dx,dy, prv_time, Encdr_Distance, Desired_Angle, gyro_Angle, cntR_int, cntL_int, R_start, L_start , cntR_prev2 , cntL_prev2 , avrgTheta, uwb_angle, =0, 0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

# sleep(10)

def postion_xy(angle , distance):
    angle = (math.pi*angle) / 180
    dy = distance * math.cos(angle)
    dx = distance * math.sin(angle)
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


    
    Encdr_Distance = (dAvg/166)
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


def angleUWB(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return math.degrees(math.atan2(dy, dx))


def goAngle(Angle):
    global new_time, dT,prv_time,gyro_Angle,timeAngle
    global avrgTheta,Encdr_angle,cntL_prev2,cntR_prev2
    
    Encdr_angle=-1*Encdr_angle
    # print("Encdr_angle= ",Encdr_angle)

    

    
   
    
    if abs(Angle) < abs(gyro_Angle):
        Encdr_angle = encoder_Acalcs(cntR_int,cntL_int) 
         
        avrgTheta = (Encdr_angle + gyro_Angle) / 2
        TCPLink.send(S,0,20)

        cntR_prev2 = cntR_int
        cntL_prev2 = cntL_int

        if cntR_prev2 > 4500:
            cntR_prev2-=9000

        if cntL_prev2 > 4500:
            cntL_prev2-=9000

    elif abs(Angle) > abs(gyro_Angle):
        TCPLink.send(S,0,-20)
        Encdr_angle = encoder_Acalcs(cntR_int,cntL_int)  
        avrgTheta = (Encdr_angle + gyro_Angle) / 2
        cntR_prev2 = cntR_int
        cntL_prev2 = cntL_int

        if cntR_prev2 > 4500:
            cntR_prev2-=9000

        if cntL_prev2 > 4500:
            cntL_prev2-=9000            
        # break
        
    elif Angle == 0:
        if Encdr_angle<0:
            TCPLink.send(S,0,-20)
        else:
            TCPLink.send(S,0,20)
            
            
    else:
        TCPLink.send(S,0,0)
        
            

def goDis(dis):
        global new_time, dT,prv_time,gyro_Angle,Encdr_angle,timeAngle
        global avgX , avgY, avgDis,dx,dy,encoderDis,timeDis,cntR_prev2,cntL_prev2,avrgTheta
        TCPLink.send(S,20,0)
        # dx, dy = postion_xy(Encdr_angle , avgDis)
        dx, dy = postion_xy(gyro_Angle , avgDis)
        
        avgX = (dx*0.7 )+(CommUWB.X * 0.3)
        avgY = (dy*0.7 )+(CommUWB.Y * 0.3)

        Encdr_Distance = encoder_Dcalcs(cntR_int,cntL_int,cntR_prev2,cntL_prev2)

        encoderDis += Encdr_Distance

        timeDis += 0.20*dT

        avgDis = (encoderDis + timeDis)/2

        cntR_prev2 = cntR_int
        cntL_prev2 = cntL_int

        if cntR_prev2 > 4500:
            cntR_prev2-=9000

        if cntL_prev2 > 4500:
            cntL_prev2-=9000



TF=True
def goPoint(srcX,srcY,destX,destY):

    global new_time, dT,prv_time,gyro_Angle,Encdr_angle,timeAngle,avrgTheta,avgDis,Distance, Angle,x_path,y_path,j,dest,TF



    Distance, Angle = calc_dis_ang(srcX,srcY, destX, destY)
    # Angle = 90-Angle

    avgDis=0
    TCPLink.send(S,0,0)
    print(Angle)
    print("going to ",destX,destY)
    while True:
        
        Obstacles=ultrasonicOne.checkObstacle()

        
        
  
        
        if Angle == 180 and gyro_Angle < 0:
            Angle = -180
        # print(Angle)

        # TCPLink.send(S,0,0)
        calc()
        # print("timeDis",timeDis)
        
        
        # elif Angle == 0:
    #     if gyro_Angle<0:
    #         TCPLink.send(S,0,20)
    #     else:
    #         TCPLink.send(S,0,-20)
    
    
        if  abs(Angle - gyro_Angle) >= 5:
            # print(Angle - gyro_Angle)
            goAngle(Angle)
        
        elif ((timeDis)<=Distance) :
            goDis(Distance)
        else:
            avgDis=0
            break

        if (Obstacles==1 and TF==True ):
            TCPLink.send(S,0,0)
            TF=False

            print("BLOCKED",x_path[j], y_path[j])
            
            Astar.SetBlocked(x_path[j], y_path[j])
            
            dest = [-3, 1]
            
            new_src=[x_path[j-1],y_path[j-1]]
            # new_src=[round(CommUWB.X), round(CommUWB.Y)]

            print(new_src)
            print(dest)
            x_path,y_path=Astar.main(new_src, dest)
            print(x_path)
            print(y_path)
            
            j=0
            break 

        # print("avgDis= ",avgDis)



dT=0
new_time=0
timeAngle=0
def calc():
    global new_time, dT,prv_time,gyro_Angle,Encdr_angle,timeAngle

    new_time=time.time()

    dT=new_time-prv_time

    prv_time = new_time

    TCPLink.receive(S,False)     

    gyro_Angle=Comm.latest_angle_value

    cntR_int=TCPLink.cntR_int
    cntL_int=TCPLink.cntL_int

    Encdr_angle = encoder_Acalcs(cntR_int,cntL_int)     
    
    timeAngle = ((time.time() - start_time) * 360) / 50 

    # print("G    ",gyro_Angle)
    # print("EN   ",Encdr_angle)





    


encoderDis=0

# Distance, Angle = calc_dis_ang(CommUWB.X, CommUWB.Y, -1, 1)
# Angle = 90 - Angle


uwbX_prev = CommUWB.X
uwbY_prev = CommUWB.Y

x_path=[]
y_path=[]
print(CommUWB.X, CommUWB.Y)

src =  [round(CommUWB.X), round(CommUWB.Y)]
# src =  [0, 0]
dest = [-3, 1]

# Astar.SetBlocked(-1,-1)


x_path,y_path=Astar.main(src, dest)
print(x_path)
print(y_path)
j=1

enter=0

while True:

    

# print("X: %d|| Y: %d",uwb.x ,uwb.y)


        
        
        

        

    # new_time=time.time()

    # dT=new_time-prv_time

    # prv_time = new_time

    # TCPLink.receive(S,False)     

    # gyro_Angle=Comm.latest_angle_value

    # cntR_int=TCPLink.cntR_int
    # cntL_int=TCPLink.cntL_int

    # Encdr_angle = encoder_Acalcs(cntR_int,cntL_int)     
    
    # timeAngle = ((time.time() - start_time) * 360) / 50 #calculate current angle using time
    

    


    # print("G    ",gyro_Angle)
    # print("EN   ",Encdr_angle)
    # # print("|||||||||||||||||||||")
    
    if j == len(x_path):
        # goPoint(CommUWB.X,CommUWB.Y,dest[0],dest[1])
        break

    if j>2:
        TF=True
    print("j= ",j)
    goPoint(x_path[j-1],y_path[j-1], x_path[j], y_path[j])
    
    
    
    
    

    

  
    # avgDis=0
    # print("uwb_angle= ",uwb_angle)
    # print("X= ",avgX," Y= ",avgY)
    # # print("enX= ",dx," enY= ",dy)
    # print("uwbX= ",CommUWB.X," uwbY= ",CommUWB.Y)
    # # print("ED= ",Encdr_Distance)
    # print("encoderDis", encoderDis)
    # print("avrgTheta",avrgTheta)
    # print("avgDis= ",avgDis)


    print("Distance = ",Distance)
    print("Angle = ",Angle)

    # print("j= ",j)
    print(x_path[j-1],y_path[j-1])
    print(x_path[j], y_path[j])
    
    
    timeDis=0
    dT=0
    new_time=time.time()
    encoderDis=0
    

    
    if j< len(x_path):
        j+=1
    

    TCPLink.send(S,0,0)

print("i'm done")
    
    
    
    

    

# print("X: %d|| Y: %d",uwb.x ,uwb.y)
