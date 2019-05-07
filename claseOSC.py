# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 18:32:07 2019

@author: Publico
"""



class OsciloscopeTDS1002B():
      
    def __init__(self,serial):
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
#        self.__xun=self.ins.query('WFMP:XUN?')
#        self.__yun=self.ins.query('WFMP:YUN?')
#        self.canalinic=self.ins.query('DAT:SOU?')
#        self.__canal=self.canalinic[:3]
        

    def idn(self):
        return self.ins.query('*IDN?')

    @property
    def canal(self):
        print('canal de toma de datos de curva configurado en instrumento:')
        return self.ins.query('DAT:SOU?')
    
    @canal.setter
    def canal(self,CH,set_value=True): #CH=CH1 o CH2
        if not CH in (1,2):
            raise ValueError('El valor debe ser numérico 1 o 2')
        else:
            self.ins.write('DAT:SOU'+' '+str(CH))
            self.ins.write('MEASU:IMM:SOU'+' '+str(CH))
       
  
    def set_yun(self, yun): #yun= Volts,VV, U: nro divisiones, A:amps,AA, VA:volamps, dB
        self.ins.write('WFMP:YUN'+' '+yun)
        
    def get_yun(self):
        return self.ins.query('WFMP:YUN?')

    yun=property(get_yun,set_yun)
    
    def set_xun(self, xun):  #xun= Hz, s
         self.ins.write('WFMP:XUN'+' '+xun)

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
        return np.array([Xn,Yn])
    
        
    def medir_frec(self): #un método
        self.ins.write('MEASU:IMM:TY FREQ')
        return self.ins.query('MEASU:IMM:VAL?')
        
        
############################################################



