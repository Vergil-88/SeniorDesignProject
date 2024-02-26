import math

def calc_dis_ang(x1, y1, x2, y2):
    # Calculate distance
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    # Calculate angle in radians
    angle_radians = math.atan2(y2 - y1, x2 - x1)
    
    # Convert angle to degrees
    angle_degrees = math.degrees(angle_radians) 
    
    return distance, angle_degrees

def encoder_calcs(cntR,cntL):
    
    
    dR=cntR-cntR_prev
    dL=cntL-cntL_prev
    k=0.85
    
    dTheta = k * (dR-dL) 
    
    
    cntL_prev=cntL
    cntR_prev=cntR



# Distance,Angle=calc_dis_ang(0,0,0,100)
# print("Distance",Distance)
# print("Angle",Angle)

