# ----- Controlling the function generator -----------------------------------------------------------------------------

import visa
# import numpy as np
# from matplotlib import pyplot as plt

rm = visa.ResourceManager('C:\\Windows\\system32\\visa64.dll')
instruments = rm.list_resources()
fgen = rm.open_resource('USB0::0x0699::0x0346::C034165::INSTR')     # Function generator

CH = '1'            # Select the output channel.
V = '1'             # Select the output voltage in V_unit units.
V_offset = '0'      # Select the output offset in V_unit units.
V_unit = 'VPP'      # Select the voltage unit.
Freq = '1000'       # Select the output frequency in Freq_units.
Freq_unit = 'Hz'    # Select the frequency unit.
Phase = '0'         # Select phase value.
Phase_unit = 'RAD'  # Select phase unit.
Shape = 'SINusoid'  # Select the shape of the output waveform. Examples: 'SINusoid', 'SQUare', 'PULSe', 'RAMP'. (p. 100)

# ----------------------------------------------------------------------------------------------------------------------
# In the following lines we consider a AFG3021B function generator (see programmer's manual).
# ----------------------------------------------------------------------------------------------------------------------

# Set

fgen.query('SOURce{}:VOLTage:LEVel:IMMediate:AMPLitude {}{}'.format(CH, V, V_unit))      # Set output amplitude.
fgen.query('SOURce{}:FREQuency {}{}'.format(CH, Freq, Freq_unit))                        # Set center frequency.
fgen.query('SOURce{}:VOLTage:LEVel:IMMediate:OFFSet {}{}'.format(CH, V_offset, V_unit))  # Set the output offset.
fgen.query('SOURce{}:FUNCtion:SHAPe {}'.format(CH, Shape))                      # Set the shape of the output waveform.
fgen.query('SOURce{}:PHASe:ADJust {}{}'.format(CH, Phase, Phase_unit))                   # Set the phase of output.

# Queries

fgen.query('OUTPut{}:STATe?'.format(CH))                # Query output on or off. (p. 48)
fgen.query('SOURce{}:VOLTage:UNIT?'.format(CH))         # Query the output amplitude units.
fgen.query('SOURce{}:VOLTage?'.format(CH))              # Query the output amplitude.
fgen.query('SOURce{}:FREQuency:CENTer?'.format(CH))     # Query center frequency (not the modulation frequency).
fgen.query('SOURce{}:VOLTage:LEVel:IMMediate:OFFSet?'.format(CH))  # Query the output offset (unit: V).
