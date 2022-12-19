import ctypes, sys
import numpy as np
import pyaudio as pa
import struct
import matplotlib.pyplot as plt
import time
import sounddevice as sd
import cffi

CHUNK = 1024 * 2
FORMAT = pa.paInt16
CHANNELS = 2
RATE = 44100 # in Hz

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def rerun_as_admin(file):
    ctypes.windll.shell32.ShellExecuteW(
        None,
        u"runas",
        (sys.executable),
        (file),
        None,
        1
    )

def pythonAudioTest():
    p = pa.PyAudio()

    print ( "Available devices:\n")
    for i in range(0, p.get_device_count()):
        info = p.get_device_info_by_index(i)
        print ( str(info["index"]) +  ": \t %s \n \t %s \n" % (info["name"], p.get_host_api_info_by_index(info["hostApi"])["name"]))
        pass
    device_id = 12
    device_info = p.get_device_info_by_index(device_id)
    print(device_info)
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=int(device_info["defaultSampleRate"]),
        #input=True,
        output=True,
        frames_per_buffer=CHUNK,
        input_device_index=device_info["index"]
    )

    data = stream.read(CHUNK)
    dataInt = struct.unpack(str(CHUNK) + 'h', data)
    print(dataInt)

    fig, ax = plt.subplots()
    x = np.arange(0, 2*CHUNK, 2)
    line, = ax.plot(x, np.random.rand(CHUNK), 'r')
    ax.set_ylim(-60000,60000)
    ax.set_xlim(0,CHUNK)
    fig.show()

    isRunning = True
    while isRunning:
        data = stream.read(CHUNK)
        dataInt = struct.unpack(str(CHUNK) + 'h', data)
        line.set_ydata(dataInt)
        fig.canvas.draw()
        fig.canvas.flush_events()

def sounddeviceTest():
    devices = sd.query_devices()
    print(devices)
    
    stream = sd.RawInputStream(
        samplerate= RATE,
        blocksize=CHUNK,
    )
    input()
    #data = input.read(CHUNK)
    #print(data)
    #dataInt = struct.unpack(str(CHUNK) + 'h', data)
    #print(dataInt)
    #output = sd.RawOutputStream()

cumulated_status = sd.CallbackFlags()

def callback(indata, outdata, frames, time, status):
    global cumulated_status
    cumulated_status |= status
    
    if status:
        print(status, flush=True)
    outdata[:] = indata
    
    #print(sd.get_status(), flush=True)

   
    #print(cumulated_status)
sd.default.blocksize = CHUNK
sd.default.latency = [0.1, 0.1]
sd.default.channels = [2,2]
print("device=", sd.default.device, "\n",
    "samplerate=", RATE, "\n",
    "blocksize=", sd.default.blocksize, "\n",
    "dtype=", sd.default.dtype, "\n",
    "latency=", sd.default.latency, "\n",
    "channels=", sd.default.channels,)
rawStream = sd.RawStream(
    device=sd.default.device,
    samplerate=RATE,
    blocksize=sd.default.blocksize,
    dtype=sd.default.dtype,
    latency=sd.default.latency,
    channels=sd.default.channels,
    #callback=callback
    )
rawStream.start()

ffi = cffi.FFI()
rawBuffer,_ =  rawStream.read(CHUNK)

data = ffi.from_buffer(rawBuffer)

print(data,rawBuffer)
#dataInt = struct.unpack(str(CHUNK) + 'h', data)
#print(dataInt)
isRunning = True
while isRunning:
    rawStream
    time.sleep(0.1)

#if __name__ == "__main__":
#sounddeviceTest()