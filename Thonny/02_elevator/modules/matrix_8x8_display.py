import utime
from libs.max7219 import Matrix8x8
import framebuf

font_4x8 = {
    '10': bytearray([
        0b01001110,
        0b11010001,
        0b01010001,
        0b01010001,
        0b01010001,
        0b01010001,
        0b01001110,
        0b00000000]),
    '11': bytearray([
        0b01000100,
        0b11001100,
        0b01000100,
        0b01000100,
        0b01000100,
        0b01000100,
        0b01000100,
        0b00000000]),
    '12': bytearray([
        0b01001110,
        0b11010001,
        0b01000001,
        0b01000010,
        0b01000100,
        0b01001000,
        0b01011111,
        0b00000000]),
    '13': bytearray([
        0b01011111,
        0b11000010,
        0b01000100,
        0b01000010,
        0b01000001,
        0b01010001,
        0b01001110,
        0b00000000]),
    '14': bytearray([
        0b01000010,
        0b11000110,
        0b01001010,
        0b01010010,
        0b01011111,
        0b01000010,
        0b01000010,
        0b00000000]),
    '15': bytearray([
        0b01011111,
        0b11010000,
        0b01011110,
        0b01000001,
        0b01000001,
        0b01010001,
        0b01001110,
        0b00000000]),
    '16': bytearray([
        0b01000110,
        0b11001000,
        0b01010000,
        0b01011110,
        0b01010001,
        0b01010001,
        0b01001110,
        0b00000000]),
}


class Matrix8x8Display(Matrix8x8):  # 扩展原始的 Matrix8x8 类
    UP = 0
    DOWN = 7
    # 创建一个简单的字体（这里只创建了0-9）
    
    
    def show_text(self, string, x, y):
        self.text(string, x, y)
        self.show()
    
    def draw_digit_4x8(self, digit, x_offset=0):
        
        self.blit(fb, 0, x_offset)

    def draw_two_digits_4x8(self, number):
        fb = framebuf.FrameBuffer(font_4x8[str(number)], 8, 8, framebuf.MONO_HLSB)
        
        self.blit(fb, 0, 0)

        self.show()  # 更新显示
         
    def move_arrow(self, mode = UP, x = 0, delay=200):
        # 定义箭头"->"的位图
        arrow = [
                0b00010000,
                0b00111000,
                0b01010100,
                0b10010010,
                0b00010000,
                0b00010000,
                0b00010000,
                0b00000000,
            ]
        # 从最右侧开始显示箭头，并逐列向左移动
        self.fill(0)  # 清除屏幕
        for col in range(len(arrow)):
            # 使用取模运算来实现箭头的环形移动
            position = (col + x) % 10
            if position >= len(arrow):
                continue 
            buffer_col = abs(mode - col)
            self.buffer[buffer_col] = arrow[position]
        self.show()  # 更新显示
        utime.sleep_ms(delay)  # 等待一段时间后再移动




