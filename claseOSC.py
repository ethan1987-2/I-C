# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 18:32:07 2019

@author: Publico
"""
import time
import pyvisa as visa
import numpy as np
from matplotlib import pyplot as pp
from datetime import datetime, timezone, timedelta

# Define GMT-3 timezone
gmt_minus_3 = timezone(timedelta(hours=-3))

# Get current time in GMT-3

timestamp=str(datetime.now()).replace(' ','_').replace(':','-')[:-7]

class OsciloscopeTDS2024B():
      
    def __init__(self,serial):  #osciloscopio sala B serial en la parte de atras = C101178
        self.rm = visa.ResourceManager()        
        self.serial = serial
        self.ins = self.rm.open_resource('USB0::0x0699::0x036A::{}::INSTR'.format(serial))
        self.ins.timeout=20000;
        self.ins.write('ACQ:STATE 1')
        self.ins.write('WFMP:BYT_N'+' '+'1')
        self.ins.write('WFMP:BIT_N'+' '+'8')
        self.ins.write('WFMP:BN_F'+' '+'RP')
        self.ins.write('WFMP:BYT_O'+' '+'MSB') #así como está da little endian  # MSB al final de transm: Big Endian, LSB al final de transm: Little Endian. # Big-endian systems store the most significant byte (MSB) at the lowest memory address.
                                                                                    # Little-endian systems store the least significant byte (LSB) at the lowest memory address.
        self.ins.write('WFMP:ENC'+' '+'BIN')
        

    def run(self): # detener osciloscopio
        self.ins.write('ACQ:STATE 0')
    
    def stop(self):
        self.ins.write('ACQ:STATE 1')
        
    def autoconf(self): # ejecutar autoconfiguracion del osciloscopio
        self.ins.write('AUTOS EXEC')
    
    def set_tscalScreen(self, tsca=0.5): #Examples HORIZONTAL:MAIN:SCALE 2.5E-6 sets the main scale to 2.5 ms per division. The range depends on the oscilloscope model.
                               #The acceptable values are in a 1-2.5-5 sequence. 
        self.ins.write(f'HOR:MAI:SCA {tsca}')
        
    def get_tscalScreen(self):
        print('unidades de tiempo en la pantalla del osciloscopio:')
        return self.ins.query('HOR:MAI:SCA?')

    def set_vscalScreen(self, CH,vsca=50E-3): #Examples CH1:SCALE 100E-3 sets the channel 1 gain to 100 mV/div
        self.ins.write('CH{}'.format(CH)+':SCA'+' '+str(vsca))
        
    def get_vscalScreen(self,CH):
        print('unidades de voltaje en la pantalla del osciloscopio:')
        return self.ins.query(f'CH{CH}'+':SCA?')

    def ident(self):
        return self.ins.query('*IDN?')

    def get_canal(self):
        print('canal de toma de datos de curva configurado en instrumento:')
        return self.ins.query('DAT:SOU?')
    
    def set_canal(self,CH,set_value=True): #CH=CH1 o CH2
        if not CH in (1,2):
            raise ValueError('El valor debe ser numérico 1 o 2')
        else:
            self.ins.write('DAT:SOU CH'+str(CH))
            self.ins.write('MEASU:IMM:SOU CH'+str(CH))
       
  
    def set_yun(self, yun): #yun= Volts,VV, U: nro divisiones, A:amps,AA, VA:volamps, dB
        if not isinstance(yun, str):    
            raise TypeError('el valor (texto) debe ser uno de los siguientes: "Volts","VV", "U": nro divisiones, "A":amps,"AA", "VA":volamps, "dB"')    
        self.ins.write('WFMP:YUN'+' '+yun)
        
    def get_yun(self):
        print('unidades de voltaje configuradas en instrumento para devolver valores medidos:')
        return self.ins.query('WFMP:YUN?')

    def set_xun(self, xun):  #xun= Hz, s
        if not isinstance(xun, str):    
            raise TypeError('el valor (texto) debe ser uno de los siguientes: "Hz", "s"')
        self.ins.write('WFMP:XUN'+' '+xun)

    def get_xun(self): #WFMPre:XUNit <Qstring>   WFMPre:XUNit?   Arguments <Qstring> is "s" or "Hz"
        print('unidades de tiempo configuradas en instrumento para devolver valores medidos:')
        return self.ins.query('WFMP:XUN?')

    def set_ygain(self, ymu):  # ej "5" volt/div
        if not isinstance(ymu, str):    
            raise TypeError('el valor debe ser numérico')
        self.ins.write('WFMP:YMU'+' '+ymu)

    def get_ygain(self): 
        print('ganancia configurada en instrumento para devolver valores medidos:')
        return self.ins.query('WFMP:YMU?')

    def set_yoff(self, yof):  # offset de canales o divisiones
        if not isinstance(yof, str) or isinstance(yof, int):    
            raise TypeError('el valor debe ser numérico entero')
        self.ins.write('WFMP:YOF'+' '+yof)

    def get_yoff(self): 
        print('offset eje y de canales o divisiones configurado en instrumento para devolver valores medidos:')
        return self.ins.query('WFMP:YOF?')
  
    def set_yzero(self, yzero):  # zero de y
        if not isinstance(yzero, float):     
            raise TypeError('el valor debe ser numérico')
        self.ins.write('WFMP:YZE'+' '+yzero)

    def get_yzero(self): 
        print('zero de eje y configurado en instrumento para devolver valores medidos:')
        return self.ins.query('WFMP:YZE?')

    def set_xsampleperiod(self, xincr):  # valor en segundos del intervalo de muestreos
        if not isinstance(xincr, float):     
            raise TypeError('el valor debe ser numérico')
        self.ins.write('WFMP:XIN'+' '+xincr)

    def get_xsamplepriod(self): 
        print('valor en segundos del intervalo de muestreos configurado en instrumento para devolver valores medidos:')
        return self.ins.query('WFMP:XIN?')

    def set_xoff(self, xof):  # offset de canales o divisiones
        if not isinstance(xof, str) or isinstance(xof, int):    
            raise TypeError('el valor debe ser numérico entero')
        self.ins.write('WFMP:PT_OF'+' '+xof)

    def get_xoff(self): 
        print('offset eje x de canales o divisiones configurado en instrumento para devolver valores medidos:')
        return self.ins.query('WFMP:PT_OF?')
  
    def set_xzero(self, xzero):  # zero de y
        if not isinstance(xzero, float):     
            raise TypeError('el valor debe ser numérico')
        self.ins.write('WFMP:XZE'+' '+xzero)

    def get_xzero(self): 
        print('zero de eje x configurado en instrumento para devolver valores medidos:')
        return self.ins.query('WFMP:XZE?')
    
    def paresXY(self):
        print(f'pares XY del canal {self.ins.query('DAT:SOU?')[:-2]} . cambiar con el comando set_canal' )
        YMU = float(self.ins.query('WFMP:YMU?')) 
        YOF = float(self.ins.query('WFMP:YOF?'))
        YZE = float(self.ins.query('WFMP:YZE?'))
        
        yn_dl = self.ins.query_binary_values('CURV?',datatype='B', is_big_endian=True)
        
        Yn = YZE + YMU*(np.array(yn_dl) - YOF) #value_in_YUNits = ((curve_in_dl - YOFF_in_dl) * YMUlt) + YZERO_in_YUNits

        XIN=float(self.ins.query('WFMP:XIN?'))
        XZE = float(self.ins.query('WFMP:XZE?'))
        PT_OF = float(self.ins.query('WFMP:PT_OF?'))

        Xn = XZE + XIN*(np.linspace(1,2500,2500) - PT_OF)
        return np.array(list(zip(Xn,Yn)))
    
    def screenshot(self,layout="PORTR",imgfmt="JPEG"): 
    #imgfmt: (str) uno de las sgtes opciones: BMP | BUBBLEJet | DESKJet | DPU3445 | DPU411 | DPU412 | EPSC60 | EPSC80 | EPSIMAGE | EPSOn | INTERLEAF | JPEG | LASERJet | PCX | RLE | THINKjet | TIFF         
        print("formato por defecto es jpg. cambiar extension si no es asi")
        self.ins.write("HARDC:LAY"+" "+layout)                                 #layout:  { LANdscape | PORTRait }
        self.ins.write("HARDC:FORM"+" "+imgfmt)
        self.ins.query('HARDCopy?')            
        self.ins.write('HARDCopy:PORT USB')            
        self.ins.write('HARDCopy STARt') 
        image_data = self.ins.read_raw()           

        with open("scope_capture-"+timestamp+".jpg", "wb") as f:
            f.write(image_data)
    
    def medir_frec(self): #un método
        self.ins.write('MEASU:IMM:TYP FREQ')
        time.sleep(1)
        return self.ins.query('MEASU:IMM:VAL?').replace('\n','')
    
    def medir_amp(self,medida): #{ FREQuency | MEAN | PK2pk | CRMs | MINImum | MAXImum |   esto no es amp: RISe | FALL |PWIdth | NWIdth }
        self.ins.write('MEASU:IMM:TYP {}'.format(medida))
        time.sleep(1)
        return self.ins.query('MEASU:IMM:VAL?').replace('\n','')
     
        
############################################################



