from machine import Pin, PWM
import utime as time
import network, socket
import sys
import keys
# Make sure keys.py in copied to the Raspberry Pi Pico W in root or /lib directory

# Setup the LEDs
redPin = 16
greenPin = 17
bluePin = 18
redLED = PWM(Pin(redPin))
greenLED = PWM(Pin(greenPin))
blueLED = PWM(Pin(bluePin))
redLED.freq(1000)
greenLED.freq(1000)
blueLED.freq(1000)
redLED.duty_u16(0)
greenLED.duty_u16(0)
blueLED.duty_u16(0)

picoLED = Pin('LED', Pin.OUT)

# Connect to WiFi and create a UDP socket
connected = False
count = 20
# Connect to WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(keys.SSID, keys.PSWD)
while connected == False and count > 0:
    print('Waiting for Connection...')
    picoLED.on()
    time.sleep(0.2)
    picoLED.off()
    count = count - 1
    connected = wifi.isconnected()
    time.sleep(1)

if connected:
    wifiInfo = wifi.ifconfig()	# Grab the server IP address
    print(wifiInfo)
    picoLED.on()
    ServerIP = wifiInfo[0]
    ServerPort = 2222			# Set the server port and buffer size
    bufferSize = 1024
    
    # Open a UDP socket and bind the IP to it
    # Put Try-Except around socket creation / binding?
    UDPServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPServer.bind((ServerIP, ServerPort))	# bind wants to be passed a tuple...
    print('UDP Server Up and Waiting...')
    serving = True
else:
    print("Connection Failed")      
    serving = False
    sys.exit("No network connection. Closing Program.")

# Listen for commands from clients
print("Serving")
try:
    while serving:
        # Here is where the server will loop to receive commands from the clients
        #print("Serving")
        time.sleep(0.25)
        
        message, address = UDPServer.recvfrom(bufferSize)
        messageDecoded = message.decode('utf-8')
        #print('Message Received: ', messageDecoded, 'From: ', address[0])
        if 'PING' in messageDecoded.upper():
            dataString = "PONG"
            dataStringEncoded = dataString.encode('utf-8')
            UDPServer.sendto(dataStringEncoded, address)
        elif 'RGBLED' in messageDecoded.upper():
            # Parse commands of form: 'RGBLED/RED:redval,GREEN:greenval,BLUE:blueval'
            params = messageDecoded.split('/')
            valPairs = params[1].split(',')
            vDict = {}
            for valPair in valPairs:
                vList = valPair.split(':')
                vKey = vList[0]
                val = int(vList[1])
                vDict[vKey] = val
            redLED.duty_u16(vDict['RED'])
            greenLED.duty_u16(vDict['GREEN'])
            blueLED.duty_u16(vDict['BLUE'])
        elif 'EXIT' in messageDecoded.upper():
            print("User EXIT command received.")
            serving = False
            dataString = "Pico Server: EXIT command received. Disconnecting..."
            dataStringEncoded = dataString.encode('utf-8')
            UDPServer.sendto(dataStringEncoded, address)
        else:
            dataString = "Pico Server: Command not recognized"
            dataStringEncoded = dataString.encode('utf-8')
            UDPServer.sendto(dataStringEncoded, address)

except KeyboardInterrupt:
    print("Keyboard Interrupt")

# Shutdown the server, network connection and application
redLED.duty_u16(0)
greenLED.duty_u16(0)
blueLED.duty_u16(0)
if connected:
    print("Closing server and disconnecting from WiFi")
    picoLED.off()
    UDPServer.close()
    wifi.disconnect()    
print("Program Halted")
