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
funcg=FunctionGeneratorAFG3021B('C034166')


#SIMULT EN ENTRADA

device_list = sd.query_devices()

sd.default.device = 1, 3                  # [input, output] device id from sd.query_devices() list
sd.default.channels = 2, 1                # Number of input/output channels.
sd.default.dtype = 'float32', 'float32'   # Data type used for input/output samples.
# sd.default.latency = 'high', 'high'     # Suggested input/output latency in seconds.
sd.default.samplerate = 46000         

funcg.prende()
funcg.set_frec(5,'kHZ') #ALTERNATIVA: segun hilario, si ponemos una onda generada a la fs de la placa de audio, si los canales no son simultaneos debería notarse una diferencia.
funcg.set_amp(2)
#funcg.set_fase(1/3,'RAD') #preguntar esto, si asigne bien valores multiples a la propiedad
#funcg.set_offset(4)

DATA=audio.record(fs=46000, duration=10)
#Con esta señal , deduzco, que se puede luego de la toma sumar los datos de los 2 canales y deberán estar desfasados si no son simultáneos , porque tendrán igual cantidad de puntos pero toman la onda en distintos puntos, luego se tendran 2 iguales pero desfasadas en 1 punto....el desfasaje es chico, por eso conviene que la frec sea alta

#Pensando mejor, me doy cuenta que si parto del GF con un señal a altisima fs, y tomo 2 canales supuestam NO simult , con apreciablemente distinta fs, entonces simplemente los primeros datos no serán iguales...acá hay que tener en cuenta que |T1-T2|/Tg debe ser menor q 1 o pueden repetirse los valores y no darnos cuenta del desfasaje
