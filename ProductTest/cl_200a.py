import serial
import serial.tools.list_ports
import time
import math
STX = b'\x02'
ETX = b'\x03'
CR = b'\x0D'
LF = b'\x0A'
DATA_OFFSET = 8
def XOR(nums):
    res = 0
    for num in nums:
        res ^= num
    return res

class CL200A_prase_data(object):
    def __init__(self,data):
        self.__data = data
        
    def ReceptorHead(self):
        return self.__data[0:2]

    def Command(self):
        return self.__data[2:4]

    def Status(self):
        return self.__data[4:8]

    def Raw(self):
        return self.__data

    def Data(self):
        d_len = len(self.__data)
        if d_len > 9:
            if d_len == 27:#Long communication format
                s_d = [0,0,0]
                i_d = [0,0,0]
                for i in range(0,3):
                    s_p = DATA_OFFSET+6*i
                    e_p = s_p + 6
                    s_d[i] = str((self.__data[s_p:e_p]),encoding = 'utf-8')
                    i_d[i] = int(s_d[i][1:5])
                    power = int(s_d[i][5])-4
                    if power >= 0:
                        i_d[i] *= math.pow(10,power)
                    else:
                        i_d[i] /= math.pow(10,-power)
                    if s_d[0]=="-":
                        i_d[i] -= i_d[i]
                    else:
                        if s_d[0]=="=":
                            i_d[i] = 0
            return i_d
        else:
            return []



class CL200A(object):
    #def __init__(self,uart_com=""):

    
    def measurement(self):
        #Perform measurement
        self.send_data("994021  ")
        time.sleep(0.5)

    def Ev_x_y(self,CF=True):
        #Read the colorimetric measurement value
        erro = ['1','2','3','4','5','6','7']
        if CF:
            self.send_data("00021300")
        else:
            self.send_data("00021200")
        response = self.read_data()
        status = response.Status()
        if not status:
            return ""

        if status[3] == '1':
            print("CL-200>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Low battery")
        if status[2] == '0' or status[2] == '6':
            print("CL-200>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Range Erro!")
        if status[1] in erro:
            print("CL-200>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Erro:%s" % (status[1]))
        return response.Data()

    def connect(self,uart_com=""):
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list)<=0:
            print("The Serial port can't find!")
        else:
            for port_info in port_list:
                self.com = port_info[0]
                try:
                    self.ser = serial.Serial(self.com,9600,bytesize=7,stopbits=1,timeout=1,parity=serial.PARITY_EVEN)
                    #Switch the CL-200A to PC connection mode
                    self.send_data("00541   ")
                    response = self.read_data()
                    recmd = response.Command()
                    if recmd  == b'54':
                        #Set the CL-200A to Hold status
                        time.sleep(0.5)
                        self.send_data("99551  0")
                        time.sleep(0.5)
                        #Set CL-200A to EXT mode
                        self.send_data("004010  ")
                        response = self.read_data()
                        print("EXT response.status"+str(response.Status()))
                        time.sleep(0.2)
                        return True
                    else:
                        self.ser.close()
                except Exception:
                    pass
        return False

    def send_data(self,string):
        #              字符串转bytes
        bcc_nums = bytes(string,'ascii')+ ETX
        bcc = XOR(bcc_nums)
        bcc_h = bcc>>4
        bcc_l = bcc%16
        #                             注意：不能将10-15转成'A' - 'F'
        data = STX + bcc_nums + bytes(str(bcc_h),'ascii') + bytes(str(bcc_l),'ascii') + CR + LF
        #print(data)
        return self.ser.write(data)
    def read_data(self,timeout = 1):
        ser = self.ser
        if ser.read(1)==STX:
            data = ser.readline()
            data = data[0:len(data)-2]#去掉\r\n
            d_len = len(data)
            b_bcc = data[d_len-2:]
            s_bcc = str(b_bcc,encoding = "utf-8")
            bcc = int(s_bcc,base = 16)
            data = data[0:len(data)-2]#去掉校验
            if bcc == XOR(data):
                return CL200A_prase_data(data)
            else:
                print("CL200A data check erro!")
        else:
            print("CL200A read erro!")
        return CL200A_prase_data("")

#res = bcc(b'\x30\x31\x30\x32\x31\x32\x30\x30\x03')

if __name__ == '__main__':
    cl200a = CL200A()
    if cl200a.connect()==True:
        while True:
            cl200a.measurement()
            print(cl200a.Ev_x_y())
            #time.sleep(1)
    else:
        print("Can't find CL-200A device!")
    
    


