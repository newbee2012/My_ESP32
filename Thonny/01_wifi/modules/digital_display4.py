#四位数码管

import time
from machine import Pin

# 定义位选线对象
seg_1 = Pin(5, Pin.OUT)
seg_2 = Pin(18, Pin.OUT)
seg_3 = Pin(19, Pin.OUT)
seg_4 = Pin(21, Pin.OUT)

# 定义位选线列表
seg_list = [seg_1, seg_2, seg_3, seg_4]

# 定义段选线对象
a = Pin(32, Pin.OUT)
b = Pin(25, Pin.OUT)
c = Pin(27, Pin.OUT)
d = Pin(12, Pin.OUT)
e = Pin(13, Pin.OUT)
f = Pin(33, Pin.OUT)
g = Pin(26, Pin.OUT)
dp = Pin(14, Pin.OUT)

# 定义段选线对象
led_list = [a, b, c, d, e, f, g, dp]

number_dict = {
    #  [a, b, c, d, e, f, g, dp]
    0: [1, 1, 1, 1, 1, 1, 0, 0],
    1: [0, 1, 1, 0, 0, 0, 0, 0],
    2: [1, 1, 0, 1, 1, 0, 1, 0],
    3: [1, 1, 1, 1, 0, 0, 1, 0],
    4: [0, 1, 1, 0, 0, 1, 1, 0],
    5: [1, 0, 1, 1, 0, 1, 1, 0],
    6: [1, 0, 1, 1, 1, 1, 1, 0],
    7: [1, 1, 1, 0, 0, 0, 0, 0],
    8: [1, 1, 1, 1, 1, 1, 1, 0],
    9: [1, 1, 1, 1, 0, 1, 1, 0],
    ".":[0, 0, 0, 0, 0, 0, 0, 1],
    }

class DigitalDisplay4:
    def __init__(self):
        self.clear()

    # 清空位选线函数
    def __clear_seg(self):
        # 清空所有的位选线，将所有位选线设置为高电平
        for seg in seg_list:
            seg.off()

    # 清空段选线函数
    def __clear_led(self):
        # 清空所有的段选线，将所有段选线设置为低电平
        for led in led_list:
            led.on()

    # 清屏函数
    def clear(self):
        self.__clear_seg()
        self.__clear_led()
        
    def self_check(self):
        # 按顺序让所有位置显示0~9
        for i in range(4):
            for j in range(10):
                self.display_number(i, j)
                time.sleep(0.05)
        self.clear()

    # 显示数字的函数
    def display_number(self, order, number):
        # 逻辑电平列表
        logic_list = number_dict.get(number)

        if logic_list and 0 <= order < 4:
            # 清屏
            self.clear()
            # 指定要显示的位置，把电平拉低
            seg_list[order].on()
            # 显示数字
            for i in range(len(logic_list)):
                led_list[i].value(1-logic_list[i])


    


