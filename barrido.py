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
funcg=FunctionGeneratorAFG3021B('C034166')


device_list = sd.query_devices()

sd.default.device = 1, 3                  # [input, output] channels by default.
sd.default.channels = 1, 1                # Number of input/output channels.
sd.default.dtype = 'float32', 'float32'   # Data type used for input/output samples.
# sd.default.latency = 'high', 'high'     # Suggested input/output latency in seconds.
sd.default.samplerate = 46000         


#
#rm = visa.ResourceManager()
#
#rm.list_resources()


#oscil=rm.get_instrument('USB0::0x0699::0x0363::C065089::INSTR')
#oscil.write('ACQ:STATE 1')
#oscil.write('MEASU:IMM:TYP PERI')
#oscil.query('MEASU:IMM:VAL?')
#oscil.query('MEASU:IMM:TYP?')
#
#oscil.query('MEASU:IMM:SOU?')
#osc.medir()
#osc.apagar()
osc.medir_frec()
osc.xun='s'
osc.yun='Volts'
osc.canal=1

D=np.array(osc.datos())

funcg.set_amp(2)
amplitud=funcg.get_amp()
funcg.fase(1/3,'RAD') #preguntar esto, si asigne bien valores multiples a la propiedad
funcg.set_freq(1000,'Hz')
funcg.prende()
D=0
D=np.array(osc.datos())

pp.plot(D[0,:],D[1,:],'.')


osc.get_vscal(1)
osc.medir_vpp()

#CARACTERIZAR OUTPUT PLACA SONIDO



#audio.stop


#Barrido en frecuencias

#frecs=np.logspace(1,5.3, num=40)
#pp.plot(np.log(frecs),'.')

frecs=np.linspace(10000, 50000, 40)
b=1
for i in frecs:
    
    osc.set_tscal(1/i)
    audio.playback(fs=46000, duration=10, frequency=i, amplitude=1, phase=0, waveform='SIN', loop=False)
    time.sleep(5)
    #osc.auto()
    outputf.append(osc.medir_frec())
    outputv.append(osc.medir_vpp())
    print(b)
    b=b+1
    print(i)


outputV=[]
outputF=[]

for v in outputf:
    outputF.append(float(v))
for v in outputv:
    outputV.append(float(v))

pp.plot(frecs, outputF, '.')
pp.ylim(0,100000)
pp.plot(frecs, outputV, '.')
pp.xlim(0,100000)
pp.plot(outputF, outputV, '.')
pp.xlim(0,100000)

M=np.transpose([frecs,outputF,outputV])
np.savetxt('frecs_sampleo46k.txt', M, header='frec, outputf, outputv, sampleo 46kHz')



#Barrido en AMPLITUDES

outputf3=[]
outputa3=[]

amps3=np.linspace(2,4,10)

b=0
for i in amps3:
#    osc.set_vscal(2*2.7,1)
    osc.set_tscal(1/1000)
    audio.playback(fs=96000, duration=10, frequency=1000, amplitude=i, phase=0, waveform='SIN', loop=False)
    time.sleep(3)
    print(b)
    b=b+1
    print(i)
    outputf3.append(osc.medir_frec())
    outputa3.append(osc.medir_vpp())


audio.playback(fs=96000, duration=10, frequency=1000, amplitude=0.8, phase=0, waveform='SIN', loop=False)
#outputf.append(osc.medir_frec())
time.sleep(3)
osc.medir_vpp()
   
    
outputF3=[]
outputV3=[]

for v in outputf3:
    outputF3.append(float(v))
for v in outputa3:
    outputV3.append(float(v))

pp.plot(amps3, outputV3, '.')

pp.plot(amps, outputV, '.')

pp.plot(outputF, outputV, '.')
pp.xlim(0,1500)


ampu=np.concatenate((amps,amps2,amps3))
outF=np.concatenate((outputF,outputF2,outputF3))

pp.plot(outF,'.')

M=np.transpose([ampu,outF,outV])
np.savetxt('ampu_sampleo96k.txt', M, header='amp, outputf, outputv, sampleo 96kHz')
