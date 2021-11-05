# fit_data.py
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torch
from torch import autograd

def get_cost(y_t, pred_y_t, ):
    sq_err = (y_t - pred_y_t)**2
    sq_err_sum = torch.sum(sq_err)
    return sq_err_sum

def get_y_t(A, w, beta, t0, t, offset, phi):
    w_d = w*(torch.sqrt(1-beta**2))
    Amp_t = (A*w/torch.sqrt(1-beta**2))*torch.exp(-beta*w*(t-t0))
    y_t = Amp_t * torch.sin(w_d * (t-t0) + phi) - offset
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

    ##############################################################
    #### Filt accel data
    ##############################################################
    pos_time, pos = filt_data(data_time, data)

    plt.plot(pos_time, pos)
    plt.show()
    # sys.exit()
    ##############################################################

    ##############################################################
    #### Fit eq onto data
    ##############################################################
    A = autograd.Variable(torch.FloatTensor([0.4]),requires_grad=True)
    offset = autograd.Variable(torch.FloatTensor([0]),requires_grad=True)
    w = autograd.Variable(torch.FloatTensor([2*np.pi*4.0]),requires_grad=True)
    beta = autograd.Variable(torch.FloatTensor([0.1]),requires_grad=True)
    # t0 = autograd.Variable(torch.FloatTensor([11.02]),requires_grad=True)
    phi = autograd.Variable(torch.FloatTensor([2.5]),requires_grad=True)
    t0 = pos_time[0]

    data_time = torch.from_numpy(pos_time.astype(dtype=float))
    data = torch.from_numpy(pos.astype(dtype=float))

    total = autograd.Variable(torch.FloatTensor([0]))

    for i in range(50000):
        pred_y_t = get_y_t(A, w, beta, t0, data_time, offset, phi)
        total = get_cost(data, pred_y_t)

        # total = torch.square(data_time[0] - t0) * 10000.0 + total

        total.backward()
        A.data -= .00005 * A.grad.data
        offset.data -= .00001 * offset.grad.data
        w.data -= .0001 * w.grad.data
        beta.data -= .000001 * beta.grad.data
        # t0.data -= .00001 * t0.grad.data
        phi.data -= .0000001 * phi.grad.data


        if i%250 == 0:
            print(i, total, A.data, offset.data, w.data, beta.data, t0, phi.data)
            print('\n')

        A.grad.data.zero_()
        offset.grad.data.zero_()
        w.grad.data.zero_()
        beta.grad.data.zero_()
        # t0.grad.data.zero_()
        phi.grad.data.zero_()

    print(A.data, w.data, beta.data, phi.data)



