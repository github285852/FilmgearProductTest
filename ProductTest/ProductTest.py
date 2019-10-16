
from hid_dmx512 import hid_dmx
from cl_200a import CL200A
import time
import matplotlib.pyplot as plt
from pylab import *  
mpl.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体  
mpl.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题

dmx512 = hid_dmx()
dmx512.find_dev()

cl200a = CL200A()
if cl200a.connect() != True:
    print("Can't find CL-200A device!")

dmx_data = [0]*512
T = 30
tim = T/256
dmx_data[1] = 126
#dmx_data[2] = 100

x = []
y = []
y_t = []
x.append(0)
y.append(0)
y_t.append(0)

cl200a.measurement()
cl200a.Ev_x_y()
cl200a.measurement()
cl200a.Ev_x_y()
cl200a.measurement()
cl200a.Ev_x_y()

while dmx_data[0] < 255:
    dmx_data[0] += 1
    x.append(dmx_data[0])
    dmx512.write(dmx_data)
    cl200a.measurement()
    y.append(cl200a.Ev_x_y()[0])
   # y_t.append(pow(dmx_data[0],2.4))
plt.title('亮度曲线')
plt.plot(x,y,'r.',label = "实际")
#plt.plot(x,y_t,'b',label = "理论")
plt.ylabel("流明")
plt.xlabel("亮度")
plt.legend()
plt.show()
