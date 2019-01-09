# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

format_text(): formatiert ein wavToTag-File (franz. Sprachdaten)

"""

from scipy.io import wavfile
#import matplotlib.pyplot as plt
import numpy as np
#from random import randint

def format_text():
    text = open("sound/wavToTag.txt", "r")
    text_out  = open("sound/wavToTag_format.txt", "w")
    i = 0
    mylist = []
    mytext = ''
    for line in text:
        mylist.append(' | ' + str(i) + ' | ' + line.rstrip())
        i = i + 1
    text.close()
    i = 0
    while i < len(mylist):
        for k in range(5):
            mytext = mytext + mylist[i + k]
        mytext = mytext[2:] + '\n'
        text_out.write(mytext)
        i = i + 5
        mytext = ''
    text_out.close()
    
#def get_info(file):
#    text = open("sound/wavToTag.txt", "r")
#    mylist = []
#    for line in text:
#        mylist.append(line.rstrip())
#    text.close()
#    file_name = 'sound/' + str(file) + '.wav'
#    fs, numarray = wavfile.read(file_name)
#
#    string0 = 'Dateiname: ' + str(file) + '.wav \n'
#    string1 = 'Abtastfrequenz: ' + str(fs) + ' Hz \n'
#    string2 = 'Datenformat: ' + str(numarray.dtype) + '\n'
#    string3 = 'Anzahl ATW: ' + str(len(numarray)) + '\n'
#    string4 = 'Maximum: ' + str(max(numarray)) + '\n'
#    string5 = 'Minimum: ' + str(min(numarray)) + '\n'
#    string6 = 'Wort: ' + mylist[file]  + '\n'
#    info_string = string0 + string6 + string1 + string2 + string3 + string4 + string5
#    return(info_string)

def get_info(file):
    """Ermittlung der Informationen zu einem Soundfile
    - Dateiname, Wort, Abtastfrequenz, Format, Anz. ATW, Häufigkeit des Wortes im Korpus, Dauer [s], Maximum, Minimum
    
    file ... Name des Soundfiles"""
    
    text = open("sound/wavToTag.txt", "r")
    mylist = []
    for line in text:
        mylist.append(line.rstrip())
    text.close()
    file_name = 'sound/' + str(file) + '.wav'
    fs, numarray = wavfile.read(file_name)
    info_string = [file, mylist[file], fs, numarray.dtype, len(numarray), mylist.count(mylist[file]),
                   np.round(len(numarray)/fs,3), max(numarray), min(numarray) ]
    return(info_string)

    
def generate_data(anz, type, kanz):
    data = np.random.randint(100, size=(anz,2))
    sp = np.random.randint(100, size=(kanz,2))
    return(data, sp)

def calc_dist(data, sp):
    c = [0,0,0]
    cres = np.zeros(data.shape[1])
    for i in range(0,data.shape[1]):
        for j in range(0,sp.shape[1]):
            c[j] = np.sqrt(np.sum((data[:,i:i+1]-sp[:,j:j+1])**2))
        cres[i] = c.index(min(c))
    data = np.append(data, cres).reshape(3,20)
    return(data)

def calc_sp(data, kanz):
    sp_new = np.array([[],[]])
    for i in range(0,kanz):
        b = data[2]==i 
        print(len(b))
        print(data[0:2,b])
        print(np.mean(data[0:2,b]))
        np.append(sp_new, np.mean(data[0:2,b]))
        #np.append(sp_new[0],np.mean(data[0,b]))
        #np.append(sp_new[1],np.mean(data[1,b]))
    return(sp_new)


#mycolor = ['green', 'blue', 'red']
#data, sp = generate_data(20, 'equal', 3)
#plt.figure(figsize=(10,10))
#plt.subplot(221)
#plt.plot(data[0], data[1], linestyle='', marker='*')
#plt.plot(sp[0], sp[1], linestyle='', marker='*', color='red')

#data = calc_dist(data, sp)
#plt.subplot(222)
#for i in range(0,data.shape[1]):
#    plt.plot(data[0,i],data[1,i], color = mycolor[int(data[2,i])], marker='*')

#sp_new = calc_sp(data, 3)
#plt.subplot(223)
#plt.plot(data[0], data[1], linestyle='', marker='*')
#for i in range(0,3):
#    print(sp_new[2*i], sp_new[2*i+1])
#    plt.plot(sp_new[2*i], sp_new[2*i+1], color = 'red', marker='*')

#print(sp_new)