import nidaqmx as ni
import numpy as np
import time
from matplotlib import pyplot as pp
import claseGF
# import nimax_clase
# import claseOSC

fg = FunctionGeneratorAFG3021B('C034198')

system = ni.system.System.local()           # Create an instance of the acquisition system
# system.driver_version                     # Information about the system version

for device in system.devices:
    print(device)                           # Available devices

############################## ---- Test DAQ reading
with ni.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev22/ai0", terminal_config=ni.constants.TerminalConfiguration.RSE)
    pp.plot(task.read(1024))


############################## ---- Test DAQ writing            
#Turn on DAQ writing
            
with ni.Task() as tarea:
    tarea.ao_channels.add_ao_voltage_chan("Dev22/ao0", min_val=0, max_val=5)
    tarea.write(4, auto_start=True)

#Turn off DAQ writing
with ni.Task() as tarea:
    tarea.ao_channels.add_ao_voltage_chan("Dev22/ao0", min_val=0, max_val=5)  
    tarea.write(0, auto_start=True)
    

####################################

# ------- Set_point determination --------------------------------------------------------------------------------------

# Turn on the reference LED with a constant voltage and 
#measure the output voltage of the photodiode
fg.apaga()
fg.prende()
fg.set_forma('squ')#string = {SINusoid|SQUare|PULSe|RAMP|PRNoise|DC|SINC|GAUSsian|LORentz|ERISe|EDECay|HAVersine|USER[1]|USER2|USER3|USER4|EMEMory|EFILe}
fg.set_frec(0.1, 'Hz')
fg.set_amp(2)
T_0 = 2
reference_intensity = []

t_0 = time.time()
while (time.time() - t_0) < T_0:

    with ni.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev22/ai0", terminal_config=ni.constants.TerminalConfiguration.RSE)
        reference_intensity.append(task.read(1)[0])

mean_reference_intensity = np.mean(reference_intensity)              # To use as set point
dispersion = np.max(reference_intensity)-np.min(reference_intensity) # Intensity dispersion with 'constant' illumination

pp.plot(reference_intensity)
# ------- PID ----------------------------------------------------------------------------------------------------------

with ni.Task() as tarea:
    tarea.ao_channels.add_ao_voltage_chan("Dev22/ao0", min_val=0, max_val=5)  
    tarea.write(0, auto_start=True)
    
set_point = mean_reference_intensity        # Intensity (voltage proportional to it) on the photodiode to keep constant
T = 10                                      # Total time in which the PID loop is implemented (in seconds)
t = 0

photodiode_data = []                        # Signal measured with the photodiode
time_data = [t]                             # Time

last_error = 0                              # Initial condition
integral = 0                              # Initial condition
Kp = 1                                      # Proportional constant
Ki = 0.1                                    # Integral constant
Kd = 0.3                                    # Derivative constant

output = [0]

# Begins the PID loop
t0 = time.time()            # Initial time
time.sleep(0.025)
while t < T:

    t = time.time() - t0
    time_data.append(t)

    # Measure the current intensity
    with ni.Task() as task:

        task.ai_channels.add_ai_voltage_chan("Dev22/ai0", terminal_config=ni.constants.TerminalConfiguration.RSE)
        actual_intensity = task.read(1)[0]
        photodiode_data.append(actual_intensity)

        error = set_point - actual_intensity

        dt = time_data[-1] - time_data[-2]
        integral = integral + error * dt
        derivative = (error - last_error) / dt
        output.append(Kp * error + Ki * integral + Kd * derivative)
        last_error = error

    # Set the voltage on the LED controlled by the DAQ
    with ni.Task() as task:

        task.ao_channels.add_ao_voltage_chan("Dev22/ao0", min_val=0, max_val=5)
        task.write(output[-1]+output[-2], auto_start=True)         # If output < 0 ? --> Error ?


plt.plot(time_data[1:], photodiode_data, 'o-')


# ----------------------------------------------------------------------------------------------------------------------
# With the condition on the variability of the photodiode measurement
# ----------------------------------------------------------------------------------------------------------------------
with ni.Task() as tarea:
    tarea.ao_channels.add_ao_voltage_chan("Dev22/ao0", min_val=0, max_val=5)  
    tarea.write(0, auto_start=True)

set_point = mean_reference_intensity        # Intensity (voltage proportional to it) on the photodiode to keep constant
T = 20                                      # Total time in which the PID loop is implemented (in seconds)
t = 0

photodiode_data = []                        # Signal measured with the photodiode
time_data = [t]                             # Time

last_error = 0                              # Initial condition
integral = 1.5                              # Initial condition
Kp = 2                                      # Proportional constant
Ki = 0.6                                      # Integral constant
Kd = 0.8                                    # Derivative constant

# Begins the PID loop

t0 = time.time()            # Initial time
time.sleep(0.025)
while t < T:

    t = time.time() - t0
    time_data.append(t)

    # Measure the current intensity
    with ni.Task() as task:

        task.ai_channels.add_ai_voltage_chan("Dev22/ai0", terminal_config=ni.constants.TerminalConfiguration.RSE)
        actual_intensity = task.read(1)[0]

    photodiode_data.append(actual_intensity)

    error = set_point - actual_intensity

    if error > dispersion:

        dt = time_data[-1] - time_data[-2]
        integral = integral + error * dt
        derivative = (error - last_error) / dt
        output = Kp * error + Ki * integral + Kd * derivative
        last_error = error

        # Set the voltage on the LED controlled by the DAQ
        with ni.Task() as task:

            task.ao_channels.add_ao_voltage_chan("Dev22/ao0", min_val=0, max_val=5)
            task.write(output, auto_start=True)         # If output < 0 ? --> Error ?

    else:

        print("Error <= Dispersion")


plt.plot(time_data[1:], photodiode_data, 'o-')


# ----------------------------------------------------------------------------------------------------------------------
# Useful codes
# ----------------------------------------------------------------------------------------------------------------------

# Turn ON the LED
with ni.Task() as task:
    task.ao_channels.add_ao_voltage_chan("Dev22/ao0", min_val=0, max_val=5)
    task.write(3, auto_start=True)

# Turn OFF the LED
with ni.Task() as task:
    task.ao_channels.add_ao_voltage_chan("Dev22/ao0", min_val=0, max_val=5)
    task.write(0, auto_start=True)

# ----------------------------------------------------------------------------------------------------------------------
to = time.time()
t = time.time() - to


#-------------------------------------------------PRUEBA TOMAS

fg.apaga()
fg.prende()
fg.set_forma('SIN') #string = {SINusoid|SQUare|PULSe|RAMP|PRNoise|DC|SINC|GAUSsian|LORentz|ERISe|EDECay|HAVersine|USER[1]|USER2|USER3|USER4|EMEMory|EFILe}
fg.set_frec(4, 'Hz')
fg.set_amp(3)
T_0 = 3
reference_intensity = []

t_0 = time.time()
while (time.time() - t_0) < T_0:

    with ni.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev22/ai0", terminal_config=ni.constants.TerminalConfiguration.RSE)
        reference_intensity.append(task.read(1)[0])

mean_reference_intensity = np.mean(reference_intensity)              # To use as set point
dispersion = np.max(reference_intensity)-np.min(reference_intensity) # Intensity dispersion with 'constant' illumination

pp.plot(reference_intensity)
# ------- PID ----------------------------------------------------------------------------------------------------------

with ni.Task() as tarea:
    tarea.ao_channels.add_ao_voltage_chan("Dev22/ao0", min_val=0, max_val=5)  
    tarea.write(0, auto_start=True)
    
set_point = mean_reference_intensity        # Intensity (voltage proportional to it) on the photodiode to keep constant
T = 15                                      # Total time in which the PID loop is implemented (in seconds)
t = 0

photodiode_data = []                        # Signal measured with the photodiode
time_data = [t]                             # Time

last_error = 0                              # Initial condition
integral = 0                              # Initial condition
Kp = 50                                      # Proportional constant
Ki = 20                               # Integral constant
Kd = 20                            # Derivative constant

output = [0]

# Begins the PID loop
t0 = time.time()            # Initial time
time.sleep(0.025)
while t < T:

    t = time.time() - t0
    time_data.append(t)

    # Measure the current intensity
    with ni.Task() as task:

        task.ai_channels.add_ai_voltage_chan("Dev22/ai0", terminal_config=ni.constants.TerminalConfiguration.RSE)
        actual_intensity = task.read(1)[0]
        photodiode_data.append(actual_intensity)

        error = set_point - actual_intensity

        dt = time_data[-1] - time_data[-2]
        integral = integral + error * dt
        derivative = (error - last_error) / dt
        output.append(Kp * error + Ki * integral + Kd * derivative)
        last_error = error

    # Set the voltage on the LED controlled by the DAQ
    alimentacion=output[-1]+actual_intensity
    
    if alimentacion > 0 and alimentacion < 5:
        with ni.Task() as task:
            task.ao_channels.add_ao_voltage_chan("Dev22/ao0", min_val=0, max_val=5)
            task.write(alimentacion, auto_start=True)        # If output < 0 ? --> Error ?

with ni.Task() as tarea:
    tarea.ao_channels.add_ao_voltage_chan("Dev22/ao0", min_val=0, max_val=5)  
    tarea.write(0, auto_start=True)
    
plt.plot(time_data[1:], photodiode_data)

M = [time_data[1:], photodiode_data]
np.savetxt('PIDprueba7.txt', np.transpose(M), header='setpoint = {}'.format(set_point)+'  '+'P {}'.format(Kp)+' '+'I {}'.format(Ki)+' '+'D {}'.format(Kd))

np.mean(photodiode_data)
np.max(photodiode_data)-np.min(photodiode_data)

pp.plot(np.transpose(np.loadtxt('PIDprueba.txt'))[0], np.transpose(np.loadtxt('PIDprueba.txt'))[1])

