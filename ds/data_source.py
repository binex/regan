#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# @author kangao
# @since 2019/11/23


class DataSource(object):

    def __init__(self, parameters):
        self.__parameters = parameters

    @property
    def parameters(self):
        return self.__parameters

    @parameters.setter
    def parameters(self, parameters):
        if not isinstance(parameters, dict):
            raise Exception('DataSource parameters must be dict type')
        self.__parameters = parameters

    def get_or_default(self, key, default):
        if self.__parameters and key in self.parameters:
            return self.__parameters[key]
        else:
            return default

    def open(self):
        raise NotImplementedError('DataSource is not implemented open operation.')

    def close(self):
        raise NotImplementedError('DataSource is not implemented close operation.')


class InputDataSource(DataSource):

    def __init__(self, parameters):
        super(InputDataSource, self).__init__(parameters)

    def read_line(self):
        raise NotImplementedError('InputDataSource is not implemented read_line operation.')

    def can_read(self):
        raise NotImplementedError('InputDataSource is not implemented can_read operation.')


class OutputDataSource(DataSource):

    def __init__(self, parameters):
        super(OutputDataSource, self).__init__(parameters)

    def write_line(self, line):
        raise NotImplementedError('OutputDataSource is not implemented write_line operation.')

    def can_write(self):
        raise NotImplementedError('OutputDataSource is not implemented can_write operation.')
