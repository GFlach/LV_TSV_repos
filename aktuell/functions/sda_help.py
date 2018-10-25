#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 17:01:41 2017
Hilfsfunktionen für Datenanalyse (TSV)
@author: gudrun
"""

import matplotlib.pyplot as plt
import numpy as np
import random as rd
import pandas as pd

#from random import randint


def plot_data(dr, hist, min_d, max_d):
    plt.figure(figsize=(12,5))
    plt.subplot(121)
    plt.plot(dr, 'b.')
    plt.title('Datenreihe')
    plt.xlabel('Index')
    plt.ylabel('Wert')
    plt.subplot(122)
    x = np.arange(min_d, max_d, 1)
    plt.stem(x, hist, markerfmt='.')
    #plt.xticks(np.arange(min_d, max_d + 10, 10))
    plt.title('Histogramm')
    plt.xlabel('Wert')
    plt.ylabel('Häufigkeit')
    plt.show()
    
# Gleichverteilung
def randnum(anz, zmin, zmax, mu, sigma):
    zz = np.zeros(anz)
    for i in range(0, anz):
        zz[i] = rd.uniform(zmin, zmax)
        #zz[i] = randint(min_z, max_z)
    mybins = np.arange(zmin + 1, zmax + 2, 1)
    zzhist, zzbins = np.histogram(zz, mybins)
    return(zz, zzhist)

# Normalverteilung
def norm(anz, zmin, zmax, mu, sigma):
    zz = np.zeros(anz)
    for i in range(0, anz):
        zz[i] = rd.normalvariate(mu, sigma)
    mybins = np.arange(zmin, zmax + 1, 1)
    zzhist, zzbins = np.histogram(zz, mybins)
    return(zz, zzhist)

def test_vt(anz, zmin, zmax, mu, sigma, vt, save=False, name='xxx.jpg', nv=True):
    if vt == 'randnum':
        zz, zzhist = randnum(anz, zmin, zmax, mu, sigma)
        mu_r = np.mean(zz)
        sig_r = np.sqrt(np.var(zz))
        print(print_info(vt, anz, zmin, zmax, mu, sigma, mu_r, sig_r))
        x = np.arange(zmin, zmax, 1)
        plt.stem(x,zzhist, markerfmt = '.')
        if nv == True:
            y = 1/(sig_r * np.sqrt(2*np.pi))*np.exp(-0.5*((x-mu_r)/sig_r)**2)*anz
            plt.plot(x, y, 'r')
    if vt == 'norm':
        zz, zzhist = norm(anz, zmin, zmax, mu, sigma)
        mu_r = np.mean(zz)
        sig_r = np.sqrt(np.var(zz))
        print(print_info(vt, anz, zmin, zmax, mu, sigma, mu_r, sig_r))
        x = np.arange(zmin, zmax, 1)
        plt.stem(x,zzhist, markerfmt = '.')
        if nv == True:
            y = 1/(sig_r * np.sqrt(2*np.pi))*np.exp(-0.5*((x-mu_r)/sig_r)**2)*anz
            plt.plot(x, y, 'r')
    if save == True:
        plt.savefig(name)
        
def print_info(vt, anz, zmin, zmax, mu, sigma, mu_r, sig_r):
    string0 = 'Verteilung: ' + vt + '\n'
    string1 = 'Anzahl Werte: ' + str(anz) + '\n'
    info = string0 + string1
    if vt in ('randnum', 'triangle', 'gamma', 'beta'):
        string2 = 'kleinster Wert: ' + str(zmin) + '\n'
        string3 = 'größter Wert: ' + str(zmax) + '\n'
        info = info + string2 + string3
    if vt == 'norm':
        string4 = 'Mittelwert(vorgegeben): ' + str(mu) + '\n'
        string5 = 'Standardabweichung(vorgegeben): ' + str(sigma) + '\n'
        info = info + string4 + string5
    string6 = 'Mittelwert(berechnet): ' + str(np.round(mu_r,2)) + '\n'
    string7 = 'Standardabweichung(berechnet): ' + str(np.round(sig_r,2)) + '\n'
    info = info + string6 + string7
    return(info)

def generate_data(anz, zmin, zmax, mu, sigma, vt):
    if vt == 'randnum':
        data, hist = randnum(anz, zmin, zmax, mu, sigma)
    if vt == 'norm':
        data, hist = norm(anz, zmin, zmax, mu, sigma)
    return(data)
    
def auto_generate(anz, zmin, zmax, mu, sigma, vt):
    #info = []
    if vt == 'randnum':
        d = generate_data(anz, zmin, zmax, mu, sigma, vt)
        dmu = np.round(np.mean(d),2)
        sig = np.round(np.sqrt(np.var(d)),2)
        #info.append(['randnum', anz, zmin, zmax, '-', '-', dmu, sig])
        info = ['randnum', anz, zmin, zmax, '-', '-', dmu, sig]
        
    if vt == 'norm':
        d = generate_data(anz, zmin, zmax, mu, sigma, vt)
        dmu = np.round(np.mean(d),2)
        sig = np.round(np.sqrt(np.var(d)),2)
        #info.append(['norm', anz, '-', '-', mu, sigma, dmu, sig])
        info = ['norm', anz, '-', '-', mu, sigma, dmu, sig]
        
    return(info)
    
def build_df(data_files, class_labels):
    i = 0
    for fn in data_files:
        dname = 'data/' + fn + '.npy'
        d = np.load(dname)
        df = pd.DataFrame(np.transpose(d), columns=['x1', 'x2'])
        kn = [class_labels[i]]
        for j in range(0,d.shape[1]-1):
            kn = kn + [class_labels[i]]
        dfk = pd.DataFrame(np.transpose(kn), columns=['Klasse'])
        if i == 0:
            df_ges = df
            df_cn = dfk
        else:
            df_ges = df_ges.append(df)
            df_cn = df_cn.append(dfk)
        i = i + 1
    df_ges = pd.concat([df_ges, df_cn], axis = 1)  
    return(df_ges)

def show_res(df_ges, w):
    colors = ['green', 'red', 'blue', 'yellow', 'magenta', 'lime', 'skyblue', 'orangered', 'cyan', 'aqua']
    hist_cl = np.unique(df_ges['Klasse'].values)
    eps = 10**(-6)
    plt.figure(figsize=(7,7))
    for hist_cl, color in zip(hist_cl, colors):
        df_h = df_ges[df_ges.Klasse == hist_cl].values
        y = df_h[:,0:2]
        plt.scatter(y[:,0], y[:,1], color=color, marker='o', label='Klasse ' + str(hist_cl))
    p1 = w[1]/(w[2] + eps) -w[0]/(w[2] + eps)
    p2 = -w[1]/(w[2] + eps)*5 -w[0]/(w[2] + eps)
    plt.plot([-1, 5], [p1, p2])
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.legend(loc='upper left')
    plt.axis([-1, 5, -1, 5])
    plt.grid()
    plt.show()
    
def show_res1(df_ges, w):
    colors = ['green', 'red', 'blue', 'yellow', 'magenta', 'lime', 'skyblue', 'orangered', 'cyan', 'aqua']
    hist_cl = np.unique(df_ges['Klasse'].values)
    eps = 10**(-6)
    plt.figure(figsize=(7,7))
    for hist_cl, color in zip(hist_cl, colors):
        df_h = df_ges[df_ges.Klasse == hist_cl].values
        y = df_h[:,0:2]
        plt.scatter(y[:,0], y[:,1], color=color, marker='o', label='Klasse ' + str(hist_cl))
    p1 = w[1]/(w[2] + eps) -w[0]/(w[2] + eps)
    p2 = -w[1]/(w[2] + eps)*120 -w[0]/(w[2] + eps)
    plt.plot([0, 120], [p1, p2])
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.legend(loc='upper left')
    plt.axis([0, 120, 0, 120])
    plt.grid()
    plt.show()
 
