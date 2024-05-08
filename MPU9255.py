import smbus2
import time

bus = smbus2.SMBus(1)
MPU9250_ADDR = 0x68
PWR_MGMT_1 = 0x6B
GYRO_CONFIG = 0x1B
GYRO_XOUT_H = 0x43
GYRO_ZOUT_H = 0x47

def setup_mpu():
    # Wake up the MPU-9250
    bus.write_byte_data(MPU9250_ADDR, PWR_MGMT_1, 0x00)
    # Set gyroscope to +/- 250 degrees/sec (smallest range for better precision)
    bus.write_byte_data(MPU9250_ADDR, GYRO_CONFIG, 0x00)

def read_i2c_word(reg):
    high = bus.read_byte_data(MPU9250_ADDR, reg)
    low = bus.read_byte_data(MPU9250_ADDR, reg + 1)
    value = (high << 8) | low
    if value >= 0x8000:
        return -((65535 - value) + 1)
    else:
        return value

def get_gyro_data():
    z = read_i2c_word(GYRO_ZOUT_H)
    return z / 131.0  # Divide by sensitivity scale factor for +/- 250 deg/sec

setup_mpu()
yaw = 0.0
time_prev = time.time()

try:
    while True:
        z_rate = get_gyro_data()  # Angular rate in degrees/sec
        time_now = time.time()
        dt = time_now - time_prev
        time_prev = time_now

        yaw += z_rate * dt  # Integrate angular rate over time to estimate angle
        print(f"Yaw: {(yaw+0.76755725190839698):.2f} degrees")

        time.sleep(0.1)
except KeyboardInterrupt:
    print("Measurement stopped by User")
