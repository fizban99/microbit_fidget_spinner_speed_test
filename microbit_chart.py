import serial
import serial.tools.list_ports
import numpy
import matplotlib.pyplot
from drawnow import *


def find_microbit():
    """
    Returns the port for the first microbit it finds connected to the host
    computer. If no microbit is found, returns None.
    """
    available_ports = serial.tools.list_ports.comports()
    for port in available_ports:
        pid = port.pid
        vid = port.vid
        # Look for the port VID & PID of the micro_bit.
        if (vid, pid) ==  (0x0D28, 0x0204):
            port_name = port.device
            return port_name
    return None


def makeFig():
    plt.ylim(0,1000)  
    plt.grid(True)
    plt.ylabel(param[0])
    plt.plot(value,"ro-")

max_value=1000
min_value=0
x = 0
x_range = 1000
x_offset = x_range / 10
y_offset= max_value * 0.9
device = find_microbit()
value=[]
if device is None:
    print("Micro:bit not found")
else:
    try:
        ser = serial.Serial(device, 115200)
    except:
        text_turtle.write("Unable to open {}".format(device))
    else:
        print("Waiting")
    while True:
        if ser.in_waiting > 0:
            while ser.in_waiting > 0:
                data = ser.readline().rstrip() # read data from serial
            try:
                data=data.decode("ascii")
            except:
                pass
            else:
                print(data)
                param = data.split(":")
                if len(param)>1:
                    value.append(int(param[1]))
                    drawnow(makeFig)
                    plt.pause(.000001)
                    x=x+1
                    if x>50:
                        value.pop(0)
    ser.close()