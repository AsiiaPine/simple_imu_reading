from dataclasses import dataclass
from typing import Any, Dict
import numpy as np
from datetime import datetime
import abc
import traceback


class Message(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> None:
        pass

    @abc.abstractmethod
    def to_dict(self) -> dict:
        pass


@dataclass
class IMUData:
    acc: np.ndarray
    gyr: np.ndarray


@dataclass
class IMU9250Data(IMUData):
    mag: np.ndarray


@dataclass
class IMUMessage(Message):
    imu: IMUData

    @classmethod
    def from_dict(cls, data: dict[str, float]):
        """
        Deserialize message from JSON received from redis.
        """

        imu = IMUData(acc=np.array(data["acc"]), gyr=np.array(data["gyr"]))
        return cls(imu=imu)

    def to_dict(self):
        data = {}

        data["acc"] = self.imu.acc
        data["gyr"] = self.imu.gyr

        return data


@dataclass
class IMU9250Message(IMUMessage):
    imu: IMU9250Data

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        """
        Deserialize message from JSON received from redis.
        """

        imu = IMU9250Data(
            acc=np.array(data["acc"]),
            gyr=np.array(data["gyr"]),
            mag=np.array(data["mag"]),
        )
        return cls(imu=imu)

    def to_dict(self):
        data = {}
        data["acc"] = self.imu.acc
        data["gyr"] = self.imu.gyr
        data["mag"] = self.imu.mag
        return data



def dump_clean(obj, s="") -> str:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                s += '\n' + k + ':\n'
                s = dump_clean(v, s)
            else:
                s += '%s : %s' % (k, v) + '\n'
    elif isinstance(obj, list):
        for v in obj:
            if hasattr(v, '__iter__'):
                s = dump_clean(v, s)
            else:
                s += v + '\n'
    else:
        s += obj + '\n'
    return s


@dataclass
class LogMessage(Message):
    date: datetime
    process_name: str
    status: dict[str, Any]

    date_format = '%m/%d/%Y\t%H:%M:%S'

    @staticmethod
    def exception_to_dict(exception: Exception) -> dict[str, Any]:
        exception_dict = {
            'type': type(exception).__name__,
            'message': str(exception),
            'args': str(exception.args),
            'traceback': traceback.format_exc()
        }
        return exception_dict

    @classmethod
    def from_dict(cls, data: dict[str, str | dict]):
        assert isinstance(data["process"], str)
        assert isinstance(data["date"], str)
        assert isinstance(data["status"], dict)

        process_name = data["process"]
        date_str_de_DE: str = data["date"]

        date: datetime = datetime.strptime(date_str_de_DE, cls.date_format)
        status: dict = data["status"]
        return cls(date=date, process_name=process_name, status=status)

    def to_dict(self) -> dict:
        data: dict[str, Any] = {}
        data["date"] = datetime.strftime(self.date, self.date_format)
        data["process"] = self.process_name
        data["status"] = self.status
        return data

    def __str__(self) -> str:
        return f'{self.date}\t{self.process_name}' + dump_clean(self.status)
