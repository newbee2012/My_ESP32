from machine import Pin, Timer
from modules.laser_ranging import LaserRanging
from modules.matrix_8x8_display import Matrix8x8Display
from modules.on_off_4x4 import OnOff4x4
from modules.motor_driver import Motor
from machine import Pin, SPI, SoftI2C, I2C, SoftSPI
import time
import os
import machine
import utime
import _thread
import sys
import math
from log import logger

class Elevator():
    def __init__(self):
        self.stop_thread = False
        self.matrix_4x4_press_key = 1.0
        self.target_floor = self.matrix_4x4_press_key
        self.floor = self.target_floor
        self.allowable_floor_error = 0.1
        self.distance = 0
        self.press_key_event = False
        #self.lcd1602 = LCD1602(sda = Pin(13), scl = Pin(14), freq = 400000)
        
    def __vl53l0x_thread(self):
        try:
            laser = LaserRanging(irq=9, scl=5, sda=4, freq=100000)
            laser.start()
            self.distance = laser.read()
            self.floor = self.__get_current_floor(self.distance)
            self.target_floor = self.floor
            self.matrix_4x4_press_key = self.target_floor
            self.allowable_floor_error = 0.05
            logger.info(f"distance:{self.distance},floor:{self.floor}")
            while not self.stop_thread:
                self.distance = laser.read()
                logger.debug("{:>4}mm".format(self.distance))
                self.floor = self.__get_current_floor(self.distance)
                time.sleep_ms(100)
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt (Ctrl+C) received.")
        except Exception as e:
            time.sleep_ms(2000)
        self.stop_thread = True
        
            
    def __matrix_8x8_display_thread(self):
        spi = SoftSPI(sck=Pin(2), mosi=Pin(10), miso = Pin(11))
        cs = Pin(7, Pin.OUT)
        matrix8x8 = Matrix8x8Display(spi, cs, 1)
        matrix8x8.fill(0)
        matrix8x8.show_text(str(math.floor(self.floor + 0.5)),0,1)
        old_key = self.matrix_4x4_press_key
        while not self.stop_thread:
            if self.__is_target_floor_arrived() == False and self.matrix_4x4_press_key != old_key:
                old_key = self.matrix_4x4_press_key
                step = 0
                while not self.stop_thread and self.__is_target_floor_arrived() == False:
                    if self.floor < self.target_floor:
                        matrix8x8.move_arrow(mode = Matrix8x8Display.UP, x = step, delay=200)
                    elif self.floor > self.target_floor:
                        matrix8x8.move_arrow(mode = Matrix8x8Display.DOWN, x = step, delay=200)
                    step += 1
                matrix8x8.fill(0)
                if self.floor < 10:
                    matrix8x8.show_text(str(self.target_floor),0,1)
                else:
                    matrix8x8.draw_two_digits_4x8(self.target_floor)    
            time.sleep_ms(500)
         
    def __on_off_4x4_thread(self):
        onOff4x4 = OnOff4x4()
        while not self.stop_thread:
            key = onOff4x4.read_keypad()
            if key is not None and key <= 6:
                self.matrix_4x4_press_key = key
                self.target_floor = self.matrix_4x4_press_key
                self.press_key_event = True 
                logger.debug(f"Press key:{self.matrix_4x4_press_key}")
            time.sleep_ms(200)

    def __get_current_floor(self, height):
        floor_height=[45,91,180,269,345,425]
        if height < floor_height[0]:
            return 1
        if height > floor_height[5]:
            return 6
        
        for i, h in enumerate(floor_height):
            if h >= height:
                return (height - floor_height[i-1]) / (h - floor_height[i-1]) + i

    def __is_target_floor_arrived(self):
        return abs(self.floor - self.target_floor) <= self.allowable_floor_error
        
    def __motor_control_thread(self):
        motor = Motor()
        while not self.stop_thread:
            if self.__is_target_floor_arrived() == False and self.press_key_event == True:
                while not self.stop_thread and self.__is_target_floor_arrived() == False:
                    if self.target_floor != self.matrix_4x4_press_key:
                        self.target_floor = self.matrix_4x4_press_key
                    if self.floor < self.target_floor:
                        if motor.status() != Motor.FOREWARD:
                            motor.rotate_foreward()
                    elif self.floor > self.target_floor:
                        if motor.status() != Motor.REVERSELY:
                            motor.rotate_reversely()
                    time.sleep_ms(100)
                if self.target_floor == 1:
                    time.sleep_ms(800)
                        
                motor.brake()
                self.press_key_event = False 
            time.sleep_ms(500)
            
    def run(self):
        thread_vl53l0x = _thread.start_new_thread(self.__vl53l0x_thread, ())
        time.sleep_ms(1000)
        thread_matrix4x4_onoff = _thread.start_new_thread(self.__on_off_4x4_thread, ())
        thread_max7219 = _thread.start_new_thread(self.__matrix_8x8_display_thread, ())
        thread_motor_control = _thread.start_new_thread(self.__motor_control_thread, ())
        
        

