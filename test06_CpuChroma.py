import pyaudio
import os
import numpy as np
import matplotlib.pyplot as plt

# NOTE: this only works on python 3.8
class textcolors:
    if not os.name == 'nt':
        blue = '\033[94m'
        green = '\033[92m'
        warning = '\033[93m'
        fail = '\033[91m'
        end = '\033[0m'
    else:
        blue = ''
        green = ''
        warning = ''
        fail = ''
        end = ''

recorded_frames = []
device_info = {}
useloopback = True
#recordtime = 5

#Use module
p = pyaudio.PyAudio()

#Set default to first in list or ask Windows
try:
    default_device_index = 9 #p.get_default_input_device_info()
except IOError:
    default_device_index = -1

#Select Device
print (textcolors.blue + "Available devices:\n" + textcolors.end)
for i in range(0, p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if p.get_host_api_info_by_index(info["hostApi"])["name"] == "Windows WASAPI":
        print (textcolors.green + str(info["index"]) + textcolors.end + ": \t %s \n \t %s \n" % (info["name"], p.get_host_api_info_by_index(info["hostApi"])["name"]))

    if default_device_index == -1:
        default_device_index = info["index"]

#Handle no devices available
if default_device_index == -1:
    print (textcolors.fail + "No device available. Quitting." + textcolors.end)
    exit()


#Get input or default
device_id = int(input("Choose device [" + textcolors.blue + str(default_device_index) + textcolors.end + "]: ") or default_device_index)
print ("")

#Get device info
try:
    device_info = p.get_device_info_by_index(device_id)
except IOError:
    device_info = p.get_device_info_by_index(default_device_index)
    print (textcolors.warning + "Selection not available, using default." + textcolors.end)

#Choose between loopback or standard mode
is_input = device_info["maxInputChannels"] > 0
is_wasapi = (p.get_host_api_info_by_index(device_info["hostApi"])["name"]).find("WASAPI") != -1
if is_input:
    print (textcolors.blue + "Selection is input using standard mode.\n" + textcolors.end)
else:
    if is_wasapi:
        useloopback = True
        print (textcolors.green + "Selection is output. Using loopback mode.\n" + textcolors.end)
    else:
        print (textcolors.fail + "Selection is input and does not support loopback mode. Quitting.\n" + textcolors.end)
        exit()

#recordtime = int(input("Record time in seconds [" + textcolors.blue + str(recordtime) + textcolors.end + "]: ") or recordtime)

#Open stream
channelcount = device_info["maxInputChannels"] if (device_info["maxOutputChannels"] < device_info["maxInputChannels"]) else device_info["maxOutputChannels"]
defaultframes = 4096 #int(device_info['defaultSampleRate'])
sampleRate = int(device_info["defaultSampleRate"])
print(device_info)
stream = p.open(format = pyaudio.paInt16,
                channels = channelcount,
                rate = sampleRate,
                input = True,
                frames_per_buffer = defaultframes,
                input_device_index = device_info["index"],
                as_loopback = useloopback)

#Start Recording
print (textcolors.blue + "Starting..." + textcolors.end)


#for i in range(0, int(int(device_info["defaultSampleRate"]) / defaultframes * recordtime)):
#    recorded_frames.append(stream.read(defaultframes))
#    print (".")
samples = int(defaultframes)
fig, ax = plt.subplots()
x = np.arange(0, samples, 1)
#lineData, = ax.plot(x, np.random.rand(samples), 'r')
lineFFT, = ax.plot(x, np.random.rand(samples), 'r')

ax.set_ylim(-6000,6000)
ax.set_xlim(0, samples)
fig.show()
isRunning = True
while isRunning:

    #data = stream.read(defaultframes)
    #print(data)
    #dataInt = struct.unpack(str(defaultframes) + 'h', data)
    data = np.fromstring(stream.read(defaultframes),dtype=np.int16)
    data = data * np.hanning(len(data)) # smooth the FFT by windowing data
    fft = abs(np.fft.fft(data))#.real)
    fft = fft[:int(len(fft)/2)] # keep only first half
    freq = np.fft.fftfreq(defaultframes,1.0/sampleRate)
    freq = freq[:int(len(freq)/2)] # keep only first half
    
    #print(len(data),data)
    print(len(fft),fft)
    #print(len(freq),freq)
    
    #freqPeak = freq[np.where(fft==np.max(fft))[0][0]]+1
    #lineData.set_ydata(data)
    lineFFT.set_ydata(fft)
    fig.canvas.draw()
    fig.canvas.flush_events()

print (textcolors.blue + "End." + textcolors.end)
#Stop Recording

stream.stop_stream()
stream.close()

#Close module
p.terminate()
'''
filename = input("Save as [" + textcolors.blue + "out.wav" + textcolors.end + "]: ") or "out.wav"

waveFile = wave.open(filename, 'wb')
waveFile.setnchannels(channelcount)
waveFile.setsampwidth(p.get_sample_size(pyaudio.paInt16))
waveFile.setframerate(int(device_info["defaultSampleRate"]))
waveFile.writeframes(b''.join(recorded_frames))
waveFile.close()
'''