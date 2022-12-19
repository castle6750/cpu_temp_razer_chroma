import readSensors
from RazerChroma.ChromaPythonApp import *
Info = ChromaAppInfo()
Info.DeveloperName = 'Stuart Castle'
Info.DeveloperContact = 'castle6750@gmail.com'
Info.Category = 'application'
Info.SupportedDevices = ['keyboard', 'mouse', 'mousepad', 'headset', 'keypad', 'chromalink']
Info.Description = 'Python Script for displaying cpu temp'
Info.Title = 'CPU Chroma'

App = ChromaPythonApp(Info)

signal.signal(signal.SIGINT, App.stop)

print("Starting the app")
time.sleep(2)
print("App is started")



print("OpenHardwareMonitor:")
HardwareHandle = readSensors.initialize_openhardwaremonitor()
temperature = readSensors.fetch_stats(HardwareHandle,False)
#print("\nCPUMonitor:")
#CPUHandle = cpuTemp.initialize_cputhermometer()
#cpuTemperature, value = cpuTemp.fetch_stats(CPUHandle)

App.Keyboard.applyChromaStaticColor(ChromaColor(0,255,0))
time.sleep(1)

for i in range(20):
    temperature = readSensors.fetch_stats(HardwareHandle,False,{})
    cpuTemp = temperature['AMD Ryzen 9 5900X - CPU CCD Average']
    color = int(cpuTemp / 90 * 255) % 255
    print(cpuTemp,color)
    App.Keyboard.applyChromaStaticColor(ChromaColor(color,0,0))
    time.sleep(1)

App.Keyboard.applyChromaNoneEffect()
App.Keyboard.stop()
App.stop()