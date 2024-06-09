from time import sleep
from operator import truediv
import socket
import numpy as np
from numpy.core import uint16
import Comm
import threading
import time


"""
@author: Ahmed Patwa
Last updated on 8/6/2022
"""
# my_thread = threading.Thread(target=Comm.main)
# # Start the thread
# my_thread.start() 

angle_values=0


def TCP_init():
    # IP and PORT of the ESP server
    TCP_IP, TCP_PORT = "192.168.4.1", 8000
    # Receive and send buffer information
    Read_Buffer_size_bytes = 22
    # Establish connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.settimeout(20)
    print("Connected successfully")
    print(s.getsockname())
    return s


def send(s, speed, steer):
    # Send Commands
    
    start = uint16(43981)  # Start (2 bytes)
    if(steer<0):
        steer = steer + 65535
    
    steerp = uint16(steer)  # Steer (2 bytes) (Steer is inverted)
    
    if(speed<0):
        speed = speed + 65535
    
    speedp = uint16(speed)  # Speed (2 bytes)

    chkSum = (start ^ steerp) ^ speedp
    chkSum = uint16(chkSum)  # Error detection bytes (2 bytes)
    write_buffer = np.array([start, steerp, speedp, chkSum])
    write_buffer = write_buffer.tobytes()  # Group them into one command as 8 byest
    s.send(write_buffer)  # Send command

cntR_int=0
cntL_int=0

def receive(s, debug):
    global cntR_int,cntL_int
    feedback = s.recv(22)
    
    if len(feedback) >= 22:
        # print("message from server:", feedback.decode("UTF-8"))   # For debugging, if sent message is UTF-8
        # print("message from server:", feedback)                   # For debugging, if sent message is numeric
        header = feedback[0:2]
        cmd1 = feedback[2:4]  # Current steer
        cmd2 = feedback[4:6]  # Current speed
        spdR = feedback[6:8]  # Motor speed R
        spdL = feedback[8:10]  # Motor speed L
        cntR = feedback[10:12]  # Wheels encoder R
        cntL = feedback[12:14]  # Wheels encoder L
        batV = feedback[14:16]  # Battery voltage
        temp = feedback[16:18]  # Temperature
        cmdLED = feedback[18:20]  # LED
        chkSum = feedback[20:22]  # Error detection
        
        cntR_int = int.from_bytes(cntR, byteorder='little')
        cntL_int = int.from_bytes(cntL, byteorder='little')
        
        if debug:
            # TODO: Cast all the byte-type variables into the appropriate type (int16-uint16)
            # print(
            #     f"speed: {int.from_bytes(cmd2, byteorder='little')} | temp: {int.from_bytes(temp, byteorder='little')} | "
            #     f"voltage: {int.from_bytes(batV, byteorder='little')}")
            # print(f"temp: {int.from_bytes(temp, byteorder='little')}")
            # print(f"voltage: {int.from_bytes(batV, byteorder='little')}")
            # print("---------------------------")
            # print(f"cntR: {int.from_bytes(cntR, byteorder='little')}")
            # print(f"cntL: {int.from_bytes(cntL, byteorder='little')}")
            pass



# start_time = time.time()
# Pi=0
# prv_time=time.time()
# S=TCP_init()
# while True:
    
#     send(S,10,0)
#     receive(S,False)
    
    
#     new_time=time.time()

#     dT=new_time-prv_time

#     prv_time = new_time

#     Pi += 0.10*dT
    
    
    
#     print("dT: ",dT)

#     print("Y: ",Pi)
#     if Pi >= 1 :
#         break




# S=TCP_init()
# angle=0

# R_start=0
# L_start=0

# while True:
    
    
    
    
#     angle=Comm.angle_values
#     meters=1
#     margin=0.5
#     print(angle)
    
#     if  angle<=45  :
    
#         send(S,10,10)
#         R_start=cntR_int
#         L_start=cntL_int   
    
#     elif ((cntR_int-R_start)<=166*meters and (cntL_int-L_start)<=166*meters):
#         send(S,10,0)
#     else:
        
#         send(S,0,0)

#     receive(S,True)  
# def main():     
#     s = TCP_init()   
#     while True:
#         receive(s,False)


# if __name__ == '__main__':

#     main()
    
    
    
