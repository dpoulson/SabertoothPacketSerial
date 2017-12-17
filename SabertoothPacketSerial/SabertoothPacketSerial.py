#!/usr/bin/python
# ===============================================================================
# Copyright (C) 2017 Darren Poulson
#
# This file is part of SabertoothPacketSerial.
#
# SabertoothPacketSerial is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# SabertoothPacketSerial is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SabertoothPacketSerial.  If not, see <http://www.gnu.org/licenses/>.
# ===============================================================================


import serial
import time
import binascii

class SabertoothPacketSerial(object):

    _conn = None
    _address = None
    _crc = False

    """ Main class """
    def __init__(self, port='/dev/ttyACM0', baudrate='9600', address=128, check='Checksum'):
        if __debug__:
            print "Initialising SabertoothPacketSerial: Port %s : baudrate %s : address %s : Checksum %s " % (port, baudrate, address, check)
        try:
            self._conn = serial.Serial(port,baudrate=baudrate)
        except:
            print "Failed to open serial port %s" % port
        if check == 'CRC':
            self._crc = True
        self._address = address


    def _write_data(self,data):
        try:
            sent = self._conn.write(data)
        except:
            print "Failed to send data"
        if __debug__:
            print "Packet contents: %s" % str(data)
            print "Data sent: {0}".format(sent)
#            return_bytes = self._conn.read(sent)
#            print "Loopback data - type: ", type(return_bytes), ", length: ",len(return_bytes), ", raw value: ", ','.join([x for x in return_bytes]), ", unicode representation: ", unicode(return_bytes)




    def _generate_checksum_packet(self, command, com_value, data):
        checksum = (self._address + int(command) + int(data)) & 0b01111111 
        if __debug__:
            print "Checksum generated : %s" % checksum
        packet = bytearray(4)
        packet[0] = self._address
        packet[1] = chr(int(command))
        packet[2] = chr(int(data))
        packet[3] = chr(checksum)

        return bytes(packet)


    def driveCommand(self, value):
        print "Drive...."
        if value > 1 or value < -1:
            print "Invalid value (%s)" % value
        else:
            if __debug__:
                print "Value: %s" % value
            if value < 0:
                value = -value # Negative numbers have different command and should be positive
                command = 9
            else:
                command = 8
            data = value * 127
            self._write_data(self._generate_checksum_packet(command, 0, data))
        return 0


    def turnCommand(self, value):
        print "Turn...."
        if value > 1 or value < -1:
            print "Invalid value (%s)" % value
        else:
            if __debug__:
                print "Value: %s" % value
            if value < 0:
                value = -value # Negative numbers have different command and should be positive
                command = 11
            else:
                command = 10
            data = value * 127
            self._write_data(self._generate_checksum_packet(command, 0, data))
        return 0



    def sendText(self, cmds):
        self._conn.write(cmds + b'\r\n')
 

    def getText(self, cmds):
        self.sendText(cmds)
        result = self._conn.read(100)
        return result


