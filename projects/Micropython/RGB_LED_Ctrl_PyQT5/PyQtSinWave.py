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

# Test for connection to Pico
cmd = 'PING'
udpSend(cmd)
decodedData = udpReceive()
if decodedData == 'PONG':
    print(decodedData)
else:
    UDPClient.close()
    sys.exit("Pico not connected.")

numPoints = 400
xStart = 0
xStop = 4 * np.pi
frequency = 1
count = 0

# Set up increments to change sin wave at different rates
Inc = 2*np.pi/400

# x is an array that holds 200 points that traverses from 0 to 4 * pi radians
x = np.linspace(xStart, xStop, numPoints)
# ySin is an array of Sin(x) values
ySin = np.sin(frequency * x)
ySin2 = np.sin(frequency*x + 2*np.pi/3)
ySin3 = np.sin(frequency*x + 4*np.pi/3)

def updatePlot():
    global numPoints, xStart, xStop, Inc, frequency, count
    xStart = xStart + Inc
    xStop = xStop + Inc
    x = np.linspace(xStart, xStop, numPoints)
    ySin = np.sin(frequency * x)
    ySin2 = np.sin(frequency*x + 2*np.pi/3 + count*Inc)
    ySin3 = np.sin(frequency*x + 4*np.pi/3 + 2*count*Inc)
    plotSin.setData(x, ySin)
    plotSin2.setData(x, ySin2)
    plotSin3.setData(x, ySin3)
    red = int((ySin[0]+1)*65535/2)
    green = int((ySin2[0]+1)*65535/2)
    blue = int((ySin3[0]+1)*65535/2)
    cmd = "RGBLED/"+"RED"+":"+str(red)+","+"GREEN"+":"+str(green)+","+"BLUE"+":"+str(blue)
    udpSend(cmd)
    count = count + 1

def updateFrequency(value):
    global frequency, sliderLabel
    frequency = value/10
    sliderLabel.setText("Frequency: " + str(frequency) + " Hz")

# Setup main PyQt window
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("The Magic of Sin Waves")
window.setGeometry(100, 100, 800, 600)
layout = QVBoxLayout(window)    # window is the parent for the layout
window.setLayout(layout)

# Add slider and label
sliderLabel = QLabel("Frequency: 1 Hz")
layout.addWidget(sliderLabel)
slider = QSlider(Qt.Horizontal)
slider.setMinimum(1)
slider.setMaximum(40)
slider.setValue(10)
slider.valueChanged.connect(updateFrequency)
layout.addWidget(slider)

# Create the Graph widget
graphWidget = pyg.PlotWidget()
layout.addWidget(graphWidget)
plotSin = graphWidget.plot(x, ySin, pen=pyg.mkPen('r', width=4))
plotSin2 = graphWidget.plot(x, ySin2, pen=pyg.mkPen('g', width=4))
plotSin3 = graphWidget.plot(x, ySin3, pen=pyg.mkPen('b', width=4))
graphWidget.setYRange(-1.25, 1.25)

# Create a Timer
timer = QTimer()
timer.timeout.connect(updatePlot)
timer.start(50)

# Execute the PyQt app
window.show()
#sys.exit(app.exec_())
app.exec_()
# Close the client when the UI closes
UDPClient.close()