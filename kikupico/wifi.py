import network
import machine
from . import led
from . import logging

ssid = ""
key = ""

nic = network.WLAN(network.STA_IF)
wifipin = machine.Pin(23, machine.Pin.OUT)

__limit = 10

def connect():
    try:
        wifipin.high()
        nic.active(True)
        nic.connect(ssid, key)
        for i in range(__limit):
            led.tick(1, 0.5)
            if nic.status() != network.STAT_CONNECTING:
                break
    except Exception as e:
        logging.error(e)

def disconnect():
    try:
        nic.disconnect()
        nic.active(False)
        wifipin.low()
    except Exception as e:
        logging.error(e)
