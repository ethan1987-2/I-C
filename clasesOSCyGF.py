# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 18:32:07 2019

@author: Publico
"""

import visa
import numpy as np
from matplotlib import pyplot as plot



class OsciloscopeTDS1002B():
      
    def __init__(self, serial):
        self.rm = visa.ResourceManager()        
        self.serial = serial
        self.osci = self.rm.open_resource('USB0::0x0699::0x0363::{}::INSTR'.format(serial))
        self.acquire = self.osci.write('ACQ:STATE 1')
    
    def idn(self):
        return self.osci.query('*IDN?')
        
    def data_points(self):
        YMU = float(self.osci.query('WFMP:YMU?'))
        YOF = float(self.osci.query('WFMP:YOF?'))
        YZE = float(self.osci.query('WFMP:YZERO?'))
        yn_dl = self.osci.query_binary_values('CURV?',datatype='B', is_big_endian=True)
        
        Yn = YZE + YMU*(np.array(yn_dl) - YOF)

        XIN=float(self.osci.query('WFMP:XIN?'))
        #XUN = self.osci.query('WFMP:XUN?')
        XZE = float(self.osci.query('WFMP:XZE?'))
        PT_OF = float(self.osci.query('WFMP:PT_OF?'))

        Xn = XZE + XIN*(np.linspace(1,2500,2500) - PT_OF)
        return (Xn,Yn)    
    
    def set_yscale(self, yscale, channel = 1):
        self.osci.write('CH'+str(channel)+':SCA'+str(yscale))
        
    def get_yscale(self, channel = 1):
        return self.osci.query('CH'+str(channel)+':SCA?')
    
    def set_xscale(self, xscale):
        self.osci.write('HOR:DEL:SCA'+ str(xscale))
        
    def get_freq(self):
        self.osci.query()
        
class FunctionGeneratorAFG3021B():
    
    def __init__(self, serial):
        self.rm = visa.ResourceManager()        
        self.serial = serial
        self.fgen = self.rm.open_resource('USB0::0x0699::0x0346::{}::INSTR'.format(serial))
        #self.fgen.turn_on = self.fgen.write('OUTP1:STAT 1')
        
    def set_amp(self, amp):
        self.fgen.write('SOUR1:VOLT:LEV:IMM:AMPL '+str(amp)+'VPP')
        
    def set_freq(self, freq):
        self.fgen.write('SOUR1:FREQ {}'.format(freq))
        
    def get_freq(self):
        return self.fgen.query('SOUR1:FREQ?') 
        
    def set_offset(self, offset):
        self.fgen.write('SOUR1:VOLT:OFFSET {}'.format(offset))
    
    
    
osc = OsciloscopeTDS1002B('C065089')
#OsciloscopeTDS1002B.osci
#oscil.idn()
#oscil.read_yscale(1)
#datos = oscil.data_points()


    
    
        
    