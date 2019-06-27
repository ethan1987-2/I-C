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
fg = FunctionGeneratorAFG3021B('C033248')

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

#intento del dia 14-6
        
#POR FIN!!! ASI SE HACE ESTO!! CAMBIAR LA FS:
tarea1=ni.Task()
tarea1.ai_channels.add_ai_voltage_chan("Dev11/ai0", terminal_config = ni.constants.TerminalConfiguration.DIFFERENTIAL)
tarea1.timing.cfg_samp_clk_timing(30000)
tarea1.start()
print(tarea1.timing.samp_clk_rate)

#PARAR Y CERRAR TAREAS NO ES LO MISMO!!!!
tarea1.stop()
tarea1.name
tarea1.close()



with ni.Task() as tarea:
    tarea.ai_channels.add_ai_voltage_chan("Dev11/ai0", terminal_config = ni.constants.TerminalConfiguration.DIFFERENTIAL)
    tarea.timing.cfg_samp_clk_timing(48000)
    tarea.start()
    print(tarea.timing.samp_clk_rate)
    vector=tarea.read(1024)


q = 999
fs = 48000
N = 20
frecs = np.linspace(1000, 30000, N)
b = 0
DATA1 = np.zeros([N, q])
#DATA1=q*[]

with ni.Task() as tarea:
    tarea.ai_channels.add_ai_voltage_chan("Dev11/ai0", terminal_config = ni.constants.TerminalConfiguration.DIFFERENTIAL)
    tarea.timing.cfg_samp_clk_timing(fs)
    tarea.start()
    print(tarea.timing.samp_clk_rate)
    for i in frecs:
        fg.set_frec(i, 'Hz')
        time.sleep(2)
        DATA1[b]=tarea.read(q)
        print(i, b)
        b = b+1        

for j in range(5): 
    pp.figure()
    pp.plot(np.linspace(0, q/fs, q), DATA2[0], '.')

#hasta acá fue lo del dia 14-6 ...sigue script viejo
    




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

######--BARRIDO DE ENTRADA EN AMPLITUD
##Prueba read

with ni.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev22/ai0", terminal_config=ni.constants.TerminalConfiguration.DIFFERENTIAL)
#    task.ai_channels.add_ai_voltage_chan("Dev20/ai1", terminal_config=ni.constants.TerminalConfiguration.DIFFERENTIAL)
#    task.timing.samp_clk_rate = fs #Consultar o cambiar la frecuencia de muestreo de la tarea
    PRUEBA = task.read(1024)
pp.plot(PRUEBA, 'o')

q = 1024
fs = 48000
N = 5
amps = np.linspace(11, 13, N)
b = 0
DATA = np.zeros([N, q])

with ni.Task() as tarea:
    tarea.ai_channels.add_ai_voltage_chan("Dev22/ai0", terminal_config = ni.constants.TerminalConfiguration.DIFFERENTIAL)
    #0tarea.timing.cfg_samp_clk_timing(48000)
    #tarea.start()
    for i in amps:
        fg.set_amp(i)
        time.sleep(2)
        DATA[b] = tarea.read(q)
        print(i, b)
        b = b+1  

for i in range(5):
    pp.figure()
    pp.plot(np.linspace(0,1024,1024)/13400,DATA[i],'.')
    
M = np.transpose(DATA)
np.savetxt('barridoamps3.txt', M, header='amps = np.linspace(11, 13, 5) frec = 1kHz')
#---------------------------------------------------------------
#BARRIDOS DE SALIDA


#BARR EN FRECS


#

system = ni.system.System.local()


osc=OsciloscopeTDS1002B('C065089')
fg = FunctionGeneratorAFG3021B('C034198')






osc.set_yun('Volts')
osc.get_yun()
osc.set_xun('s')
osc.get_xun()


fs = 150 #???
d=2#
#N = 23
#frecs = np.linspace(1,300, 16)

f=1000

b = 0
DATA=[]
DATAf =[]
DATAa = []

t=np.linspace(0,d,15*f*d)
seno=1+np.sin(2*np.pi*f*t)
pp.plot(t,seno,'.-')

osc.medir()
time.sleep(7/f)
t0=time.time()

osc.set_tscal(1/f)
with ni.Task() as tarea:
    tarea.ao_channels.add_ao_voltage_chan("Dev22/ao0",min_val=0,max_val=5)
#            tarea.timing.cfg_samp_clk_timing(1000)
#            tarea.start()
#            print(tarea.timing.samp_clk_rate)      
    tarea.write(seno, auto_start=True,timeout=5.0)
#            time.sleep(2/f)
osc.apagar()
tf=time.time()
TTOTAL=tf-t0

DATA=osc.datos()
pp.plot(DATA[0],DATA[1],'.-')


M = np.transpose(DATA)
np.savetxt('senoSALIDA-parafs3.txt', M, header='f=1000 dur=2 N=f*dur*15 fs=150¡??')


#-----------------------------------------barrido amplitudes

amps=np.linspace(0,2.5,20)
f=500


t=np.linspace(0,d,15*f*d)

#pp.plot(t,seno,'.-')

b=0
AMPLITS=[]
for amp in amps:
    seno=amp+amp*np.sin(2*np.pi*f*t)
    osc.set_vscal(amp/2,1)
    with ni.Task() as tarea:
        tarea.ao_channels.add_ao_voltage_chan("Dev22/ao0",min_val=0,max_val=5)
        tarea.write(seno, auto_start=True,timeout=5.0)
        AMPLITS.append(osc.medir_amp('PK2'))
    #    osc.apagar


for i in range(len(AMPLITS)):
    AMPLITS[i]=float(AMPLITS[i])

pp.plot(2*amps, AMPLITS, '-o')

AMPLITS=np.array(AMPLITS)
M = np.transpose([amps,AMPLITS])
np.savetxt('senoSALIDA-AMPS2.txt', M, header='f=500 dur=2 N=f*dur*15 fs=150¡??')


with ni.Task() as Task:
    Task.ao_channels.add_ao_voltage_chan("Dev22/ao0",min_val=0,max_val=2)
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
