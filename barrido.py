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

audio=AudioCard()
osc=OsciloscopeTDS1002B('C065089')
funcg=FunctionGeneratorAFG3021B('C034167')

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
osc.canal=2

D=np.array(osc.datos)

funcg.amp=2
amplitud=funcg.amp
funcg.amp
funcg.fase=(1/3,'RAD') #preguntar esto, si asigne bien valores multiples a la propiedad
funcg.set_freq(100,'Hz')
funcg.prende
D=0
D=np.array(osc.datos())

pp.plot(D[0,:],D[1,:],'.')

#medidas=np.zeros(N)
medidas=[]


osc.get_vscal(1)
osc.medir_vpp()

#CARACTERIZAR OUTPUT PLACA SONIDO

amplitud=1
osc.set_vscal(float(amplitud)*2,1)
frecs=np.linspace(10000,100000,21)
N=np.size(frecs)

outputF5=[]
outputV5=[]

#audio.stop

for i in frecs:
    
    osc.set_tscal(1/i)
    audio.playback(fs=46000, duration=15, frequency=i, amplitude=amplitud, phase=0, waveform='SIN', loop=False)
    #time.sleep(1)
    #osc.auto()
    time.sleep(2)
    outputF5.append(osc.medir_frec())
    outputV5.append(osc.medir_vpp())
    #time.sleep(1)

pp.plot(outputF5,outputV5,'.')
pp.plot(frecs, outputF5,'.')




##################################
for i in frecs:
    
    time.sleep(1)
    osc.set_tscal(1/i)
    osc.get
    time.sleep(1)
    funcg.set_freq(i,'Hz')
    time.sleep(1)
    M=osc.medir_frec()
    medidas.append(M)
    time.sleep(1)
