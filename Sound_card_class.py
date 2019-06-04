# ----- Sound card class -----------------------------------------------------------------------------------------------

import sounddevice as sd
import numpy as np
import scipy.signal as sg


class AudioCard:

    def __init__(self):

        self.device_list = sd.query_devices()                             # List the supported devices.
        self.stop = sd.stop()
        self.duration = None
        self.fs = None
        self.frequency = None
        self.phase = None
        self.waveform = None
        self.loop = None
        self.amplitude = None

    def record(self, fs, duration):                                       # Enter sampling frequency (fs) and duration.

        self.fs = fs
        self.duration = duration

        time = np.linspace(start=0, stop=duration, num=duration*fs)
        recording = sd.rec(frames=int(self.duration * self.fs),
                           samplerate=fs,
                           channels=2,
                           blocking=False,
                           dtype='float32')
        return time, recording

    def playback(self, fs, duration, amplitude, frequency, phase, waveform, loop):
        # loop: boolean; waveform: SIN/SQR/RAMP/PULSE.
        self.fs = fs
        self.duration = duration
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.waveform = waveform
        self.loop = loop

        # Set the input numpy.array to reproduce.
        time = np.linspace(start=0, stop=duration, num=duration*fs)
        sound = None

        if waveform == 'SIN':
            sound = amplitude * np.sin(2 * np.pi * frequency * time + phase)
        elif waveform == 'SQR':
            sound = amplitude * sg.square(2 * np.pi * frequency * time + phase, 0.5)
        elif waveform == 'RAMP':
            sound = amplitude * sg.sawtooth(2 * np.pi * frequency * time + phase, 0.5)
        elif waveform == 'PULSE':
            sound = amplitude * sg.unit_impulse(shape=np.size(time), idx='mid')

        sd.play(data=sound,
                samplerate=fs,
                blocking=False,
                loop=loop)

        return time, sound

    def playback_record(self, fs, duration, amplitude, frequency, phase, waveform, loop):

        self.fs = fs
        self.duration = duration
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.waveform = waveform
        self.loop = loop

        # Set the input numpy.array to reproduce
        time = np.linspace(start=0, stop=duration, num=duration*fs)
        sound = None

        if waveform == 'SIN':
            sound = amplitude * np.sin(2 * np.pi * frequency * time + phase)
        elif waveform == 'SQR':
            sound = amplitude * sg.square(2 * np.pi * frequency * time + phase, 0.5)
        elif waveform == 'RAMP':
            sound = amplitude * sg.sawtooth(2 * np.pi * frequency * time + phase, 0.5)
        elif waveform == 'PULSE':
            sound = amplitude * sg.unit_impulse(shape=np.size(time), idx='mid')

        recording = sd.playrec(data=sound,
                               samplerate=fs,
                               blocking=False)  # If False, return immediately (but continue playrec in the background).

        return time, sound, recording
