from __future__ import print_function
import sys
import time
import serial
import threading
import signal

class DataReader(serial.Serial):

    ResetSleepDt = 2.0
    Baudrate = 115200

    def __init__(self,port,timeout=10.0):
        param = {'baudrate': self.Baudrate, 'timeout': timeout}
        super(DataReader,self).__init__(port,**param)
        time.sleep(self.ResetSleepDt)

    def get_data(self):
        data = {}
        if self.in_waiting > 0:
            line = self.readline()
            if line:
                line = line.strip()
                # Turn bytes to string, remove unicode:
                line = line.decode("UTF-8", "ignore") 
                data = line.split(' ')
                try:
                    t = 1.0e-3*int(data[0])
                    raw_list = [float(x) for x in data[1:]]
                    have_data = True
                except (IndexError, ValueError):
                    have_data = False
                if have_data:
                    flow_list = [self.raw_to_liter_per_min(x) for x in raw_list]
                    data = {'t':t, 'flow': flow_list}
                else:
                    data = {}
        return data

    def raw_to_liter_per_min(self,raw_val):
        volt = 5.0*float(raw_val)/float(1023)
        return 0.4*(volt  - 0.045)


# ------------------------------------------------------------------------------------------
if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = '/dev/ttyUSB0'
    reader = DataReader(port)
    for i in range(75):
        print(reader.get_data())
        time.sleep(0.1)








