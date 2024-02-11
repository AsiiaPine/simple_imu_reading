import utime
from machine import I2C, Pin
from micropython_mpu9250.mpu9250 import MPU9250
import json
i2c = I2C(scl=Pin(22), sda=Pin(21))
sensor = MPU9250(i2c)

print("MPU9250 id: " + hex(sensor.whoami))

data = {}
sensor.ak8963.calibrate()
sensor.mpu6500.calibrate()
print("Calibration complete")
while True:
    data = {"acc": sensor.acceleration, "gyr": sensor.gyro, "mag": sensor.magnetic, "tem": sensor.temperature}
    # print(f"\{"acc": {sensor.acceleration}\}")
    # print("gyr ", sensor.gyro)
    # print("mag ", sensor.magnetic)
    # print("tem ", sensor.temperature)
    print(json.dumps(data))
    utime.sleep_ms(1000)