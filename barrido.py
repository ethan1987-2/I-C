# -*- coding: utf-8 -*-
"""
Created on Tue May  7 06:19:55 2019

@author: KBZ
"""
#from folder.file import Class    #esto importa una clase o funcion desde el archivo file en subcarpeta folder
#
#from folder import file #esto importa todo la subcarpeta folder (libreria)
#clase=file.Class   #luego selecciono la clase Class de la libreria folder importada

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
osc=OsciloscopeTDS1002B('C065087')
funcg=FunctionGeneratorAFG3021B('C036492')


device_list = sd.query_devices()

sd.default.device = 1, 3                  # [input, output] device id from sd.query_devices() list
sd.default.channels = 1, 1                # Number of input/output channels.
sd.default.dtype = 'float32', 'float32'   # Data type used for input/output samples.
# sd.default.latency = 'high', 'high'     # Suggested input/output latency in seconds.
sd.default.samplerate = 46000         

osc.medir()
#osc.apagar()
osc.xun='s'
osc.yun='Volts'


osc.get_vscal(1)
osc.medir_amp('PK2')

#CARACTERIZAR OUTPUT PLACA SONIDO

#audio.stop


#BARRIDO EN FRECUENCIAS

#frecs=np.logspace(1,5.3, num=40)
#pp.plot(np.log(frecs),'.')

outputv=[]
outputf=[]
frecs=np.linspace(10000, 50000, 40)
b=0
for i in frecs:
    
    osc.set_tscal(1/i)
    audio.playback(fs=46000, duration=10, frequency=i, amplitude=1, phase=0, waveform='SIN', loop=False)
    time.sleep(5)
    #osc.auto()
    outputf.append(float(osc.medir_frec()))
    outputv.append(float(osc.medir_amp('PK2')))
#    outputf.append(osc.medir_frec())
#    outputv.append(osc.medir_amp('PK2'))
    print(b)
    b=b+1
    print(i)

for v in outputf: #si falla lo anterior probar esto
    outputf(v)=float(v)
    outputv(v)=float(v)
    
    
M=np.transpose([frecs,outputF,outputV])
np.savetxt('frecs_sampleo46k.txt', M, header='frec, outputf, outputv, sampleo 46kHz')

#outputV=[]
#outputF=[]
#
#for v in outputf:
#    outputF.append(float(v))
#for v in outputv:
#    outputV.append(float(v))

pp.plot(frecs, outputF, '.')
pp.ylim(0,100000)
pp.plot(frecs, outputV, '.')
pp.xlim(0,100000)
pp.plot(outputF, outputV, '.')
pp.xlim(0,100000)





#Barrido en AMPLITUDES

outputf=[]
outputv=[]

amps=np.linspace(2,4,10)

b=0
for i in amps:
#    osc.set_vscal(2*2.7,1)
    osc.set_tscal(1/1000)
    audio.playback(fs=96000, duration=10, frequency=1000, amplitude=i, phase=0, waveform='SIN', loop=False)
    time.sleep(3)
    print(b)
    b=b+1
    print(i)
    outputf.append(float(osc.medir_frec()))
    outputv.append(float(osc.medir_amp('PK2')))
#    outputf3.append(osc.medir_frec())
#    outputa3.append(osc.medir_amp('PK2'))

M=np.transpose([ampu,outF,outV])
np.savetxt('ampu_sampleo96k.txt', M, header='amp, outputf, outputv, sampleo 96kHz')
    
#outputF3=[]
#outputV3=[]
#
#for v in outputf3:
#    outputF3.append(float(v))
#for v in outputa3:
#    outputV3.append(float(v))

pp.plot(amps3, outputV3, '.')

pp.plot(amps, outputV, '.')

pp.plot(outputF, outputV, '.')
pp.xlim(0,1500)


#ampu=np.concatenate((amps,amps2,amps3))
#outF=np.concatenate((outputF,outputF2,outputF3))

pp.plot(outF,'.')

#------------------------------------------------------------------------

#CARACTERIZAR INPUT PLACA SONIDO

funcg.prende()
funcg.set_frec(5,'kHZ')
funcg.set_amp(2)
funcg.set_fase(1/3,'RAD') #preguntar esto, si asigne bien valores multiples a la propiedad
funcg.set_offset(4)


#BARRIDO EN FRECUENCIA(INPUT)
device_list = sd.query_devices()
duration = 4
fs = 96000

N = 10
frecs = np.linspace(100, 100000, N)
d = 0
DATAA = np.zeros([N, int(duration*fs)])

for i in frecs:
    funcg.set_frec(i,'Hz')
    time.sleep(1)
    DATAA[d] = np.transpose(sd.rec(frames=int(duration * fs),samplerate=fs,channels=1,
        blocking=True,dtype='float32'))
    d=d+1
        
M=np.transpose([ampu,outF,outV])
np.savetxt('entrada_freqs.txt', np.transpose(DATAA), header='4 seg, sampleo 96kHz, frecs = np.linspace(100, 100000, 10)')

DATA = np.transpose
pp.plot(DATA[1])
#BARRIDO EN AMPLITUD (INPUT)

outputv=[]
outputf=[]
DATAMPS = np.zeros([10, int(duration*fs)])
amps = np.linspace(0.1, 2, 10)
b=0
funcg.set_frec(1000,'Hz')
for i in amps:
    funcg.set_amp(i)
    time.sleep(2)
    DATAMPS[b] = np.transpose(sd.rec(frames=int(duration * fs),samplerate=fs,channels=1,
        blocking=True,dtype='float32'))
    print(b)
    b=b+1
    print(i)
    
    
M=np.transpose([ampu,outF,outV])
np.savetxt('entrada_amps_2.txt', np.transpose(DATAMPS), header='4 seg, 1 kHz, sampleo 96kHz')
