# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 03:52:54 2025

@author: tomyg
"""
import time
import claseOSC
from matplotlib import pyplot as pp

osc=claseOSC.OsciloscopeTDS2024B("C101178")

osc.screenshot()

pares=osc.paresXY()

pp.plot(pares[:,0],pares[:,1])


osc.set_tscalScreen(5E-3)



osc.set_vscalScreen(1,1)

#superponer varias adquisiciones para tener mejor idea del ruido
for i in range(0,6):
    pares=osc.paresXY()
    time.sleep(1)
    pp.plot(pares[:,0],pares[:,1],'b')
    pp.show()