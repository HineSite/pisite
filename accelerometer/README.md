## Overview
I bought this accelerometer breakout board years ago (from sparkfun) for another project, it is has been laying around ever since. So I decided it would be fun to make a remote control of it.
I placed the accelerometer, the ADC, and two momentary buttons on a small bread board, arrange in a way that allows it to be held like a game console controller.


## Configuration
For this test, I just followed the ADC tutorial on adafruit and replace the potentiometer with my accelerometer.
`https://learn.adafruit.com/mcp3008-spi-adc/python-circuitpython`

For the wiring, I hooked up the ADC as described in the adafruit article:
```
MCP3008 CLK  to Pi SCLK
MCP3008 DOUT to Pi MISO
MCP3008 DIN  to Pi MOSI
MCP3008 VDD  to Pi 3.3V
MCP3008 VREF to Pi 3.3V
MCP3008 AGND to Pi GND
MCP3008 DGND to Pi GND
MCP3008 CS   to Pi GPI022

ACCEL Z   to MCP3008 CH0
ACCEL Y   to MCP3008 CH1
ACCEL X   to MCP3008 CH2
ACCEL GND to Pi GND
ACCEL VCC to Pi 3.3V
```

*P.S. Don't forget to turn SPI on using raspi-config.*


### Libraries
I used the following libraries as described in the adafruit article:
`sudo pip3 install adafruit-blinka`
`sudo pip3 install adafruit-circuitpython-mcp3xxx`


### Software
When the script first runs, it establishes a baseline of the accelerometer's current position (which is displayed to the terminal).
Then, as the accelerometer is moved, it displays:
* delta: How much the reading has changed since it was lasted moved.
* actual: The current ADC value from the mcp3xxx library.
* baseD: The delta between the current ADC value and the initial baseline ADC value.


### Thoughts
* Based on this article describing the math behind getting the g-force: `http://physics.wku.edu/phys318/hardware/sensors/adxl335/`,
	* TLDR: the accelerometer will output a value from 0v to VCC, 0g will measure <sup>1</sup>/<sub>2</sub> VCC, and will output &plusmn;(<sup>1</sup>/<sub>10</sub> VCC)/g.
	* For example, if VCC is 3.3v, 0g will measure 1.65v, and &plusmn; .33v for each g (i.e. -1g = 1.32v, 0g = 1.65v, 1g = 1.98v).
	* To calculate the g-force, I will be using the following formula (where 65535 is the upper value of the resolution from the ADC library I am using): `g = (reading - (65535 * .5)) / (65535 * .1)` or &plusmn; 6553.5/g.
	
* Note: Despite being a 10bit ADC, the adafruit mcp3xxx library provides the ADC values in a 16bit range (0 - 65535).

### Next Steps
* My next step with the accelerometer is measure its angle with relation to ground (i.e. its orientation/tilt).
* Snake!!!

### Fin
These are the parts I bought, though I am pretty sure I didn't pay $16 for the accelerometer...
`https://www.sparkfun.com/products/9269`
`https://www.adafruit.com/product/856`

<sup><sub>Note: if you're using a raspberry pi breakout board, make sure you have the header oriented the right way so you don't end up with -1.6v across VREF and GND on your ADC. I wouldn't know anything about that of course, but something tells me they don't like that and overheat.<sub></sup>
