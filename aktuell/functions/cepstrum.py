
# coding: utf-8

# In[ ]:
import scipy.io.wavfile
from scipy.fftpack import dct
import numpy as np
import matplotlib.pyplot as plt


def read_show_sig(file_name, sig_dur):
    sample_rate, signal = scipy.io.wavfile.read(file_name)  
    if len(signal)/sample_rate < sig_dur:
        sig_dur = len(signal)/sample_rate
    signal = signal[0:int(sig_dur * sample_rate)]
    print('Abtastfrequenz: ' + str(sample_rate) + 'Hz')
    show_sig(signal, sig_dur, file_name)    
    return (sample_rate, signal)

def show_sig(signal, sig_dur, file_name):
    t = np.linspace(0, sig_dur, len(signal))
    plt.figure(figsize=(12,4))
    plt.plot(t, signal, label=file_name)
    plt.xlabel('Time(s)')
    plt.ylabel('Amplitude')
    plt.axis((0, sig_dur, min(signal)-500, max(signal)+500))
    plt.legend()
    plt.grid()
    
def wind_sig(frame_size, frame_stride, sample_rate, signal):
    # Convert from seconds to samples
    frame_length, frame_step = frame_size * sample_rate, frame_stride * sample_rate  
    signal_length = len(signal)
    frame_length = int(round(frame_length))
    frame_step = int(round(frame_step))
    # Make sure that we have at least 1 frame
    num_frames = int(np.ceil(float(np.abs(signal_length - frame_length)) / frame_step))  
    pad_signal_length = num_frames * frame_step + frame_length
    z = np.zeros((pad_signal_length - signal_length))
    # Pad Signal to make sure that all frames have equal number of samples without truncating any samples from the original signal
    pad_signal = np.append(signal, z) 
    indices = np.tile(np.arange(0, frame_length), (num_frames, 1)) + np.tile(np.arange(0, num_frames * frame_step, frame_step), (frame_length, 1)).T
    frames = pad_signal[indices.astype(np.int32, copy=False)]
    frames *= np.hamming(frame_length)
    return(frames)
def show_spectrogram(frames, sig_dur,sample_rate):
    plt.figure(figsize=(12,4))
    plt.imshow(frames.T, cmap='Blues', extent=[0,sig_dur*100,int(frames.shape[1]),0], aspect='auto')
    plt.ylim(0, int(frames.shape[1]/2))
    plt.xlabel('Time(s)')
    plt.ylabel('Frequency [kHz])')
    plt.xticks(np.arange(0, sig_dur*100, step=sig_dur*20), np.round(np.arange(0, sig_dur, step=sig_dur/5), 3))
    plt.yticks(np.arange(0, int(frames.shape[1]/2), step=frames.shape[1]/16), np.round(np.arange(0, sample_rate / 2000, step=sample_rate / 16000), 2)) 
    plt.title('Spektrogramm')
    plt.show()
    
def mel_spec(nfilt,sample_rate, NFFT, sig_frames):
    low_freq_mel = 0
    high_freq_mel = (2595 * np.log10(1 + (sample_rate / 2) / 700))  # Convert Hz to Mel
    mel_points = np.linspace(low_freq_mel, high_freq_mel, nfilt + 2)  # Equally spaced in Mel scale
    hz_points = (700 * (10**(mel_points / 2595) - 1))  # Convert Mel to Hz
    bin = np.floor((NFFT + 1) * hz_points / sample_rate)

    fbank = np.zeros((nfilt, int(np.floor(NFFT / 2 + 1))))
    for m in range(1, nfilt + 1):
        f_m_minus = int(bin[m - 1])   # left
        f_m = int(bin[m])             # center
        f_m_plus = int(bin[m + 1])    # right

        for k in range(f_m_minus, f_m):
            fbank[m - 1, k] = (k - bin[m - 1]) / (bin[m] - bin[m - 1])
        for k in range(f_m, f_m_plus):
            fbank[m - 1, k] = (bin[m + 1] - k) / (bin[m + 1] - bin[m])
    filter_banks = np.dot(sig_frames, fbank.T)
    filter_banks = np.where(filter_banks == 0, np.finfo(float).eps, filter_banks)  # Numerical Stability
    filter_banks = 20 * np.log10(filter_banks)  # dB
    return(filter_banks)

def show_melspec(mel_frames, sig_dur, nfilt):
    plt.figure(figsize=(12,4))
    plt.imshow(mel_frames.T, cmap='Blues', extent=[0,sig_dur*100,mel_frames.shape[1],0], aspect='auto')
    plt.ylim(0, nfilt)
    plt.xlabel('Time(s)')
    plt.ylabel('Frequency band')
    plt.xticks(np.arange(0, sig_dur*100, step=sig_dur*20), np.round(np.arange(0, sig_dur, step=sig_dur/5), 2))
    plt.yticks(np.arange(0, nfilt, step=nfilt/8), np.arange(0, nfilt, step=nfilt/8) )
    plt.show()
    
def show_mfcc(mfcc, sig_dur, num_ceps):
    plt.figure(figsize=(12,4))
    plt.imshow(mfcc.T, cmap='Blues', extent=[0,sig_dur*100,mfcc.shape[1],0], aspect='auto')
    plt.ylim(0, num_ceps)
    plt.xlabel('Time(s)')
    plt.ylabel('MFCC Coefficients')
    plt.xticks(np.arange(0, sig_dur*100, step=sig_dur*20), np.round(np.arange(0, sig_dur, step=sig_dur/5), 2))
    plt.show()

