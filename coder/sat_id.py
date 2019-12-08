#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# @author kangao
# @since 2019/11/24
import satellite_system


class SatID(object):

    def __init__(self, number=None, ss=satellite_system.GPS):
        self.__satellite_system = ss
        self.__number = number

    @property
    def satellite_system(self):
        return self.__satellite_system

    @satellite_system.setter
    def satellite_system(self, ss):
        self.__satellite_system = ss

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, number):
        self.__number = number

    def __eq__(self, sat_id):
        if not isinstance(sat_id, SatID):
            return False
        return self.satellite_system == sat_id.satellite_system and self.number == sat_id.number

    def __str__(self):
        return '{}{:0>2d}'.format(self.satellite_system.sname, self.number)

    def __repr__(self):
        return self.__str__()

    def parse(self, formatted_string):
        self.__number = int(formatted_string[1:])
        self.__satellite_system = satellite_system.find_satellite_system(formatted_string[0])
        return self
