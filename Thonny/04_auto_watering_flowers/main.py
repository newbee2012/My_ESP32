import config
from machine import Pin, Timer
from modules.wifi import Wifi
from modules.umqttsimple import MQTTClient
from projects.auto_watering_flowers import AutoWateringFlowers
from machine import Pin, SPI, SoftI2C, I2C, SoftSPI
import time
import os
import machine
import utime
import _thread
import sys
import math
import ujson
from modules.my_time import *

class ESP32:
    def __init__(self):
        self.wifi = Wifi('Redmi_dj', 'xiaomi.com2014')
        self.stop_thread = False
    def setup(self):
        self.wifi.connect()
        thread_id = _thread.start_new_thread(self.wifi.checkAndKeepConnect, ())
        #sync_time_by_rtc()
        #print("正在同步时间...")
        print(f"当前时间:{get_current_date()} {get_current_time()}")

if __name__ == '__main__':
    myEsp32 = ESP32()
    myEsp32.setup()
    autoWateringFlowers = AutoWateringFlowers()
    autoWateringFlowers_thread = _thread.start_new_thread(autoWateringFlowers.run, ())
    try:
        while True:
            time.sleep_ms(500)
    except KeyboardInterrupt:
        print("Ctrl+C received. Stopping main thread.")
    config.stop_all_threads = True
    #等待子线程退出
    time.sleep_ms(1000)
    
    

        
        


    
    
