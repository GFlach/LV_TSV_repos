# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 14:29:56 2019

@author: flach
"""
from scipy.io import wavfile
import numpy as np

## Dokumentation für die Klasse Sounddata
#
# Handling von Sounddaten
#
# Zur Beschreibung der Objekte werden folgende Attribute verwendet:                      
# Filename;
# Verschriftung;
# Abtastfrequenz;
# Datenformat;
# Anz. Abtastwerte;
# Minumum;
# Maximum
#     
# Folgende Methoden stehen zur Verfügung:
#   set_info(); get_info(); read_sound(); write_sound(); normalize_sound();play_sound().

class Sounddata():
    def __init__(self, fn, vs = '', fs = 44000, df = '', atw = 0, sd_min = 0, sd_max = 0, data = []):
        ## Filename
        self.Filename = fn 
        ## Verschriftung der Sprachäußerung
        self.Verschriftung = vs
        ## Abtastfrequenz in Hz
        self.Abtastfrequenz = fs
        ## Datenformat
        self.Datenformat = df
        ## Anzahl Abtastwerte
        self.ATW = atw
        ## kleinster Abtastwert
        self.min = sd_min
        ## größter Abtastwert
        self.max = sd_max
        ## Datenfeld
        self.data = data
        
        
    ## setzt für angegebenes Soundobjekt die Attributwerte
    #  @param self Objektzeiger
    def set_info(self):
        file_name = 'sound/' + str(self.Filename) + '.wav'
        self.Abtastfrequenz, self.data = wavfile.read(file_name)
        text = open("sound/wavToTag.txt", "r")
        mylist = []
        for line in text:
            mylist.append(line.rstrip())
                         
        self.ATW = len(self.data)
        self.min = min(self.data)
        self.max = max(self.data)
        self.Datenformat = self.data.dtype
        self.Verschriftung = mylist[self.Filename]
        
    ## ermittelt für angegebenes Soundobjekt Wert des Attributes, wenn leer, dann alle Attribute
    # @param self Objektzeiger
    # @param attr gewünschtes Attribut
    def get_info(self,attr):
        pass
  
    ## liest Daten in Soundobjekt ein
    #  @param self Objektzeiger
    def read_sound(self):
        pass
    
    ## schreibt Daten des Soundobjektes
    #  @param self Objektzeiger
    def write_sound(self):
        pass
        
    ## normiert Soundobjekt
    #  @param self Objektzeiger
    def normalize_sound(self):
        pass
        
    ## gibt Soundobjekt wieder
    #  @param self Objektzeiger
    def play_sound(self):
        pass
