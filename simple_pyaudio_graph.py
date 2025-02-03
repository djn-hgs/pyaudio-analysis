import os
import pyaudio
import wave
import numpy
import numpy.fft as fft
import matplotlib.pyplot as plt


# Size of buffer in frames

CHUNK = 1024

# Open an audio file for analysis and playback

base_directory = os.getcwd()
audio_file = 'wavTones.com.unregistred.sin_1000Hz_-6dBFS_3s_lower.wav'
filename = os.path.join(base_directory, audio_file)
wave_file = wave.open(filename, "rb")

# Get meta

rate = wave_file.getframerate()
channels = wave_file.getnchannels()
sample_width = wave_file.getsampwidth()

# Open a playback handle using PyAudio

audio_out = pyaudio.PyAudio()

audio_format = audio_out.get_format_from_width(sample_width)


stream = audio_out.open(format=audio_format, channels=channels, rate=rate, output=True)

# Create a set of axes to display our analysis

plt.ion()

fig, ax = plt.subplots(nrows=1, ncols=1)

title_text = f'File: {audio_file}, Channels: {channels}, Rate: {rate}'

print(title_text)

ax.set_title(title_text)
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('log(Amplitude)')

# Create a line-plot that we can update later

line, = ax.plot([],[])

monitoring = True

while monitoring:

    # Grab a chunk of data from the audio file to analyse

    data = wave_file.readframes(CHUNK)

    if len(data) < CHUNK:
        print('End of file reached')
        monitoring = False

    # Play it (not necessary if we are only analysing)

    stream.write(data)

    # Push data into numpy for analysis

    data_np = numpy.frombuffer(data, dtype=numpy.int16)

    # Append 0s to correct size

    data_np = numpy.pad(data_np, (0, CHUNK-data_np.size), mode='constant', constant_values=0)

    # Analyse using numpy (or scipy - just change at the top)

    # Get the fft data

    yf = fft.fft(data_np)

    # Get amplitudes

    amp = numpy.log(numpy.abs(yf))
    max_amp = numpy.max(amp)

    # Get the analysis frequencies

    xf = fft.fftfreq(CHUNK, 1 / rate)

    data_range = CHUNK // 2

    # Plot them

    line.set_xdata(xf[0:data_range])
    line.set_ydata(amp[0:data_range])

    # Amend the axes

    ax.set_xlim(0, max(xf))
    ax.set_ylim(0, max(1, max_amp))

    # Draw them

    fig.canvas.draw()

    # Not sure what this does

    fig.canvas.flush_events()






