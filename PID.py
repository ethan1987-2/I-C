import nidaqmx as ni
import numpy as np
import time
from matplotlib import pyplot as pp
from scipy import fftpack
import nimax_clase
import claseGF
import claseOSC
import nimax_claseTOMAS

fg = FunctionGeneratorAFG3021B('C033250')


fg.prende()
fg.apaga()


q = 1024
fs = 10000/5
N = 20
frecs = np.linspace(1000, 30000, N)
b = 0
DATA2 = np.zeros([N, q])




system = ni.system.System.local() #Crea instancia del sistema de adquisicion
system.driver_version #Info sobre la versión

for device in system.devices:
    print(device) #Lista de dispositivos disponibles
    
#Crea una tarea, le añade un canal para medir voltaje, especifica modo (RSE, NRSE, DIFF, etc) 
#LEER 1024 PUNTOS
with ni.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev20/ai0", terminal_config=ni.constants.TerminalConfiguration.RSE)
#    task.ai_channels.add_ai_voltage_chan("Dev20/ai1", terminal_config=ni.constants.TerminalConfiguration.DIFFERENTIAL)
    task.timing.samp_clk_rate=fs #Consultar o cambiar la frecuencia de muestreo de la tarea
    DATOS=task.read(1024) #Mide voltaje, entre 1 y 1024 valores consecutivos.

task.timing.cfg_samp_clk_timing(4096,sample_mode = AcquisitionType.CONTINUOUS)




with ni.Task('tarea') as nitask:
    nitask.ai_channels.add_ai_voltage_chan("Dev20/ai0", terminal_config=ni.constants.TerminalConfiguration.RSE)
#    ni.Task.name=
    nitask.timing.samp_clk_rate=fs #Consultar o cambiar la frecuencia de muestreo de la tarea
    
    print(nitask.name)
    ni.task.InStream(nitask)
#    ni.Task.in
    ni.stream_readers.AnalogSingleChannelReader.read_many_sample(DATOSCONT,timeout=10)
    ni.stream_readers.AnalogSingleChannelReader.read_many_sample(DATOSCONT,timeout=10)

ni.stream_readers
ni.stream_readers.
ni.Task.in_stream
ni.task.InStream.
ni.Task()  
ni.task.
ni.Task.ai_channels.add_ai_voltage_chan("Dev20/ai0", terminal_config=ni.constants.TerminalConfiguration.RSE)
ni.Task.timing.samp_clk_rate=fs #Consultar o cambiar la frecuencia de muestreo de la tarea
ni.Task.in_stream
ni.stream_readers.AnalogSingleChannelReader.read_many_sample(DATOSCONT,timeout=10)
    
    


nitask.in_stream


nidaqmx.stream_readers.AnalogSingleChannelReader(task_in_stream)
nidaqmx._task_modules.in_stream.InStream(task)

number_of_devices

t = np.linspace(0,1024/fs,1024)
pp.plot(t,DATOS,'-o')

1/20




with nitask() as task:
    task.ai_channels.add_ai_voltage_chan("Dev20/ai0", terminal_config=ni.constants.TerminalConfiguration.DIFFERENTIAL)
    task.timing.samp_clk_rate=46000 #Consultar o cambiar la frecuencia de muestreo de la tarea
    print(task.read(10)) #Mide voltaje, entre 1 y 1024 valores consecutivos.

1024/46000
200/46000
1/



task.start()
task.stop()

