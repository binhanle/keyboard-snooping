import numpy as np
from skimage import util


def parse_accel_csv( filename ):
    
    data1 = np.genfromtxt( filename, delimiter=',' )

    idx = np.argwhere( data1[:,0] <= 30000 ).flatten()
    data = data1[ idx ]
    
    data = data[:, 1:]

    if data.shape[0] > 6000 and data.shape[0] < 7000:
        data = data[:6000]

    elif data.shape[0] > 11000:
        data = data1[:12000, 1:]
        data = data[::2]


    result = []
    for i in range(0, len(data), 300):
        avg = np.mean( data[i:i+300-1], axis=0 )
        sig = np.std( data[i:i+300-1], axis=0 )
        
        result.append( np.append(avg, sig) )

    result = np.array(result)

    return result


def parse_wave_csv( filename, fft=False, window_stride=0.001, window_size=0.02, sampling_rate=44100 ):

    data = np.genfromtxt( filename, delimiter=',' )[:30*sampling_rate, 1:].flatten()

    if fft:
        fft_data = []
        N = 2**int(np.ceil(np.log2(window_size * sampling_rate)))
        assert N <= len(data), "Segment too short"
        hann = np.hanning(N)
        stride = int(round(window_stride * sampling_rate))
        windows = util.view_as_windows(data, window_shape=N, step=stride)
        windows = hann * windows
        spectrum = np.fft.fft(windows)
        return np.mean(np.abs(spectrum)[:, 1:(N - 1)//2 + 1], axis=0)

    return data


