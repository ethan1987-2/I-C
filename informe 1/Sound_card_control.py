# ----- Controling a sound card device ---------------------------------------------------------------------------------

# conda install -c conda-forge python-sounddevice       # Install sounddevice package with Anaconda.

# ======================================================================================================================


import sounddevice as sd                  # sd.get_portaudio_version()
import numpy as np
import matplotlib.pyplot as plt

device_list = sd.query_devices()          # List the supported devices. Return one dictionary for each available device.
# device_list = sd.query_devices(kind=input)


# ---------- Set defaults for the sounddevice module -------------------------------------------------------------------

sd.default.device = 1, 4                  # [input, output] channels by default.
sd.default.channels = 1, 1                # Number of input/output channels.
sd.default.dtype = 'float32', 'float32'   # Data type used for input/output samples.
# sd.default.latency = 'high', 'high'     # Suggested input/output latency in seconds.
sd.default.samplerate = 46000             # Sampling frequency in Hertz (= frames per second).
# reset()                                 # Reset all attributes to their “factory default”.


# ---------- Recording -------------------------------------------------------------------------------------------------
# To record audio data from sound device into a NumPy array (my_recording).

duration = 10                # (seconds) Duration of the recording.
fs = 46000                   # (frames per second) Sampling frequency.
frames = fs * duration       # Total number of frames.

my_recording = sd.rec(frames=int(duration * fs),   # (int, sometimes optional) – Number of frames to record.
                      samplerate=fs,
                      channels=1,                  # (int, optional) – Number of channels to record.
                      mapping=[1],                 # (array_like, optional) – List of channel numbers to record.
                      blocking=True)               # If True, wait until recording is finished.

sd.wait()                   # Wait for rec() to be finished.
# sd.stop()                 # Stop recording

plt.plot(np.linspace(0, duration, frames), my_recording)
plt.xlabel('Time [s]')
plt.ylabel('Signal [arb. unit]')


# ---------- Playback --------------------------------------------------------------------------------------------------
# To playback a NumPy array containing audio data.

duration = 10                # (seconds) Duration of the recording.
fs = 46000                   # (frames per second) Sampling frequency.
frequency = 1                # Frequency in Hz.
phase = 0                    # Phase in radians.

time = np.linspace(start=0, stop=duration, num=duration*fs)
sound_array = np.sin(2 * np.pi * frequency * time + phase)

# plt.plot(time, sound_array)
# plt.xlabel('Time [s]')
# plt.ylabel('Signal [arb. unit]')
# plt.show()

sd.play(data=sound_array,    # Audio data to be played back.
        samplerate=fs,       # Sampling frequency.
        blocking=True,       # If False playback continues in the background, if True, wait until playback is finished.
        loop=False)          # Play data in a loop.

sd.wait()                    # Wait to play() to be finished.
# sd.stop()                  # Stop playback.
