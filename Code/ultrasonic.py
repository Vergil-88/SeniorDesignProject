import RPi.GPIO as gpio
import time

# Setup GPIO mode and warnings
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

distances = [0, 0, 0, 0]

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

    # Wait for the echo to become high (start of echo pulse)
    start_time = time.time()
    if gpio.wait_for_edge(echo, gpio.RISING, timeout=1000):
        pulse_start = time.time()
    else:
        return -1  # Timeout waiting for rising edge

    # Wait for the echo to become low (end of echo pulse)
    if gpio.wait_for_edge(echo, gpio.FALLING, timeout=1000):
        pulse_end = time.time()
    else:
        return -1  # Timeout waiting for falling edge

    # Calculate distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

def check_obstacle():
    obstacles = [0, 0, 0, 0]
    sensors = [(trigF, echoF), (trigR, echoR), (trigL, echoL), (trigRear, echoRear)]

    for i, (trig, echo) in enumerate(sensors):
        distance = read_distance(trig, echo)
        if distance != -1 and distance < 100:
            obstacles[i] = 1
        else:
            obstacles[i] = 0
        time.sleep(0.01)  # Delay to avoid sensor cross-talk

    return obstacles
