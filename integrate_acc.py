#integrate_acc.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

def get_int_pos(data_time, data):
    p = 0
    v = 0

    pos = []
    vel = []

    pos.append((data_time.iloc[0], 0))
    vel.append((data_time.iloc[0], 0))

    for i in data.index:
        if i >= data.index[-1]-1:
            break
        dt = data_time[i+1] - data_time[i]
        
        p = p + v * dt + 0.5 * data[i] * (dt**2)
        v = v + data[i] * dt

        pos.append((data_time[i+1], p))
        vel.append((data_time[i+1], v))

    return np.array(pos), np.array(vel)

def get_int_pos_np(data_time, data):
    p = 0
    v = 0

    pos = []
    vel = []

    pos.append((data_time[0], 0))
    vel.append((data_time[0], 0))

    for i in range(len(data)):
        if i >= len(data)-1:
            break
        dt = data_time[i+1] - data_time[i]
        
        p = p + v * dt + 0.5 * data[i] * (dt**2)
        v = v + data[i] * dt

        pos.append((data_time[i+1], p))
        vel.append((data_time[i+1], v))

    return np.array(pos), np.array(vel)

if __name__ == '__main__':
    data_filename = 'imu_cap_7_16_21_44.csv'
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

    data = az[2937:3719]/1000.0
    data_time = time[2937:3719]
    data_sq = sq[2937:3719]
    av = np.average(data)

    ###############################################################
    #### Acc filtering
    ###############################################################
    dt = data_time.iloc[1] - data_time.iloc[0]
    freq = 1/dt
    print("Timeperiod: " + str(dt))
    print("freq: "+ str(freq))
    print("len: " + str(len(data)))

    fft_ = np.fft.rfft(data)
    frequencies = np.fft.rfftfreq(len(data), d=0.005)

    filt_fft = fft_.copy()
    filt_fft[:2] = 0
    # filt_fft[80:] = 0

    # plt.plot(frequencies, abs(fft_), label='fft')
    # plt.plot(frequencies, abs(filt_fft), label='filt fft')
    # plt.legend()
    # plt.show()

    filt_data = np.fft.irfft(filt_fft)
    # plt.plot(data_time, filt_data, label='fft')
    # plt.plot(data_time, data-av, label='average')
    # plt.legend()
    # plt.show()
    ###############################################################

    ###############################################################
    #### integrate Accel
    ###############################################################
    pos, vel = get_int_pos_np(np.array(data_time), filt_data)
    ###############################################################

    ###############################################################
    #### pos filtering
    ###############################################################
    fft_ = np.fft.rfft(pos[:,1])
    frequencies = np.fft.rfftfreq(len(pos[:,1]), d=0.005)
    filt_fft = fft_.copy()
    filt_fft[:16] = 0
    # filt_fft[17:] = 0

    # plt.title("fft pos")
    # plt.plot(frequencies, abs(fft_), label="fft pos")
    # plt.plot(frequencies, abs(filt_fft), label="filt fft pos")
    # plt.legend()
    # plt.show()

    filt_data_pos = np.fft.irfft(filt_fft)
    # plt.title("pos")
    # plt.plot(data_time, filt_data_pos, label='fft filt')
    # plt.plot(data_time, pos[:,1], label='normal')
    # plt.legend()
    # plt.show()
    ###############################################################

    ###############################################################
    #### Plot final pose data
    ###############################################################
    # extraction_span = range(16,450)
    # final_pos_data = filt_data_pos[extraction_span]
    # final_data_time = data_time.iloc[extraction_span]
    # plt.title("final pos filt data")
    # plt.plot(final_data_time, final_pos_data, label='fft filt')
    # plt.show()
