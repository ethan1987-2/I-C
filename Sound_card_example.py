# ----- An example of how to use the defined classes in Sound_card_class.py and clasesOSCyGF.py ------------------------

import numpy as np
import matplotlib.pyplot as plt
from Sound_card_class import AudioCard
from Oscilloscope_and_Function_generator_classes import OscilloscopeTDS1002B, FunctionGeneratorAFG3021B

audio = AudioCard()

# ----------------------------------------------------------------------------------------------------------------------
# Record an incoming signal.
# The output is a time array and a array with the recorded signal.

time_1, recorded_signal = audio.record(fs=46000, duration=10)  # Record for 10 second at 46000 frames per second.
plt.plot(time_1, recorded_signal)
plt.xlabel('Time [s]')
plt.ylabel('Recorded signal [?]')

fs = audio.fs
duration = audio.duration


# ----------------------------------------------------------------------------------------------------------------------
# Playback some common periodic signal, like sinusoidal or square, to use the sound card like a function generator.
# The output is the time array and a array with the reproduced signal.

time_2, sound = audio.playback(fs=46000, duration=10, frequency=1, phase=0, waveform='SIN', loop=False)
plt.plot(time_2, sound)
plt.xlabel('Time [s]')
plt.ylabel('Playback signal [?]')


# ======================================================================================================================

# Generate a signal with the sound card and acquire it with the oscilloscope

osc = OscilloscopeTDS1002B(serial='C108012')  # Change the serial number
audio = AudioCard()

# Generates a continuous square signal:
time, sound = audio.playback(fs=46000, duration=10, frequency=1, phase=0, waveform='SQR', loop=True)
# Acquire with the oscilloscope:
osc.medir
osc.xun = 's'
osc.yun = 'Volts'
osc.canal = 1
(X, Y) = osc.datos
[X, Y] = np.array([X, Y])

audio.stop
osc.apagar

# Plot acquired data
plt.plot(X, Y)
plt.xlabel('Time [{}]'.format(osc.xun))
plt.ylabel('Signal [{}]'.format(osc.yun))
