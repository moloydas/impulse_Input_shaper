import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    data_filename = 'imu_cap_10_30_22_26.csv'
    df = pd.read_csv(data_filename, delimiter=',')
    start_time = df['time'][0]
    time = (df['time'] - start_time)/1000.0

    sq = df['Unnamed: 0']
    ax = df['ax']
    ay = df['ay']
    az = df['az']
    gx = df['gx']
    gy = df['gy']
    gz = df['gz']

    # plt.figure(1)
    # plt.plot(time, gx, label='gx')
    # plt.plot(time, gy, label='gy')
    # plt.plot(time, gz, label='gz')
    # plt.legend()
    # plt.figure(2)
    # plt.plot(sq, ax, label='ax')
    # plt.plot(sq, ay, label='ay')
    # plt.plot(sq, az, label='az')
    # plt.legend()
    # plt.show()
    offset = 2204
    data = az[offset:]
    data_time = time[offset:]
    data_sq = sq[offset:]
    plt.title('Raw imu deflection data')
    plt.xlabel('s')
    plt.ylabel('mg')
    plt.plot(data_time, data, label='az')
    plt.legend()
    plt.show()

