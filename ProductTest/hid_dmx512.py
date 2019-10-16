import pywinusb.hid as hid
from ctypes import *
import ctypes
import time

dev_idProduct = "USB-DMX512 BOX"
class hid_dmx(object):
    def __init__(self,name=dev_idProduct):
        self.name = name
        self.dev =  None

    def find_dev(self):
        all_devices =hid.HidDeviceFilter().get_devices()
        if not all_devices:
            printf("Can't find HID device!")
            return None
        for dev in all_devices:
            if dev.product_name == self.name:
                self.dev = dev
                self.hanle = self.dev.open()
                self.target_usage = hid.get_full_usage_id(0x0c,0x1)
                self.reports = self.dev.find_output_reports() 
                return dev
        return None

    def write(self,data):
        resever = [0]*(512 - len(data))
        data = data + resever
        send_list = [0]*64
        for i in range(9):
            send_list[0] = 0x3f
            send_list[1] = i
            start = i*62
            end = start + 62
            send_list[2:64] = data[start:end] #没有的就会减掉
            resever = [0]*(64 - len(send_list)) 
            send_list = send_list + resever
            print(send_list)
            self.reports[62].send(send_list)               

if __name__ == '__main__':
    dmx512 = hid_dmx()
    send_data = [0]*255
    for i in range(250):
        send_data[i] = i+1   
    while True:
        dmx512.write(send_data)
        time.sleep(0.02)

    def AngleCurrentOut(ch,I):
        dmx_data = [0]*512
        dmx_data[0] = I/255
        dmx_data[1] = I%255
        dmx_data[2+2*ch] = 255
        self.dmx.write(dmx_data)



