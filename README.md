# Audio-Waveform-Plotter

Small python project to plot the waveform of any audio .wav file.

The final plot uses a slider to scroll through the whole wavefrom graph, so that you can have a better image of how the plot looks.
(If you try to plot the whole thing into one figure you might not get a good picture of how it really looks)

I am using a pyaudio stream to get the date I need from the audio file and then I smooth the data out using a gaussian fliter (although
there is also the option to use cubic interpolation commented out in WaveformPlotter.py)

HOW TO USE:
1. Put the audio file you want to plot into the "sounds" folder
2. Rename the audio file to have the name "input"
3. Run the WaveformPlotter.py script
# Audio-Waveform-Plotter
