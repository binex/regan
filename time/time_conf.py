#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# @author kangao
# @since 2019/11/19

import yaml
import os

# difference between julian day and modify julian day
JD_TO_MJD = 2400000.5

# convert day to second
DAY_TO_SEC = 24 * 3600

EPSON = 1e-12

# load time reference frame configuration
TIME_REFER_FRAME_CONF = {}
CONF_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'conf')
TIME_REFER_FRAME_YAML_FILE = os.path.join(os.path.abspath(CONF_DIR), 'time_refer_frame.yaml')
if os.path.exists(TIME_REFER_FRAME_YAML_FILE):
    with open(TIME_REFER_FRAME_YAML_FILE, 'r') as reader:
        TIME_REFER_FRAME_CONF = yaml.load(reader, Loader=yaml.FullLoader)
else:
    raise Exception('time refer frame configuration cannot be loaded, path=%s' % TIME_REFER_FRAME_YAML_FILE)


def get_init_leap_sec():
    return TIME_REFER_FRAME_CONF.get('init_leap_sec')


def get_leap_sec_list():
    return TIME_REFER_FRAME_CONF.get('leap_sec_list')


def set_leap_sec_list(leap_sec_list):
    TIME_REFER_FRAME_CONF['leap_sec_list'] = leap_sec_list


