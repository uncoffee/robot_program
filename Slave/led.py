import utime
import time
from machine import Pin, Timer

led = Pin(25, Pin.OUT) #GP25を出力モードに設定

def led_power_on(count) :

    for i in range(count) :

        led.value(1)
        time.sleep(0.5)
        led.value(0)
        time.sleep(0.5)
        led.value(1)
        time.sleep(0.5)
        led.value(0)
        time.sleep(1.0)

def led_on() :
        led.value(1)

def led_off() :
        led.value(0)
