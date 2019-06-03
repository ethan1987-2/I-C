# -*- coding: utf-8 -*-
"""
Created on Tue May 28 14:23:58 2019

@author: Publico
"""

import nidaqmx as ni
import numpy as np
import time
from matplotlib import pyplot as pp
from scipy import fftpack
import nimax_clase
import claseGF

system = ni.system.System.local()

fg = FunctionGeneratorAFG3021B('C033250')

q = 1024
fs = 48000
N = 20
frecs = np.linspace(1000, 30000, N)
b = 0
DATA2 = np.zeros([N, q])

#fg.set_freq(200, 'Hz')
#
#with ni.Task('Tarea') as task:
#    task.ai_channels.add_ai_voltage_chan("Dev20/ai0", terminal_config = ni.constants.TerminalConfiguration.DIFFERENTIAL)
#    task.timing.samp_clk_timing = 48000
#    pp.plot(np.linspace(0, q/fs, q), task.read(q))

with ni.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev20/ai0", terminal_config = ni.constants.TerminalConfiguration.DIFFERENTIAL)
    task.timing.cfg.samp_clk_timing(fs)
    for i in frecs:
        fg.set_freq(i, 'Hz')
        time.sleep(2)
        DATA2[b] = task.read(q)
        print(i, b)
        b = b+1        

for j in range(5): 
    pp.plot(np.linspace(0, q/fs, q), data2[0], '.')

pp.plot(fftpack.fft(DATA2[0]))

with ni.Task() as task2:
    task2.ai_channels.add_ai_voltage_chan("Dev20/ai0", terminal_config = ni.constants.TerminalConfiguration.DIFFERENTIAL)
    task2.timing.samp_clk_timing = fs
    print(task2.timing.samp_clk_timing)
    #task2.timing.samp_clk_rate
    prueba = task2.read(q)

M3 = np.transpose(DATA2)
np.savetxt('barridofreq3_48k.txt', M3)

print(frecs)

def fourier(y,fs):
    N=len(y)
    T=N/fs    
#    x = np.linspace(0.0, N*T, N)
    xf = np.linspace(0.0, fs/2.0, N//2)
    yf = fftpack.fft(y)
    return xf, 2.0/N * np.abs(yf[0:N//2])

trafoF=fourier(DATA2[6],fs)

pp.plot(trafoF[0], trafoF[1])

task = ni.Task()
task.ai_channels.add_ai_voltage_chan("Dev20/ai0", terminal_config = ni.constants.TerminalConfiguration.DIFFERENTIAL)
task.timing.cfg_samp_clk_timing(2000)
task.start()
task.stop()
task.timing.samp_clk_rate

pp.plot(np.linspace(0, 1024/fs, 1024), DATA2[2])

system.driver_version
task.channels
task.channel_names
data = task.read(q)

task.timing.samp_clk_rate
task.stop()

sin = np.sin(2*np.pi*np.linspace(0,1,1000)*15)
ff = fftpack.fft(DATA[4])
pp.plot(np.linspace(0,1024,1024), np.abs(ff))
pp.plot(fftpack.fft(sin))

frecs[8]

DATA2


