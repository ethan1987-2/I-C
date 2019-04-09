# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 16:54:11 2019

@author: Publico
"""

import visa

rm = visa.ResourceManager('C:\\Windows\\system32\\visa64.dll')
instrumentos=rm.list_resources()
# rm.list_resources('?*') lista aún más cosas que el siguiente comando si están conectadas
# rm.list_resources('?*::INSTR') es el equivalente de   rm.list_resources()
# estos comandos devuelven una tupla de strings
#osci=rm.open_resource(instrumentos[0]) #abrir el primer dispositivo de la tupla
osci=rm.open_resource('USB0::0x0699::0x0363::C108013::INSTR')
# inst = rm.open_resource('ASRL1::INSTR')
#my_instrument = rm.open_resource('ASRL1::INSTR')


print(osci.query('*IDN?'))
#todo lo que está con signo de preguntas al final es un query o un read, solo toma valores no da ordenes
osci.write('')

help(osci.write)
osci.query('ACQ:NUMAC?')
#resultado 'HBA;CH1;SECO;-1.98E-3;2.02E-3;VOL;4.0E-3;-6.48E-3\n'
osci.write('ACQ:STATE 1') #prende y apaga la toma de datos, equivale al boton run / stop del osciloscopio
osci.write('ACQ:STATE 0')
osci.read('CURV 1')

valor = osci.query_binary_values('CURV?')


osci.write('DAT:SOU CH1') #de que canal salen los datos
osci.read('DAT?')
osci.query('WFMP:XUN?') #QUERY unidades de x
osci.query('WFMP:NR_P?')  #nro de puntos a retirar 

osci.query('DAT:STOP?')

osci.query_binary_values('MEASUrement:IMMed:VALue?') #esto es lo q quiere HERNAN


osci.query_ascii_values('DISplay?')

#para escribirle un mensaje al instrumento:
#inst.write()
#estos mensajes deben ir con una secuencia de caracteres que lo terminan "terminador" cuyo formato especifican los manuales de los instrumentos

#por ejemplo un terminador de linea puede ser CR "carriage return" o LF "line fill" o también  \n
#pero el paquete pyvisa ya hace esto automaticamente
#inst.query('*IDN?') funciona pero inst.query('*IDN?\n') porque estaría duplicando el terminador
#query hace un write y un read a la vez


#para ayuda 
help(inst.write)

#help(inst.read)
#help(inst.write)

#a veces la memoria de los instrumentos queda llena con cosas pasadas, y esto traba los comandos, entonces probar reiniciar


#visa.log_to_screen() habilita la informacion de que está ocurriendo mientras nos comunicamos y operamos con el aparato para poder hacer debugging por ejemplo 
