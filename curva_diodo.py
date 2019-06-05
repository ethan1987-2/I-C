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
osc=OsciloscopeTDS1002B('C065093')
funcg=FunctionGeneratorAFG3021B('C036492')


fs = 96000
duration = 100
frequency = 100
amplitude = 1
phase = 0
RES_Ohm = 1165

sd.query_devices()
#Alimentar al diodo con una señal producida por la placa de audio
audio.playback(fs, duration, amplitude, frequency, phase, 'RAMP',
               loop=False)

osc.set_canal(1)
osc.set_canal(2)
osc.get_canal()
voltsch1_1er = osc.datos() #Medir pantalla del osciloscopio
prueba= osc.datos() 
voltsch2_1er = osc.datos()

#pp.plot(amp * sg.sawtooth(2 * np.pi * freq * np.linspace(0,10,1000)))
np.max(voltsch1_1er[1])-np.min(voltsch1_1er[1])

voltsch1_1er_corr = voltsch1_1er[1]-np.mean(voltsch1_1er[1])

pp.plot(voltsch1_1er[0], voltsch1_1er[1])
pp.plot(prueba[0], prueba[1])

pp.plot(voltsch1_1er[0], voltsch1_1er[1])
pp.plot(voltsch1_1er[1][350:850], voltsch2_1er[1][350:850])
pp.plot(voltsch1_1er[1], voltsch2_1er[1])
corriente_1er = voltsch2_1er[1]/RES_Ohm 
pp.plot(voltsch1_1er[1][350:850], corriente_1er[350:850])
##########

osc.set_canal(1)
osc.set_canal(2)
osc.get_canal()
voltsch1_2do = osc.datos() #Medir pantalla del osciloscopio
prueba= osc.datos() 
voltsch2_2do = osc.datos()

pp.plot(voltsch1_2do[0], voltsch1_2do[1])
pp.plot(voltsch2_2do[0], voltsch2_2do[1])
pp.plot(voltsch1_2do[1][800:1300], voltsch2_2do[1][800:1300])
pp.plot(voltsch1_2do[1], voltsch2_2do[1])
corriente_2do = voltsch2_2do[1]/RES_Ohm 
pp.plot(voltsch1_2do[1][800:1300], corriente_2do[800:1300])

np.savetxt('diodoch1_2do.txt', np.transpose(voltsch1_2do), header='freq 100 Hz, amp 1, RES 1165, sampleo 96kHz')









