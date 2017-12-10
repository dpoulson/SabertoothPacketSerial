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

class SabertoothPacketSerial(object):

    _conn = None
    _address = None

    """ Main class """
    def __init__(self, port='ttyACM0', baudrate='9600', address=128, check='Checksum'):
        if __DEBUG__:
            print "Initialising SabertoothPacketSerial"
        try:
            self._conn = serial.Serial(port,baudrate=baudrate)
        except:
            print "Failed to open serial port"
        self.__address = address


    def _write_data(self,data):
        try:
            self._conn.write(data)
        except
            print "Failed to send data"
        if __debug__
            print "Data contents: %s" % data



