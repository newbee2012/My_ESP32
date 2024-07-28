import esp
import machine
import micropython
import gc
import sys
def print_machine_info():
    print("---------------flash_size-----------------")
    print("{}MB".format(esp.flash_size()/1024/1024))
    print("---------------mem_info-------------------")
    micropython.mem_info()
    print("---------------system version-------------")
    print(sys.version)  # 打印MicroPython版本信息
    print("------------------------------------------")
