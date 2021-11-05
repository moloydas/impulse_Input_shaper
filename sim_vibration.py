import numpy as np
import scipy
import matplotlib.pyplot as plt

f = 10 #Hz
w = 2*np.pi*f

beta = 0.02

A = 10
w_d = w*(np.sqrt(1-beta**2))

sampling_interval = 0.001
sampling_freq = 1000
time = np.arange(0, 10, sampling_interval)

y = []

for t in time:
    Amp_t = (A*w/np.sqrt(1-beta**2))*np.exp(-beta*w*t)
    y_t = Amp_t * np.sin(w_d * t) + 971.4255
    y.append(y_t)

y = np.array(y)

plt.plot(time,y)
plt.show()

# Frequency domain representation

fourierTransform = np.fft.fft(y)/len(y)           # Normalize y
fourierTransform = fourierTransform[range(int(len(y)/2))] # Exclude sampling frequency 

tpCount     = len(y)
values      = np.arange(int(tpCount/2))
timePeriod  = tpCount/sampling_freq
frequencies = values/timePeriod

plt.title('Fourier transform depicting the frequency components')
plt.plot(frequencies, abs(fourierTransform))
plt.xlabel('Frequency')
plt.ylabel('Amplitude')
plt.show()
