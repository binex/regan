#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# @author kangao
# @since 2019/11/17

import time_conf
import time_system
from time_system import TimeSystem
import re


class TimeBase(object):

    def __init__(self, ts=time_system.UNKNOWN, formatted_string=None):
        self.__time_system = ts
        if formatted_string and len(formatted_string) > 0:
            self.parse(formatted_string)

    @property
    def time_system(self):
        return self.__time_system

    @time_system.setter
    def time_system(self, ts):
        if not isinstance(ts, TimeSystem):
            raise Exception('time system is invalid.')
        self.__time_system = ts

    def parse(self, formatted_string):
        if not formatted_string or len(formatted_string) <= 1:
            raise Exception('time string is invalid, str=%s' % formatted_string)
        self.__time_system = time_system.find_time_system(formatted_string[-1])
        return formatted_string[:-1]

    def clone(self):
        raise Exception('TimeBase is not implemented clone operation.')

    def convert_from_common_time(self, time):
        if type(time) != CommonTime:
            raise Exception('time is not type of CommonTime, type = %s' % type(time))
        self.__time_system = time.time_system

    def convert_to_common_time(self):
        return CommonTime(self.time_system)

    def __sub__(self, time):
        if isinstance(time, TimeBase):
            left_common_time = self.convert_to_common_time()
            right_common_time = time.convert_to_common_time()
            return left_common_time - right_common_time
        elif isinstance(time, int) or isinstance(time, float):
            left_common_time = self.convert_to_common_time()
            if time < 0:
                left_common_time = left_common_time + abs(time)
            else:
                left_common_time = left_common_time - abs(time)
            new_time_base = self.clone()
            new_time_base.convert_from_common_time(left_common_time)
            return new_time_base
        else:
            raise Exception('the type of time is invalid, type = %s' % type(time))

    def __add__(self, sec):
        if not isinstance(sec, float) and not isinstance(sec, int):
            raise Exception('second must be integer or float')
        common_time = self.convert_to_common_time()
        if sec < 0:
            common_time = common_time - sec
        else:
            common_time = common_time + sec
        new_time_base = self.clone()
        new_time_base.convert_from_common_time(common_time)
        return new_time_base

    def __lt__(self, time):
        if isinstance(time, TimeBase):
            left_common_time = self.convert_to_common_time()
            right_common_time = time.convert_to_common_time()
            return left_common_time < right_common_time
        else:
            return False

    def __eq__(self, time):
        if isinstance(time, TimeBase):
            left_common_time = self.convert_to_common_time()
            right_common_time = time.convert_to_common_time()
            return left_common_time == right_common_time
        else:
            return False

    def __ne__(self, time):
        return not (self == time)

    def __le__(self, time):
        return not (self > time)

    def __gt__(self, time):
        return (not (self < time)) and (self != time)

    def __ge__(self, time):
        return not (self < time)


class CommonTime(TimeBase):

    def __init__(self, ts=time_system.UNKNOWN, formatted_string=None):
        self.__day = 0
        self.__sod = 0
        self.__fsod = 0.0
        super(CommonTime, self).__init__(ts, formatted_string)

    @property
    def day(self):
        return self.__day

    @day.setter
    def day(self, day):
        if not isinstance(day, int):
            raise Exception('day must be integer')
        if day < 0:
            raise Exception('day must be larger than zero.')
        self.__day = day

    @property
    def sod(self):
        return self.__sod

    @sod.setter
    def sod(self, sod):
        if not isinstance(sod, int):
            raise Exception('second of day must be integer')
        if sod < 0 or sod >= time_conf.DAY_TO_SEC:
            raise Exception('second of day must be in [0,86400)')
        self.__sod = sod

    @property
    def fsod(self):
        return self.__fsod

    @fsod.setter
    def fsod(self, fsod):
        if not isinstance(fsod, float):
            raise Exception('fraction second of day must be float')
        if fsod < 0 or fsod >= 1000:
            raise Exception('fraction second of day must be in [0,100)')
        self.__fsod = fsod

    def __str__(self):
        return '{} {}:{:.10f}{}'.format(self.__day, self.__sod, self.__fsod, self.time_system.sname)

    def clone(self):
        new_instance = CommonTime(self.time_system)
        new_instance.__day = self.__day
        new_instance.__sod = self.__sod
        new_instance.__fsod = self.__fsod
        return new_instance

    def parse(self, formatted_string):
        formatted_string = super(CommonTime, self).parse(formatted_string)
        segments = [segment.strip() for segment in re.split(' |:|', formatted_string) if len(segment) > 0]
        self.__day = int(segments[0])
        self.__sod = int(segments[1])
        self.__fsod = float(segments[2])

    def convert_from_common_time(self, time):
        super(CommonTime, self).convert_from_common_time(time)
        self.__day = time.day
        self.__sod = time.sod
        self.__fsod = time.fsod

    def convert_to_common_time(self):
        super(CommonTime, self).convert_to_common_time()
        new_common_time = CommonTime()
        new_common_time.__day = self.day
        new_common_time.__sod = self.sod
        new_common_time.__fsod = self.fsod
        return new_common_time

    def normalize(self):
        while self.__fsod >= 1000:
            self.__fsod -= 1000
            self.__sod += 1
        while self.__fsod < 0:
            self.__fsod += 1000
            self.__sod -= 1
        while self.__sod >= time_conf.DAY_TO_SEC:
            self.__sod -= time_conf.DAY_TO_SEC
            self.__day += 1
        while self.__sod < 0:
            self.__sod += time_conf.DAY_TO_SEC
            self.__day -= 1

    def __sub__(self, time):
        if type(time) == CommonTime:
            diff_day = self.__day - time.day
            diff_sod = self.__sod - time.sod
            diff_fsod = self.__fsod - time.fsod
            return diff_day * time_conf.DAY_TO_SEC + diff_sod + diff_fsod / 1000
        elif isinstance(time, int) or isinstance(time, float):
            if time < 0:
                return self + abs(time)
            else:
                common_time = self.clone()
                diff_sod = common_time.__sod - time
                while diff_sod < 0:
                    diff_sod += time_conf.DAY_TO_SEC
                    common_time.__day -= 1
                common_time.__sod = int(diff_sod)
                common_time.__fsod += 1000*(diff_sod-int(diff_sod))
                common_time.normalize()
                return common_time
        else:
            raise Exception('time is not type of CommonTime, type = %s' % type(time))

    def __add__(self, sec):
        if not isinstance(sec, float) and not isinstance(sec, int):
            raise Exception('second must be integer or float')
        if sec < 0:
            return self - abs(sec)
        common_time = self.clone()
        common_time.__sod += int(sec)
        common_time.__fsod += 1000*(sec-int(sec))
        common_time.normalize()
        return common_time

    def __eq__(self, time):
        if type(time) == CommonTime:
            return self.__day == time.__day and self.__sod == time.__sod \
                   and abs(self.__fsod - time.__fsod) <= time_conf.EPSON and self.time_system == time.time_system
        else:
            return False

    def __lt__(self, time):
        if type(time) == CommonTime and self.time_system == time.time_system:
            if self == time:
                return False
            if self.__day < time.__day:
                return True
            elif self.__day > time.__day:
                return False
            elif self.__sod < time.__sod:
                return True
            elif self.__sod > time.__sod:
                return False
            elif self.__fsod < time.__fsod:
                return True
            else:
                return False
        else:
            raise Exception('time is not type of CommonTime, type = %s' % type(time))

