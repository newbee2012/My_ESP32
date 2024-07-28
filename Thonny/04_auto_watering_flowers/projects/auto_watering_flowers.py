import config
from machine import Pin, ADC, Timer
from modules.umqttsimple import MQTTClient
from log import logger
import time
import json
from modules.my_time import *

class AutoWateringFlowers():
    def __init__(self):
        self.device_id = "2"
        self.mqtt_topic_cmd = f"awf_cmd_{self.device_id}"
        print(self.mqtt_topic_cmd)
        self.mqtt_topic_data = f"awf_data_{self.device_id}"
        self.mqtt_client = MQTTClient(f"esp32-c3-{self.device_id}", "43.130.239.227", keepalive=600)  # 建立一个MQTT客户端
        self.mqtt_client.set_callback(self.mqtt_handler)  # 设置回调函数
        self._mqtt_connect()
        self.adc = ADC(Pin(2),atten=ADC.ATTN_11DB)
        self.pinOnOff = Pin(6 , Pin.OUT, value = 0)
        # 定义定时器
        self.timer = Timer(0)
        # 初始化定时器
        self.timer.init(period=60000, mode=Timer.PERIODIC, callback=self.timer_irq)

    def _mqtt_connect(self):
        try:
            if self.mqtt_client.connect() == 0:
                logger.info(f"Successfully connected to MQTT server!")
                self.mqtt_client.subscribe(self.mqtt_topic_cmd.encode('utf-8'))
                return 0
            else:
                logger.info("Connected to MQTT server failed!")
                return -1
        except Exception as e:
            logger.info(f"Connected to MQTT server exception! {e}")
        return -1

    def _mqtt_reconnect(self):
        while not config.stop_all_threads:
            try:
                if self._mqtt_connect() == 0:
                    return
            except OSError as e:
                logger.info(f"MQTT reconnect error! {e}")
            time.sleep_ms(5000)
        
    def timer_irq(self, timer_pin = None):
        try:
            self.mqtt_client.ping()
            logger.info("mqtt send PINGREQ")
        except Exception as e:
            logger.info(f"Ping MQTT server exception! {e}!Try reconnecting after 5 seconds!")
            time.sleep_ms(5000)
            self._mqtt_reconnect()
    
    def mqtt_pushlish(self, data):
        self.mqtt_client.publish(self.mqtt_topic_data.encode('utf-8'), data)
        
    def mqtt_handler(self, topic, msg): # 回调函数，收到服务器消息后会调用这个函数
        # 解码为字符串
        str_data = msg.decode('utf-8')
        # 替换非断空白符
        clean_data = str_data.replace(u'\xa0', ' ')
        json_data = json.loads(clean_data)
        logger.info(f"MQTT recv data:\n{json_data}")
        cmd = json_data['cmd']
        data = {
            "deivce_id":self.device_id,
            "type":cmd,
            "result":""
        }
        
        if cmd == 'query':
            moisture = self.querySoilMoisture()
            logger.info(f"query current soil moisture:{moisture}")
            data['result'] = moisture
            data['time'] = f"{get_current_date()} {get_current_time()}"
            self.mqtt_pushlish(json.dumps(data))
        elif cmd == 'watering':
            second = json_data['second']
            ts = 0
            self.startWatering()
            logger.info(f"Start watering...{second} seconds")
            data['result'] = "start"
            data['time'] = f"{get_current_date()} {get_current_time()}"
            self.mqtt_pushlish(json.dumps(data))
            while ts < second:
                time.sleep(1)
                ts = ts + 1
            self.stopWatering()
            logger.info(f"Stop watering...")
            data['result'] = "stop"
            data['time'] = f"{get_current_date()} {get_current_time()}"
            self.mqtt_pushlish(json.dumps(data))
            
    
    def querySoilMoisture(self):
        min = 1300
        max = 4095
        read_value =  self.adc.read()
        if read_value < min:
            read_value = min
        return  1 - (read_value - min) / (max - min)

    def startWatering(self):
        self.pinOnOff.value(1)
        
    def stopWatering(self):
        self.pinOnOff.value(0)
        
    def run(self):
        while not config.stop_all_threads:
            try:
                self.mqtt_client.check_msg()
                time.sleep_ms(500)
            except Exception as e:
                logger.info(f"AutoWateringFlowers run() catch a exception {e}! Try reconnecting after 5 seconds!")
                time.sleep_ms(5000)
                self._mqtt_reconnect()
        
        self.timer.deinit()
        self.mqtt_client.disconnect()
        
            
            
            
