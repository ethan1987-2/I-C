import nidaqmx as ni
import numpy as np
import time
from matplotlib import pyplot as pp
from scipy import fftpack
import nimax_clase
import claseGF
import claseOSC
import nimax_claseTOMAS

fg = FunctionGeneratorAFG3021B('C033248')

fg.prende()
fg.apaga()

q = 1024
fs = 1024
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


tiempos = np.linspace(0,1024/fs,1024)
pp.plot(t, DATOS)

############################################################################################



with ni.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev22/ai0", terminal_config=ni.constants.TerminalConfiguration.RSE)
#    task.ai_channels.add_ai_voltage_chan("Dev20/ai1", terminal_config=ni.constants.TerminalConfiguration.DIFFERENTIAL)
    task.timing.samp_clk_rate = fs #Consultar o cambiar la frecuencia de muestreo de la tarea
    DATOS = task.read(1024) #Mide voltaje, entre 1 y 1024 valores consecutivos.

pp.plot(DATOS)
promGF=np.mean(DATOS)

########Calibracion fotodiodo
flanco = DATOS[652:880]
voltajes = np.linspace(0,5,np.size(DATOS))
flanco = np.array(flanco)
#Intensidad = Av^2 + Bv + C
C = 0.22851
B = 0.04595
A = -0.0054

def VaI_quad(i): #Inversa 
    return 4.25463 - 0.00207043 * np.sqrt(1.40944*10**7 - i*4.32*10**7)

#Mejor una exponencial tipo 1-exp(-algo), se parece mas
#Intensidad = F + G exp(H v)
F = 0.33224
G = -0.11445
H = -0.64978

def VaI_exp(i):
    return -1.53898 * np.log(-8.73744 * (i - 0.33224))
############################################################################################


##########IMPLEMENTACION DE PID
set_point = 0.32 #Intensidad a mantener fija
T = 5 #Tiempo máximo
to = time.time() #Tiempo inicial
t = 0
medidas = []
error = 10*[0]
P = 20
integ = 0.2
deriv = 0.1
tiempos = [t]
while t < T:
    t = time.time() - to
    tiempos.append(t)
    with ni.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev22/ai0", terminal_config=ni.constants.TerminalConfiguration.RSE)
        task.timing.samp_clk_rate = fs #Consultar o cambiar la frecuencia de muestreo de la tarea
        intensidad_in = task.read(1)[0]
        error.append(set_point - intensidad_in)
        medidas.append(intensidad_in)
        rango_int = error[-10:]    
    with ni.Task() as tarea:
        tarea.ao_channels.add_ao_voltage_chan("Dev22/ao0", min_val=0, max_val=5)
        tarea.write(abs(P*error[-1]+integ*np.sum(rango_int)+deriv*(error[-1]-error[-2])/(tiempos[-1]-tiempos[-2])), auto_start=True)
        
pp.plot(tiempos[0:-1], medidas)
pp.plot(tiempos, error[0:np.size(tiempos)])

######### CÓDIGO QUE FUNCIONA


p = 45
set_point = 0.3 #Intensidad a mantener fija
# set_point = 0.32 #Intensidad a mantener fija
T = 5 #Tiempo máximo
to = time.time() #Tiempo inicial
t = 0
while t < T:
    t = time.time() - to
    with ni.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev22/ai0", terminal_config=ni.constants.TerminalConfiguration.RSE)
#       task.timing.samp_clk_rate = fs #Consultar o cambiar la frecuencia de muestreo de la tarea
        intensidad_in = task.read(1)[0]
        error = set_point - intensidad_in
    
    if intensidad_in > 0.3 and intensidad_in < 0.38:
        a = 0
    elif intensidad_in < 0.3:
        with ni.Task() as tarea:
            tarea.ao_channels.add_ao_voltage_chan("Dev22/ao0", min_val=0, max_val=5)
            tarea.write(2, auto_start=True)
    else:
        with ni.Task() as tarea:
            tarea.ao_channels.add_ao_voltage_chan("Dev22/ao0", min_val=0, max_val=5)
            tarea.write(0, auto_start=True)


##############################            
#PRENDER
            
with ni.Task() as tarea:
    tarea.ao_channels.add_ao_voltage_chan("Dev22/ao0", min_val=0, max_val=5)
    tarea.write(5, auto_start=True)

#APAGAR
with ni.Task() as tarea:
    tarea.ao_channels.add_ao_voltage_chan("Dev22/ao0", min_val=0, max_val=5)  
    tarea.write(0, auto_start=True)
    
    


####################################
    
task.timing.cfg_samp_clk_timing(4096,sample_mode = AcquisitionType.CONTINUOUS)

with ni.Task('tarea') as nitask:
    nitask.ai_channels.add_ai_voltage_chan("Dev22/ai0", terminal_config=ni.constants.TerminalConfiguration.RSE)
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

