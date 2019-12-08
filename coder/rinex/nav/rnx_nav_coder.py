#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# @author kangao
# @since 2019/11/23

from coder.rinex.rnx_coder import RNXCoder
from coder.rinex.rnx_coder import RNXHeader
import coder.rinex.rnx_const as rnx_const


class RNXNavCoder(RNXCoder):

    def __init__(self, ds):
        super(RNXNavCoder, self).__init__(ds)
        self.__rnx_nav_header = None

    def read_header(self):
        if self.__rnx_nav_header:
            return self.__rnx_nav_header
        self.__rnx_nav_header = RNXNavHeader()
        self.__rnx_nav_header.read(self.data_source)
        return self.__rnx_nav_header

    def read_epoch(self):
        pass

    def write_header(self, header):
        pass

    def write_epoch(self, epoch):
        pass


class RNXNavHeader(RNXHeader):

    def __init__(self):
        super(RNXNavHeader, self).__init__()
        self.ionospheric_corr = None
        self.time_sys_corr = None

    def _init_handler_map(self):
        self._read_handler_map[rnx_const.__IONOSPHERIC_CORR__] = self.__read_ionospheric_corr
        self._read_handler_map[rnx_const.__TIME_SYSTEM_CORR__] = self.__read_time_sys_corr
        self._write_handler_list.append(self.__write_ionospheric_corr)
        self._write_handler_list.append(self.__write_time_sys_corr)
        super(RNXNavHeader, self)._init_handler_map()

    def __read_ionospheric_corr(self, ds, line):
        if not self.ionospheric_corr:
            self.ionospheric_corr = {}
        params = []
        key = line[0:4]
        params.append(float(line[5:17]))
        params.append(float(line[17:29]))
        params.append(float(line[29:41]))
        params.append(float(line[41:53]))
        self.ionospheric_corr[key] = params
        return True

    def __write_ionospheric_corr(self, ds):
        pass

    def __read_time_sys_corr(self, ds, line):
        if not self.time_sys_corr:
            self.time_sys_corr = {}
        params = []
        key = line[0:4]
        params.append(float(line[5:22]))
        params.append(float(line[22:38]))
        params.append(float(line[38:45]))
        params.append(float(line[45:50]))
        self.time_sys_corr[key] = params
        return True

    def __write_time_sys_corr(self, ds):
        pass
