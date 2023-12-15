from machine import Pin, SoftI2C, I2C
from libs.i2c_lcd import I2cLcd

class LCD1602:
    def __init__(self, sda = Pin(13), scl = Pin(14), freq = 100000):
        # 定义 SoftI2C 控制对象
        self.i2c = SoftI2C(sda = sda, scl = scl, freq = freq)
        # 获取 I2C 从机地址
        self.address = self.i2c.scan()[0]
        # 定义 I2CLCD 对象
        self.i2c_lcd = I2cLcd(self.i2c, self.address, 2, 16)
        print("LCD_1602 init finished.")
    
    def putstr(self, string, cursor_x = 0, cursor_y = 0, clear = False):
        if clear:
            self.i2c_lcd.clear()
        self.i2c_lcd.move_to(cursor_x, cursor_y)
        self.i2c_lcd.putstr(string)

