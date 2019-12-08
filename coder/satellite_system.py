#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# @author kangao
# @since 2019/11/24

SATELLITE_SYSTEMS = []


class SatelliteSystem(object):

    def __init__(self, sname, lname):
        self.__sname = sname
        self.__lname = lname
        SATELLITE_SYSTEMS.append(self)

    @property
    def sname(self):
        return self.__sname

    @property
    def lname(self):
        return self.__lname

    def __eq__(self, ss):
        if not isinstance(ss, SatelliteSystem):
            return False
        return self.sname == ss.sname and self.lname == ss.lname

    def __str__(self):
        return '{}'.format(self.sname)

    def __repr__(self):
        return self.__str__()


GPS = SatelliteSystem('G', 'GPS')
GLONASS = SatelliteSystem('R', 'GLONASS')
GALILEO = SatelliteSystem('E', 'GALILEO')
BEIDOU = SatelliteSystem('C', 'BEIDOU')
SBAS = SatelliteSystem('S', 'SBAS')


def find_satellite_system(name):
    for satellite_system in SATELLITE_SYSTEMS:
        if satellite_system.sname == name or satellite_system.lname == name:
            return satellite_system
    raise Exception('cannot find satellite system by name, name = %s', name)

