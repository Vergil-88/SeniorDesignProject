import Astar
import math

# x_path=[]
# y_path=[]

# x,y,dest_x,dest_y=0,0,-2,1

# src =  [0.07 ,0.09]
# dest = [-2,-2]

# x_path,y_path=Astar.main(src, dest)

# print(x_path)
# print(y_path)

def calc_dis_ang(x1, y1, x2, y2): # Distance and angle USING THE BEACONS
    # Calculate distance
    distance = math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
    
    # Calculate angle in radians
    angle_radians = math.atan2(y2 - y1, x2 - x1)
    
    # Convert angle to degrees
    
    if (y2-y1)<0 and (x2-x1)<0:
        angle_radians = math.atan2(x2 - x1,y2 - y1)
       
        angle_degrees = math.degrees(angle_radians)
        
        
        
    else:
        angle_radians = math.atan2(y2 - y1, x2 - x1)
        angle_degrees =90 - math.degrees(angle_radians)
        
        
        
   
    return distance, angle_degrees



N,M=calc_dis_ang(0,0,-2,3)

# M= -90 
print(M)