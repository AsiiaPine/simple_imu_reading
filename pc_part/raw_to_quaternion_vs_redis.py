from typing import Callable
from RedisPostman.models import LogMessage, Message, IMU9250Message, IMUMessage, Quaternion
from config import log_message_channel, raw_to_quaternion_channel, imu_data_channel
from RedisPostman.RedisWorker import AsyncRedisWorker

from drawing.madgwick_filter import MadgwickAHRS
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


async def visualize_graph(reader: Callable, dataClass: type[Message]):
    """
    Generalized function for plotting the data from IMU, all possible options listed in reader_options.py
    """
    
    worker = AsyncRedisWorker()
    madgwick = MadgwickAHRS()
    async for message in worker.subscribe_grouped(block=1, count=1000000, dataClass=dataClass, channel=imu_data_channel):
        if message is not None:
            try:
                curr_time: float = time.time() - start_time
                times.append(curr_time)

                result: dict[str, np.ndarray] = reader(message)
                madgwick.update(result["acc"], result["gyr"], result["mag"])
                quaternion = madgwick.quaternion
                quaternion_msg = Quaternion(q0=quaternion.q[0], q1=quaternion.q[1], q2=quaternion.q[2], q3=quaternion.q[3])
                worker.broker.publish(raw_to_quaternion_channel, json.dumps(quaternion_msg.to_dict()))
                
            except Exception as e:
                error_message = LogMessage(date=datetime.datetime.now(), process_name="visualize", status=LogMessage.exception_to_dict(e))
                await worker.broker.publish(log_message_channel, json.dumps(error_message.to_dict()))

if __name__ == '__main__':
    asyncio.run(visualize_graph(reader=read_mpu9250_data, dataClass=IMU9250Message))