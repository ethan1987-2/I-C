


class FunctionGeneratorAFG3021B():
    
    def __init__(self, serial):
        self.rm = visa.ResourceManager()        
        self.serial = serial
        self.ins = self.rm.open_resource('USB0::0x0699::0x0346::{}::INSTR'.format(serial))
        self.__canal='1' #self.ins.query('SOUR?')
        self.prende= self.ins.write('OUTP{}'.format(self.__canal)+':STAT ON')
        self.apaga= self.ins.write('OUTP{}'.format(self.__canal)+':STAT OFF')
#        self.__fase=self.ins.query('SOUR{}'.format(self.__canal)+':PHAS?')
#        self.__amp=self.ins.query('SOUR{}'.format(self.__canal)+':VOLT:LEV:IMM:AMPL?)
#        self.__frec=self.ins.query('SOUR{}'.format(self.__canal)+':FREQ?')
#        self.__offset=self.ins.query('SOUR{}'.format(self.__canal)+':VOLT:OFFS?')
    
    @property
    def canal(self):
        print('canal actual  (1 por defecto)')
        return self.__canal
    
    @canal.setter
    def canal(self,CH,set_value=True):    
        if not(CH in (1,2)):
            raise ValueError('El valor debe ser numérico 1 o 2')
        else:
            self.__canal=CH
        
    def set_amp(self, ampVpp):
        self.ins.write('SOUR{}'.format(self.canal)+':VOLT:LEV:IMM:AMPL '+str(ampVpp)+'VPP')
#        self.__amp=self.ins.query('SOUR{}'.format(self.canal)':VOLT:LEV:IMM:AMPL?)

    def get_amp(self):
#        print ('amplitud seleccionada {}'.format(self.__amp))        
        print('amplitud configurada en el instrumento')
        return self.ins.query('SOUR{}'.format(self.__canal)+':VOLT:LEV:IMM:AMPL?')
        
    amp=property(get_amp,set_amp)
        
    def set_freq(self, freq, frecun): #freq es un nro frecun=Hz, MHz, kHz
        self.ins.write('SOUR{}'.format(self.__canal)+':FREQ:FIX {}'.format(freq) + frecun)
        self.__frec=self.ins.query('SOUR{}'.format(self.__canal)+':FREQ?')
    
    def get_freq(self):
#        print ('frec seleccionada: {}'.format(self.__frec))        
        print('frecuencia configurada en el instrumento')
        return self.ins.query('SOUR{}'.format(self.__canal)+':FREQ:FIX?') 

    frec=property(get_freq,set_freq)
    
    def set_offset(self, offset):
        self.ins.write('SOUR{}'.format(self.__canal)+':VOLT:OFFS {}'.format(offset))
#        self.__offset=self.ins.query('SOUR{}'.format(self.__canal)+':VOLT:OFFS?')
        
    def get_offset(self):
#        print ('clavo de continua seleccionado: {}'.format(self.__offset))        
        print('clavo configurado en el instrumento')
        return self.ins.query('SOUR{}'.format(self.__canal)+':VOLT:OFFS?') 
    
    offset=property(get_offset,set_offset)   
    
    @property
    def fase(self):
#        print ('fase seleccionado: {}'.format(self.__fase))        
        print('fase configurado en el instrumento')
        return self.ins.query('SOUR{}'.format(self.__canal)+':PHAS:ADJ?')
    
    @fase.setter
    def fase(self,phi,phiUn):#phiUN= RAD va entre -1 y 1 , DEG va entre -180 y 180
        if phiUN==RAD:
            print('fase en RADs: el valor debe ser entre 1 y -1 y no PI y -PI')
            phi='{} PI'.format(phi) #PROBAR ESTO
        self.ins.write('SOUR{}'.format(self.__canal)+':PHAS:ADJ {}'.format(phi+' '+phiUn))
#        self.__fase=self.ins.query('SOUR{}'.format(self.__canal)+':PHAS:ADJ?')# -*- coding: utf-8 -*-
"""
Created on Tue May  7 06:25:41 2019

@author: KBZ
"""

