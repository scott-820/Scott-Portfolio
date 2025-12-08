# Controlling a Raspberry Pi Pico's RGB LED over a WiFi Network using UDP
This project demonstrates control of an RGB LED hosted on a Raspberry Pi Pico microcontroller from a Python PyQt5 client running on a PC. Communication between the two programs is through a UDP/IP network, with the Pico W connected on local WiFi. The client PC would normally be connected through Ethernet or WiFi. 

The Pico Server was programmed in Micropython using the Thonny IDE, and the PyQT5 client was programmed using Python 3 with VS Code as the IDE.  Click here to see an overly long video demo of the system in use, along with some discussion of both client and server coding highlights:  <https://youtu.be/Ybl9M-CCBwQ>

The project is my solution to an assignment given by Paul McWhorter in his wonderful YouTube series on how to get the most out of your Raspberry Pi Pico W.  If you want to see his treasure trove of useful microcontroller / maker / STEM related tutorials, Paul's YouTube page can be found here: [Paul McWhorter's YouTube Page ](https://www.youtube.com/@paulmcwhorter)

## The PyQt5 Client
The PyQt client software runs on a PC and communicates to the Raspberry Pi Pico server over a UDP socket.  The program plots time-varying, offset waveforms for red, green and blue LED values and sends a stream of UDP commands to the Raspberry Pi Pico server that corresponds to the time varying RGB values. There are two versions of the client in this repo:
* 'PyQtSinWave.py' uses sin waves to generate the R, G and B values
* 'PyQtHSV2.py' uses piece-wise linear waveforms for the R, G and B values that more fully exercise the Hue, Saturation and Value (intensity) combinations in the HSV color wheel.
### Client Requirements
To run either client, the following Python packages must be installed either globally or within a Virtual Environment on your PC:
* numpy
* PyQt5
* pyqtgraph

## The Raspberry Pi Pico Server
The Pico W Micropython server code was developed using the Thonny IDE. It is recommended that the server code be executed while the Pico W is connected over USB to Thonny so that print outputs from the Micropython program can be seen in the IDE.

The GPIO pin selection and connection of the RGB LED to the Pico W are easily determined by inspecting the Micropython code.
### Server Requirements
To run the Pico W server, the following micropython packages must be available to the Pico W:
* machine, Pin, PWM
* time, network, socket, sys
* keys (see discussion on 'keys.py' below)

## Operational Sequence
There are several steps that must be taken to get the client and server to work together properly:
### On the Pico W Server
* Update the 'keys.py' file to reflect the SSID and Password for the WiFi network that the Raspberry Pi Pico W will connect to.
* After modification, ensure that the file 'keys.py' has been copied to the Raspberry Pi Pico into either the root or the /lib directory. This is so that the 'import keys' statement in the micropython program will load the WiFi network login info correctly.
* Start the Pico W server using Thonny and while connected to the Pico W over USB. This will allow you to see console prints to the IDE that include the IP address that as assigned to the Pico W.
* The Pico W's on-board LED will blink slowly while it is connecting to the WiFi network, and will remain solidly lit once the connection has been made.
* Once connected, the Pico W's IP address will be printed to the Thonny IDE. Record the IP address as you will need it to update the client python code so that client and server can communicate over a UDP socket.

### On the PC based client
* Ensure that the Raspberry Pi Pico W server is running and that you have captured the Pico W IP address as noted above.
* In your Python IDE, update the value of the 'address' variable near the top of the client file to reflect the Pico W's IP address.  For example, set:  address = '192.168.1.77' if that is what the Pico W was assigned.
* Run the client code.

You should now see a time varying plot of 3 waveforms, one each for Red, Green and Blue on the client PC, as well as a stream of UDP commands in the client console that are being sent to the Pico W.  You should also see the RGB LED on the Pico W circuit updating in sync with the time varying client RGB waveforms as the Pico W receives and processes the UDP commands from the client.

#### End README.md

