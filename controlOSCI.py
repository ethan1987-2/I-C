# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 06:34:48 2019

@author: KBZ
"""

import visa
import numpy as np
import pyplot from matplotlib as pp

rm = visa.ResourceManager('C:\\Windows\\system32\\visa64.dll')
instrumentos=rm.list_resources()
osci=rm.open_resource('USB0::0x0699::0x0363::C108013::INSTR')
funcgen=rm.open_resource('USB0::0x0699::0x0363::C108013::INSTR')
print(osci.query('*IDN?'))

#generador funciones

funcgen_f=
funcgen_amp=
funcgen_desf=


#osciloscopio
CH='CH1' #CH1 CH2
ini='1' #1-2500
final='2500' #1-2500
ENC='RPB' #ASCI=ASCII o RIB=signed integer SRI=RIB con orden inverso  RPB=positive integer SRP=RPB orden inverso
DatWidth=1 #1= 1byte data o 2


osci.write('ACQ:STATE 1')
osci.query('DAT:SOU'+' '+CH)
osci.query('DAT:ENC'+' '+ENC)
osci.query('DAT:WID'+' '+DatWidth)
osci.query('DAT:STAR'+' '+inicio)
osci.query('DAT:STOP'+' '+final)
osci.read('DAT?')

FORMAT='RP' #RI=signed integer RP=positive integer
endian2='MSB' #MSB=Big Endian LSB=Little Endian
ENC2='BIN' #ASC=ASCII o BIN=binary
ptsOpico='Y' #Y=el valor de la imagen por punto ENV=posicion de picos
Ut='s' #XUNit= 's' or 'Hz'
Dt='.1' #cant tiempo por división en las unidades Ut
#en este ejemplo debería dar décimas de segundos entre cada pto
t0='0' # expresado en Ut's
Dy_dl='1' #valor en YUN/dl dl:digitizer values del factor de escala para los datos u ordenadas
y0_dl='0'# afecta solo el cursor dice el manual
Uy='v' #unidades del eje y
y0='0' #zero del valor de la onda

osci.query('WFMPR:BYT_N'+' '+DatWidth)
osci.query('WFMPR:BIT_N'+' '+DatBit)
osci.query('WFMPR:BN_F'+' '+FORMAT)
osci.query('WFMPR:BYT_O'+' '+endian)
osci.query('WFMPR:ENC'+' '+ENC2)
#Xn = XZEro + XINcr (n -- PT_OFf) FORMULA CONVERSION X
osci.query('WFMPR:PT_F'+' '+ptsOpico)
osci.query('WFMPR:XIN'+' '+Dt)
osci.query('WFMPR:XUN'+' '+Ut)
osci.query('WFMPR:XZE'+' '+t0)
#Yn = YZEro + YMUIty (yn -- YOFf)  FORMULA CONVERSION y
YMUIty=osci.query('WFMPR:YMU'+' '+Dy_dl)
YOFf=osci.query('WFMPR:YOF'+' '+y0_dl)
YZEro=osci.query('WFMPR:YZERO'+' '+y0)

osci.read('WFMPR?')


yn_dl= osci.query_binary_values('CURV?')

Yn = YZEro + YMUIty*(yn_dl - YOFf)
Xn = XZEro + XINcr*(np.linspace(1,2500,1) - PT_OFf)

pp.plot(Xn,Yn,'.')

