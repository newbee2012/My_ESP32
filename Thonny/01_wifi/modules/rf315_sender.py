from config import stop_all_threads
from machine import Pin, Timer
import time,math
import _thread
from log import logger
protocol = {
    "pulseLength": 350,
    "syncFactor": (1, 31),
    "zero": (1, 3),
    "one": (3, 1),
    "invertedSignal": False
}

class RF315Sender():
    def __init__(self):
        self.tx_pin = Pin(4, Pin.OUT, Pin.PULL_DOWN)
    
    def send_pulse(self, high, low):
        self.tx_pin.value(1 if not protocol["invertedSignal"] else 0)
        time.sleep_us(protocol["pulseLength"] * high)
        self.tx_pin.value(0 if not protocol["invertedSignal"] else 1)
        time.sleep_us(protocol["pulseLength"] * low)
        
    def send_signal(self, data, repeat = 1, interval_ms = 0, group = 1, group_interval_ms = 0):
        # Send data
        for g in range(group):
            for i in range(repeat):
                for bit in data:
                    if bit == '0':
                        self.send_pulse(protocol["zero"][0], protocol["zero"][1])
                    else:
                        self.send_pulse(protocol["one"][0], protocol["one"][1])
                # Send sync
                self.send_pulse(protocol["syncFactor"][0], protocol["syncFactor"][1])
                self.tx_pin.value(0)
                logger.debug(f"send group({g}) signal:{data}")
                if interval_ms > 0:
                    time.sleep_ms(interval_ms)
            if group_interval_ms > 0:
                time.sleep_ms(group_interval_ms)          

        
        



