#overlay_real_sim_data.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_y_t(A, w, beta, t0, t, offset, phi):
    w_d = w*(np.sqrt(1-beta**2))
    Amp_t = (A*w/np.sqrt(1-beta**2))*np.exp(-beta*w*(t-t0))
    y_t = Amp_t * np.sin(w_d * (t-t0) + phi) - offset
    return y_t

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

def filt_data(data_time, data):
    dt = data_time.iloc[1] - data_time.iloc[0]

    ###############################################################
    #### Accel filtering
    ###############################################################
    fft_ = np.fft.rfft(data)
    frequencies = np.fft.rfftfreq(len(data), d=0.005)

    filt_fft = fft_.copy()
    filt_fft[:1] = 0
    # filt_fft[80:] = 0

    filt_data = np.fft.irfft(filt_fft)
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
    # filt_fft[:16] = 0
    filt_fft[:10] = 0
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

    extraction_span = range(16,450)
    final_pos_data = filt_data_pos[extraction_span]
    final_data_time = data_time.iloc[extraction_span]

    return pd.Series.to_numpy(final_data_time), final_pos_data

if __name__ == '__main__':
    # data_filename = 'imu_cap_7_16_21_44.csv'
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

    offset = 2204
    data = az[offset:]
    data_time = time[offset:]
    data_sq = sq[offset:]
    av = np.average(data)

    ##############################################################
    #### Filt accel data
    ##############################################################
    pos_time, pos = filt_data(data_time, data)
    ##############################################################

    sim_y = []

    ### Previous Result... VERYVERY VERY IMP
    # A = 0.0810/1000.0
    # offset = -0.0138/1000.0
    # w = 25.6437
    # beta = 0.0552
    # phi = 0.0003

    A = 0.4675#/1000.0
    offset = -0.0158#/1000.0
    w = 18.0822
    beta = 0.0699
    phi = 2.5471

    # t0 = 11.019

    t0 = pos_time[0]
    sim_time = np.arange(pos_time[0], pos_time[0] + 3, 0.005)

    for i in range(sim_time.shape[0]):
        sim_y.append(get_y_t(A, w, beta, t0, sim_time[i], offset, phi))

    sim_y = np.array(sim_y)

    plt.plot(sim_time, sim_y, label='sim')
    plt.plot(pos_time, pos, label='real_data')
    plt.legend()
    plt.show()

