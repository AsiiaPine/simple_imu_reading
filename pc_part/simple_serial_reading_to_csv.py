import serial
import numpy as np
import pandas as pd
import datetime
import json
from drawing.drawing import plot_imu_data

headers = [
    "acc",
    "gyr",
    "mag",
    "tem",
    "time"
]

serialPort = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)  # open serial port
print(serialPort.name)  # check which port was really used

input_array = []
time = []
prev_time = datetime.datetime.now()
try:
    while (1):

        # Wait until there is data waiting in the serial buffer
        if (serialPort.in_waiting > 0):
            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline()

            # Print the contents of the serial data
            print(serialString.decode('Ascii'))
            result = json.loads(serialString.decode("Ascii"))

            curr_time = datetime.datetime.now()
            result["time"] = curr_time
            input_array.append(result)
            time.append(curr_time - prev_time)
            prev_time = curr_time
            
except:
    # what to do at KeyboardInterrupt
    serialPort.close()  # close port
    df = pd.DataFrame.from_records(input_array, columns=headers)
    # for key in headers:
    #     # df[key].apply(lambda r: tuple(r))
    #     df[key] = df[key].apply(lambda x: np.array(x))
        
    df.to_csv("imu_results.csv", index=False, header=True, sep=";")    
    # a = np.asarray(input_array)
    # np.savetxt("imu_results.csv", a, delimiter=";", header=";".join(headers))
