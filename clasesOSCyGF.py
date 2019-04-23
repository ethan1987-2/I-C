# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 18:32:07 2019

@author: Publico
"""

import visa
import numpy as np
from matplotlib import pyplot as pp

rm1=visa.ResourceManager()
rm1.list_resources()

class OsciloscopeTDS1002B():
      
    def __init__(self, serial,xun='s',yun='Volts'):
        self.rm = visa.ResourceManager()        
        self.serial = serial
        self.ins = self.rm.open_resource('USB0::0x0699::0x0363::{}::INSTR'.format(serial))
        self.medir= self.ins.write('ACQ:STATE 1')
        self.apagar= self.ins.write('ACQ:STATE 0')
        self.ins.write('WFMP:BYT_N'+' '+'1')
        self.ins.write('WFMP:BIT_N'+' '+'8')
        self.ins.write('WFMP:BN_F'+' '+'RP')
        self.ins.write('WFMP:BYT_O'+' '+'MSB')
        self.ins.write('WFMP:ENC'+' '+'BIN')
        self.set_xun(xun)
        self.set_yun(yun)
        

    def idn(self):
        return self.ins.query('*IDN?')

    @property
    def canal(self):
        return self.__canal
    
    @canal.setter
    def canal(self,CH,set_value=True):
        self.ins.write('DAT:SOU'+' '+str(CH))
        self.ins.write('MEASU:IMM:SOU'+' '+str(CH))
    
    
    @canal.getter
    def canal(self):
        self.ins.query('DAT:SOU?')
  
    def set_yun(self, yun): #yun= Volts,VV, U: nro divisiones, A:amps,AA, VA:volamps, dB
        self.__yun=self.ins.write('WFMP:YUN'+' '+yun)
        
    def get_yun(self):
        return self.ins.query('WFMP:YUN?')

    yun=property(get_yun,set_yun)
    
    def set_xun(self, xun):  #xun= Hz, s
         self.__xun=self.ins.write('WFMP:XUN'+' '+xun)

    def get_xun(self):
        return self.ins.query('WFMP:XUN?')

    xun=property(get_xun,set_xun)
    
    
    def datos(self):
        YMU = float(self.ins.query('WFMP:YMU?'))
        YOF = float(self.ins.query('WFMP:YOF?'))
        YZE = float(self.ins.query('WFMP:YZE?'))
        
        yn_dl = self.ins.query_binary_values('CURV?',datatype='B', is_big_endian=True)
        
        Yn = YZE + YMU*(np.array(yn_dl) - YOF)

        XIN=float(self.ins.query('WFMP:XIN?'))
        XZE = float(self.ins.query('WFMP:XZE?'))
        PT_OF = float(self.ins.query('WFMP:PT_OF?'))

        Xn = XZE + XIN*(np.linspace(1,2500,2500) - PT_OF)
        return (Xn,Yn)    
        
    def frec(self):
        self.ins.write('MEASU:IMM:TY FREQ')
        return self.ins.query('MEASU:IMM:VAL?')
        
        
        
        
        
        
############################################################
class FunctionGeneratorAFG3021B():
    
    def __init__(self, serial):
        self.rm = visa.ResourceManager()        
        self.serial = serial
        self.ins = self.rm.open_resource('USB0::0x0699::0x0346::{}::INSTR'.format(serial))
        self.prende= self.ins.write('OUTP1:STAT 1')
        self.apaga= self.ins.write('OUTP1:STAT 0')
        
    
    @property
    def canal(self):
         return self.__canal
    
    @canal.setter
    def canal(self,CH,set_value=True):
        self.canal=CH
    
    @canal.getter
    def canal(self):
        return self
        
    def set_amp(self, ampVpp):
        self.ins.write('SOUR{}'.format(self.canal)':VOLT:LEV:IMM:AMPL '+str(ampVpp)+'VPP')

    def get_amp(self):
        self.ins.query('SOUR{}'.format(self.canal)':VOLT:LEV:IMM:AMPL?)
        
    self.ampVPP=property(get_amp,set_amp)
        
    def set_freq(self, freq, frecun): #freq es un nro frecun=Hz, MHz, kHz
        self.ins.write('SOUR{}'.format(self.canal)':FREQ:FIX {}'.format(freq) + frecun)
        
    def get_freq(self):
        return self.ins.query('SOUR{}'.format(self.canal)':FREQ:FIX?') 

    self.frec=property(get_freq,set_freq)
    
    def set_offset(self, offset):
        self.ins.write('SOUR{}'.format(self.canal)':VOLT:OFFSET {}'.format(offset))
        
    def get_offset(self):
        return self.ins.query('SOUR{}'.format(self.canal)':VOLT:OFFSET?') 
    
    self.offset=property(get_offset,set_offset)   
    
    @property
    def fase(self):
        return self.fase
    
    @fase.setter
    def fase(self,phi,phiUn):#phiUN= RAD, DEG
        self.ins.write('SOUR{}'.format(self.canal)+':PHAS {}'.format(phi) + phiUn)
    
    @fase.getter
    def fase(self):
        self.ins.query('SOUR{}'.format(self.canal)+':PHAS?')
    
osc = OsciloscopeTDS1002B('C108012') #CAMBIAR!!!

osc.medir
osc.xun='s'
osc.yun='Volts'
osc.canal=2
frecVal=osc.frec()

(X,Y)=osc.datos
[X,Y]=np.array([X,Y])


pp.plot(X,Y,'.')
pp.title('Captura de pantalla')
pp.xlabel(osc.xun)
pp.ylabel(osc.yun)
        
     


funcg=FunctionGeneratorAFG3021B('C108012') #CAMBIAR!!!

funcg.ampVPP=5
funcg.fase=(np.pi/3,'RAD') #preguntar esto, si asigne bien valores multiples a la propiedad
funcg.frec=(1,'kHz')
funcg.prende

    
osc.ins.query('MEASU:IMM?')
osc.ins.query('DAT:SOU?')
osc.yun='A'

osc.ins.write('WFMP:YUN dB')
osc.ins.query('WFMP:YUN?')
