from __future__ import print_function
import sys
import time
import serial
import signal
import csv

import matplotlib
import matplotlib.pyplot as plt

class LivePlot(serial.Serial):

    ResetSleepDt = 0.5
    Baudrate = 115200

    def __init__(self,port,timeout=10.0):
        param = {'baudrate': self.Baudrate, 'timeout': timeout}
        super(LivePlot,self).__init__(port,**param)
        time.sleep(self.ResetSleepDt)


        self.num_lines = 2
        self.window_size = 10.0
        self.data_file = 'flow_data.csv'
        self.color_list = ['b', 'r', 'g', 'm', 'c']
        self.label_list = ['sensor {}'.format(i+1) for i in range(self.num_lines)]

        self.t_init =  time.time()
        self.t_list = []
        self.list_of_data_lists = [[] for i in range(self.num_lines)]

        self.running = False
        signal.signal(signal.SIGINT, self.sigint_handler)

        plt.ion()
        self.fig = plt.figure(1)
        self.ax = plt.subplot(111) 
        self.line_list = []
        for i in range(self.num_lines):
            color_ind = i%len(self.color_list)
            line, = plt.plot([0,1], [0,1],self.color_list[color_ind])
            line.set_xdata([])
            line.set_ydata([])
            self.line_list.append(line)
        plt.grid('on')
        plt.xlabel('t (sec)')
        plt.ylabel('flow  (L/min)')
        self.ax.set_xlim(0,self.window_size)
        self.ax.set_ylim(-0.01,2.01)
        plt.title("FS2012 Flow Sensor")
        plt.figlegend(self.line_list,self.label_list,'upper right')
        self.fig.canvas.flush_events()


    def sigint_handler(self,signum,frame):
        self.running = False


    def raw_to_liter_per_min(self,raw_val):
        volt = 5.0*float(raw_val)/float(1023)
        return 0.4*(volt  - 0.045)

    def run(self):

        self.running = True

        csv_file_handle = open(self.data_file, "w", newline="")
        col_names = ["t (secs)", "sensor 1", "sensor 2"]
        csv_writer = csv.DictWriter(csv_file_handle, fieldnames=col_names)
        csv_writer.writeheader()
        
        while self.running:
            have_data = False
            while self.in_waiting > 0:
                # Not the best - throwing points away. Maybe put points in list, process later. 
                line = self.readline()
                have_data = True
            if have_data:
                line = line.strip()
                # Turn bytes to string, remove unicode:
                line = line.decode("UTF-8", "ignore") 
                data = line.split(' ')
                try:
                    t = 1.0e-3*int(data[0])
                    raw_list = [data[1], data[2]]
                except IndexError:
                    continue
                except ValueError:
                    continue

                liter_per_min_list = [self.raw_to_liter_per_min(x) for x in raw_list]
                for data, data_list in zip(liter_per_min_list, self.list_of_data_lists):
                    data_list.append(data)

                t_elapsed = time.time() - self.t_init
                self.t_list.append(t_elapsed)

                num_pop = 0
                while (self.t_list[-1] - self.t_list[0]) > self.window_size:
                    self.t_list.pop(0)
                    num_pop += 1

                for line, data_list in zip(self.line_list, self.list_of_data_lists):
                    for i in range(num_pop):
                        data_list.pop(0)
                    line.set_xdata(self.t_list)
                    line.set_ydata(data_list)

                xmin = self.t_list[0]
                xmax = max(self.window_size, self.t_list[-1])

                self.ax.set_xlim(xmin,xmax)
                self.fig.canvas.flush_events()
                csv_writer.writerow({col_names[0]: t_elapsed, 
                                     col_names[1]: liter_per_min_list[0], 
                                     col_names[2]: liter_per_min_list[1]})

                print('{:0.2f} '.format(t_elapsed),end='')
                for val in liter_per_min_list:
                    print('{:0.2f} '.format(val),end='')
                print()

        csv_file_handle.close()
        print('Successfully quitted')



# ---------------------------------------------------------------------------------------
if __name__ == '__main__':

    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = '/dev/ttyUSB0'

    liveplot = LivePlot(port=port)
    liveplot.run()



