from typing import Callable
from RedisPostman.models import LogMessage, Message, IMU9250Message, IMUMessage
from config import imu_data_channel, log_message_channel
from RedisPostman.RedisWorker import AsyncRedisWorker

from drawing.drawing import plot_imu_data
import matplotlib.pyplot as plt
import numpy as np
import asyncio
import datetime
import time
import json


acc = []
gyr = []
mag = []
times = []
input_array = []
start_time = time.time()

# since there are two types for messages, use the reader function
def read_mpu9250_data(message: IMU9250Message) -> dict[str, np.ndarray]:
    return {"acc": message.imu.acc, "gyr": message.imu.gyr, "mag": message.imu.mag}

def read_mpu6500_data(message: IMUMessage) -> dict[str, np.ndarray]:
    return {"acc": message.imu.acc, "gyr": message.imu.gyr, "mag": None}


async def visualize_graph(reader: Callable,  channel: str, dataClass: type[Message], fig, axs):
    """
    Generalized function for plotting the data from IMU, all possible options listed in reader_options.py
    """
    
    worker = AsyncRedisWorker()

    async for message in worker.subscribe_grouped(block=1, count=1000000, dataClass=dataClass, channel=channel):
        if message is not None:
            try:
                curr_time: float = time.time() - start_time
                times.append(curr_time)

                result: dict[str, np.ndarray] = reader(message)
                acc.append(result["acc"])
                gyr.append(result["gyr"])
                mag.append(result["mag"])
                
                
                fig, axs = plot_imu_data(
                    accels=np.array(acc),
                    gyros=np.array(gyr),
                    magnets=np.array(mag),
                    time=times,
                    axs=axs,
                    fig=fig,
                )
                plt.pause(0.0001)

            except Exception as e:
                error_message = LogMessage(date=datetime.datetime.now(), process_name="visualize", status=LogMessage.exception_to_dict(e))
                await worker.broker.publish(log_message_channel, json.dumps(error_message.to_dict()))

if __name__ == '__main__':
    fig, axs = plt.subplots(ncols=1, nrows=3, figsize=(18 * 2, 6 * 3))

    asyncio.run(visualize_graph(reader=read_mpu9250_data, channel=imu_data_channel, dataClass=IMU9250Message, fig=fig, axs=axs))