# Microwave Antenna DC Voltage Output Simulator
This Arduino sketch implements a Microwave Receiver Signal Strength to DC Volts Output Simulator using an Arduino Nano, a SSD-1306 OLED, an Adafruit BNO055 9-axis Inertial Measurement Unit and a MCP4725 I2C 12-bit DAC.  SSD1306-based OLED.

You can see a quick video demo of the circuit here: <https://madeitup.com>

## Circuit description: 
A single I2C bus is used by the Arduino Nano to communicate to the OLED, the BNO055 and the MCP4725. The I2C is implemented on default Nano pins: SDA = pin A4; SCL = pin A5; 5.0V = pin 5V on the nano; GND = pin GND on the nano.
* The SSD1306 OLED uses I2C address 0x3c hex
* The BNO055 IMU uses 12C address 0x29 hex
* The MCP4725 uses I2C address 0x62 hex.  Vcc is 5.0V so the analog output range of the MCP4725 will be 0.0V to 5.0V.

The analog output of the MCP4725 represents the object of this simulation, and is meant to mimic the output voltage port of a Microwave receiver, normally used to align the receiver to a distant microwave transmitter. In this case, the higher the received signal strength, the higher the voltage seen at the output port.  The MCP4725 output is connected back to the pin A3 of the Nano for verification and plotting on the OLED.

A momentary pushbutton switch is connected to D5 on the Nano, setup as a digital input with pullup. A switch press will toggle the operational mode between tracking/graphing either Azimuth or Tilt.

## Operation:
In this simulation, changes in Azimuth or Tilt (depending on operational mode) will generate a varying analog output level that simulates slewing the receiver across the main and secondary lobes of a Microwave transmitter signal pattern. Movement of 10 degrees of Azimuth (or Tilt in Tilt mode) from the initial startup / reset position of the BNO055 will generate voltage output that simulates passing through a transmitter's secondary lobe, followed by the main lobe, and then by another secondary lobe.  The multi-lobe output simulation is modeled with 3 piece-wise fitted parobolic curves.

The IMU is configured to use the fast Fusion mode, which provides Euler angles that are relative to the resting point of the board at power on or reset.  The Euler X value represents relative heading and is used as the Azimuth value. Euler Y is Tilt.  The measured azimuth/tilt is applied to a function that returns a corresponding DC voltage value based on 3 piece-wise parabolic equations to simulate the main lobe and two smaller side lobes seen by a microwave receiver when the far end of the link is transmitting.  The returned voltage value is converted to 12-bit digital value and sent to the MCP4725 DAC.  The output of the DAC (which is the subject of our simulation) is tied back to pin A3 on the Nano where it can be read / validated.

Within each measurement loop, the current azimuth/tilt value is printed at the top of the OLED display for reference, and the azimuth/tilt + A3 voltage pair is graphed as an individual pixel on the bottom portion of the OLED.  Reset of the Arduino resets the relative Euler angles to the current board position, resets the OLED display, and the Az vs Tilt mode switch will be read again.

## Calculating End-to-End Fitted Parabolas
The 3 parabolas are fitted end-to-end using the approach shown below. For a single vertically oriented parabola, opening downward:

![Alternate equation for vertical parabola](parabolas.jpg)

With careful design, the h, k and d values for the 3 parabolas can be calculated such that each parabola connects to the next in sequence precisely at the y = 0 crossing points, like so:

![3 piece-wise parabolas](three.jpg)

The getVoltage() function in the Arduino sketch implements this head to tail approach to simulate Side Lobe to Main Lobe to Side Lobe pattern as the BNO055's Azimuth (or Tilt) is traversed through 10 degrees from initial position.

#### End README.md

