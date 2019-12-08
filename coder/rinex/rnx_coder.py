#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# @author kangao
# @since 2019/11/23
import ds.data_source as data_source
import coder.rinex.rnx_const as rnx_const


class RNXCoder(object):

    def __init__(self, ds):
        if not isinstance(ds, data_source.DataSource):
            raise Exception('ds must be instance of DataSource')
        self.__data_source = ds

    @property
    def data_source(self):
        return self.__data_source

    def read_header(self):
        raise NotImplementedError('RNXCoder is not implemented read_header operation.')

    def write_header(self, header):
        raise NotImplementedError('RNXCoder is not implemented write_header operation.')

    def read_epoch(self):
        raise NotImplementedError('RNXCoder is not implemented read_epoch operation.')

    def write_epoch(self, epoch):
        raise NotImplementedError('RNXCoder is not implemented write_epoch operation.')

    def open(self):
        if self.data_source:
            self.data_source.open()

    def close(self):
        if self.data_source:
            self.data_source.close()


class RNXHeader(object):

    def __init__(self):
        self._read_handler_map = {}
        self._write_handler_list = []
        self._init_handler_map()
        self.version = None
        self.file_type = None
        self.satellite_system = None
        self.pgm = None
        self.run_by = None
        self.date_for_create = None
        self.comments = None
        self.leap_second = None

    def _init_handler_map(self):
        self._read_handler_map[rnx_const.__RINEX_VERSION_TYPE__] = self._read_rinex_verion_type
        self._read_handler_map[rnx_const.__PGM_RUN_BY_DATE__] = self._read_pgm_run_by_date
        self._read_handler_map[rnx_const.__COMMENT__] = self._read_comment
        self._read_handler_map[rnx_const.__END_OF_HEADER__] = self._read_end_of_header
        self._read_handler_map[rnx_const.__LEAP_SECONDS__] = self._read_leap_second
        self._write_handler_list.insert(0, self._write_rinex_version_type)
        self._write_handler_list.insert(1, self._write_pgm_run_by_date)
        self._write_handler_list.append(self._write_leap_second)
        self._write_handler_list.append(self._write_comment)
        self._write_handler_list.append(self._write_end_of_header)

    def read(self, ds):
        line = ds.read_line()
        while line:
            label = line[60:].strip(' ').strip()
            read_handler = self._read_handler_map[label]
            if read_handler:
                if not read_handler(ds, line):
                    break
            line = ds.read_line()

    def write(self, ds):
        for write_handler in self._write_handler_list:
            write_handler(ds)

    def _read_rinex_verion_type(self, ds, line):
        self.version = float(line[0:9])
        self.file_type = line[20]
        self.satellite_system = line[40]
        return True

    def _write_rinex_version_type(self, ds):
        pass

    def _read_pgm_run_by_date(self, ds, line):
        self.pgm = line[0:20]
        self.run_by = line[20:40]
        self.date_for_create = line[40:60]
        return True

    def _write_pgm_run_by_date(self, ds):
        pass

    def _read_comment(self, ds, line):
        if not self.comments:
            self.comments = []
        self.comments.append(line[0:60])
        return True

    def _write_comment(self, ds):
        pass

    def _read_leap_second(self, ds, line):
        if not self.leap_second:
            self.leap_second = []
        self.leap_second.append(int(line[0:6]))
        self.leap_second.append(int(line[6:12]))
        self.leap_second.append(int(line[12:18]))
        self.leap_second.append(int(line[18:24]))
        return True

    def _write_leap_second(self, ds):
        pass

    def _read_end_of_header(self, ds, line):
            return False

    def _write_end_of_header(self, ds):
        pass