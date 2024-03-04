import network
from machine import Pin, PWM
import time
class Wifi:
    def __init__(self, ssid: str, password: str):
        self.wlan = network.WLAN(network.STA_IF)
        self.ssid = ssid
        self.password = password
        self.led2 = PWM(Pin(13))
        self.led2.freq(10000)
        
    def led2_blink(self, ms = 1000):
        for i in range(0, ms + 1):
            self.led2.duty(i)
            time.sleep_ms(1)
        for i in range(ms, -1, -1):
            self.led2.duty(i)
            time.sleep_ms(1)
        
    def connect(self):
        print("self.wlan.isconnected() = {}".format(self.wlan.isconnected()))
        if not self.wlan.isconnected():
            if not self.wlan.active():
                self.wlan.active(True)
            print('connecting to network...')
            self.wlan.connect(self.ssid, self.password)
            timeout = 20
            t = 0
            while not self.wlan.isconnected():
                if t >= timeout:
                    print("Connect network timeout!")
                    break
                if self.wlan.isconnected():
                    break
                self.led2_blink(500)
                t = t + 1
                pass
            if self.wlan.isconnected():
                print("Successfully connected to the network!")
            else:
                print("Failed to connect to the network!")
        print('network config:', self.wlan.ifconfig())
        self.led2.deinit()
        
    def disconnect(self):
        if self.wlan.isconnected():
            print('Disconnecting network...')
            self.wlan.disconnect()
            timeout = 20
            t = 0
            while self.wlan.isconnected():
                if t >= timeout:
                    print("Disconnect network timeout!")
                    break
                if not self.wlan.isconnected():
                    break
                self.led2_blink(500)
                t = t + 1
                pass
            if not self.wlan.isconnected():
                print("Successfully disconnected from the network")
                if self.wlan.active():
                    self.wlan.active(False)
            else:
                print("Disconnect network failed")
        print('network config:', self.wlan.ifconfig())
        self.led2.deinit()

