# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 16:35:44 2019

@author: KBZ
"""

# -*- coding: utf-8 -*-
import nidaqmx as ni
import numpy as np
import time



class NISensorDAQ():
    def __init__(self):
        self.system = ni.system.System.local() #Initiates acqusition instance 
        
    def devices(self): #available daq devices
        for dev in self.system.devices:
            print(dev)       

    @property    
    def freq(self):
        return self.__freq
    
    @freq.setter
    def freq(self, f):
        self.__freq = f

    @property
    def dev_chan(self):
        return self.__dev_chan

    @dev_chan.setter
    def dev_chan(self, device, chan): #sets device, channel and acquisition config (DIFF, NRSE, RSE) to task
            self.__dev_chan= ("Dev" + str(device) + "/" + str(chan))

    def measure(self, config, points=1024):
            with ni.Task() as task:
                if config == 'DIFF':
                    task.ai_channels.add_ai_voltage_chan(self.__dev_chan, terminal_config = ni.constants.TerminalConfiguration.DIFFERENTIAL)
                elif config == 'NRSE':
                    task.ai_channels.add_ai_voltage_chan(self.__dev_chan, terminal_config = ni.constants.TerminalConfiguration.NRSE)
                elif config == 'RSE':
                    task.ai_channels.add_ai_voltage_chan(self.__dev_chan, terminal_config = ni.constants.TerminalConfiguration.RSE)
                task.timing.samp_clk_timing = self.__freq #da igual esto o lo otro REVISAR! PREGUNTAR A LOS PROFES DE ENTRADA
                task.timing.samp_clk_rate=self.__freq  #Consultar o cambiar la frecuencia de muestreo de la tarea
                data =task.read(points) #Mide voltaje, entre 1 y 1024 valores consecutivos.
                return data
