import serial
import serial.tools.list_ports

class rs485_dmx(object):
    def connect(self,uart_com=""):
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list)<=0:
            print("The Serial port can't find!")
        else:
             for port_info in port_list:
                if uart_com in port_info:
                    self.com = uart_com
                else:
                    self.com = port_info[0]
                try:
                    self.ser = serial.Serial(self.com,9600,bytesize=8,stopbits=1,timeout=1,parity=serial.PARITY_EVEN)
                    #self.ser.close()
                    return True
                except Exception:
                    pass
        return False

    def send(self,data,len):
        bytes_data = b''
        for i in range(len):
            bytes_data += data[i].to_bytes(length = 1,byteorder='big')
#        ser = serial.Serial(self.com,9600)
        self.ser.write(b'\x00')
        self.ser.baudrate='250000'
        self.ser._reconfigure_port()
        time.sleep(0.001)
        self.ser.write(bytes_data)
        self.ser.baudrate='9600'
        self.ser._reconfigure_port()

if __name__ == '__main__':
    import time
    dmx = rs485_dmx()
    dmx.connect()
    data=[0,1,2,3,4]
    while True:
        dmx.send(data,5)
        time.sleep(0.04)