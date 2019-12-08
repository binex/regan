#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# @author kangao
# @since 2019/11/20

TIME_SYSTEMS = []


class TimeSystem(object):

    def __init__(self, sname, lname):
        self.__sname = sname
        self.__lname = lname
        TIME_SYSTEMS.append(self)

    @property
    def sname(self):
        return self.__sname

    @property
    def lname(self):
        return self.__lname

    def __eq__(self, ts):
        return type(ts) == TimeSystem and self.__sname == ts.__sname and self.__lname == ts.__lname

    def __str__(self):
        return '{} {}'.format(self.__sname, self.__lname)


UNKNOWN = TimeSystem('U', 'UNKNOWN')
GPS = TimeSystem('G', 'GPS')
BDT = TimeSystem('C', 'BDT')
GLO = TimeSystem('R', 'GLO')
GAL = TimeSystem('E', 'GAL')
QZS = TimeSystem('Q', 'QZS')
TT = TimeSystem('T', 'TT')
UTC = TimeSystem('Z', 'UTC')


def find_time_system(name):
    for ts in TIME_SYSTEMS:
        if ts.sname == name or ts.lname == name:
            return ts
    raise Exception('unknown time system name, name = %s' % name)

