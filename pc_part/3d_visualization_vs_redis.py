from vpython import *
from time import *
import numpy as np
import math


from typing import Callable
from RedisPostman.models import LogMessage, Message, Quaternion
from config import log_message_channel, quaternion_channel
from RedisPostman.RedisWorker import AsyncRedisWorker

import numpy as np
import asyncio
import datetime
import json


# set the scene and object for visualization    
scene.range=5
toRad=2*np.pi/360
toDeg=1/toRad
scene.forward=vector(-1,-1,-1)

scene.width=600
scene.height=600

xarrow=arrow(lenght=2, shaftwidth=.1, color=color.red,axis=vector(1,0,0))
yarrow=arrow(lenght=2, shaftwidth=.1, color=color.green,axis=vector(0,1,0))
zarrow=arrow(lenght=4, shaftwidth=.1, color=color.blue,axis=vector(0,0,1))

frontArrow=arrow(length=4,shaftwidth=.1,color=color.purple,axis=vector(1,0,0))
upArrow=arrow(length=1,shaftwidth=.1,color=color.magenta,axis=vector(0,1,0))
sideArrow=arrow(length=2,shaftwidth=.1,color=color.orange,axis=vector(0,0,1))

bBoard=box(length=6,width=2,height=.2,opacity=.8,pos=vector(0,0,0,))
bn=box(length=1,width=.75,height=.1, pos=vector(-.5,.1+.05,0),color=color.blue)
nano=box(lenght=1.75,width=.6,height=.1,pos=vector(-2,.1+.05,0),color=color.green)
myObj=compound([bBoard,bn,nano])



# def read_quaternion_data(message: Quaternion) -> dict[str, np.ndarray]:
#     return {"q0": message.q0, "q1": message.q1, "q2": message.q2, "q3": message.q3}


import math

def quat2eulers(q0:float, q1:float, q2:float, q3:float) -> tuple:
    """
    Compute yaw-pitch-roll Euler angles from a quaternion.
    
    Args
    ----
        q0: Scalar component of quaternion.
        q1, q2, q3: Vector components of quaternion.
    
    Returns
    -------
        (roll, pitch, yaw) (tuple): 321 Euler angles in radians
    """
    roll = math.atan2(
        2 * ((q2 * q3) + (q0 * q1)),
        q0**2 - q1**2 - q2**2 + q3**2
    )  # radians
    pitch = math.asin(2 * ((q1 * q3) - (q0 * q2)))
    yaw = math.atan2(
        2 * ((q1 * q2) + (q0 * q3)),
        q0**2 + q1**2 - q2**2 - q3**2
    )
    return (roll, pitch, yaw)


async def visualize_quaternion(channel: str, dataClass: type[Message]):
    """
    Generalized function for plotting the data from IMU, all possible options listed in reader_options.py
    """
    
    worker = AsyncRedisWorker()

    async for message in worker.subscribe_grouped(block=1, count=1000000, dataClass=dataClass, channel=channel):
        assert message is Quaternion
        if message is not None:
            try:
                roll, pitch, yaw = quat2eulers(message.q0, message.q1, message.q2, message.q3)
                
                for yaw in np.arange(0,2*np.pi,.01):
                    rate(50)
                    k=vector(np.cos(yaw)*np.cos(pitch), np.sin(pitch),np.sin(yaw)*np.cos(pitch))
                    y=vector(0,1,0)
                    s=np.cross(k,y)
                    v=np.cross(s,k)

                    frontArrow.axis=k
                    sideArrow.axis=s
                    upArrow.axis=v
                    myObj.axis=k
                    myObj.up=v
                    sideArrow.length=2
                    frontArrow.length=4
                    upArrow.length=1

            except Exception as e:
                error_message = LogMessage(date=datetime.datetime.now(), process_name="visualize_roll_pitch_yaw", status=LogMessage.exception_to_dict(e))
                await worker.broker.publish(log_message_channel, json.dumps(error_message.to_dict()))

if __name__ == '__main__':
    asyncio.run(visualize_quaternion(channel=quaternion_channel, dataClass=Quaternion))