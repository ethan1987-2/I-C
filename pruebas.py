# -*- coding: utf-8 -*-
"""
Created on Tue May  7 07:18:09 2019

@author: KBZ
"""

######################################################
        
    
osc = OsciloscopeTDS1002B('C108012') #CAMBIAR!!!

osc.medir
osc.xun='s'
osc.yun='Volts'
osc.canal=2
frecVal=osc.frec()

D=osc.datos

pp.plot(X,Y,'.')
pp.title('Captura de pantalla')
pp.xlabel(osc.xun)
pp.ylabel(osc.yun)
        
     

funcg=FunctionGeneratorAFG3021B('C108012') #CAMBIAR!!!

funcg.ampVPP=5
funcg.fase=(1/3,'RAD') #preguntar esto, si asigne bien valores multiples a la propiedad
funcg.frec=(1,'kHz')
funcg.prende


osc.ins.query('MEASU:IMM?')
osc.ins.query('DAT:SOU?')
osc.yun='Volts'

osc.ins.write('WFMP:YUN dB')
osc.ins.query('WFMP:YUN?')



