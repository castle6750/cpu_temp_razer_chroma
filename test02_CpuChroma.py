import readSensors
from chroma_python_master.ChromaPython import ChromaApp, ChromaAppInfo, ChromaColor, Colors, ChromaGrid
from time import sleep
import ctypes, sys, subprocess
import random

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def rerun_as_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None,
        u"runas",
        (sys.executable),
        (__file__),
        None,
        1
    )

def main():
    Info = ChromaAppInfo()
    Info.DeveloperName = 'Stuart Castle'
    Info.DeveloperContact = 'castle6750@gmail.com'
    Info.Category = 'application'
    Info.SupportedDevices = ['keyboard', 'mouse', 'mousepad', 'headset', 'keypad', 'chromalink']
    Info.Description = 'Python Script for displaying cpu temp'
    Info.Title = 'CPU Chroma'

    App = ChromaApp(Info)

    sleep(2)

    print("OpenHardwareMonitor:")
    HardwareHandle = readSensors.initialize_openhardwaremonitor()
    hardwareSensors = readSensors.fetch_stats(HardwareHandle,False)
    print(hardwareSensors)
    KeyboardGrid = ChromaGrid('Keyboard')

    isRunning = True
    i = 0
    cpuTemp = 0    
    maxTemp = 75
    maxKeyLen = len(KeyboardGrid[i])

    while isRunning:
        temperature = readSensors.fetch_stats(HardwareHandle,False,{})
        cpuTemp = temperature['AMD Ryzen 9 5900X - CPU CCD Average']
        tempRatio = cpuTemp/maxTemp
        n=int(tempRatio*maxKeyLen)
        colorR = int(tempRatio*255)
        colorG = colorR
        for j in range(0, len(KeyboardGrid[i])):
            if j < n:
                #KeyboardGrid[i][j].set(red=color, green=random.random()*100, blue=int(j/maxKeyLen*255))
                #print(int(254-j*12)%255)
                KeyboardGrid[i][j].set(red=colorR%255, green=colorG%255, blue=int(254-j*12)%255)
            else:
                KeyboardGrid[i][j].set(red=0, green=0, blue=0)
        App.Keyboard.setCustomGrid(KeyboardGrid)
        App.Keyboard.applyGrid()
        sys.stdout.write("N: %d Temperature: %d\u00B0C \r" % (n,cpuTemp) )
        sys.stdout.flush()
        #print(n, cpuTemp, end="\r", flush=True)#,colorR%255, colorG%255, int(255-j*12)%255)
        i=(i+1)% len(KeyboardGrid)
        sleep(0.2)

if  __name__ == "__main__":
    #main()

    if is_admin():
        main()
    else:
        rerun_as_admin()