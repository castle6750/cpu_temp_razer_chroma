import clr #package pythonnet, not clr
import os, sys
openhardwaremonitor_hwtypes = ['Mainboard','SuperIO','CPU','RAM','GpuNvidia','GpuAti','TBalancer','Heatmaster','HDD']
openhardwaremonitor_sensortypes = ['Voltage','Clock','Temperature','Load','Fan','Flow','Control','Level','Factor','Power','Data','SmallData']

cputhermometer_hwtypes = ['Mainboard','SuperIO','CPU','GpuNvidia','GpuAti','TBalancer','Heatmaster','HDD']
cputhermometer_sensortypes = ['Voltage','Clock','Temperature','Load','Fan','Flow','Control','Level']

def initialize_openhardwaremonitor():
    file = os.path.join(os.path.dirname(__file__),"OpenHardwareMonitor\OpenHardwareMonitorLib.dll")
    clr.AddReference(file)

    from OpenHardwareMonitor import Hardware

    handle = Hardware.Computer()
    #handle.MainboardEnabled = True
    handle.CPUEnabled = True
    #handle.RAMEnabled = True
    #handle.GPUEnabled = True
    #handle.HDDEnabled = True
    handle.Open()
    return handle

def initialize_cputhermometer():
    file = os.path.join(os.path.dirname(__file__),"CPUThermometer\CPUThermometerLib.dll")
    clr.AddReference(file)
    
    from CPUThermometer import Hardware
    handle = Hardware.Computer()
    handle.CPUEnabled = True
    handle.Open()
    return handle

def fetch_stats(handle, printer=True, temp = {}):
    for i in handle.Hardware:
        i.Update()
        for sensor in i.Sensors:
            parse_sensor(sensor, printer, temp)
        for j in i.SubHardware:
            j.Update()
            for subsensor in j.Sensors:
                parse_sensor(subsensor, printer, temp)
    return temp

def parse_sensor(sensor, printer, temp):
        if sensor.Value is not None:
            if type(sensor).__module__ == 'CPUThermometer.Hardware':
                sensortypes = cputhermometer_sensortypes
                hardwaretypes = cputhermometer_hwtypes
            elif type(sensor).__module__ == 'OpenHardwareMonitor.Hardware':
                sensortypes = openhardwaremonitor_sensortypes
                hardwaretypes = openhardwaremonitor_hwtypes
            else:
                return
            if sensor.SensorType.value__ == sensortypes.index('Temperature'):
                if printer:
                    print(u"%s %s Temperature Sensor #%i %s - %s\u00B0C" % (hardwaretypes[sensor.Hardware.HardwareType], sensor.Hardware.Name, sensor.Index, sensor.Name, sensor.Value))
                temp[str(sensor.Hardware.Name) + " - " + str(sensor.Name)] = sensor.Value
            else:
                if printer:
                    print(u"%s %s  Sensor #%i %s - %s" % (hardwaretypes[sensor.Hardware.HardwareType], sensor.Hardware.Name, sensor.Index, sensor.Name, sensor.Value))


if __name__ == "__main__":

    print("OpenHardwareMonitor:")
    HardwareHandle = initialize_openhardwaremonitor()
    print(fetch_stats(HardwareHandle))
    #print("\nCPUMonitor:")
    #CPUHandle = initialize_cputhermometer()
    #fetch_stats(CPUHandle)