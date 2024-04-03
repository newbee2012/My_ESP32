import utime
from machine import Pin

class OnOff4x4():
    def __init__(self,
                 row_pins_id = [1,0],
                 col_pins_id = [12,18,19,13]):
        self.row_pins = [Pin(id, Pin.IN, Pin.PULL_UP) for id in row_pins_id]
        self.col_pins = [Pin(id, Pin.OUT) for id in col_pins_id]

    def read_keypad(self):
        keys = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16]
        ]

        for j, col_pin in enumerate(self.col_pins):
            col_pin.value(0)  # 将当前列设置为低电平
            for i, row_pin in enumerate(self.row_pins):
                if row_pin.value() == 0:  # 检测行引脚的状态
                    while row_pin.value() == 0: #等待按键松开
                        utime.sleep_ms(10)
                    return keys[i][j]  # 返回按下的按键
            col_pin.value(1)  # 将当前列恢复为高电平

        return None  # 没有按键被按下

        

