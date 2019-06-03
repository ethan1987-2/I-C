
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
    task.ai_channels.add_ai_voltage_chan("Dev19/ai0", terminal_config=ni.constants.TerminalConfiguration.DIFFERENTIAL)
    print(task.read()) #Mide voltaje, entre 1 y 1024 valores consecutivos.



t = np.linspace(0,1024/46000,1024)

#investigacion TOMAS:
nidaqmx._task_modules.in_stream.InStream(task) #Exposes an input data stream on a DAQmx task. TOM
nidaqmx.stream_readers.AnalogSingleChannelReader(task_in_stream) #Reads samples from an analog input channel in an NI-DAQmx task. RETURNS: Indicates the number of samples acquired by each channel. NI-DAQmx returns a single value because this value is the same for all channels.
    read_many_sample(data, number_of_samples_per_channel=-1, timeout=10.0) #data (numpy.ndarray) –Specifies a preallocated 1D NumPy array of floating-point values to hold the samples requested.
nidaqmx.stream_readers.AnalogMultiChannelReader(task_in_stream) #lectura multiple canal
    read_many_sample(data, number_of_samples_per_channel=-1, timeout=10.0)  #data (numpy.ndarray) –Specifies a preallocated 2D NumPy array of floating-point values to hold the samples requested. The size of the array must be large enough to hold all requested samples from all channels in the task; otherwise, an error is thrown.

nidaqmx._task_modules.channel_collection.ChannelCollection(task_handle) #TOM varias formas de medir cosas fisicamente distintas
nidaqmx.task.ai_channel_collection
#Docs » nidaqmx.task » nidaqmx.task.channel_collection »


#para mas, luego vi que la intro de la pagina sugiere..."Consider using the nidaqmx.stream_readers and nidaqmx.stream_writers classes to increase the performance of your application, which accept pre-allocated NumPy arrays."





