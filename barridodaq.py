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
import claseOSC

system = ni.system.System.local()

osc=OsciloscopeTDS1002B('C108013')
fg = FunctionGeneratorAFG3021B('C034198')

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
    task.ai_channels.add_ai_voltage_chan("Dev21/ai0", terminal_config = ni.constants.TerminalConfiguration.DIFFERENTIAL)
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

#---------------------------------------------------------------
#BARRIDOS DE SALIDA


#BARR EN FRECS


#

system = ni.system.System.local()


osc=OsciloscopeTDS1002B('C108013')
fg = FunctionGeneratorAFG3021B('C034198')


fs = 48000
duracion=10
N = 23
frecsA = np.linspace(1000, fs/2, N)
frecsB=np.linspace(fs/2, 48000, N)
b = 0
DATAfrec = []
DATAamp = []
seno=1+np.sin(2*np.pi*1000*np.linspace(0,duracion,duracion*10))

osc.set_yun('Volts')
osc.get_yun()
osc.set_xun('s')
osc.get_xun()

#ni.Task()
##ni.Task.channels.description()
#ni.task.AOChannelCollection.add_ao_voltage_chan(physical_channel='Dev21/ao0')
#ni.task.AOChannelCollection.add_ao_voltage_chan("Dev21/ao0",min_val=-1,max_val=1)
#ni.Task.ao_channels.add_ao_voltage_chan("Dev21/ao0",min_val=-1,max_val=1)
#
#ni.stream_writers.AnalogSingleChannelWriter.write_many_sample(seno,timeout=duracion)
#ni.task.Timing.cfg_pipelined_samp_clk_timing=fs
#ni.Task.stop('Tarea')
ni.Task.timing.cfg_samp_clk_timing(fs)
ni.Task.tim



with ni.Task() as tarea:
    tarea.do_channels.add_do_chan()


with ni.Task() as tarea:
    tarea.ao_channels.add_ao_voltage_chan("Dev21/ao0",min_val=0,max_val=5)
#    print(tarea.timing.samp_timing_type)
#    print(tarea.timing.cfg_pipelined_samp_clk_timing)
#    tarea.wait_until_done(timeout=5.0)
    tarea.write(seno, auto_start=True,timeout=5.0)
    tarea.timing.samp_timing_type.PIPELINED_SAMPLE_CLOCK

#    tarea.timing.cfg_samp_clk_timing(fs,samps_per_chan=100)
    
#    ni.task.timing.cfg_pipelined_samp_clk_timing(fs,samps_per_chan=1000)



with ni.Task() as Task:
    Task.ao_channels.add_ao_voltage_chan("Dev21/ao0",min_val=0,max_val=2)
    ni.task.Timing.cfg_pipelined_samp_clk_timing=fs
    ni.stream_writers.AnalogSingleChannelWriter.write_many_sample(seno,timeout=duracion)
#    Task.timing.cfg_samp_clk_timing(150)
#    Task.timing.cfg_pipelined_samp_clk_timing(fs)
#    .cfg_pipelined_samp_clk_timing(fs,sample_mode=ni.constants.SampleTimingType.ON_DEMAND,samps_per_chan=1000)
#    Task.timing
    
    for i in frecsA:
        osc.set_tscal(2/i)
        time.sleep(1)
        DATAfrec.append(osc.medir_frec())
        DATAamp.append(osc.medir_amp('PK2'))
        print(i, b)
        b = b+1
    for i in frecsB:
        osc.set_tscal(1/i/b/2)
        time.sleep(1)
        DATAfrec.append(osc.medir_frec())
        DATAamp.append(osc.medir_amp('PK2'))
        print(i, b)
        b = b+1
        
frecs=frecsA.append( frecsB)