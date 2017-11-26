# heatpump
Retrofitted controller for an IVT greenline 14e-9.
The old controller gave up the magic smoke and this is my way to fix it. 

The controller consists of a raspberry pi 3 with a DAQCplate for sensors and controlling relays.
I am using the original NTC thermistors.  The sensors are connected: one lead to +5V, the other lead to ADC input, and a 1.5kΩ between ADC input and GND. This makes a voltage divider and 1.5kΩ fits the complete sensor range for the ADC.
A 5v relay is connected to the output. +5V to flyback protection and the othera lead to GND. The 5V relay run the big 3-phase relay for the compressor. 
