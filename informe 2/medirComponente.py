# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 11:28:05 2019

@author: KBZ
"""

#MI IDEA ES MEDIR UN DIODO...ASI FACIL Y CORTA, O HASTA SI CARADUREAMOS ALGUNA RESISTENCIA NOMÁS, PREGUNTEMOS A VER Q DICEN

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


#PLACA DE AUDIO COMO GF

#ESCALERA DE VOLTAJE

fsamp=46000
amps=np.linspace(0.1,2,0.2)
b=0
d=10/fsamp
osc.set_tscal(d/100)
outputVout=[]
outputVin=[]


for i in amps:
    audio.playback(fs=fsamp, duration=d, frequency=.5/d, amplitude=i, phase=0, waveform='SQR', loop=False)
    osc.set_canal(1) #CANAL 1 MIDE EL COMPONENTE
    outputVout.append(float(osc.medir_amp('CRM')))
    #    outputv.append(osc.medir_vpp())
    time.sleep(1)
    osc.set_canal(2)  #CANAL 2 MIDE LA PLACA
    outputVin.append(float(osc.medir_amp('CRM')))
    print(b)
    b=b+1
        #LA ALTERNATIVA ES SUPONER QUE EL VOLT ENTRADA SIGUE LA FORMA IDEAL
#    outputVin=i*CALIBRACION


M=np.transpose([ampu,outF,outV])
np.savetxt('ampu_sampleo96k.txt', M, header='amp, outputf, outputv, sampleo 96kHz')


#RESPUESTA EN FRECUENCIA

outputVout=[]
outputFout=[]
frecs=np.linspace(10000, 50000, 40)
b=0
for i in frecs:
    
    osc.set_tscal(1/i)
    audio.playback(fs=46000, duration=10, frequency=i, amplitude=1, phase=0, waveform='SIN', loop=False)
    time.sleep(5)
    #osc.auto()
    outputFout.append(float(osc.medir_frec()))
    time.sleep(1)
    outputVout.append(float(osc.medir_amp('CRM')))
#    outputf.append(osc.medir_frec())
#    outputv.append(osc.medir_vpp())
    print(b)
    b=b+1
    print(i)
    
M=np.transpose([ampu,outF,outV])
np.savetxt('ampu_sampleo96k.txt', M, header='amp, outputf, outputv, sampleo 96kHz')
    
#   ---------------------------------------------------------------- AL PARECER ES MAS SIMPLE LO SGTE
# porque andar cuidando la señal q produce la placa como entrada es trabajo adicional....acá directamente le creo al GF
    
#PLACA DE AUDIO COMO OSC
    
funcg.prende()
funcg.set_frec(5,'kHZ')
funcg.set_amp(2)
#funcg.set_fase(1/3,'RAD') #preguntar esto, si asigne bien valores multiples a la propiedad
#funcg.set_offset(4)

#BARRIDO EN AMPLITUD (INPUT)


amps=np.linspace(10000, 50000, 40) #anotar la frec tmb!!
b=0

for i in amps:
    funcg.set_amp(i)
    time.sleep(2)
    DATA=audio.record(fs=46000, duration=10)
    print(b)
    b=b+1
    print(i)  

M=np.transpose([ampu,outF,outV])
np.savetxt('ampu_sampleo96k.txt', M, header='amp, outputf, outputv, sampleo 96kHz')

#BARRIDO EN FRECUENCIA(INPUT)

frecs=np.linspace(10000, 50000, 40) #anotar la amp!!
b=0
for i in frecs:
    funcg.set_frec(i,'Hz')
    time.sleep(2)
    DATA=audio.record(fs=46000, duration=10)
    print(b)
    b=b+1
    print(i)
    
    
M=np.transpose([ampu,outF,outV])
np.savetxt('ampu_sampleo96k.txt', M, header='amp, outputf, outputv, sampleo 96kHz')


