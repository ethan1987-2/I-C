import visa
import numpy as np
from matplotlib import pyplot as pp


class FunctionGeneratorAFG3021B():
    
    def __init__(self, serial):
        self.rm = visa.ResourceManager()        
        self.serial = serial
        self.ins = self.rm.open_resource('USB0::0x0699::0x0346::{}::INSTR'.format(serial))
        self.__canal='1' #self.ins.query('SOUR?')

    def prende(self): # habilita la salida del canal seleccionado       
        self.ins.write('OUTP{}'.format(self.__canal)+':STAT 1')
        
    def apaga(self): # corta la salida del canal seleccionado
        self.ins.write('OUTP{}'.format(self.__canal)+':STAT 0')
    
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


    def get_amp(self):  
        print('amplitud configurada en el instrumento')
        return self.ins.query('SOUR{}'.format(self.__canal)+':VOLT:LEV:IMM:AMPL?')
       
    def set_frec(self, freq, frecun): #freq es un nro frecun=Hz, MHz, kHz
        self.ins.write('SOUR{}'.format(self.__canal)+':FREQ:FIX {}'.format(freq) + frecun)
    
    def get_frec(self):
        print('frecuencia configurada en el instrumento')
        return self.ins.query('SOUR{}'.format(self.__canal)+':FREQ:FIX?') 
   
    def set_offset(self, offset): # en voltios
        self.ins.write('SOUR{}'.format(self.__canal)+':VOLT:OFFS {}'.format(offset))
        
    def get_offset(self):
        print('clavo configurado en el instrumento')
        return self.ins.query('SOUR{}'.format(self.__canal)+':VOLT:OFFS?') 

    def get_fase(self):
        print('fase configurado en el instrumento')
        return self.ins.query('SOUR{}'.format(self.__canal)+':PHAS:ADJ?')
    
    def set_fase(self,phi,phiUn):#phiUN= RAD va entre -1 y 1 , DEG va entre -180 y 180
        if phiUn=='RAD':
            print('fase en RADs: el valor debe ser entre 1 y -1 y no PI y -PI, se autocorregirá y enviará')
            phi='{} PI'.format(phi) #PROBAR ESTO
        self.ins.write('SOUR{}'.format(self.__canal)+':PHAS:ADJ {}'.format(phi+' '+phiUn))
        
    def set_forma(self,forma):#string = {SINusoid|SQUare|PULSe|RAMP|PRNoise|DC|SINC|GAUSsian|LORentz|ERISe|EDECay|HAVersine|USER[1]|USER2|USER3|USER4|EMEMory|EFILe}
        self.ins.write('SOUR{}'.format(self.__canal)+':FUNC:SHAP {}'.format(forma))
        
    def get_forma(self):
        print('forma configurado en el instrumento')
        return self.ins.query('SOUR{}'.format(self.__canal)+':FUNC:SHAP?')