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
        self.set = None #受信内容(0)
        self.send = None #返信内容(1)
        self.run_time = 5
        self.wifi_info = {"ssid":None, "key": None}

    #命令を確認して実行
    def check(self):
        #聞き専
        if self.s_i2c.any():
            get = self.s_i2c.get()
            led.led_power_on(len(get))#受信したbit分光る。
            if not self.set == None:
                self.set = get
                pass

            #聞き専
            if get == 1:
                self.motor()

            if get == :
                self.set_wifi()

            if get == :
                self.on_wifi()

            if get == :
                self.off_wifi()

            #返信専
            if get == :
                self.wet()

            if get == :
                self.temp

        #返信の要求
        if self.s_i2c.anyRead():
            self.s_i2c.put(self.send & 0xff)
            self.send = None
    
    #実際のプログラム
    def motor(self):
        kikupico.equipment.motor.run(self.run_time)

    def wet(self):
        self.send = kikupico.sensor.soil.get()

    def temp(self):
        self.send = kikupico.sensor.temperature.get()

    def set_wifi(self):
        get = self.s_i2c.get()
        for i in range(get):
            
            

    def on_wifi(self):
        kikupico.wifi.connect(self.wifi_info["ssid"],self.wifi_info["key"])

    def off_wifi(self):
        kikupico.wifi.disconnect()
        