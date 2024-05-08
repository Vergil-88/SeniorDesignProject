import RPi.GPIO as gpio
import time

# Setup GPIO mode and warnings
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

distances = [0,0,0,0]

# Define GPIO pins for HC-SR04
trigF = 12
echoF = 18

trigR = 20
echoR = 24

trigL = 16
echoL = 23

trigRear = 21
echoRear = 25

# Set up GPIO pins
gpio.setup(trigF, gpio.OUT)
gpio.setup(echoF, gpio.IN)

gpio.setup(trigR, gpio.OUT)
gpio.setup(echoR, gpio.IN)

gpio.setup(trigL, gpio.OUT)
gpio.setup(echoL, gpio.IN)

gpio.setup(trigRear, gpio.OUT)
gpio.setup(echoRear, gpio.IN)

def read_distance(trig, echo):
    # Send a short pulse to trigger the sensor
    gpio.output(trig, True)
    time.sleep(0.00001)
    gpio.output(trig, False)

    # Measure the duration of the echo pulse
    while gpio.input(echo) == 0:
        pulse_start = time.time()
        # print("asdfasdf")
        
    while gpio.input(echo) == 1:
        pulse_end = time.time()

    # Calculate distance in centimeters
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound is approximately 343 meters per second (17150 cm/s)
    distance = round(distance, 2)  # Round to two decimal places
    return distance


def checkObstacle():
    obstacle = [0,0,0,0]
    
    distF = read_distance(trigF, echoF)
    time.sleep(0.01)
    distR = read_distance(trigR, echoR)
    time.sleep(0.01)
    distL = read_distance(trigL, echoL)
    time.sleep(0.01)
    distRear = read_distance(trigRear, echoRear)
    time.sleep(0.01)

    distances = [distF, distR, distL, distRear]

    for i in range(4):
        
        if distances[i] < 100:
            obstacle[i] = 1
        else
            obstacle[i] = 0


    return obstacle
        




