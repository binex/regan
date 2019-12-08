#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# @author kangao
# @since 2019/11/17

from time_base import TimeBase
import time_conf
import time_system
import re


class CivilTime(TimeBase):

    def __init__(self, ts=time_system.UNKNOWN, formatted_string=None):
        self.__year = 0
        self.__month = 0
        self.__day = 0
        self.__hour = 0
        self.__minute = 0
        self.__ms = 0.0
        super(CivilTime, self).__init__(ts, formatted_string)

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, year):
        if not isinstance(year, int):
            raise Exception('year must be integer')
        self.__year = year

    @property
    def month(self):
        return self.__month

    @month.setter
    def month(self, month):
        if not isinstance(month, int):
            raise Exception('month must be integer')
        if month < 1 or month > 12:
            raise Exception('month must be in [1,12]')
        self.__month = month

    @property
    def day(self):
        return self.__day

    @day.setter
    def day(self, day):
        if not isinstance(day, int):
            raise Exception('day must be integer')
        if day < 1 or day > 366:
            raise Exception('day must be in [1,366]')
        self.__day = day

    @property
    def hour(self):
        return self.__hour

    @hour.setter
    def hour(self, hour):
        if not isinstance(hour, int):
            raise Exception('hour must be integer')
        if hour < 0 or hour > 23:
            raise Exception('hour must be in [0,23]')
        self.__hour = hour

    @property
    def minute(self):
        return self.__minute

    @minute.setter
    def minute(self, minute):
        if not isinstance(minute, int):
            raise Exception('minute must be integer')
        if minute < 0 or minute > 59:
            raise Exception('minute must be [0,59]')
        self.__minute = minute

    @property
    def second(self):
        return self.__ms/1000.0

    @second.setter
    def second(self, second):
        if not isinstance(second, float):
            raise Exception('second must be float')
        if second < 0:
            raise Exception('second must larger than zero')
        self.__ms = second*1000.0

    def convert_to_common_time(self):
        common_time = super(CivilTime, self).convert_to_common_time()
        y = self.__year
        m = self.__month
        if self.__month <= 2:
            y = self.__year - 1
            m = self.__month + 12
        common_time.day = int(365.25*y) + int(30.6001*(m+1)) + self.day + 1720981
        sod = 12*3600 + self.__hour*3600 + self.__minute*60 + int(self.__ms/1000.0)
        while sod > time_conf.DAY_TO_SEC:
            sod -= time_conf.DAY_TO_SEC
            common_time.day += 1
        common_time.sod = sod
        common_time.fsod = self.__ms - int(self.__ms / 1000.0) * 1000
        return common_time

    def convert_from_common_time(self, time):
        super(CivilTime, self).convert_from_common_time(time)
        a = int(time.day + time.sod * 1.0 / time_conf.DAY_TO_SEC + 0.5)
        b = a + 1537
        c = int((b-122.1)/365.25)
        d = int(365.25*c)
        e = int((b-d)/30.6001)
        self.__month = e - 1 - 12 * int(e/14.0)
        self.__year = c - 4715 - int((7+self.__month)/10.0)
        self.__day = b - d - int(30.6001*e)
        self.__hour = int(time.sod/3600.0)
        self.__minute = int((time.sod-self.__hour*3600)/60.0)
        self.__ms = 1000*(time.sod - self.hour*3600 - self.minute*60) + time.fsod
        self.__hour += 12
        while self.__hour >= 24:
            self.__hour -= 24

    def __str__(self):
        return '{:0>4d}-{:0>2d}-{:0>2d} {:0>2d}:{:0>2d}:{:.10f}{}'.format(
            self.year, self.month, self.day, self.hour, self.minute, self.second, self.time_system.sname)

    def parse(self, formatted_string):
        formatted_string = super(CivilTime, self).parse(formatted_string)
        segments = [segment for segment in re.split(' |-|:|', formatted_string) if len(segment) > 0]
        self.__year = int(segments[0])
        self.__month = int(segments[1])
        self.__day = int(segments[2])
        self.__hour = int(segments[3])
        self.__minute = int(segments[4])
        self.__ms = 1000*float(segments[5])

    def clone(self):
        new_civil_time = CivilTime(self.time_system)
        new_civil_time.__year = self.__year
        new_civil_time.__month = self.__month
        new_civil_time.__day = self.__day
        new_civil_time.__hour = self.__hour
        new_civil_time.__minute = self.__minute
        new_civil_time.__ms = self.__ms
        return new_civil_time

