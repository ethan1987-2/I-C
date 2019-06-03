# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 18:32:07 2019

@author: Publico
"""
import time
import visa
import numpy as np
from matplotlib import pyplot as pp


class OsciloscopeTDS1002B():
      
    def __init__(self,serial):
        self.rm = visa.ResourceManager()        
        self.serial = serial
        self.ins = self.rm.open_resource('USB0::0x0699::0x0363::{}::INSTR'.format(serial))
        self.medir= self.ins.write('ACQ:STATE 1')
        self.ins.write('WFMP:BYT_N'+' '+'1')
        self.ins.write('WFMP:BIT_N'+' '+'8')
        self.ins.write('WFMP:BN_F'+' '+'RP')
        self.ins.write('WFMP:BYT_O'+' '+'MSB')
        self.ins.write('WFMP:ENC'+' '+'BIN')
        

    def apagar(self): # detener osciloscopio
        self.ins.write('ACQ:STATE 0')
        
    def auto(self): # ejecutar autoconfiguracion del osciloscopio
        self.ins.write('AUTOS EXEC')
    
    def set_tscal(self, tsca): #yun= Volts,VV, U: nro divisiones, A:amps,AA, VA:volamps, dB
        self.ins.write('HOR:MAI:SCA {}'.format(tsca))
        
    def get_tscal(self):
        return self.ins.query('HOR:MAI:SCA?')

    def set_vscal(self, vsca,CH): #yun= Volts,VV, U: nro divisiones, A:amps,AA, VA:volamps, dB
        self.ins.write('CH{}'.format(CH)+':SCA'+' '+str(vsca))
        
    def get_vscal(self,CH):
        return self.ins.query('CH{}'.format(CH)+':SCA?')

    def idn(self):
        return self.ins.query('*IDN?')

    def get_canal(self):
        print('canal de toma de datos de curva configurado en instrumento:')
        return self.ins.query('DAT:SOU?')
    
    def set_canal(self,CH,set_value=True): #CH=CH1 o CH2
        if not CH in (1,2):
            raise ValueError('El valor debe ser numérico 1 o 2')
        else:
            self.ins.write('DAT:SOU'+' '+str(CH))
            self.ins.write('MEASU:IMM:SOU'+' '+str(CH))
       
  
    def set_yun(self, yun): #yun= Volts,VV, U: nro divisiones, A:amps,AA, VA:volamps, dB
        self.ins.write('WFMP:YUN'+' '+yun)
        
    def get_yun(self):
        return self.ins.query('WFMP:YUN?')

    def set_xun(self, xun):  #xun= Hz, s
         self.ins.write('WFMP:XUN'+' '+xun)

    def get_xun(self):
        return self.ins.query('WFMP:XUN?')

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
    
        
    def medir_frec(self): #un método
        self.ins.write('MEASU:IMM:TYP FREQ')
        time.sleep(1)
        return self.ins.query('MEASU:IMM:VAL?').rstrip(self.ins.query('MEASU:IMM:VAL?')[-2:])
    
    def medir_amp(self,medida): #{ FREQuency | MEAN | PK2pk | CRMs | MINImum | MAXImum |   esto no es amp: RISe | FALL |PWIdth | NWIdth }
        self.ins.write('MEASU:IMM:TYP {}'.format(medida))
        time.sleep(1)
        return self.ins.query('MEASU:IMM:VAL?').rstrip(self.ins.query('MEASU:IMM:VAL?')[-2:])
     
        
############################################################



