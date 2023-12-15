from config import stop_all_threads
from machine import Pin, Timer
import time,math
import _thread

DEBOUNCE_TIME = 10  # milliseconds
class RF433Receiver():
    def __init__(self):
        # 计数器和时间间隔
        self.value1 = 0.0
        self.value2 = 0.0
        self.counter1 = 0
        self.counter2 = 0
        self.last_time = 0
        self.last_interrupt_time1 = 0
        self.last_interrupt_time2 = 0
        # 初始化RF接收模块连接的GPIO为输入
        self.rx_pin1 = Pin(35, Pin.IN)
        self.rx_pin2 = Pin(33, Pin.IN)
        # 初始化GPIO引脚
        self.tx_pin = Pin(32, Pin.OUT)
        # 初始化定时器
        self.timer = Timer(0)
        self.timer.init(period=1000, mode=Timer.PERIODIC, callback=self.calculate_frequency)
        # 将ISR绑定到rf433_pin
        self.rx_pin1.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.pulse_detected_1)
        self.rx_pin2.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.pulse_detected_2)

        #thread_tx = _thread.start_new_thread(self.send_signal, ())
        
    def send_signal(self):
        global stop_all_threads
        while stop_all_threads == False :
            self.tx_pin.value(1)  # 逻辑高电平
            time.sleep_ms(200)
            self.tx_pin.value(0)  # 逻辑高电平
            time.sleep_ms(200)

    # 定义回调函数和定时器
    def calculate_frequency(self,timer):
        current_time = time.ticks_ms()
        time_difference = time.ticks_diff(current_time, self.last_time)
        frequency1 = (self.counter1 / time_difference) * 1000  # 换算成每秒
        frequency2 = (self.counter2 / time_difference) * 1000  # 换算成每秒
        print("Frequency: {} Hz, {} Hz".format(frequency1, frequency2))
        self.last_time = current_time
        self.counter1 = 0
        self.counter2 = 0

    # 定义中断服务程序（ISR）
    def pulse_detected_1(self, pin):
        current_time = time.ticks_ms()
        if current_time - self.last_interrupt_time1 >= DEBOUNCE_TIME:
            # 在此处处理接收到的数据
            self.last_interrupt_time1 = current_time
            self.value1 = pin.value()
            self.counter1 += 1
        
    # 定义中断服务程序（ISR）
    def pulse_detected_2(self, pin):
        current_time = time.ticks_ms()
        if current_time - self.last_interrupt_time2 >= DEBOUNCE_TIME:
            # 在此处处理接收到的数据
            self.last_interrupt_time2 = current_time
            self.value2 = pin.value()
            self.counter2 += 1

        
    def close(self):
        #self.rx_pin1 = Pin(33,Pin.OUT)
        #self.rx_pin2 = Pin(35,Pin.OUT)
        self.timer.deinit()
        
        


