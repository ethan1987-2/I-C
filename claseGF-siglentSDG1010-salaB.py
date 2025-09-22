import time
import pyvisa as visa
import numpy as np
from matplotlib import pyplot as pp
from datetime import datetime, timezone, timedelta

# Define GMT-3 timezone
gmt_minus_3 = timezone(timedelta(hours=-3))

# Get current time in GMT-3

timestamp=str(datetime.now()).replace(' ','_').replace(':','-')[:-7]

class FunctionGeneratorSDG1010():  

    def __init__(self,serial):  #el serial del de sala B es SDG10GAQ1R1117
        self.rm = visa.ResourceManager('@py')   #el '@py' es vital (en otra pc puede o debe omitirse) porque en esta computadora se instalo pyusb que se usa para controlar la comunicacion de pyvisa con la interfaz usb, sin esto el driver visa al perecer no funciona en ubuntu porque no se comunica bien con el usb, al menos no directamente como ocurre en otra computadora.
        self.serial = serial
        self.ins = self.rm.open_resource(f'USB0::0x0699::0x036A::{serial}::INSTR')
        self.__canal='1' #self.ins.query('SOUR?')

    def ident(self):
        return self.ins.query('*IDN?')


    def prende(self): # habilita la salida del canal seleccionado       
        self.ins.write(f'C{self.__canal}:OUTP ON')
        
    def apaga(self): # corta la salida del canal seleccionado
        self.ins.write(f'C{self.__canal}:OUTP OFF')
    
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
        
    def set_amp(self, ampVpp,ampun):
        print(f'la amplitud es ahora {ampVpp}{ampun}')
        text=self.ins.query(f'C{self.__canal}:BSWV WVTP?')
        if ('NOISE' in text) or ('DC' in text):
            self.ins.write(f'C{self.__canal}:BSWV AMP, {ampVpp}{ampun}')
        else: print(f'no se puede setear este parámetro porque el tipo de onda es: {text}')


    def get_amp(self):  
        print('amplitud configurada en el instrumento en voltios')
        return self.ins.query(f'C{self.__canal}:BSWV AMP?')
       
    def set_frec(self, freq, frecun): #freq es un nro frecun=Hz, MHz, kHz
        print(f'la frecuencia es ahora {freq}{frecun}')
        text=self.ins.query(f'C{self.__canal}:BSWV WVTP?')
        if ('NOISE' in text) or ('DC' in text):
            self.ins.write(f'C{self.__canal}:BSWV FRQ, {freq}{frecun}')
        else: print(f'no se puede setear este parámetro porque el tipo de onda es: {text}')
        
    def get_frec(self):
        print('frecuencia configurada en el instrumento')
        return self.ins.query(f'C{self.__canal}:BSWV FRQ?') 
   //////////SEGUIR DESDE ACA/////////////
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