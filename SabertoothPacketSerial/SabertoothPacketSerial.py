#!/usr/bin/python
"""Packet Serial class for Sabertooth speed controllers from Dimension Engineering"""
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


from __future__ import print_function
from builtins import chr
from builtins import bytes
from builtins import range
from builtins import object
import binascii
import datetime
import time
import serial

class SabertoothPacketSerial():
    """Main class"""

    SABERTOOTH_CMD_SET = 40
    SABERTOOTH_CMD_GET = 41
    SABERTOOTH_RC_GET = 73

    SABERTOOTH_GET_VALUE = 0x00
    SABERTOOTH_GET_BATTERY = 0x10
    SABERTOOTH_GET_CURRENT = 0x20
    SABERTOOTH_GET_TEMPERATURE = 0x40

    SABERTOOTH_SET_VALUE = 0x00
    SABERTOOTH_SET_KEEPALIVE = 0x10
    #SABERTOOTH_SET_KEEPALIVE = 16
    SABERTOOTH_SET_SHUTDOWN = 0x20
    SABERTOOTH_SET_TIMEOUT = 0x40

    _conn = None
    _address = None
    _crc = False
    _legacy = False


    """ Main class """
    def __init__(self, port='/dev/ttyACM0', baudrate='9600', address=128,
                 check='Checksum', legacy=False, type='Sabertooth'):
        """ Initialise the object and connect to the serial port

        Parameters:
            self: self
            port: Port to use
            baudrate: Connection baudrate
            address: Address of sabertooth speed controller
            check: Use Checksum or CRC checks
            legacy: Boolean to use new or legacy packet serial mode
            type: Sabertooth or Syren
        """
        if __debug__:
            print("%s : Initialising SabertoothPacketSerial: Port %s : baudrate %s : address %s : Checksum %s " % \
                                    (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                                     port, baudrate, address, check))
        try:
            self._conn = serial.Serial(port, baudrate=baudrate)
        except:
            print("Failed to open serial port %s" % port)
        if check == 'CRC':
            self._crc = True
        else:
            self._crc = False
        self._address = address
        self._legacy = legacy
        self._type = type


    def _write_data(self, data):
        """ Write the data to the serial port object """
        try:
            sent = self._conn.write(data)
        except:
            print("Failed to send data")
        if __debug__:
            print("Private: Packet contents: %s" % binascii.hexlify(data))

    @staticmethod
    def _generate_checksum(data):
        """ Sum of data & 0b01111111 """
        total = sum(bytearray(data))
        checksum = (total & 0b01111111)
        if __debug__:
            print("Private: Checksum generated: %s" % checksum)
        return checksum

    @staticmethod
    def _generate_crc7(data):
        """ Generate a 7-bit CRC """
        return 0

    @staticmethod
    def _generate_crc14(data):
        """ Generate a 14-bit CRC """
        return 0

    def _command(self, command, data):
        """ Run command """
        size_d = len(data)
        if self._crc:
            self._address = address | 0xf0
            # Do some CRC stufF
        buffer = bytearray()
        buffer.append(self._address)
        buffer.append(command)
        buffer.append(data[0])
        if self._crc:
            buffer.append(self._generate_crc7(buffer[0:3]))
        else:
            buffer.append(self._generate_checksum(buffer[0:3]))
        if len(data) > 1:
            for x in range(1, size_d):
                buffer.append(data[x])
            if self._crc:
                buffer.append(self._generate_crc14(buffer[4:4+size_d]))
            else:
                buffer.append(self._generate_checksum(buffer[4:4+size_d]))
        if __debug__:
            print("Private: Command buffer: %s" % binascii.hexlify(buffer))
        self._write_data(buffer)

    def _set(self, type, number, value, setType):
        """ Create the set packet """
        flag = bytes(setType)
        if value < 0:
            print("Value less than 0")
            value = -value
            flag = flag | 1
        data = bytearray(5)
        data[0] = chr(int(flag))
        data[1] = 0 # Reverse bits from value
        data[2] = 0 # Reverse bits from value
        data[3] = type
        data[4] = number
        if __debug__:
            print("Private: Data to send: %s" % binascii.hexlify(data))
        self._command(self.SABERTOOTH_CMD_SET, data)


    def motor(self, number, value):
        """ Set motor :number to :value """
        if __debug__:
            print("Public: Command received: Motor %s %s" % (number, value))
        self._set('M', number, value, self.SABERTOOTH_SET_VALUE)


    def drive(self, value):
        """ Mixed mode drive """
        if __debug__:
            print("Public: Command received: Drive %s" % value)
        if self._legacy == True:
            if value > 1 or value < -1:
                print("Invalid value (%s)" % value)
            else:
                if __debug__:
                    print("Value: %s" % value)
                if value < 0:
                    value = -value # Negative numbers have different command and should be positive
                    command = 9
                else:
                    command = 8
                data = value * 127
                self._write_data(self._generate_checksum_legacy(command, 0, data))
            return 0
        else:
            self.motor('D', value)
            return 0


    def turn(self, value):
        """ Mixed mode turn """
        if __debug__:
            print("Public: Command received: Turn %s" % value)
        if self._legacy == True:
            if value > 1 or value < -1:
                print("Invalid value (%s)" % value)
            else:
                if __debug__:
                    print("Value: %s" % value)
                if value < 0:
                    value = -value # Negative numbers have different command and should be positive
                    command = 11
                else:
                    command = 10
                data = value * 127
                self._write_data(self._generate_checksum_legacy(command, 0, data))
            return 0
        else:
            self.motor('T', value)


    def keepAlive(self):
        """ Send a keepalive call """
        if __debug__:
            print("Public: Command received: keepAlive")
        self._set('M', '*', 0, self.SABERTOOTH_SET_KEEPALIVE)

    ##############################
    # Legacy routines

    def _generate_checksum_legacy(self, command, com_value, data):
        """ Generate a checksum for legacy serial """
        checksum = (self._address + int(command) + int(data)) & 0b01111111
        # if __debug__:
        #    print "Checksum generated : %s" % str(binascii.hexlify(checksum))
        packet = bytearray(4)
        packet[0] = self._address
        packet[1] = chr(int(command))
        packet[2] = chr(int(data))
        packet[3] = chr(checksum)

        return bytes(packet)

    def deadBand(self, value):
        """ Set Deadband """
        if __debug__:
            print("Dead Band...")
        command = 17
        self._write_data(self._generate_checksum_legacy(command, 0, value))
        return 0

    def driveCommand(self, value):
        """ Send a Drive command """
        if __debug__:
            print("Drive....")
        if value > 1 or value < -1:
            print("Invalid value (%s)" % value)
        else:
            if __debug__:
                print("Value: %s" % value)
            if value < 0:
                value = -value # Negative numbers have different command and should be positive
                if self._type == 'Syren':
                    command = 1
                else:
                    command = 9
            else:
                if self._type == 'Syren':
                    command = 0
                else:
                    command = 8
            data = value * 127
            self._write_data(self._generate_checksum_legacy(command, 0, data))
        return 0

    def turnCommand(self, value):
        """ Send a turn command """
        if __debug__:
            print("Turn....")
        if value > 1 or value < -1:
            print("Invalid value (%s)" % value)
        else:
            if __debug__:
                print("Value: %s" % value)
            if value < 0:
                value = -value # Negative numbers have different command and should be positive
                command = 11
            else:
                command = 10
            data = value * 127
            self._write_data(self._generate_checksum_legacy(command, 0, data))
        return 0
