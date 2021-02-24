import time
from fs2012_flow_sensor import DataReader

port = '/dev/ttyUSB0'
reader = DataReader(port)
reader.start()
for i in range(75):
    print(reader.get_data())
    time.sleep(0.1)
reader.stop()
