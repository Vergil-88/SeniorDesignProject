import RPi.GPIO as gpio
import time

# Setup GPIO mode and warnings
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

# Define GPIO pins for HC-SR04
trig1 = 21
echo1 = 25

trig2 = 20
echo2 = 24

trig3 = 16
echo3 = 23

trig4 = 12
echo4 = 18
# Set up GPIO pins
gpio.setup(trig1, gpio.OUT)
gpio.setup(echo1, gpio.IN)

gpio.setup(trig2, gpio.OUT)
gpio.setup(echo2, gpio.IN)

gpio.setup(trig3, gpio.OUT)
gpio.setup(echo3, gpio.IN)

gpio.setup(trig4, gpio.OUT)
gpio.setup(echo4, gpio.IN)

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

try:
    while True:
        dist1 = read_distance(trig1, echo1)
        print("Distance 1:", dist1, "cm")
        time.sleep(0.1)
        dist2 = read_distance(trig2, echo2)
        print("Distance 2:", dist2, "cm")
        time.sleep(0.1)
        dist3 = read_distance(trig3, echo3)
        print("Distance 3: ", dist3, "cm")
        time.sleep(0.1)
        dist4 = read_distance(trig4, echo4)
        print("Distance 4:", dist4, "cm")
        time.sleep(0.5)  # Wait for 1 second before next reading
except KeyboardInterrupt:
    print("Measurement stopped by user")
finally:
    gpio.cleanup()  # Clean up GPIO pins
