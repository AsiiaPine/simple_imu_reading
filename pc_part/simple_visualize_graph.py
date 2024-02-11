import serial
import numpy as np
import pandas as pd
import datetime
import json
from drawing.drawing import plot_imu_data
import matplotlib.pyplot as plt
import time

headers = ["acc", "gyr", "mag", "tem", "time"]

acc = []
gyr = []
mag = []
times = []
input_array = []
start_time = time.time()


def main(serialPort: serial.Serial) -> Exception | None:
    try:
        fig, axs = plt.subplots(ncols=1, nrows=3, figsize=(18 * 2, 6 * 3))
        while 1:
            # Wait until there is data waiting in the serial buffer
            if serialPort.in_waiting > 0:

                serialPort.reset_input_buffer()
                last_received = serialPort.readline()

                # Print the contents of the serial data
                print(last_received.decode("Ascii"))
                result = json.loads(last_received.decode("Ascii"))

                curr_time: float = time.time() - start_time
                
                result["time"] = datetime.time()

                input_array.append(result)

                times.append(curr_time)
                acc.append(np.array(result["acc"]))
                gyr.append(np.array(result["gyr"]))
                mag.append(np.array(result["mag"]))
                
                fig, axs = plot_imu_data(
                    accels=np.array(acc),
                    gyros=np.array(gyr),
                    magnets=np.array(mag),
                    time=times,
                    axs=axs,
                    fig=fig,
                )

                plt.pause(0.0001)
    except KeyboardInterrupt as e:
        return e
    except Exception as e:
        print(e)
        return e
        


if __name__ == "__main__":
    
    serialPort = serial.Serial(port="/dev/ttyUSB0", baudrate=115200)  # open serial port
    print(serialPort.name)  # check which port was really used
    
    error = main(serialPort=serialPort)
    if error == KeyboardInterrupt:
        serialPort.close()  # close port
        df = pd.DataFrame.from_records(input_array, columns=headers)
        for key in headers:
            df[key] = df[key].apply(lambda x: np.array(x))
        df.to_csv("imu_results.csv", index=False, header=True)
    else:
        serialPort = serial.Serial(port="/dev/ttyUSB0", baudrate=115200)  # open serial port
        main(serialPort=serialPort)