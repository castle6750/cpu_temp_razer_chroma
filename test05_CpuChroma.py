import pyaudio
import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(suppress=True) # don't use scientific notation

CHUNK = 4096 # number of data points to read at a time
#RATE = 44100 # time resolution of the recording device (Hz)


p=pyaudio.PyAudio() # start the PyAudio class
deviceArray = []
for deviceIndex in range(p.get_device_count()):
    info = p.get_device_info_by_index(deviceIndex)
    #if not info["maxOutputChannels"]>0:
    print(info)
    deviceArray.append(deviceIndex)
device_id = deviceArray[19]
device_info = p.get_device_info_by_index(device_id)
if (device_info["maxOutputChannels"] < device_info["maxInputChannels"]):
    channelcount = device_info["maxInputChannels"]
else:
    channelcount = device_info["maxOutputChannels"]

RATE = int(device_info["defaultSampleRate"])
print(device_info)
stream=p.open(
    format=pyaudio.paInt16,
    channels=channelcount,
    rate = RATE,
    input=True,
    #output=True,
    input_device_index=device_id,
    frames_per_buffer=CHUNK, 
    as_loopback = True)

fig, ax = plt.subplots()
x = np.arange(0, 2*CHUNK, 2)
line, = ax.plot(x, np.random.rand(CHUNK), 'r')
ax.set_ylim(-60000,60000)
ax.set_xlim(0,CHUNK)
fig.show()
# create a numpy array holding a single read of audio data
isRunning = True
while isRunning:
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    data = data * np.hanning(len(data)) # smooth the FFT by windowing data
    fft = abs(np.fft.fft(data).real)
    fft = fft[:int(len(fft)/2)] # keep only first half
    freq = np.fft.fftfreq(CHUNK,1.0/RATE)
    freq = freq[:int(len(freq)/2)] # keep only first half
    freqPeak = freq[np.where(fft==np.max(fft))[0][0]]+1
    #print("peak frequency: %d Hz"%freqPeak)

    line.set_ydata(data)
    fig.canvas.draw()
    fig.canvas.flush_events()
    # uncomment this if you want to see what the freq vs FFT looks like
    #plt.plot(freq,fft)
    #plt.axis([0,4000,None,None])
    #plt.show()
    #plt.close()

# close the stream gracefully
stream.stop_stream()
stream.close()
p.terminate()