import os

import matplotlib
import pyaudio
import wave
import numpy as np
import numpy.fft as fft
import matplotlib.pyplot as plt


# Size of buffer in frames

CHUNK = 4096

# Open an audio file for analysis and playback

base_directory = os.getcwd()
filename = os.path.join(base_directory, 'sweep.wav')
wf = wave.open(filename, "rb")

# Get meta

rate = wf.getframerate()
channels = wf.getnchannels()

# Open a playback handle using PyAudio

p = pyaudio.PyAudio()

audio_format = p.get_format_from_width(wf.getsampwidth())

stream = p.open(format=audio_format, channels=channels, rate=rate, output=True)

# Create a set of axes to display our analysis

plt.ion()

fig, ax = plt.subplots(nrows=1, ncols=1)

ax.set_title('Audio Example')

# Create a line-plot that we can update later

line, = ax.plot([],[])

# Show it (but we're going to keep updating it)

plt.show()


monitoring = True

while monitoring:

    # Grab a chunk of data from the audio file to analyse

    data = wf.readframes(CHUNK)

    # Play it (not necessary if we are only analysing)

    stream.write(data)

    # Push data into numpy for analysis

    data_np = np.frombuffer(data, dtype=np.int16)

    # Analyse using numpy (or scipy - just change at the top)

    # Get the fft data

    yf = fft.fft(data_np)

    # Get amplitudes

    amp = np.abs(yf)

    # Get the analysis frequencies

    xf = fft.fftfreq(CHUNK, channels / rate)

    data_range = CHUNK // 2

    # Plot them

    line.set_xdata(xf[0:data_range])
    line.set_ydata(amp[0:data_range])

    # Amend the axes

    ax.set_xlim(0, max(xf))
    ax.set_ylim(0, max(amp))

    # Draw them

    fig.canvas.draw()

    # Not sure what this does

    fig.canvas.flush_events()






