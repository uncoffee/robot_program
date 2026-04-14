import ntptime
import machine
import time
from . import logging

ntptime.host = "ntp.nict.jp"


class Time:
    __epoch = 0
    year = 1970
    month = 12
    date = 31
    hour = 23
    minute = 58
    second = 59

    def __init__(self, epoch):
        self.set(epoch)

    def __str__(self):
        return "{:04d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(
            self.year, self.month, self.date, self.hour, self.minute, self.second
        )

    def set(self, epoch):
        self.__epoch = epoch
        now = time.gmtime(epoch)  # type: ignore
        self.year = now[0]
        self.month = now[1]
        self.date = now[2]
        self.hour = now[3]
        self.minute = now[4]
        self.second = now[5]

    def add(self, second):
        self.set(self.__epoch + second)

def init():
    try:
        ntptime.settime()
    except Exception as e:
        logging.error(e)


def get():
    t = Time(time.time() + 9 * 60 * 60)
    return t


def sleep(sec):
    time.sleep(sec)


def deepsleep(sec):
    machine.deepsleep(int(sec * 1000))
