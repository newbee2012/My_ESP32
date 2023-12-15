from machine import Pin, PWM
import utime

class Motor():
    STOPED = 0
    FOREWARD = 1
    REVERSELY = 2
    BREAKING= 3

    def __init__(self, pin_a1 = Pin(21, Pin.OUT), pin_a2 = Pin(22, Pin.OUT)):
        self.pin_a1 = pin_a1
        self.pin_a2 = pin_a2
        self.pin_a1.value(0)
        self.pin_a2.value(0)

    def status(self):
        if self.pin_a1.value() == 1 and self.pin_a2.value() == 0:
            return Motor.FOREWARD
        elif self.pin_a1.value() == 0 and self.pin_a2.value() == 1:
            return Motor.REVERSELY
        elif self.pin_a1.value() == 1 and self.pin_a2.value() == 1:
            return Motor.BREAKING
        elif self.pin_a1.value() == 0 and self.pin_a2.value() == 0:
            return Motor.STOPED
        
    
    def rotate_foreward(self):
        if self.status() != Motor.FOREWARD:
            if self.status() == Motor.REVERSELY:
                self.stop()
                utime.sleep_ms(200)
            self.pin_a1.value(1)
            self.pin_a2.value(0)
            print("电机正转")
        
    def rotate_reversely(self):
        if self.status() != Motor.REVERSELY:
            if self.status() == Motor.FOREWARD:
                self.stop()
                utime.sleep_ms(200)
            self.pin_a1.value(0)
            self.pin_a2.value(1)
            print("电机反转")
        
    def brake(self):
        if self.status() == Motor.FOREWARD or self.status() == Motor.REVERSELY:
            self.pin_a1.value(1)
            self.pin_a2.value(1)
            print("电机刹车")
        
    def stop(self):
        if self.status() != Motor.STOPED:
            self.pin_a1.value(0)
            self.pin_a2.value(0)
            print("电机停止")
        
        
        
    
