
import config
from machine import Pin, Timer
from modules.wifi import Wifi
from modules.umqttsimple import MQTTClient
from projects.elevator import Elevator
from projects.auto_sleeping_light import AutoSleepingLight
from machine import Pin, SPI, SoftI2C, I2C, SoftSPI
import time
import os
import machine
import utime
import _thread
import sys
import math
import ujson

class ESP32:
    def __init__(self):
        self.wifi = Wifi('Redmi_dj', 'xiaomi.com2014')
        #self.DigitalDisplay4 = DigitalDisplay4()
        #self.chatGPT = ChatGPT()
        #self.timer_irq()
        self.stop_thread = False
        
    def setup(self):
        self.wifi.connect()
#         self.DigitalDisplay4.self_check()
        print("当前时间:{}".format(self.get_current_time_tuple()))
#         self.sync_time_by_rtc()
#         print("当前时间:{}".format(self.get_current_time_tuple()))
        
    
    def sync_time_by_rtc(self):
        import ntptime
        ntptime.settime()
        
    def get_current_time_tuple(self):
        # 获取当前UTC时间
        current_utc_time = utime.time()

        # 东八区偏移量为8小时（8 * 3600秒）
        utc_offset = 8 * 3600

        # 计算东八区的本地时间
        eastern_time = current_utc_time + utc_offset

        # 将UTC时间转换为元组
        local_time_tuple = utime.localtime(eastern_time)
        return local_time_tuple
    
    # 定义定时器中断的回调函数
    def timer_irq(self, timer_pin = None):
        self.time_tuple = self.get_current_time_tuple()
        # 获取当前小时和分钟
        current_hour = self.time_tuple[3]
        current_minute = self.time_tuple[4]
        current_second = self.time_tuple[5]

        # 计算小时的十位和个位
        self.hour_tens = current_hour // 10
        self.hour_units = current_hour % 10

        # 计算分钟的十位和个位
        self.minute_tens = current_minute // 10
        self.minute_units = current_minute % 10
        
        # 计算分钟的十位和个位
        self.second_tens = current_second // 10
        self.second_units = current_second % 10

    def show_current_time(self):
        while not self.stop_thread:
            self.DigitalDisplay4.display_number(0,self.hour_tens)
            time.sleep_ms(4)
            self.DigitalDisplay4.display_number(1,self.hour_units)
            time.sleep_ms(4)
            self.DigitalDisplay4.display_number(2,self.minute_tens)
            time.sleep_ms(4)
            self.DigitalDisplay4.display_number(3,self.minute_units)
            time.sleep_ms(4)
        print("Thread 'show_current_time' ended.")

    def mqtt_handler(self, topic, msg): # 回调函数，收到服务器消息后会调用这个函数
        # 解码为字符串
        str_data = msg.decode('utf-8')
        # 替换非断空白符
        clean_data = str_data.replace(u'\xa0', ' ')
        json_data = ujson.loads(clean_data)
        print(f"MQTT recv data:\n{json_data}")
        #LD2410.MOTION_ENERGY_COUNTER_MAX = json_data["MOTION_ENERGY_COUNTER_MAX"]
        #LD2410.MOTION_ENERGY_DECAY_RATE = json_data["MOTION_ENERGY_DECAY_RATE"]
    
    def testMqtt(self):
        # 2. 创建mqt
        c = MQTTClient("umqtt_client", "43.128.18.55")  # 建立一个MQTT客户端
        c.set_callback(self.mqtt_handler)  # 设置回调函数
        c.connect()  # 建立连接
        c.subscribe(b"ledctl")  # 监控ledctl这个通道，接收控制命令
        while not stop_all_threads:
            c.check_msg()
            time.sleep(1)
                        

if __name__ == '__main__':
    myEsp32 = ESP32()
    myEsp32.setup()
#     # 创建并启动新线程
#     thread_id = _thread.start_new_thread(myEsp32.show_current_time, ())
#     # 定义定时器
#     timer = Timer(0)
#     # 初始化定时器
#     timer.init(period=1000, mode=Timer.PERIODIC, callback=myEsp32.timer_irq)

    #elevator = Elevator()
    #elevator_thread = _thread.start_new_thread(elevator.run, ())
    
    #mqtt_thread = _thread.start_new_thread(myEsp32.testMqtt, ())
    autoSleepingLight = AutoSleepingLight()
    autoSleepingLight.run()
    try:
        while True:
            time.sleep_ms(500)
    except KeyboardInterrupt:
        print("Ctrl+C received. Stopping main thread.")
    config.stop_all_threads = True
    #等待子线程退出
    time.sleep_ms(1000)
    
    

        
        


    
    
