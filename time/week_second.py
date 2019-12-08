#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# @author kangao
# @since 2019/11/21

from time_base import TimeBase
import time_system
import time_conf
import re


class WeekSecond(TimeBase):

    def __init__(self, ts=time_system.UNKNOWN, formatted_string=None):
        self.__week = 0
        self.__sow = 0
        self.__fsow = 0.0
        super(WeekSecond, self).__init__(ts, formatted_string)

    @property
    def week(self):
        return self.__week

    @week.setter
    def week(self, week):
        if not isinstance(week, int) or week <= 0:
            raise Exception('week must be positive integer')
        self.__week = week

    @property
    def sow(self):
        return self.__sow

    @sow.setter
    def sow(self, sow):
        if not isinstance(sow, int) or sow < 0:
            raise Exception('second of week must be none negative integer')
        self.__sow = sow

    @property
    def fsow(self):
        return self.__fsow

    @fsow.setter
    def fsow(self, fsow):
        if not isinstance(fsow, float) or fsow < 0 or fsow > 1000:
            raise Exception('fraction second of week must be none negative float')
        self.__fsow = fsow

    def convert_from_common_time(self, time):
        super(WeekSecond, self).convert_from_common_time(time)
        self.__week = int(time.day)/7
        self.__sow = (int(time.day)-self.__week*7) * time_conf.DAY_TO_SEC + time.sod
        self.__fsow = time.__fsod

    def convert_to_common_time(self):
        common_time = super(WeekSecond, self).convert_to_common_time()
        common_time.day = self.__week * 7 + int(self.__sow) / time_conf.DAY_TO_SEC
        common_time.sod = int(self.__sow) % time_conf.DAY_TO_SEC
        common_time.fsod = self.__fsow
        return common_time

    def clone(self):
        week_second = WeekSecond(self.time_system)
        week_second.__week = self.__week
        week_second.__sow = self.__sow
        week_second.__fsow = self.__fsow
        return week_second

    def __str__(self):
        return '{} {}:{:.10f}{}'.format(self.__week, self.__sow, self.__fsow, self.time_system.sname)

    def parse(self, formatted_string):
        formatted_string = super(WeekSecond, self).parse(formatted_string)
        segments = [segment for segment in re.split(' |:|', formatted_string) if len(segment) > 0]
        self.__week = int(segments[0])
        self.__sow = int(segments[1])
        self.__fsow = float(segments[2])
