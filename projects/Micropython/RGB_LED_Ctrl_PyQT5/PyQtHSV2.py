import sys, socket
import numpy as np
import pyqtgraph as pyg
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

'''
This python code works together with micropython server code running on a Raspberry Pi Pico W.
The file RGBLEDCtrlWithPyQt.py is an example of Pico Micropython server code that will work properly 
with this python file.

First start the Pico W server code and capture the IP address that the Pico W has been assigned.
Update the code below such that the variable address reflects the Pico W's IP address.
Then run this client code, and it will be able to communicate with the Pico W server.
'''

# Setup network connection as a UDP client
address = '192.168.0.47'                # Get this from the Pico W server connect message
port = 2222
serverAddress = (address, port)     	
bufferSize = 1024                       # Same size as on the server
try:
    UDPClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except:
    print("Socket Error. Could not create socket.")
    sys.exit()
UDPClient.settimeout(5)                 #set time out for exception catching on recvfrom() method

# UDP Send and Receive functions
def udpSend(cmd):
    print(f"Sending {cmd} command to Pico LED Server")
    cmdEncoded = cmd.encode('utf-8')
    UDPClient.sendto(cmdEncoded, serverAddress)

def udpReceive():
    try:
        data,address = UDPClient.recvfrom(bufferSize)
    except TimeoutError:
        print("Receive Timeout Error. Pico Server not responding.")
    else:
        dataDecoded = data.decode('utf-8')
        return dataDecoded

def hsv2RGB(angleIn):
    if angleIn >= 0 and angleIn < 60:
        r = 1
        g = 0
        b = angleIn/60
    if angleIn >= 60 and angleIn < 120:
        r = 1 - (angleIn - 60)/60
        g = 0
        b = 1
    if angleIn >= 120 and angleIn < 180:
        r = 0
        g = (angleIn - 120)/60
        b = 1
    if angleIn >= 180 and angleIn < 240:
        r = 0
        g = 1
        b = 1 - (angleIn - 180)/60
    if angleIn >= 240 and angleIn < 300:
        r = (angleIn - 240)/60
        g = 1
        b = 0
    if angleIn >= 300 and angleIn <=360:
        r = 1
        g = 1 - (angleIn - 300)/60
        b = 0
    return(r, g, b)

def shiftLeft(a):
    temp = a[0]
    r = len(a)
    for i in range(r-1):
        a[i] = a[i+1]
    a[r-1] = temp
    return a

# Test for connection to Pico
cmd = 'PING'
udpSend(cmd)
decodedData = udpReceive()
if decodedData == 'PONG':
    print(decodedData)
else:
    UDPClient.close()
    sys.exit("Pico not connected.")

# Set up HSV Graph UI
numPoints = 360
count = 0

# x is an array that holds 360 points that represents one trip around the HSV color wheel
# r, g and b are arrays that hold the r,g,b values for each degree of the color wheel
x = []
r = []
g = []
b = []
for i in range(numPoints):
    x.append(i)
    R, G, B = hsv2RGB(i)
    r.append(R)
    g.append(G)
    b.append(B)

def updatePlot():
    global numPoints, x, r, g, b
    r = shiftLeft(r)
    g = shiftLeft(g)
    b = shiftLeft(b)
    plotR.setData(x, r)
    plotG.setData(x, g)
    plotB.setData(x, b)
    red = int(r[0]*65535)
    green = int(g[0]*65535)
    blue = int(b[0]*65535)
    cmd = "RGBLED/"+"RED"+":"+str(red)+","+"GREEN"+":"+str(green)+","+"BLUE"+":"+str(blue)
    udpSend(cmd)

# Setup main PyQt window
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("The HSV Wheel")
window.setGeometry(100, 100, 800, 600)
layout = QVBoxLayout(window)    # window is the parent for the layout
window.setLayout(layout)

# Create the Graph widget
graphWidget = pyg.PlotWidget()
layout.addWidget(graphWidget)
plotR = graphWidget.plot(x, r, pen=pyg.mkPen('r', width=4))
plotG = graphWidget.plot(x, g, pen=pyg.mkPen('g', width=4))
plotB = graphWidget.plot(x, b, pen=pyg.mkPen('b', width=4))
graphWidget.setYRange(-0.25, 1.25)

# Create a Timer
timer = QTimer()
timer.timeout.connect(updatePlot)
timer.start(50)

# Execute the PyQt app
window.show()
app.exec_()
# Close the client when the UI closes
UDPClient.close()
