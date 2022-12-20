import sys, os, time
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import readSensors
import chromaHelper, audioHelper

def main(chroma: chromaHelper.Helper, audio: audioHelper.Helper):
    isRunning = True
    while isRunning:
        audioKey = max(audio.data)*255
        temperature = readSensors.fetch_stats(chroma.HardwareHandle,False,{})
        chroma.cpuTemp = temperature['AMD Ryzen 9 5900X - CPU CCD Average']
        tempRatio = chroma.cpuTemp/chroma.maxTemp
        n=int(tempRatio*chroma.maxKeyLen)
        colorR = int(tempRatio*255)
        colorG = audioKey%255       
        for j in range(0, len(chroma.KeyboardGrid[chroma.i])):
            if j < n:
                #KeyboardGrid[i][j].set(red=color, green=random.random()*100, blue=int(j/maxKeyLen*255))
                #print(int(254-j*12)%255)
                chroma.KeyboardGrid[chroma.i][j].set(red=colorR%255, green=colorG%255, blue=int(254-j*12)%255)
            else:
                chroma.KeyboardGrid[chroma.i][j].set(red=0, green=0, blue=0)
        chroma.App.Keyboard.setCustomGrid(chroma.KeyboardGrid)
        chroma.App.Keyboard.applyGrid()
        sys.stdout.write("N: %d Audio: %f Temperature: %d\u00B0C \r" % (n,audioKey,chroma.cpuTemp) )
        sys.stdout.flush()
        #print(n, cpuTemp, end="\r", flush=True)#,colorR%255, colorG%255, int(255-j*12)%255)
        chroma.i=(chroma.i+1)% len(chroma.KeyboardGrid)
        #time.sleep(0.2)

        audio.line_fft.set_ydata(audio.data)
        audio.fig.canvas.draw()
        audio.fig.canvas.flush_events()
        

if  __name__ == "__main__":
    if chromaHelper.is_admin():
        chroma = chromaHelper.Helper()
        audio = audioHelper.Helper()
        audio.startDevice()
        main(chroma, audio)
    else:
        chromaHelper.rerun_as_admin()