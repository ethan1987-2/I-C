# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""

import numpy as np
import sounddevice as sd
import sys
import argparse
import queue
import sys
from matplotlib import pyplot as pp

devices = sd.query_devices() #Ver dispositivos
fs = 45000 #Frecuencia de muestreo
duration = 1  # seconds
sd.default.device = [2, None] #Canal de [IN, OUT] usado por default

myrecording = sd.rec(int(duration * fs), samplerate=fs, mapping=[1]) #Graba entrada y crea array numpy

pp.plot(np.linspace(0,1,45000,np.size(myrecording)),myrecording)

sd.play(myrecording, samplerate=None, mapping=None, blocking=False, loop=False) #Recibe array numpy y reproduce su sonido

#stream = sd.Stream(channels=1) #arreglar esto!!!
#
#stream.start()
#stream.stop()
#stream.active
#stream.device
#stream.dtype
#A=stream.read(10000)
#a=A[0]
#
#pp.plot(a)
