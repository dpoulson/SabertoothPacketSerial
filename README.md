Sabertooth Packet Serial Class
==============================

This is a python class for using a Sabertooth speed controller that supports packet serial communication

* https://www.dimensionengineering.com/
* https://www.dimensionengineering.com/datasheets/USBSabertoothPacketSerialReference.pdf

Functions 
---------

8bit mode:

* motor(number, value)
* drive(value)
* turn(value)
* keepAlive()

4bit:

* driveCommand(value)
* turnCommand(value)

