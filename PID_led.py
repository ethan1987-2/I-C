import nidaqmx as ni
import numpy as np
import time
from matplotlib import pyplot as plt
# import nimax_clase
# import claseGF
# import claseOSC

system = ni.system.System.local()           # Create an instance of the acquisition system
# system.driver_version                     # Information about the system version

for device in system.devices:
    print(device)                           # Available devices


# ------- Set_point determination --------------------------------------------------------------------------------------

# Turn on the reference LED with a constant voltage and measure the output voltage of the photodiode

T_0 = 5
reference_intensity = []

t_0 = time.time()
while (time.time() - t_0) < T_0:

    with ni.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev22/ai0", terminal_config=ni.constants.TerminalConfiguration.RSE)
        reference_intensity.append(task.read(1)[0])

mean_reference_intensity = np.mean(reference_intensity)              # To use as set point
dispersion = np.max(reference_intensity)-np.min(reference_intensity) # Intensity dispersion with 'constant' illumination


# ------- PID ----------------------------------------------------------------------------------------------------------

set_point = mean_reference_intensity        # Intensity (voltage proportional to it) on the photodiode to keep constant
T = 10                                      # Total time in which the PID loop is implemented (in seconds)
t = 0

photodiode_data = []                        # Signal measured with the photodiode
time_data = [t]                             # Time

last_error = 0                              # Initial condition
integral = 2.5                              # Initial condition
Kp = 1                                      # Proportional constant
Ki = 1                                      # Integral constant
Kd = 0.1                                    # Derivative constant

# Begins the PID loop

t0 = time.time()            # Initial time

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
        output = Kp * error + Ki * integral + Kd * derivative

    # Set the voltage on the LED controlled by the DAQ
    with ni.Task() as task:

        task.ao_channels.add_ao_voltage_chan("Dev22/ao0", min_val=0, max_val=5)
        task.write(output, auto_start=True)         # If output < 0 ? --> Error ?


plt.plot(time_data[1:], photodiode_data, 'o-')


# ----------------------------------------------------------------------------------------------------------------------
# Old code
# ----------------------------------------------------------------------------------------------------------------------


# p = 45
# set_point = 0.3 #Intensidad a mantener fija
# # set_point = 0.32 #Intensidad a mantener fija
# T = 5 #Tiempo máximo
# to = time.time() #Tiempo inicial
# t = 0
# while t < T:
#     t = time.time() - to
#     with ni.Task() as task:
#         task.ai_channels.add_ai_voltage_chan("Dev22/ai0", terminal_config=ni.constants.TerminalConfiguration.RSE)
# #       task.timing.samp_clk_rate = fs #Consultar o cambiar la frecuencia de muestreo de la tarea
#         intensidad_in = task.read(1)[0]
#         error = set_point - intensidad_in
#
#     if intensidad_in > 0.3 and intensidad_in < 0.38:
#         a = 0
#     elif intensidad_in < 0.3:
#         with ni.Task() as tarea:
#             tarea.ao_channels.add_ao_voltage_chan("Dev22/ao0", min_val=0, max_val=5)
#             tarea.write(2, auto_start=True)
#     else:
#         with ni.Task() as tarea:
#             tarea.ao_channels.add_ao_voltage_chan("Dev22/ao0", min_val=0, max_val=5)
#             tarea.write(0, auto_start=True)

# --------------------------------------------------------------------------------------

# Turn ON the LED
with ni.Task() as task:
    task.ao_channels.add_ao_voltage_chan("Dev22/ao0", min_val=0, max_val=5)
    task.write(3, auto_start=True)

# Turn OFF the LED
with ni.Task() as task:
    task.ao_channels.add_ao_voltage_chan("Dev22/ao0", min_val=0, max_val=5)
    task.write(0, auto_start=True)

# --------------------------------------------------------------------------------------
