import urequests
import ujson
import random
import utime
class ChatGPT:
    def __init__(self):
        self.url = "http://43.128.18.55/esp32"
        
    def generate_random_id(self):
        return 12345678

    def send_msg(self, msg: str):
        headers = {"Content-Type":"application/json; charset=UTF-8"}
        # 获取当前时间戳（以秒为单位）
        timestamp = utime.time()
        msg_id = self.generate_random_id()
        data = {
            "type": "text",
            "Content": msg,
            "FromUserName": "aaa",
            "ToUserName": "bbb",
            "MsgId": self.generate_random_id(),
            "CreateTime": utime.time()
        }
        
        response = urequests.post(self.url, data=ujson.dumps(data).encode('utf-8'), headers=headers)
        #response.close()
        print(response.text)
        return response.text

