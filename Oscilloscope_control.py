# ----- Controlling the oscilloscope without using Lantz ---------------------------------------------------------------

import visa                             # Control measurement devices
import numpy as np                      # Numerical Python
import matplotlib.pyplot as plt         # Plotting library

rm = visa.ResourceManager('C:\\Windows\\system32\\visa64.dll')
#  If we called this object without argument, PyVISA will use the default backend (NI), which tries to find a VISA
#  shared library.
#  print(rm)

instruments = rm.list_resources()
#  List the available resources, the output is a tuple listing the VISA resource names.
#  ‘?*::INSTR’ means that by default only instrument whose resource name ends with ‘::INSTR’ will be listed.
#  See VISA Resource Syntax: https://pyvisa.readthedocs.io/en/1.8/names.html.

osci = rm.open_resource('USB0::0x0699::0x0363::C102220::INSTR')
#  Ask the ResourceManager to open the instrument and
#  assign the returned object to the 'osci' (oscilloscope).
#  Argument --> USB[board]::manufacturer ID::model code::serial number[::USB interface number][::INSTR]
#  print(osci)

print(osci.query('*IDN?'))  # Query the device: What are you?

# ----------------------------------------------------------------------------------------------------------------------
# In the following lines we consider a TEK TDS2000 oscilloscope (see programmer's manual).
# ----------------------------------------------------------------------------------------------------------------------

# Observation: Using PyVISA, instead of separate write and read operations, you can do both with one query() call.

# So:
# >>> my_instrument.query("*IDN?")
# is the same as:
# >>> my_instrument.write('*IDN?')
# >>> print(my_instrument.read())

# ---------------------------------------------------------------------------------------------------------------------

CH = 'CH1'      # (CH2)Specify the channel to use as a mnemonic in the header. (2-9)
start = '1'     # Integer value from 1 to 2500. Specifies the first data point that will be transferred. (2-90)
stop = '2500'   # Integer value from 'start' to 2500. Specifies the last data point that will be transferred. (2-91)
ENC = 'RPB'     # Select the format of the waveform data.
#                 ASCII: ASCII data is represented by signed integer values.
#                 RIB: RIBinary is signed integer where the most significant byte is transferred first
#                 SRI: like RIB but use a swapped byte order where the least significant byte is transferred first.
#                 RPB: RPBinary is positive integer where the most significant byte is transferred first.
#                 SRP: like RPBinary but use a swapped byte order.
DatWidth = '1'  # 1 byte (8 bites) data. Number of bytes per data point.


osci.write('ACQuire:STATE 1')           # Starts (1) or stops (0) oscilloscope acquisitions. Equivalent to RUN/STOP.
osci.query('ACQuire:STATE?')            # Returns 0 or 1, depending on whether or not the acquisition system is running.

osci.query('DAT:ENC {}'.format(ENC))       # Sets  the format of the waveform data. (2-87)
osci.query('DAT:ENC?')                     # Queries  the format of the waveform data.

osci.query('DAT:SOU {}'.format(CH))        # Sets which waveform will be transferred from the oscilloscope. (2-89)
osci.query('DAT:SOU?')

osci.query('DAT:STAR {}'.format(start))    # Sets the starting data point for waveform data transfers.
osci.query('DAT:STAR?')
osci.query('DAT:STOP {}'.format(stop))     # Sets the last data point in the waveform that will be transferred.
osci.query('DAT:STOP?')

osci.query('DAT:WID {}'.format(DatWidth))  # Sets the number of bytes per waveform data point to be transferred.

osci.query('DAT?')                         # Queries the format and location of the waveform data that is transferred.


FORMAT = 'RP'    # RI: Signed Integer, RP: Positive Integer.
DatBit = '8'     # Bits per byte.
endian = 'MSB'   # MSB: Big Endian, LSB: Little Endian.
ENC2 = 'BIN'     # ASC: ASCII, BIN: Binary.
ptsOpico = 'Y'   # Y: Value per point, ENV: peaks positions.
Ut = 's'         # X unit: 's' for second or 'Hz' for hertz.
Dt = '.1'        # Time resolution (step in time domain) in Ut units.
t0 = '0'         # Time of first point, in Ut units.

Dy_dl = '1'      # Vertical scale factor.
y0_dl = '0'      # Vertical offset. This value does not affect how the oscilloscope displays the waveform,
#                  but does affect the cursor readouts.
Uy = 'v'         # Y unit: 'v' for volts.
y0 = '0'         # Waveform conversion factor.

osci.query('WFMP:BYT_N {}'.format(DatWidth))    # WFMPre:BYT_Nr Set or query the preamble byte width of waveform points.
osci.query('WFMP:BIT_N {}'.format(DatBit))      # WFMPre:BIT_Nr Set or query the preamble bit width of waveform points.
osci.query('WFMP:BN_F {}'.format(FORMAT))       # WFMPre:BN_Fmt Set or query the preamble binary encoding type.
osci.query('WFMP:BYT_O {}'.format(endian))      # WFMPre:BYT_Or Set or query the preamble byte order of waveform points.
osci.query('WFMP:ENC {}'.format(ENC2))          # WFMPre:ENCdg Set or query the preamble encoding method.

osci.query('WFMP:PT_F {}'.format(ptsOpico))     # WFMPre:PT_Fmt Set or query the format of curve points.
osci.query('WFMP:XIN {}'.format(Dt))            # WFMPre:XINcr Set or query the horizontal sampling interval.
osci.query('WFMP:XUN {}'.format(Ut))            # WFMPre:XUNit Set or query the horizontal units.
osci.query('WFMP:XZE {}'.format(t0))            # WFMPre:XZEro Set or query the time of first point in waveform.
XZEro = float(osci.query('WFMP:XZE?'))
XINcr = float(osci.query('WFMP:XINcr?'))        # Query the horizontal sampling interval.

osci.query('WFMP:YMU {}'.format(Dy_dl))         # WFMPre:YMUlt Set or query the vertical scale factor.
YMUIty = float(osci.query('WFMP:YMU?'))
osci.query('WFMP:YOF {}'.format(y0_dl))         # WFMPre:YOFf Set or query the vertical offset.
YOFf = float(osci.query('WFMP:YOF?'))
osci.query('WFMP:YZE {}'.format(y0))            # WFMPre:YZEro Set or query the waveform conversion factor.
YZEro = float(osci.query('WFMP:YZE?'))
PT_OFf = float(osci.query('WFMP:PT_OFf'))       # Query the trigger offset.

osci.query('WFMP?')                             # Return waveform preamble.
osci.query('CURV?')                             # Transfer waveform data.
osci.query('WFMP:YUN?')                         # Query the vertical units.

yn_dl = osci.query_binary_values('CURV?', datatype='B', is_big_endian=True)  # Reading binary values.
yn_dl = np.array(yn_dl)  # Create an array.

Yn = YZEro + YMUIty*(yn_dl - YOFf)                              # Formula for magnitude conversion.
Xn = XZEro + XINcr*(np.linspace(1, 2500, num=2500) - PT_OFf)    # Formula for time conversion.

plt.plot(Xn, Yn, '.')
plt.plot(np.log(Yn), '.')
plt.plot(Yn, '.')
plt.xlabel('Time [s]')
plt.ylabel('Voltage [V]')
