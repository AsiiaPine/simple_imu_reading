import utime
from machine import I2C, Pin
import sys
sys.path.append('./micropython_mpu9250')

from mpu9250 import MPU9250
import json




def read_data(sensor: MPU9250):
    data = {"acc": sensor.acceleration, "gyr": sensor.gyro, "mag": sensor.magnetic, "tem": sensor.temperature}
    print(json.dumps(data))
    utime.sleep_ms(100)

def main():

    i2c = I2C(scl=Pin(22), sda=Pin(21), timeout=50000)
    sensor = MPU9250(i2c)

    print("MPU9250 id: " + hex(sensor.whoami))

    # sensor.ak8963.calibrate()
    # sensor.mpu6500.calibrate()
    # print("Calibration complete")

    while True:
        try:
            read_data(sensor=sensor)
        except:
            utime.sleep_ms(1000)
            print("Reconnecting")
            # i2c.deinit()
            # i2c = I2C(scl=Pin(22), sda=Pin(21))
            # sensor = MPU9250(i2c)
            read_data(sensor=sensor)

if __name__ == "__main__":
    main()