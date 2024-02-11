from vpython import *
from time import *
import numpy as np
import math


from typing import Callable
from RedisPostman.models import (
    LogMessage,
    Message,
    Quaternion,
    IMU9250Message,
    IMU9250Data,
)

from config import log_message_channel, quaternion_channel, raw_to_quaternion_channel
from RedisPostman.RedisWorker import AsyncRedisWorker, RedisWorker

import numpy as np
import datetime
import json
import math
import vpython as vp


def quat2eulers(q0: float, q1: float, q2: float, q3: float) -> tuple:
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
        2 * ((q2 * q3) + (q0 * q1)), q0**2 - q1**2 - q2**2 + q3**2
    )  # radians
    pitch = math.asin(2 * ((q1 * q3) - (q0 * q2)))
    yaw = math.atan2(2 * ((q1 * q2) + (q0 * q3)), q0**2 + q1**2 - q2**2 - q3**2)
    return (roll, pitch, yaw)


print("Hi 1")
vp.scene.range = 5
toRad = 2 * np.pi / 360
toDeg = 1 / toRad
vp.scene.forward = vp.vector(-1, -1, -1)

vp.scene.width = 600
vp.scene.height = 600
print("Hi 2")
xarrow = vp.arrow()
# xarrow = vp.arrow(pos=vp.vector(0, 1, 0), color=vp.color.red, axis=vp.vector(1.0, 0.0, 0.0))

# xarrow=vp.arrow(length=2, shaftwidth=0.1, color=vp.color.red,axis=vp.vector(1.0,0.0,0.0))
print("Hi 2")
yarrow = vp.arrow(
    length=3, shaftwidth=0.1, color=vp.color.green, axis=vp.vector(0, 1, 0)
)
zarrow = vp.arrow(
    length=4, shaftwidth=0.1, color=vp.color.blue, axis=vp.vector(0, 0, 1)
)

frontArrow = vp.arrow(
    length=4, shaftwidth=0.1, color=vp.color.purple, axis=vp.vector(1, 0, 0)
)
upArrow = vp.arrow(
    length=1, shaftwidth=0.1, color=vp.color.magenta, axis=vp.vector(0, 1, 0)
)
sideArrow = vp.arrow(
    length=2, shaftwidth=0.1, color=vp.color.orange, axis=vp.vector(0, 0, 1)
)
print("Hi 2")

bBoard = vp.box(
    length=6,
    width=2,
    height=0.2,
    opacity=0.8,
    pos=vp.vector(
        0,
        0,
        0,
    ),
)

bn = vp.box(
    length=1,
    width=0.75,
    height=0.1,
    pos=vp.vector(-0.5, 0.1 + 0.05, 0),
    color=vp.color.blue,
)
nano = vp.box(
    lenght=1.75,
    width=0.6,
    height=0.1,
    pos=vp.vector(-2, 0.1 + 0.05, 0),
    color=vp.color.green,
)
myObj = vp.compound([bBoard, bn, nano])
print("Hi 2")


print("Im here")
worker = RedisWorker()

for message in worker.subscribe_grouped(
    block=1, count=1000000, dataClass=Quaternion, channel=raw_to_quaternion_channel
):
    # assert message is Quaternion
    if message is not None:
        try:
            roll, pitch, yaw = quat2eulers(
                message.q0, message.q1, message.q2, message.q3
            )
            k = vp.vector(
                vp.cos(yaw) * vp.cos(pitch), vp.sin(pitch), vp.sin(yaw) * vp.cos(pitch)
            )
            y = vp.vector(0, 1, 0)
            s = vp.cross(k, y)
            v = vp.cross(s, k)

            frontArrow.axis = k
            sideArrow.axis = s
            upArrow.axis = v
            myObj.axis = k
            myObj.up = v
            # sideArrow.length = 2
            # frontArrow.length = 4
            # upArrow.length = 1

        except Exception as e:
            error_message = LogMessage(
                date=datetime.datetime.now(),
                process_name="visualize_roll_pitch_yaw",
                status=LogMessage.exception_to_dict(e),
            )
            worker.broker.publish(
                log_message_channel, json.dumps(error_message.to_dict())
            )
