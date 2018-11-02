# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 13:47:53 2018

@author: flach
"""
import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np

def show_data(auswahl):
    file_name = 'sound/' + auswahl + '.wav'
    fs, numarray = wavfile.read(file_name)
    t = np.linspace(0, len(numarray)/fs, len(numarray))
    plt.figure(figsize=(10,4))
    plt.title('Sprachsignal')
    plt.plot(t, numarray)
    plt.xlabel('t in s')
    plt.grid()
    return(numarray, fs)

def st_energy(numarray, fs, zf_len, zf_shape, overlap):
    n = int(zf_len * fs)
    anz_zf = int(len(numarray)//n) - 1
    if overlap == 1.0:
        n1 = n
    else:
        anz_zf = int(anz_zf/(1 - overlap))
        n1 = int((1 - overlap) * n)
    if zf_shape == 'rect':
        window = np.ones(n)
    if zf_shape == 'hann':
        window = np.hanning(n)
    if zf_shape == 'hamm':
        window = np.hamming(n)
    zf_e = np.zeros(anz_zf)
    for i in np.arange(anz_zf):
        zf_e[i] = np.sum((numarray[int(i*n1):int(i*n1 + n)]* window)**2)
    zf_e = 10 * np.log(zf_e/min(zf_e))
    plt.figure(figsize=(10,4))
    plt.title('Energieverlauf des Signals')
    t_e = np.linspace(0, len(numarray)/fs, anz_zf)
    plt.xlabel('t in s')
    plt.ylabel('E in dB')
    plt.grid()
    plt.plot(t_e, zf_e)
