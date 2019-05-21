# -*- coding: utf-8 -*-

import nidaqmx as ni
import numpy as np
import time
from matplotlib import pyplot as pp
from scipy import fftpack

system = ni.system.System.local() #Crea instancia del sistema de adquisicion
system.driver_version #Info sobre la versión

for device in system.devices:
    print(device) #Lista de dispositivos disponibles
    
#Crea una tarea, le añade un canal para medir voltaje, especifica modo (RSE, NRSE, DIFF, etc) 
with ni.Task() as task:
    task.timing.samp_clk_rate #Consultar o cambiar la frecuencia de muestreo de la tarea
    task.ai_channels.add_ai_voltage_chan("Dev19/ai0", terminal_config=ni.constants.TerminalConfiguration.RSE)
    print(task.read()) #Mide voltaje, entre 1 y 1024 valores consecutivos.

task = ni.Task()
task.timing.samp_clk_rate

task.ai_channels.add_ai_voltage_chan("Dev19/ai0", terminal_config=ni.constants.TerminalConfiguration.DIFFERENTIAL)

a = task.read(1024)

t = np.linspace(0,1024/46000,1024)

a = task.read(1024)

ni.constants.AcquisitionType.CONTINUOUS #Finita

ni.constants.AcquisitionType.FINITE #Continua

ni.constants.TerminalConfiguration.DIFFERENTIAL

ni.constants.TerminalConfiguration.NRSE

ni.constants.TerminalConfiguration.RSE
