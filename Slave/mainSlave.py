### main.py
import utime
import time
from machine import mem32,Pin
import Slave.led as led
from Slave.i2cSlave import i2c_slave

import kikupico

### --- check pico power on --- ###
led.led_power_on(5)

class kansui:
    def __init__(self):
        self.s_i2c = i2c_slave(0,sda=0,scl=1,slaveAddress=0x41) #i2c通信できるようにインスタンス化する
        self.reco = None #受信内容(0)
        self.send = None #返信内容(1)
        self.run_time = 5

    def check(self):
        if self.s_i2c.any():
            get = self.s_i2c.get()
            led.led_power_on(len(get))#受信したbit分光る。
            if get == 0x1:
                self.motor()

            if get == 0x2:
                self.wet()

        if self.s_i2c.anyRead():
            self.s_i2c.put(self.send & 0xff)
            self.send = None
    
    def motor(self):
        kikupico.equipment.motor.run(self.run_time)

    def wet(self):
        self.send = kikupico.sensor.soil.get()