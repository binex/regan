#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# @author kangao
# @since 2019/11/24


class ObsType(object):

    def __init__(self, tna):
        self.__obs_type = tna[0]
        self.__band_or_freq = int(tna[1])
        self.__attribute = tna[2]

    @property
    def obs_type(self):
        return self.__obs_type

    @property
    def band_or_freq(self):
        return self.__band_or_freq

    @property
    def attribute(self):
        return self.__attribute

    def __eq__(self, obs_type):
        if not isinstance(obs_type, ObsType):
            return False
        return self.obs_type == obs_type.obs_type and self.band_or_freq == obs_type.band_or_freq \
               and self.attribute == obs_type.attribute

    def __str__(self):
        return '{}{}{}'.format(self.__obs_type, self.__band_or_freq, self.__attribute)

    def __repr__(self):
        return self.__str__()

