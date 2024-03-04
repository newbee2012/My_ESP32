import config
from machine import Pin, UART
from modules.simple_queue import SimpleQueue
import time
import _thread
from log import logger

UNKNOWN = 0xFF
NO_TARGET = 0x00
MOTION_TARGET = 0x01
STATIONARY_TARGET = 0x02
MOTION_AND_STATIONARY_TARGET = 0x03
MOTION_ENERGY_COUNTER_MAX = 300
MOTION_ENERGY_COUNTER_MIN = 0
MOTION_ENERGY_DECAY_RATE = 50
class LD2410:
    def __init__(self):
        self.uart = UART(1, baudrate=115200, tx=Pin(0), rx=Pin(1))
        self.motion_energy_counter = MOTION_ENERGY_COUNTER_MIN
        self.target_status = NO_TARGET
        self.buffer = bytearray()
        self.frame_queue = SimpleQueue()
        self.frame_start = b'\xf4\xf3\xf2\xf1'
        self.frame_end = b'\xf8\xf7\xf6\xf5'
        logger.info("LD2410 init finished.")
    
    def __recvData_thread(self):
        while not config.stop_all_threads:
            recv_data = self.uart.read()
            if recv_data:
                self.buffer.extend(recv_data)
                self.__process_buffer()
            frame_data = self.__get_frame()
            if frame_data != None:
                self.target_status = self.__cale_target_status(frame_data)
                hex_string = ' '.join(f'{byte:02x}' for byte in frame_data)
                logger.debug(f'{hex_string}|{self.frame_queue.size()}')
            time.sleep_ms(20)
        logger.info("LD2410.__recvData_thread exit.")

    def __process_buffer(self):
        while True:
            start_index = self.buffer.find(self.frame_start)
            if start_index == -1:
                # Frame start not found
                break
            end_index = self.buffer.find(self.frame_end, start_index)
            if end_index == -1:
                # Frame end not found
                break
            # Extract and enqueue the frame
            frame = self.buffer[start_index : end_index + len(self.frame_start)]
            self.frame_queue.push(frame)
            # Remove processed data from the buffer
            self.buffer = self.buffer[end_index + len(self.frame_end):]
    
    def __get_frame(self):
        return self.frame_queue.pop() if not self.frame_queue.empty() else None
    
    def getTargetStatus(self):
        return self.target_status;

    def run(self):
        thread_recvData = _thread.start_new_thread(self.__recvData_thread, ())

    def __cale_target_status(self, frame_data):
        if frame_data == None:
            return UNKNOWN
        status = frame_data[8]
        move_energy = frame_data[11]
        
        if status == NO_TARGET:
            self.motion_energy_counter = MOTION_ENERGY_COUNTER_MIN
            self.target_status = NO_TARGET
        elif self.target_status == NO_TARGET:
            if status == MOTION_TARGET or status == MOTION_AND_STATIONARY_TARGET:
                if self.motion_energy_counter < MOTION_ENERGY_COUNTER_MAX:
                    self.motion_energy_counter += move_energy
                    if self.motion_energy_counter >= MOTION_ENERGY_COUNTER_MAX:
                        self.target_status = MOTION_TARGET
                        self.motion_energy_counter = MOTION_ENERGY_COUNTER_MAX
            elif self.motion_energy_counter > MOTION_ENERGY_COUNTER_MIN:
                self.motion_energy_counter -= MOTION_ENERGY_DECAY_RATE
                if self.motion_energy_counter < MOTION_ENERGY_COUNTER_MIN:
                    self.motion_energy_counter = MOTION_ENERGY_COUNTER_MIN
        logger.debug(f"{self.getStatusAlias(self.target_status)},瞬时能量:{move_energy},能量累计:{self.motion_energy_counter}")
        return self.target_status
            
    
    def getStatusAlias(self, target_status):
        alias = "未知状态"
        if target_status == NO_TARGET:
            alias = "无目标"
        elif target_status == MOTION_TARGET:
            alias = "运动目标"
        elif target_status == STATIONARY_TARGET:
            alias = "静止目标"
        elif target_status == MOTION_AND_STATIONARY_TARGET:
            alias = "运动&静止目标"
        
        return alias

        
        

