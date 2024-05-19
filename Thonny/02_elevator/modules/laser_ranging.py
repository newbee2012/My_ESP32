from machine import I2C, Pin, SoftI2C
import utime,time
from libs.vl53l0x import VL53L0X
import math
from log import logger
class LaserRanging:
    def __init__(self, irq=9, scl=5, sda=4, freq=100000):
        self.value = -1
        self.sensor = VL53L0X(SoftI2C(scl=Pin(scl), sda=Pin(sda), freq=freq))
        gpio1 = Pin(irq, Pin.IN)
        gpio1.irq(trigger=Pin.IRQ_FALLING, handler=self.handle_interrupt)
        self.received_new_data = False  

    def handle_interrupt(self, pin):
        self.received_new_data = True
    
    def read(self):
        if self.received_new_data:
            self.received_new_data = False
            self.value = self.sensor.read()
        return self.value
    
    def start(self):
        self.sensor.start()
        time.sleep_ms(500)
        logger.info("VL53L0X is ON")
        
        
        

