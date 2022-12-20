import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import pyaudio
import os
import numpy as np
import matplotlib.pyplot as plt
import threading, time, struct

class Helper():
    def __init__(self) -> None:
        self.default_device_index = 9
        self.defaultframes = 1024 #int(device_info['defaultSampleRate'])
        self.data = np.random.rand(self.defaultframes)
        self.fig, self.ax = plt.subplots()
        #self.ax.set_ylim(0,6000)

    def startDevice(self):
        self.p = pyaudio.PyAudio()
        print("Available devices:\n")
        for i in range(0, self.p.get_device_count()):
            info = self.p.get_device_info_by_index(i)
            if self.p.get_host_api_info_by_index(info["hostApi"])["name"] == "Windows WASAPI":
                print (str(info["index"]) + ": \t %s \n \t %s \n" % (info["name"], self.p.get_host_api_info_by_index(info["hostApi"])["name"]))

        device_id = self.default_device_index#int(input("Choose device [" + str(self.default_device_index) + "]: ") or self.default_device_index)
        print ("Choosing device [" + str(device_id) + "]")
        device_info = self.p.get_device_info_by_index(device_id)
        is_input = device_info["maxInputChannels"] > 0
        is_wasapi = (self.p.get_host_api_info_by_index(device_info["hostApi"])["name"]).find("WASAPI") != -1
        if is_input:
            print ("Selection is input using standard mode.\n")
        else:
            if is_wasapi:
                useloopback = True
                print ("Selection is output. Using loopback mode.\n")
            else:
                print ("Selection is input and does not support loopback mode. Quitting.\n")
                exit()
        channelcount = device_info["maxInputChannels"] if (device_info["maxOutputChannels"] < device_info["maxInputChannels"]) else device_info["maxOutputChannels"]
        if self.defaultframes == 0:
            self.defaultframes = int(device_info['defaultSampleRate'])
        self.sampleRate = int(device_info["defaultSampleRate"])
        print(device_info)
        self.stream = self.p.open(format = pyaudio.paInt16,
                        channels = channelcount,
                        rate = self.sampleRate,
                        input = True,
                        frames_per_buffer = self.defaultframes,
                        input_device_index = device_info["index"],
                        as_loopback = useloopback)

        samples = int(self.defaultframes * 2)
        x_fft = np.linspace(0, self.sampleRate, samples)
        self.lineFFT, = self.ax.semilogx(x_fft, np.random.rand(samples), 'b')

        #x = np.arange(0, samples, 1)
        #lineData, = ax.plot(x, np.random.rand(samples), 'r')
        #self.lineFFT, = self.ax.plot(x, np.random.rand(samples), 'r')
        
        #self.ax.set_xlim(0, samples)
        self.ax.set_xlim(20,self.sampleRate/2)
        self.ax.set_ylim(0,1)
        self.fig.show()

        cThread = threading.Thread(target = self.updateData)
        cThread.deamon = True
        cThread.start()

        
    def updateData(self):
        
        isRunning = True
        
        while isRunning:
            #data = np.fromstring(self.stream.read(self.defaultframes),dtype=np.int16)
            data = self.stream.read(self.defaultframes)
            dataInt = struct.unpack(str(self.defaultframes*2) + 'h', data)
            fft = np.fft.fft(dataInt)
            freq = np.abs(fft)*2/(11000*self.defaultframes)

            #X = np.fft.fft(data)
            #N = len(X)
            #n = np.arange(N)
            #T = N/self.defaultframes
            #freq = n/T 

            #data = data * np.hanning(len(data)) # smooth the FFT by windowing data
            #fft = abs(np.fft.fft(data))#.real)
            #fft = fft[:int(len(fft)/2)] # keep only first half
            
            #freq = np.fft.fftfreq(self.defaultframes,1.0/self.sampleRate)
            #freq = freq[:int(len(freq)/2)] # keep only first half
            
            #print(len(data),data)
            #print(len(fft),type(fft),fft)
            #print(len(freq),type(freq),freq)

            #freqPeak = freq[np.where(fft==np.max(fft))[0][0]]+1
            #lineData.set_ydata(data)
            self.data = freq
            #self.ax.set_ylim(min(freq),max(freq))
            #self.lineFFT.set_xdata(freq)
            self.lineFFT.set_ydata(freq)


        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

if __name__ == "__main__":
    audio = Helper()
    audio.startDevice()
    while True:
        audio.fig.canvas.draw()
        audio.fig.canvas.flush_events()
        


