import RPi.GPIO as gpio
import time

# Setup GPIO mode and warnings
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)



# Define GPIO pins for HC-SR04
trig = 23
echo = 18
obstacle = 0

# Set up GPIO pins
gpio.setup(trig, gpio.OUT)
gpio.setup(echo, gpio.IN)

# gpio.setup(trigR, gpio.OUT)
# gpio.setup(echoR, gpio.IN)

# gpio.setup(trigL, gpio.OUT)
# gpio.setup(echoL, gpio.IN)

# gpio.setup(trigRear, gpio.OUT)
# gpio.setup(echoRear, gpio.IN)

def read_distance(trig, echo):
    # Send a short pulse to trigger the sensor
    gpio.output(trig, True)
    time.sleep(0.00001)
    gpio.output(trig, False)

    # Measure the duration of the echo pulse
    while gpio.input(echo) == 0:
        pulse_start = time.time()
        
    while gpio.input(echo) == 1:
        pulse_end = time.time()

    # Calculate distance in centimeters
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound is approximately 343 meters per second (17150 cm/s)
    distance = round(distance, 2)  # Round to two decimal places
    return distance

obstacle=0
def checkObstacle():
    global obstacle
    
    dist = read_distance(trig, echo)
    time.sleep(0.01)

        
    if dist < 40:
        obstacle = 1
    else:
        obstacle = 0

    # print(dist)
    # print(obstacle)
    return obstacle

# while 1:
#     checkObstacle()        

