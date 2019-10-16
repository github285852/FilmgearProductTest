

from hid_dmx512 import hid_dmx
import time

dmx512 = hid_dmx()
dmx512.find_dev()

dmx_data = [0]*512
T = 180
tim = T/256
dmx_data[1] = 0
dmx_data[2] = 0
dmx512.write(dmx_data)
time.sleep(3)

while True:
    dmx_data[0] += 1
    if  dmx_data[0]>=256:
        dmx_data[0] = 0
        time.sleep(3)
    dmx512.write(dmx_data)
    time.sleep(tim)