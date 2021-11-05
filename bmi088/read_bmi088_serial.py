import serial
import sys
import time
import numpy as np
from bmi088_parser import *
import pandas as pd

def check_timing(time_buff, start_time):
    end_time = time.time()
    time_buff.append(end_time-start_time)
    if len(time_buff) > 1000:
        print(f'average time: {np.average(time_buff)} std: {np.std(time_buff)}')
        time_buff.clear()
    start_time = end_time

def print_imu_data(data):
    data = break_data(raw_data)
    print(f"Acc_x: {data['ax']}, Acc_y: {data['ay']}, Acc_z: {data['az']}")

if __name__ == '__main__':
    serial_port = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, 
                                bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

    serial_port.close()
    serial_port.open()

    if not serial_port.isOpen():
        print('Serial port Could not be opened')
        sys.exit()
    print('port is opened')

    start_time = time.time()

    time_buff = []

    in_cntr = 0
    out_cntr = 0

    data_cap = dict()
    data_cap['time'] = []
    data_cap['ax'] = []
    data_cap['ay'] = []
    data_cap['az'] = []
    data_cap['gx'] = []
    data_cap['gy'] = []
    data_cap['gz'] = []

    while(1):
        try:
            if serial_port.in_waiting > 0:
                read_string = serial_port.readline()
                flag, raw_data = parse_data(read_string.decode('Ascii'))
                in_cntr += 1
                if flag:
                    out_cntr += 1
                    print_imu_data(raw_data)
                    split_data = raw_data.split(',')
                    data_cap['time'].append(split_data[0])
                    data_cap['ax'].append(split_data[1])
                    data_cap['ay'].append(split_data[2])
                    data_cap['az'].append(split_data[3])
                    data_cap['gx'].append(split_data[4])
                    data_cap['gy'].append(split_data[5])
                    data_cap['gz'].append(split_data[6])
                else:
                    print(raw_data)

                # if in_cntr > 1000:
                #     print(f'in: {in_cntr}, out: {out_cntr}')
                #     in_cntr = 0
                #     out_cntr = 0

        except KeyboardInterrupt:
            break
    
    serial_port.close()

    df = pd.DataFrame(data_cap)
    l_time = time.localtime()
    data_filename = 'imu_cap_' + str(l_time.tm_mon) + '_' + str(l_time.tm_mday) + '_' + str(l_time.tm_hour) +'_' + str(l_time.tm_min) + '.csv'
    print(f'\nfile saved at: {data_filename}')
    print(f'data captured: {out_cntr}')
    df.to_csv(data_filename)

