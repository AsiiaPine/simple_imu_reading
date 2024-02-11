import serial
import numpy as np
import pandas as pd
import datetime
import json


headers = [
    "imu_1_accel x",
    "imu_1_accel y",
    "imu_1_accel z",
    "imu_1_gyro x",
    "imu_1_gyro y",
    "imu_1_gyro z",
    "imu_2_accel x",
    "imu_2_accel y",
    "imu_2_accel z",
    "imu_2_gyro x",
    "imu_2_gyro y",
    "imu_2_gyro z",
]

serialPort = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)  # open serial port
print(serialPort.name)  # check which port was really used

input_array = []
time = []
prev_time = datetime.datetime.now()
ready_to_read = 0
try:
    while (1):

        # Wait until there is data waiting in the serial buffer
        if (serialPort.in_waiting > 0):
            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline()

            # Print the contents of the serial data
            print(serialString.decode('Ascii'))
            if serialString=="Calibration complete":
                ready_to_read = 1
            if ready_to_read:
                result = json.loads(serialString.decode("Ascii"))

                # print(float, serialString.decode('Ascii').split())
                # input_array.append(list(map(float, serialString.decode('Ascii').split())))
                curr_time = datetime.datetime.now()

                time.append(curr_time - prev_time)
                prev_time = curr_time
            # Tell the device connected over the serial port that we recevied the data!
            # The b at the beginning is used to indicate bytes!
            # serialPort.write(b"Thank you for sending data \r\n")
            
except:
    # what to do at KeyboardInterrupt
    serialPort.close()  # close port
    a = np.asarray(input_array)
    np.savetxt("imu_results.csv", a, delimiter=";", header=";".join(headers))

    # df = pd.read_csv("imu_results.csv", delimiter=";")  # will be used in future work with big data
    # print(df.head())
