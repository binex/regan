#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# @author kangao
# @since 2019/11/23

import ds.data_source as data_source
import os


class FileInputDataSource(data_source.InputDataSource):

    def __init__(self, parameters):
        super(FileInputDataSource, self).__init__(parameters)
        self.__opened = False
        self.__file = None

    def open(self):
        if self.__opened:
            return
        file_path = self.get_or_default('path', None)
        if not file_path or not os.path.exists(file_path):
            raise Exception('path is not exist or invalid, path = %s, ' % file_path)
        self.__file = open(file_path, 'r')
        self.__opened = True

    def can_read(self):
        return self.__opened and self.__file and not self.__file.closed

    def close(self):
        if self.can_read():
            self.__file.close()
            self.__file = None
            self.__opened = False

    def read_line(self):
        if self.can_read():
            return self.__file.readline()


class FileOutputDataSource(data_source.OutputDataSource):

    def __init__(self, parameters):
        super(FileOutputDataSource, self).__init__(parameters)
        self.__opened = False
        self.__file = None

    def open(self):
        if self.__opened:
            return
        file_path = self.get_or_default('path', None)
        if not file_path:
            raise Exception('path is invalid, path = %s' % file_path)
        self.__file = open(file_path, 'w')
        self.__opened = True

    def close(self):
        if self.can_write():
            self.__file.close()
            self.__file = None
            self.__opened = False

    def write_line(self, line):
        if self.can_write():
            self.__file.writelines(line)

    def can_write(self):
        return self.__opened and self.__file and not self.__file.closed
