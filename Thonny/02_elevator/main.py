import config
from machine import Pin, Timer
from projects.elevator import Elevator
from machine import Pin, SPI, SoftI2C, I2C, SoftSPI
import time
import os
import machine
import utime
import _thread

class ESP32:
    def __init__(self):
        self.stop_thread = False


if __name__ == '__main__':
    myEsp32 = ESP32()
    elevator = Elevator()
    elevator_thread = _thread.start_new_thread(elevator.run, ())
    try:
        while True:
            time.sleep_ms(500)
    except KeyboardInterrupt:
        print("Ctrl+C received. Stopping main thread.")
    config.stop_all_threads = True
    #等待子线程退出
    time.sleep_ms(1000)
    
    

        
        


    
    
