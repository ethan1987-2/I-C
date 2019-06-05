# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 13:43:30 2019

@author: KBZ
"""
#SIMULTANEIDAD EN PLACA DE AUDIO

import time
import visa
import numpy as np
from matplotlib import pyplot as pp
#antes de importar clases de archivos en el mismo carpeta hay q correr esos archivos
from claseGF import *
from claseOSC import *
from Sound_card_class import *
import sounddevice as sd 

audio=AudioCard()
funcg=FunctionGeneratorAFG3021B('C036492')

duration = 0.1
fs = 96000
#SIMULT EN ENTRADA

device_list = sd.query_devices()

sd.default.device = 2, 3                  # [input, output] device id from sd.query_devices() list
sd.default.channels = 1, 1                # Number of input/output channels.
sd.default.dtype = 'float32', 'float32'   # Data type used for input/output samples.
# sd.default.latency = 'high', 'high'     # Suggested input/output latency in seconds.
sd.default.samplerate = fs         

funcg.prende()
funcg.set_frec(100,'HZ') #ALTERNATIVA: segun hilario, si ponemos una onda generada a la fs de la placa de audio, si los canales no son simultaneos debería notarse una diferencia.
funcg.set_amp(2)

#Con esta señal , deduzco, que se puede luego de la toma sumar los datos de los 2 canales y deberán estar desfasados si no son simultáneos , porque tendrán igual cantidad de puntos pero toman la onda en distintos puntos, luego se tendran 2 iguales pero desfasadas en 1 punto....el desfasaje es chico, por eso conviene que la frec sea alta
#Pensando mejor, me doy cuenta que si parto del GF con un señal a altisima fs, y tomo 2 canales supuestam NO simult , con apreciablemente distinta fs, entonces simplemente los primeros datos no serán iguales...acá hay que tener en cuenta que |T1-T2|/Tg debe ser menor q 1 o pueden repetirse los valores y no darnos cuenta del desfasaje

tiempo = np.linspace(0,duration,fs*duration)
sen2ch = sd.rec(frames=int(duration * fs),
                           samplerate=fs,
                           channels=2,
                           blocking=False,
                           dtype='float32')

sen1ch = np.transpose(sen1ch)
pp.plot(tiempo, sen2ch)
pp.plot(tiempo, DATA)
pp.plot(tiempo, 100*DIFF)
DIFF = DATA[0]-DATA[1]


M=np.transpose([frecs,outputF,outputV])
np.savetxt('simult_seno.txt', sen2ch, header='frec 100Hz, sampleo 96 kS')
