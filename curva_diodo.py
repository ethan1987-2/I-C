# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 18:01:14 2019

@author: Publico
"""

import time
import visa
import numpy as np
from matplotlib import pyplot as pp
#Antes de importar clases desde archivos en el mismo carpeta hay que correr esos archivos
from claseGF import *
from claseOSC import *
from Sound_card_class import *
import sounddevice as sd 
import scipy.signal as sg

audio=AudioCard()
osc=OsciloscopeTDS1002B('C065089')
funcg=FunctionGeneratorAFG3021B('C036492')
osci=

fs = 96000
duration = 100
frequency = 100
amplitude = 1
phase = 0

sd.query_devices()
#Alimentar al diodo con una señal producida por la placa de audio
audio.playback(fs, duration, amplitude, frequency, phase, 'SIN',
               loop=False)

osc.set_canal(1)
ins.write('DAT:SOU 1')
osc.set_canal=2
osc.get_canal()
voltsch1_1er = osc.datos() #Medir pantalla del osciloscopio
voltsch2_1er = osc.datos()
voltsch2 = np.array(voltsch2) #Convertir tupla en array

tiempo = np.linspace(volts[0][0], volts[0][-1], 2500)
pp.plot(amp * sg.sawtooth(2 * np.pi * freq * np.linspace(0,10,1000)))

pp.plot(voltsch2[0], voltsch2[1])
pp.plot(volts[0], Vin)


