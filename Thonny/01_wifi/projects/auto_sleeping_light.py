#Automatically turn off lights when sleeping
import config
from machine import Pin
from modules.rf315_sender import RF315Sender
from modules.ld2410 import LD2410
import time
import _thread
from log import logger

SWITCH_ON_SIGNAL = "000000000001010100010001"
SWITCH_OFF_SIGNAL = "000000000001010100010100"
UNKNOWN = 0xFF
NO_TARGET = 0x00
MOTION_TARGET = 0x01
STATIONARY_TARGET = 0x02
MOTION_AND_STATIONARY_TARGET = 0x03
    
class AutoSleepingLight():
    def __init__(self):
        self.rf315Sender = RF315Sender()
        self.ld2410 = LD2410()
        self.switch_status = 0
        self.led_pin = Pin(12,Pin.OUT, Pin.PULL_DOWN)
        self.led_pin.value(0)
    
    def turn_on_light(self):
        logger.debug("turn_on_light")
        self.led_pin.value(1)
        self.rf315Sender.send_signal(SWITCH_ON_SIGNAL,5,0,1,200)
        self.rf315Sender.send_signal(SWITCH_ON_SIGNAL,5,1,1,200)
        self.rf315Sender.send_signal(SWITCH_ON_SIGNAL,5,5,1,200)
        self.rf315Sender.send_signal(SWITCH_ON_SIGNAL,5,10,1,200)
        
    def turn_off_light(self):
        logger.debug("turn_off_light")
        self.led_pin.value(0)
        self.rf315Sender.send_signal(SWITCH_OFF_SIGNAL,5,0,1,200)
        self.rf315Sender.send_signal(SWITCH_OFF_SIGNAL,5,1,1,200)
        self.rf315Sender.send_signal(SWITCH_OFF_SIGNAL,5,5,1,200)
        self.rf315Sender.send_signal(SWITCH_OFF_SIGNAL,5,10,1,200)
        
    def __light_control_thread(self):
        try:
            while not config.stop_all_threads:
                target_status = self.ld2410.getTargetStatus()
                if target_status == MOTION_TARGET and self.switch_status == 0:
                    self.switch_status = 1
                    self.turn_on_light()
                elif target_status == NO_TARGET and self.switch_status == 1:
                    self.switch_status = 0
                    self.turn_off_light()
                    
                time.sleep_ms(250)
            logger.info("AutoSleepingLight.__light_control_thread exit.")
        except KeyboardInterrupt:
            logger.info("Ctrl+C received. Stopping __light_control_thread.")
                    
    def run(self):
        self.ld2410.run()
        thread_light_control = _thread.start_new_thread(self.__light_control_thread, ())
        