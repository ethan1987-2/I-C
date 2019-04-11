# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 16:46:52 2019

@author: Publico
"""

import visa
import numpy as np
from matplotlib import pyplot as pp

rm = visa.ResourceManager('C:\\Windows\\system32\\visa64.dll')
instrumentos=rm.list_resources()
funcgen=rm.open_resource('USB0::0x0699::0x0346::C034165::INSTR')

funcgen.query('OUTP1:STAT?') #Ve si esta el canal prendido

funcgen.query('SOUR1:VOLT:UNIT?') #Unidades de output

funcgen.query('SOUR1:VOLT?') #Amplitud de output

funcgen.query('SOUR1:VOLT:LEV:IMM:AMPL 1VPP') #Setear amplitud de output, unidades VPP o VRMS

funcgen.query('SOUR1:FREQ?') #Frecuencia de output en Hz

funcgen.query('SOUR1:FREQ 10000Hz') #Setear frecuencia de output, unidades Hz, kHz, MHz

funcgen.query('SOUR1:VOLT:OFFSET?') #Offset de output en V

funcgen.query('SOUR1:VOLT:OFFSET 0') #Setear offset de output en V

funcgen.query('SOUR1:FUNC:SHAP SQU') #Setear forma de onda (SQU, SIN, RAMP) 
