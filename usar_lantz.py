# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 16:35:48 2019

@author: Publico
"""

import visa
import numpy as np
from matplotlib import pyplot as pp
from lantz import MessageBasedDriver, Feat, ureg
from lantz.core import mfeats

class Osciloscopio(MessageBasedDriver):
    
    def idn(self):
        return self.query('*IDN?')
    
    def curve(self): #Devuelve tupla de arrays: tiempo y voltaje
        YMU = float(self.query('WFMP:YMU?'))
        YOF = float(self.query('WFMP:YOF?'))
        YZE = float(self.query('WFMP:YZERO?'))
        yn_dl = self.resource.query_binary_values('CURV?',datatype='B', is_big_endian=True)
        
        Yn = YZE + YMU*(np.array(yn_dl) - YOF)

        XIN=float(self.query('WFMP:XIN?'))
        #XUN = self.osci.query('WFMP:XUN?')
        XZE = float(self.query('WFMP:XZE?'))
        PT_OF = float(self.query('WFMP:PT_OF?'))

        Xn = XZE + XIN*(np.linspace(1,2500,2500) - PT_OF)
        return (Xn,Yn)    
    
    def set_yscale(self, yscale, channel = 1):
        self.write('CH'+str(channel)+':SCA'+str(yscale))
        
    def get_yscale(self, channel = 1):
        return self.query('CH'+str(channel)+':SCA?')
    
    def set_xscale(self, xscale):
        self.write('HOR:DEL:SCA'+ str(xscale))

class FunctionGenerator(MessageBasedDriver):
    
    def set_amp(self, amp):
        self.write('SOUR1:VOLT:LEV:IMM:AMPL '+str(amp)+'VPP')
        
    def set_freq(self, freq):
        self.write('SOUR1:FREQ {}'.format(freq))
        
    def set_offset(self, offset):
        self.write('SOUR1:VOLT:OFFSET {}'.format(offset))
        
    def get_freq(self):
        return self.query('SOUR1:FREQ?') 
        

osci = Osciloscopio('USB0::0x0699::0x0363::C065089::INSTR')
osci.initialize()

#osci.finalize()

gf = FunctionGenerator('USB0::0x0699::0x0346::C034198::INSTR')
gf.initialize()

def barrido(osc, genf, fmin, fmax, cantidad):
    frecuencias = np.linspace(fmin, fmax, cantidad)
    for frec in frecuencias:
        genf.set_freq(frec)
        
    
    
    

