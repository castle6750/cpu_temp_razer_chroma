import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
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
class Helper():
    def __init__(self):
        Info = ChromaAppInfo()
        Info = ChromaAppInfo()
        Info.DeveloperName = 'Stuart Castle'
        Info.DeveloperContact = 'castle6750@gmail.com'
        Info.Category = 'application'
        Info.SupportedDevices = ['keyboard', 'mouse', 'mousepad', 'headset', 'keypad', 'chromalink']
        Info.Description = 'Python Script for displaying cpu temp'
        Info.Title = 'CPU Chroma'

        self.App = ChromaApp(Info)

        sleep(2)

        print("OpenHardwareMonitor:")
        self.HardwareHandle = readSensors.initialize_openhardwaremonitor()
        hardwareSensors = readSensors.fetch_stats(self.HardwareHandle,False)
        print(hardwareSensors)
        self.KeyboardGrid = ChromaGrid('Keyboard')

        self.i = 0
        self.cpuTemp = 0    
        self.maxTemp = 95
        self.maxKeyLen = len(self.KeyboardGrid[self.i])

    def main(self):
        isRunning = True
        while isRunning:
            temperature = readSensors.fetch_stats(self.HardwareHandle,False,{})
            self.cpuTemp = temperature['AMD Ryzen 9 5900X - CPU CCD Average']
            tempRatio = self.cpuTemp/self.maxTemp
            n=int(tempRatio*self.maxKeyLen)
            colorR = int(tempRatio*255)
            colorG = colorR
            for j in range(0, len(self.KeyboardGrid[self.i])):
                if j < n:
                    #KeyboardGrid[i][j].set(red=color, green=random.random()*100, blue=int(j/maxKeyLen*255))
                    #print(int(254-j*12)%255)
                    self.KeyboardGrid[self.i][j].set(red=colorR%255, green=colorG%255, blue=int(254-j*12)%255)
                else:
                    self.KeyboardGrid[self.i][j].set(red=0, green=0, blue=0)
            self.App.Keyboard.setCustomGrid(self.KeyboardGrid)
            self.App.Keyboard.applyGrid()
            sys.stdout.write("N: %d Temperature: %d\u00B0C \r" % (n,self.cpuTemp) )
            sys.stdout.flush()
            #print(n, cpuTemp, end="\r", flush=True)#,colorR%255, colorG%255, int(255-j*12)%255)
            self.i=(self.i+1)% len(self.KeyboardGrid)
            sleep(0.2)

if  __name__ == "__main__":
    #main()

    if is_admin():
        chroma = Helper()
        chroma.main()
    else:
        rerun_as_admin()