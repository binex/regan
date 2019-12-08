#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# @author kangao
# @since 2019/11/22

from time_base import TimeBase
from civil_time import CivilTime
import time_conf
import time_system


# convert formatted string to CivilTime
time_conf.set_leap_sec_list(
    [
        CivilTime(formatted_string=leap_sec_time) for leap_sec_time in time_conf.get_leap_sec_list()
    ]
)


def convert_to_time(time, target_time_class):
    if isinstance(time, TimeBase) and target_time_class:
        common_time = time.convert_to_common_time()
        target_time = target_time_class(time.time_system)
        target_time.convert_from_common_time(common_time)
        return target_time
    else:
        raise Exception('time is not instance of TimeBase.')


def calculate_leap_sec(time):
    if not time or not isinstance(time, TimeBase):
        raise Exception('time must be TimeBase.')
    leap_sec = time_conf.get_init_leap_sec()
    time_clone = time.clone()
    time_clone.time_system = time_system.UTC
    for leap_sec_time in time_conf.get_leap_sec_list():
        if time_clone > leap_sec_time:
            leap_sec += 1
    return leap_sec


def tai_to_utc(tai):
    pass


def utc_to_tai(utc):
    pass


