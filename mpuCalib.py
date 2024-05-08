import smbus2
import time

bus = smbus2.SMBus(1)
MPU9250_ADDR = 0x68
PWR_MGMT_1 = 0x6B
GYRO_ZOUT_H = 0x47

def setup_mpu():
    bus.write_byte_data(MPU9250_ADDR, PWR_MGMT_1, 0x00)

def read_i2c_word(reg):
    high = bus.read_byte_data(MPU9250_ADDR, reg)
    low = bus.read_byte_data(MPU9250_ADDR, reg + 1)
    value = (high << 8) | low
    if value >= 0x8000:
        return -((65535 - value) + 1)
    else:
        return value

def calibrate_gyro(samples=100):
    print("Calibrating gyroscope...")
    total = 0
    for _ in range(samples):
        z_rate = read_i2c_word(GYRO_ZOUT_H) / 131.0
        total += z_rate
        time.sleep(0.01)
    bias = total / samples
    print(f"Calibration complete. Bias: {bias:.2f} degrees/sec")
    return bias

setup_mpu()
gyro_bias = calibrate_gyro()

try:
    while True:
        z_rate = read_i2c_word(GYRO_ZOUT_H) / 131.0 - gyro_bias
        print(f"Corrected gyro rate (Z-axis): {z_rate:.2f} degrees/sec")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Measurement stopped by User   ", gyro_bias)
