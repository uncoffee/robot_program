import machine
from . import clock

led = machine.Pin("LED", machine.Pin.OUT)


def on():
    led.high()


def off():
    led.low()


def tick(count=1, sec=0.3):
    for i in range(count):
        led.high()
        clock.sleep(sec)
        led.low()
        clock.sleep(sec)
