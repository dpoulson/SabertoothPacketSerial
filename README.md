Sabertooth Packet Serial Class
==============================

This is a python class for using a Sabertooth speed controller that supports packet serial communication. Both new and legacy packet serial modes are supported.

* https://www.dimensionengineering.com/
* https://www.dimensionengineering.com/datasheets/USBSabertoothPacketSerialReference.pdf

Functions 
---------

* init(port, baudrate, address, check, legacy)
* motor(number, value)
* drive(value)
* turn(value)
* keepAlive()


