import utime
from machine import I2C, Pin
import sys
sys.path.append('./micropython_mpu9250')

from mpu9250 import MPU9250
import json




def read_data(sensor: MPU9250):
    # print ("Gyro offset", sensor.mpu6500._gyro_offset)
    # print("Mag offset", sensor.ak8963._offset)
    # print("Mag scale", sensor.ak8963._scale)
    data = {"acc": sensor.acceleration, "gyr": sensor.gyro, "mag": sensor.magnetic, "tem": sensor.temperature}
    print(json.dumps(data))
    utime.sleep_ms(100)

def main():

    i2c = I2C(scl=Pin(22), sda=Pin(21), timeout=50000)
    sensor = MPU9250(i2c)

    print("MPU9250 id: " + hex(sensor.whoami))
    sensor.ak8963._scale = 0.9181329, 1.098461, 0.9995317
    sensor.ak8963._offset = 100.7648, -10.6333, 54.01611
    sensor.mpu6500._gyro_offset = 0.06869266, -0.002352364, -0.004157747
    # sensor.ak8963.calibrate()
    # print("Magnetometer calibration complete")
    # sensor.mpu6500.calibrate()
    # print("Calibration complete")

    while True:
        try:
            read_data(sensor=sensor)
        except:
            utime.sleep_ms(1000)
            print("Reconnecting")
            i2c.deinit()
            i2c = I2C(scl=Pin(22), sda=Pin(21))
            sensor = MPU9250(i2c)
            read_data(sensor=sensor)

if __name__ == "__main__":
    main()