# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 18:32:07 2019

@author: Publico
"""

import visa
import numpy as np
from matplotlib import pyplot as pp

rm = visa.ResourceManager()

class OsciloscopeTDS1002B():
      
    def __init__(self, serial):
        self.serial = serial
        self.osci = rm.open_resource('USB0::0x0699::0x0363::{}::INSTR'.format(serial))
        self.acquire = osci.write('ACQ:STATE 1')
    
    def idn(self):
        return self.osci.query('*IDN?')
        
    def data_points(self):
        YMU = float(osci.query('WFMP:YMU?'))
        YOF = float(osci.query('WFMP:YOF?'))
        YZE = float(osci.query('WFMP:YZERO?'))
        yn_dl= osci.query_binary_values('CURV?',datatype='B', is_big_endian=True)
        
        Yn = YZE + YMU*(np.array(yn_dl) - YOF)

        XIN=float(osci.query('WFMP:XIN?'))
        #XUN = osci.query('WFMP:XUN?')
        XZE = float(osci.query('WFMP:XZE?'))
        PT_OF = float(osci.query('WFMP:PT_OF?'))

        Xn = XZE + XIN*(np.linspace(1,2500,2500) - PT_OF)
        return (Xn,Yn)    
    
    def set_yscale(self, yscale, channel = 1):
        self.osci.write('CH'+str(channel)+':SCA'+str(yscale))
        
    def read_yscale(self, channel = 1):
        return self.osci.query('CH'+str(channel)+':SCA?')
    
    def set_xscale(self, xscale):
        self.osci.write('HOR:DEL:SCA'+ str(xscale))

OsciloscopeTDS1002B.osci

#oscil = OsciloscopeTDS1002B('C102220')
#oscil.idn()
#oscil.read_yscale(1)
#datos = oscil.data_points()


    
    
        
    