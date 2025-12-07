// ***************************************************************************************************
// Sketch for Microwave Receiver DC Volts Output Simulator using Arduino Nano
// An SSD-1306 OLED, an Adafruit BNO055 9-axis Inertial Measurement Unit and a MCP4725 I2C 12-bit DAC
// SSD1306-based OLED up and running using Adafruit's GFX and SSD1306 libraries.
//
// Circuit description: 
// I2C bus implemented on default Nano pins: SDA = pin A4; SCL = pin A5; 5.0V = pin 5V on the nano; GND = pin GND on the nano.
// SSD1306 OLED using I2C address 0x3c hex
// BNO055 IMU using 12C address 0x29 hex
// MCP4725 using I2C address 0x62 hex.  Vcc is 5.0V so the analog output range of the MCP4725 will be 0.0V to 5.0V.
// The analog output of the MCP4725 is connected back to the pin A3 of the Nano for verification and plotting on the OLED.
// A momentary pushbutton switch is connected to D5, setup as a digital input with pullup. The switch value will determine if 
// angle being monitored and graphed is Azimuth (D5 = HIGH) or Tilt (D5 = LOW). 
//
// The IMU is configured to use the fast Fusion mode, which provides Euler angles that are relative to the resting point of
// the board at power on or reset.  The Euler X value represents relative heading and is used as the Azimuth value. Euler Y is Tilt.
// The measured azimuth/tilt is applied to a function that returns a corresponding DC voltage value based on 3 piece-wise parabolic
// equations to simulate the main lobe and two smaller side lobes seen by a microwave receiver when the far end of the 
// link is transmitting.
// The returned voltage value is converted to 12-bit digital value and sent to the DAC.  The output of the DAC (which is the subject
// of our simulation) is tied back to pin A3 on the Nano where it can be read / validated.
// Within each measurement loop, the current azimuth/tilt value is printed at the top of the OLED display for reference, and the 
// azimuth/tilt + A3 voltage pair is graphed as an individual pixel on the bottom portion of the OLED.
//
// Reset of the Arduino resets the relative Euler angles to the current board position, resets the OLED display, and the Az vs Tilt
// mode switch will be read again.

// Credits / history
// Created by Scott Pettygrove, 25 March 2023
    // OLED code based on Simon Monk's example in "Programming Arduino, 3rd Edition"
    // BNO055 code based on Paul Mcwhorter's youtube series on the BNO055
// ****************************************************************************************************

// Included Libraries
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_MCP4725.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <math.h>

// Defines
// Sample rate for the IMU - can go faster (10ms) using the IMU fusion mode!
#define BNO055_SAMPLERATE_DELAY_MS (10)

// Complier Directives

// Declare variables and Constants
Adafruit_SSD1306 myOLED(128, 64, &Wire, -1);
Adafruit_MCP4725 myDAC;
Adafruit_BNO055 myIMU = Adafruit_BNO055();

int vInPin = A3;          // use analog pin A3 to read DAC voltage output
int AzPin = 5;            // use D5 to detect switch position for Azimuth vs. Tilt operation
int AzPinVal = 0;         // for storing AzPin value during Setup
int buttonValOld = 1;
int buttonValNew;
bool AzMode;              // If true, operational mode is Azimuth. If false, op mode is Tilt
int xVal = 0;             // x value for graphing parabolic voltage response on OLED
int yVal = 0;             // y value for graphing parabolic voltage response on OLED
int dacSetVoltage = 0;    //digital value to write to the DAC to set it's output voltage
int dacReadVoltage = 0;   //digital value of DAC output voltage read from analog pin A3
float azimuth = 0.0;      //azimuth value to feed to the parabolic voltage response function
float voltage = 0.0;      //voltage received from the parabolic voltage response function
float dacOut = 0.0;       //voltage of DAC output after conversion from analog input ADC digital value

/*              // from initial approach using accelerometer, gyro and magnetometer (now abandoned)
float thetaM;   // tilt/pitch angle measured with the accelerometers
float phiM;     // roll angle measured with accelerometers
float thetaFold = 0; //tilt angle filtered - old value
float thetaFnew;  //tilt angle filtered - new value
float phiFold = 0;  // roll angle filtered - old value
float phiFnew;      // roll angle filtered - new value
float theta;  // system pitch from complimentary filter
float phi;    // system roll from complimentary filter
float phiRad; // phi in radians for Az projections
float thetaRad; // theta in radians
float Xm;   //magnetometer x value
float Ym;   //mag y value
float psi;  //Azimuth angle (will need to be corrected to show full 360 deg values)
*/

float EulerX;                     // for Euler X angle, which is relative heading
float EulerY;                     // for Euler Y angle, which is relative tilt
float EulerZ;                     // for Euler Z angle, which is relative roll
float angle, CompAngle;           // used for either Az or Tilt angle. angle is either EulerX or EulerY. CompAngle is angle limited between 0 and 10 deg.

float dt;                         // delta time value for gyro calculations
unsigned long millisOld;          //for calculating delta time relative to current time

void setup() {
  //Start the Arduino serial console - don't need it at the moment
  // Serial.begin(115200);
  // pinMode() statements
  pinMode(vInPin, INPUT);         // using A3 right now
  pinMode(AzPin, INPUT_PULLUP);   // D5 used for reading Az / Tilt switch
  
  // establish operating mode
  AzPinVal = digitalRead(AzPin);  // Read D5 to set operational mode. Mode only changes at power on or with reset.
  if (AzPinVal == HIGH){          // If switch value is HIGH, operational mode is for Azimuth. If LOW, mode is for Tilt.
    AzMode = true;
  }
  else{
    AzMode = false;
  }

  // Start the SSD1306 OLED
  myOLED.begin(SSD1306_SWITCHCAPVCC, 0x3c);

  // Start the MCP4725 DAC
  myDAC.begin(0x62);

  // Start the IMU
  myIMU.begin();
  delay(1000);                  // give the IMU time to start up and settle
  int8_t temp=myIMU.getTemp();  // used this to test that IMU was up and running by printing value to console or OLED
  myIMU.setExtCrystalUse(true); // use external crystal on the IMU module

  // Set up parts of the display
  myOLED.clearDisplay();
  myOLED.drawRoundRect(0, 0, 127, 63, 8, WHITE);
  myOLED.drawFastHLine(1, 15, 126, WHITE);
  myOLED.drawFastHLine(1, 16, 126, WHITE);
  myOLED.display();             // draws these initial screen elements

  millisOld = millis();  // get a good starting point for delta time calculations

} // end setup()

void loop() {
  // Get IMU calibration values and write them to the top of the OLED
  int8_t sys, gyro, accel, mg = 0;                  // Variables for storing IMU calibration values
  myIMU.getCalibration(&sys, &gyro, &accel, &mg);

  // I only need the Euler Vector since relative measurements are fine for our application!  
  //imu::Vector<3> acc = myIMU.getVector(Adafruit_BNO055::VECTOR_ACCELEROMETER);
  //imu::Vector<3> gyr = myIMU.getVector(Adafruit_BNO055::VECTOR_GYROSCOPE);
  //imu::Vector<3> mag = myIMU.getVector(Adafruit_BNO055::VECTOR_MAGNETOMETER);
  imu::Vector<3> eul = myIMU.getVector(Adafruit_BNO055::VECTOR_EULER);

  EulerX = eul.x();   //This is relative heading in degrees. At reset, this is set to 0 degrees. 
  EulerY = -eul.y();  //This is relative tilt in degrees. Set to 0 at reset.
  EulerZ = eul.z();   //This is relative roll in degrees. Set to 0 at reset.

// delta time used for calculating actual angle change from gyroscope's angular velocity values
//  dt = (millis() - millisOld)/1000;
//  millisOld = millis();


// code for graphing Angle transit from 0 deg to 10 deg.
  if (AzMode){
    angle = EulerX;    // in Azimuth mode, use EulerX.
  }
  else {
    angle = EulerY;    // in Tilt mode, use EulerY
  }
  if ((angle <= 0) || (angle > 10)){     // limiting Angle to values between 0 and 10 deg, which matches with getVoltage() function
    CompAngle = 0;
  }
  else{
    CompAngle = angle;
  }
  
  xVal = (CompAngle * 120) / 10;            // calculate an x-value for graphing across 120 pixels = 10 deg of Angle change
  voltage = getVoltage(CompAngle);          // call the piece-wise parabolic response function
  dacSetVoltage = 4095*(voltage/5.0);       // calculate digital value to send to MCP4725 DAC. DAC is 12 bit.
  myDAC.setVoltage(dacSetVoltage, false);   // set the DAC output
  delay(5);                                 // wait a bit
  dacReadVoltage = analogRead(vInPin);      // read the DAC voltage back in through analog pin A3
  dacOut = dacReadVoltage*(5.0/1024);       // calculate the voltage value read from A3. Nano analog inputs are 10 bit.
  yVal = 41 - (dacOut*41.0/3.3);            // calculate y-value for graphing
  myOLED.drawPixel(xVal+4, yVal+17, WHITE); // print voltage vs. Angle with some display offsets to place image correctly 
  myOLED.fillRect(3, 4, 120, 10, BLACK);    // erase the screen area used to update Angle value
  myOLED.setTextSize(1);
  myOLED.setTextColor(WHITE);
  myOLED.setCursor(4, 5);
  if (AzMode){
    myOLED.print("Azimuth = ");
  }
  else{
    myOLED.print("Tilt = ");
  }
  myOLED.print(angle);                      // display the non-limited angle
  //Look for pushbutton press and change mode if pressed
  buttonValNew = digitalRead(AzPin);
  if ((buttonValOld == HIGH) && (buttonValNew == LOW)){
    AzMode = !AzMode;
    myOLED.fillRect(5, 20, 120, 40, BLACK); // clear the graph area
  }
  myOLED.display();                         // this will display the pixel to be graphed along with the updated Angle value
  buttonValOld = buttonValNew;

  delay(BNO055_SAMPLERATE_DELAY_MS);        // can go faster with the IMU fusion mode!
} // end loop()


// ***********************************
// ** My Functions and Sub-routines **
// ***********************************
// getVoltage accepts an azimuth input value and returns a voltage value by implementing a piece-wise arrangement of multiple parabolic 
// responses meant to simulate the voltage output of a microwave receiver when looking at a distant microwave dish transmitter 
// as Azimuth is traversed with the receiver.  Multiple parabolas represent the multiple lobes of the Tx antenna pattern as seen by the receiver.
// The parabolas are of the form y = a(x-h)**2 + k where (h,k) is the vertex of the parabola and a is a scalar used to help set
// the 2 x-axis/y=0 zero crossings. If a is -ve, the the parabola opens downwards, which is what we want.
// For the formulas below, the equation has been re-written to replace the scalar "a" with an equivalent value based on k and d where d is the 
// x-distance from the parabola's vertex to either of the y=0 crossings.  After substitution with a = -k/(d**2) the new, reparameterized formula 
// used is now y = -(k/(d**2))*(x-h)**2 + k.  Each parabola can be described with just 3 numbers: h, k and d. (h,k) is the vertex and d is
// the x-distance from vertext to either y=0 crossing, making it easier to chain parabolas end-to-end in the piece-wise response of the function.

float getVoltage (float AzVal){

  // d, h and k for the first parabola using the form:  y = -(k/(d**2))*(x-h)**2 + k
  float d1 = 1;
  float h1 = 1;         // vertex at (1,1); y=0 crossings at x = 0 and x = 2, so d = 1
  float k1 = 1;
  // d, h and k for the second parabola using the form:  y = -(k/(d**2))*(x-h)**2 + k
  float d2 = 3;
  float h2 = 5;         // vertex at (5,3); y=0 crossings at x = 2 and x = 8, so d = 3
  float k2 = 3;
  // d, h and k for the third parabola using the form:  y = -(k/(d**2))*(x-h)**2 + k
  float d3 = 1;
  float h3 = 9;         // vertex at (9,1); y=0 crossings at x = 8 and x = 10, so d = 1
  float k3 = 1;
  float temp;

  if ((AzVal >= 0) && (AzVal < 2)){
    temp = (AzVal-h1);
    temp = sq(temp);                    // Never put an expression inside the () for the sq function. That's a no-no.
    return ((-k1*temp/(d1*d1)) + k1);  
  } 
  if ((AzVal >= 2) && (AzVal <= 8)){
    temp = (AzVal-h2);
    temp = sq(temp);
    return ((-k2*temp/(d2*d2)) + k2);
  } 
    if ((AzVal > 8) && (AzVal <= 10)){
    temp = (AzVal-h3);
    temp = sq(temp);
    return ((-k3*temp/(d3*d3)) + k3);  
  } 
  return 0; //Az value out of bounds
} // end getVoltage
