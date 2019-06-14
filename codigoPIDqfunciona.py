# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 17:51:43 2019

@author: Publico
"""

p = 45
set_point = 0.3 #Intensidad a mantener fija
# set_point = 0.32 #Intensidad a mantener fija
T = 10 #Tiempo máximo
to = time.time() #Tiempo inicial
t = 0
while t < T:
    t = time.time() - to
    with ni.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev22/ai0", terminal_config=ni.constants.TerminalConfiguration.RSE)
#       task.timing.samp_clk_rate = fs #Consultar o cambiar la frecuencia de muestreo de la tarea
        intensidad_in = task.read(1)[0]
        error = set_point - intensidad_in
    if error < 0.05:
        h = 0
    else:
        h = 4
        
    with ni.Task() as tarea:
        tarea.ao_channels.add_ao_voltage_chan("Dev22/ao0", min_val=0, max_val=5)
        tarea.write(h, auto_start=True)





#EXPERIMENTO TOMAS
gg=0        
vector=[]
while gg<500:
    with ni.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev22/ai0", terminal_config=ni.constants.TerminalConfiguration.RSE)
#        task.timing.samp_clk_rate = fs #Consultar o cambiar la frecuencia de muestreo de la tarea
        vector.append(task.read(1))
    with ni.Task() as tarea:
        tarea.ao_channels.add_ao_voltage_chan("Dev22/ao0", min_val=0, max_val=5)
        tarea.write(gg/100, auto_start=True)
    gg=gg+1

pp.plot(vector)



p = 45
set_point = promGF #Intensidad a mantener fija
# set_point = 0.32 #Intensidad a mantener fija
T = 10 #Tiempo máximo
to = time.time() #Tiempo inicial
t = 0
h=4

while t < T:
    t = time.time() - to
    with ni.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev22/ai0", terminal_config=ni.constants.TerminalConfiguration.RSE)
#       task.timing.samp_clk_rate = fs #Consultar o cambiar la frecuencia de muestreo de la tarea
        intensidad_in = task.read(1)[0]
        error = set_point - intensidad_in
    if error > 0.05:
        with ni.Task() as tarea:
        tarea.ao_channels.add_ao_voltage_chan("Dev22/ao0", min_val=0, max_val=5)
        tarea.write(h-error, auto_start=True)
    else:
        h = 4
        
    with ni.Task() as tarea:
        tarea.ao_channels.add_ao_voltage_chan("Dev22/ao0", min_val=0, max_val=5)
        tarea.write(h, auto_start=True)

fg.apagar()
