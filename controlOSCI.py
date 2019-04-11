# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 06:34:48 2019

@author: KBZ
"""

import visa
import numpy as np
from matplotlib import pyplot as pp

rm = visa.ResourceManager('C:\\Windows\\system32\\visa64.dll')
instrumentos=rm.list_resources()
osci=rm.open_resource('USB0::0x0699::0x0363::C102220::INSTR')
funcgen=rm.open_resource('USB0::0x0699::0x0363::C108013::INSTR')


#generador funciones

funcgen_f=
funcgen_amp=
funcgen_desf=


#osciloscopio
print(osci.query('*IDN?'))

CH='CH1' #CH1 CH2
ini='1' #1-2500
final='2500' #1-2500
ENC='RPB' #ASCI=ASCII o RIB=signed integer SRI=RIB con orden inverso  RPB=positive integer SRP=RPB orden inverso
DatWidth='1' #1= 1byte data o 2


osci.write('ACQ:STATE 1')
osci.query('DAT:SOU'+' '+CH)
#osci.query('DAT:SOU?')

osci.query('DAT:ENC'+' '+ENC)
osci.query('DAT:ENC?')
osci.query('DAT:WID'+' '+DatWidth)
osci.query('DAT:STAR'+' '+ini)
osci.query('DAT:STAR?')
osci.query('DAT:STOP'+' '+final)
osci.query('DAT?')

FORMAT='RP' #RI=signed integer RP=positive integer
DatBit='8' #bits por byte
endian='MSB' #MSB=Big Endian LSB=Little Endian
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

osci.query('WFMP:BYT_N'+' '+DatWidth)
osci.query('WFMP:BIT_N'+' '+DatBit)
osci.query('WFMP:BN_F'+' '+FORMAT)
osci.query('WFMP:BYT_O'+' '+endian)
osci.query('WFMP:ENC'+' '+ENC2)

#Xn = XZEro + XINcr (n -- PT_OFf) FORMULA CONVERSION X

osci.query('WFMP:PT_F'+' '+ptsOpico)
osci.query('WFMP:XIN'+' '+Dt)
osci.query('WFMP:XUN'+' '+Ut)
osci.query('WFMP:XZE'+' '+t0)

#Yn = YZEro + YMUIty (yn -- YOFf)  FORMULA CONVERSION y

osci.query('WFMP:YMU'+' '+Dy_dl)
YMUIty=osci.query('WFMP:YMU?')
YMUIty=float(YMUIty)
YOFf=osci.query('WFMP:YOF'+' '+y0_dl)
YOFf=osci.query('WFMP:YOF?')
YOFf=float(YOFf)
YZEro=osci.query('WFMP:YZERO'+' '+y0)
YZEro=osci.query('WFMP:YZERO?')
YZEro=float(YZEro)

osci.query('WFMP?')
osci.query('WFMP?')
osci.query('CURV?')
osci.query('WFMP:YUN?')

yn_dl= osci.query_binary_values('CURV?',datatype='B', is_big_endian=True)

yn_dl=np.array(yn_dl)



Yn = YZEro + YMUIty*(yn_dl - YOFf)
Xn = XZEro + XINcr*(np.linspace(1,2500,1) - PT_OFf)

pp.plot(Xn,Yn,'.')
pp.plot(np.log(Yn),'.')
pp.plot(Yn,'.')

