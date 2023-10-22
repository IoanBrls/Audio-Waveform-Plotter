import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import wave
from matplotlib.widgets import Slider
from scipy.ndimage import gaussian_filter1d
from pydub import AudioSegment

# convert audio file to mono
sound = AudioSegment.from_wav("sounds/input.wav")
sound = sound.set_channels(1)
sound.export("sounds/inputmono.wav", format="wav")

# open the file for reading.
wf = wave.open("sounds/inputmono.wav", 'rb')

# pyaudio class instance
p = pyaudio.PyAudio()

# constants
CHUNK = 512  # samples per frame
FORMAT = p.get_format_from_width(wf.getsampwidth())  # audio format (bytes per sample?)
CHANNELS = wf.getnchannels()  # single channel for microphone
RATE = wf.getframerate()  # samples per second
allFrames = wf.getnframes() # all the frames of the wav file

# create matplotlib figure and axes
fig, ax1 = plt.subplots(1, figsize=(15, 7))

# Adjust the bottom size according to the
# requirement of the user
plt.subplots_adjust(bottom=0.25)

# stream object to get data from microphone
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    output=True
)

# variable for plotting
x = np.arange(0, allFrames, 1)  # samples (waveform)

# Signal range is -32k to 32k
# limiting amplitude to +/- 4k
AMPLITUDE_LIMIT = 32000

# format waveform axes
ax1.set_title('AUDIO WAVEFORM')
ax1.set_xlabel('samples')
ax1.set_ylabel('volume')
# ax1.set_ylim(-AMPLITUDE_LIMIT, AMPLITUDE_LIMIT)
# ax1.set_xlim(0, allFrames)
# plt.setp(ax1, xticks=[0, allFrames/2, allFrames], yticks=[-AMPLITUDE_LIMIT, 0, AMPLITUDE_LIMIT])

# read data (based on the chunk size)
data = wf.readframes(-1)
data_np = np.frombuffer(data, dtype='h')

# Smooth plot using cubic interpolation
# cubic_interpolation_model = interp1d(x, data_np, kind="cubic")
# X_=np.linspace(x.min(), x.max(), allFrames)
# Y_=cubic_interpolation_model(X_)
# plt.plot(X_, Y_)

# Smooth data using gaussian filter
dataSmoothed = gaussian_filter1d(data_np, sigma=3)

plt.plot(x, dataSmoothed)

# Choose the Slider color
slider_color = 'White'

# Set the axis and slider position in the plot
axis_position = plt.axes([0.2, 0.1, 0.65, 0.03],
                         facecolor=slider_color)
slider_position = Slider(axis_position,
                         'Pos', 0, allFrames - CHUNK)

# update() function to change the graph when the
# slider is in use
def update(val):
    pos = slider_position.val
    ax1.axis([pos, pos + CHUNK, -AMPLITUDE_LIMIT, AMPLITUDE_LIMIT])
    fig.canvas.draw_idle()


# update function called using on_changed() function
slider_position.on_changed(update)

# show the plot
plt.show()

# fig.canvas.draw()
# fig.canvas.flush_events()

# cleanup stuff.
wf.close()
stream.close()
p.terminate()