# -*- coding: utf-8 -*-
import nidaqmx as ni
import numpy as np
import time
from matplotlib import pyplot as pp
from scipy import fftpack

class NISensorDAQ():
    def __init__(self):
        self.system = ni.system.System.local() #Initiates acqusition instance and creates task
        self.task = ni.Task()
        
    def version(self):
        print(self.system.driver_version)
    
    def devices(self):
        for dev in self.system.devices:
            print(dev)
    
    def get_freq(self):
        return self.task.timing.samp_clk_timing, "Hz"
    
    def set_freq(self, f):
        self.task.timing.samp_clk_timing = f
    
    def get_device(self): #daq component devices
        print(self.task.device)
    
    def set_chan(self, device, chan, config): #Asigns device, channel and acquisition config (DIFF, NRSE, RSE) to task
        
        if config == 'DIFF':
            self.task.ai_channels.add_ai_voltage_chan(("Dev" + str(device) + "/" + str(chan)), terminal_config = ni.constants.TerminalConfiguration.DIFFERENTIAL)
        elif config == 'NRSE':
            self.task.ai_channels.add_ai_voltage_chan(("Dev" + str(device) + "/" + str(chan)), terminal_config = ni.constants.TerminalConfiguration.NRSE)
        elif config == 'RSE':
            self.task.ai_channels.add_ai_voltage_chan(("Dev" + str(device) + "/" + str(chan)), terminal_config = ni.constants.TerminalConfiguration.RSE)
    
    def measure(self, points=1024, plot=False): #Measures a set amount of consecutive voltage points
        data = self.task.read(points)
        if data is not None:
            pp.plot(np.linspace(0, points/self.task.timing.samp_clk_timing, points), data) #acá se podría usar size(data)
        return data
    
    def reset_task(self): #Re-creates the task
        self.task = ni.Task()