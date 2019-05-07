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
from claseGF import *
from claseOSC import *



frecs=np.linspace(100,500,50)
N=length(frecs)

osc=OsciloscopeTDS1002B('serial')
fg=FunctionGeneratorAFG3021B('serial')

osc.medir()
osc.xun='s'
osc.yun='Volts'
osc.canal=1

funcg.ampVPP=5
funcg.fase=(1/3,'RAD') #preguntar esto, si asigne bien valores multiples a la propiedad

funcg.prende

D=osc.datos


for i in N:
    funcg.frec=(i,'Hz')
    time.sleep(2)
    medidas(i)=osc.frec()
    time.sleep(2)
