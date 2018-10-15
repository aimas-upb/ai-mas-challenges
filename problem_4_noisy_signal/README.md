# The signal challenge

The challenge is to predict / smooth the real signal from a noisy device. You will get the noisy data from the SignalReceiver class and you will have to reduce its noise. 

Get that error to minimum!

## Getting Started

You can use whatever tools or algorithms you want.

The value is received by calling the get_value function and the corrected value is added by calling push_value. A sample code is already provided in the main method.

## Submission Format

Send us the SignalReceiver.py file with the main method rewritten to reduce the error of our dumb example. 

### Rules

1. Do not change the SignalReceiver class.  
2. Do not change the test files to trick the error.
3. Any variable or method starting with __ should be considered inaccessible. 
4. Every call of get_value should be followed by a call to push_value.

## Data overview

All the tests contain 10k samples. There are 5 tests, each with a different noisy signal. 
The reading of the data is done by the SignalReceiver class.