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
osc=OsciloscopeTDS1002B('C065093')
funcg=FunctionGeneratorAFG3021B('C034167')


device_list = sd.query_devices()


sd.default.device = 5, 3                  # [input, output] device id from sd.query_devices() list
sd.default.channels = 1, 2                # Number of input/output channels.
sd.default.dtype = 'float32', 'float32'   # Data type used for input/output samples.
# sd.default.latency = 'high', 'high'     # Suggested input/output latency in seconds.
sd.default.samplerate = 96000         

osc.medir()
osc.apagar()
#osc.apagar()
osc.set_xun('s')
osc.get_xun()
osc.set_yun('Volts')
osc.get_yun()

osc.get_vscal(1)

osc.medir_amp('PK2')

#------------------------------------------------------------------------
#CARACTERIZAR OUTPUT PLACA SONIDO

#audio.stop


#BARRIDO EN FRECUENCIAS (OUTPUT)

#frecs=np.logspace(1,5.3, num=40)
#pp.plot(np.log(frecs),'.')
osc.set_canal(1)
outputv=[]
outputf=[]
frecs=np.linspace(10000, 80000, 20)
b=0
for i in frecs:
    
    osc.set_tscal(2/i)
    audio.playback(fs=96000, duration=10, frequency=i, amplitude=1, phase=0, waveform='SIN', loop=False)
    time.sleep(1)
    #osc.auto()
    outputf.append(osc.medir_frec())
    outputv.append(osc.medir_amp('PK2'))
#    outputf.append(osc.medir_frec())
#    outputv.append(osc.medir_amp('PK2'))
    print(b)
    b=b+1
    print(i)
    
#audio.playback(fs=96000, duration=10, frequency=1000, amplitude=1, phase=0, waveform='SIN', loop=False)
#
#
#time = np.linspace(start=0, stop=10, num=10*96000)
# sound = amplitude * np.sin(2 * np.pi * 1000 * time )
# 
#sd.play(data=sound,samplerate=96000,blocking=True,loop=False)
k=0
for v in outputf: #si falla lo anterior probar esto
    outputf(k)=float(v)
    k=k+1



M3=[]
v=[]
for s in np.transpose(M):
    for j in s:
        v.append(float(j))
    M3.append(v)
    v=[]


np.array(M)
np.savetxt('5-6frecs_sampleo96k.txt', M3, header='frec, outputf, outputv, sampleo 96kHz')

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

#BARRIDO EN AMPLITUDES (OUTPUT)

outputAMPf=[]
outputAMPv=[]

amps=np.linspace(0.1,3,20)

b=0
for i in amps:
#    osc.set_vscal(2*2.7,1)
    osc.set_tscal(1/1000)
    audio.playback(fs=96000, duration=10, frequency=1000, amplitude=i, phase=0, waveform='SIN', loop=False)
    time.sleep(1)
    print(b)
    b=b+1
    print(i)
    outputAMPf.append(float(osc.medir_frec()))
    outputAMPv.append(float(osc.medir_amp('PK2')))
#    outputAMPf3.append(osc.medir_frec())
#    outputa3.append(osc.medir_amp('PK2'))

M2=np.transpose([amps,outputAMPf,outputAMPv])
np.savetxt('5-6ampu_sampleo96k.txt', np.transpose(M2), header='amp, outputAMPf, outputAMPv, sampleo 96kHz')
    
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

#######
#BARRIDO EN FRECUENCIA (INPUT)
device_list = sd.query_devices()
duration = 3
fs = 96000

N = 5
frecs = np.linspace(60000, 100000, N)

funcg.set_amp(0.5)

DATAFRECS2 = []
i = 0
for f in frecs:
    print(f)
    funcg.set_frec(f,'Hz')
    time.sleep(1)
    crudo = np.transpose(sd.rec(frames=int(duration * fs),samplerate=fs,channels=2,
        blocking=True,dtype='float32'))
    DATAFRECS2.append(crudo[0])
    i=i+1
    print(i)
funcg.set_frec(frecs[0], 'Hz')


np.size(crudo[0])    

pp.plot(DATAFRECS[5])

prueba = sd.rec(frames=int(duration * fs),samplerate=fs,channels=2,
        blocking=False,dtype='float32') 
prueba[1][0]
pp.plot(prueba[1])

#M=np.transpose([ampu,outF,outV])

DATAFRECS = np.transpose
pp.plot(DATAFRECS[5])
np.savetxt('entrada_frecuencias2.txt', np.transpose(DATAFRECS2), header='3 seg, sampleo 96kHz, frecs = np.linspace(60000, 100000, 5)')


#######
#BARRIDO EN AMPLITUD (INPUT)

#outputv=[]
#outputf=[]
M = 5
amps = np.linspace(2, 2.5, M)

funcg.set_frec(1000,'Hz')
DATAMPS2 = []

j = 0
for a in amps:
    print(a)
    funcg.set_amp(a)
    time.sleep(1)
    CRUDO = np.transpose(sd.rec(frames=int(duration * fs),samplerate=fs,channels=2,
        blocking=True,dtype='float32'))
    DATAMPS2.append(CRUDO[0])
    j=j+1
    print(j)
    
pp.plot(DATAMPS2[4])
    
    
M=np.transpose([ampu,outF,outV])
np.savetxt('entrada_amplitudes2.txt', np.transpose(DATAMPS2), header='3 seg, 1 kHz, sampleo 96kHz, amps = np.linspace(0.1, 2, 10)')

FREQS = np.loadtxt('entrada_freqs.txt')
FREQS = np.transpose(FREQS)
pp.plot(time, FREQS[8])


AMPS = np.loadtxt('entrada_amps_2.txt')
AMPS = np.transpose(AMPS)

time = np.linspace(0, 4, 4*96000)
pp.plot(time, AMPS[0])
pp.plot(time, AMPS[4])

