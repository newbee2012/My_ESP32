import config
from machine import Pin, ADC
from modules.umqttsimple import MQTTClient
from log import logger
import time
import json
from modules.my_time import *
class AutoWateringFlowers():
    def __init__(self):
        self.mqtt_client = MQTTClient("umqtt_client", "43.128.18.55")  # 建立一个MQTT客户端
        self.mqtt_client.set_callback(self.mqtt_handler)  # 设置回调函数
        self.mqtt_client.connect()
        self.mqtt_client.subscribe(b"awf_cmd")
        self.adc = ADC(Pin(2),atten=ADC.ATTN_11DB)
        self.pinOnOff = Pin(6 , Pin.OUT, Pin.PULL_UP)
        self.pinOnOff.value(1)
        
    def mqtt_handler(self, topic, msg): # 回调函数，收到服务器消息后会调用这个函数
        # 解码为字符串
        str_data = msg.decode('utf-8')
        # 替换非断空白符
        clean_data = str_data.replace(u'\xa0', ' ')
        json_data = json.loads(clean_data)
        logger.info(f"MQTT recv data:\n{json_data}")
        cmd = json_data['cmd']
        data = {
            "type":cmd,
            "result":""
        }
        
        if cmd == 'query':
            moisture = self.querySoilMoisture()
            logger.info(f"query current soil moisture:{moisture}")
            data['result'] = moisture
            data['time'] = f"{get_current_date()} {get_current_time()}"
            self.mqtt_client.publish(b"awf_data",json.dumps(data))
        elif cmd == 'watering':
            second = json_data['second']
            ts = 0
            self.startWatering()
            logger.info(f"Start watering...{second} seconds")
            data['result'] = "start"
            data['time'] = f"{get_current_date()} {get_current_time()}"
            self.mqtt_client.publish(b"awf_data",json.dumps(data))
            while ts < second:
                time.sleep(1)
                ts = ts + 1
            self.stopWatering()
            logger.info(f"Stop watering...")
            data['result'] = "stop"
            data['time'] = f"{get_current_date()} {get_current_time()}"
            self.mqtt_client.publish(b"awf_data",json.dumps(data))
            
    
    def querySoilMoisture(self):
        return self.adc.read() / 4095

    def startWatering(self):
        self.pinOnOff.value(0)
        
    def stopWatering(self):
        self.pinOnOff.value(1)
        
    def run(self):
        while not config.stop_all_threads:
            self.mqtt_client.check_msg()
            moisture = self.adc.read() / 4095
            logger.info(f"query current soil moisture:{moisture}")
            time.sleep_ms(500)
            
            
            
