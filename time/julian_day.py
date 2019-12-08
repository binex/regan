#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# @author kangao
# @since 2019/11/17

from time_base import TimeBase
import time_conf
import time_system


class JulianDay(TimeBase):

    def __init__(self, ts=time_system.UNKNOWN, formatted_string=None):
        self.__day = 0.0
        super(JulianDay, self).__init__(ts, formatted_string)

    @property
    def day(self):
        return self.__day

    @day.setter
    def day(self, day):
        if not isinstance(day, float):
            raise Exception('julian day must be float')
        self.__day = day

    def convert_to_common_time(self):
        common_time = super(JulianDay, self).convert_to_common_time()
        common_time.day = int(self.__day)
        sod = (self.__day - common_time.day) * time_conf.DAY_TO_SEC
        common_time.sod = int(sod)
        common_time.fsod = 1000*(sod - common_time.sod)
        return common_time

    def convert_from_common_time(self, time):
        super(JulianDay, self).convert_from_common_time(time)
        day = time.day
        day = day + time.sod * 1.0 / time_conf.DAY_TO_SEC
        day = day + time.fsod*1.0/(1000 * time_conf.DAY_TO_SEC)
        self.__day = day

    def __str__(self):
        return '{:.16f}{}'.format(self.__day, self.time_system.sname)

    def parse(self, formatted_string):
        formatted_string = super(JulianDay, self).parse(formatted_string)
        self.__day = float(formatted_string)

    def clone(self):
        new_julian_day = JulianDay(self.time_system)
        new_julian_day.__day = self.__day
        return new_julian_day


class ModifiedJulianDay(JulianDay):

    def __init__(self, ts=time_system, formatted_string=None):
        super(ModifiedJulianDay, self).__init__(ts, formatted_string)

    def convert_from_common_time(self, time):
        super(ModifiedJulianDay, self).convert_from_common_time(time)
        self.day = self.day - time_conf.JD_TO_MJD

    def convert_to_common_time(self):
        julian_day = self.clone()
        julian_day.day = self.day + time_conf.JD_TO_MJD
        return julian_day.convert_to_common_time()


