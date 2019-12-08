#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# @author kangao
# @since 2019/11/23

import math

ELLIPSOIDS = []


class Ellipsoid(object):

    def __init__(self, name, major_axis, flattening_inverse, gm, omega):
        self.__name = name
        self.__major_axis = major_axis
        self.__flattening_inverse = flattening_inverse
        self.__gm = gm
        self.__omega = omega
        ELLIPSOIDS.append(self)

    @property
    def name(self):
        return self.__name

    @property
    def major_axis(self):
        return self.__major_axis

    @property
    def minor_axis(self):
        return self.__major_axis*(self.__flattening_inverse-1)/self.__flattening_inverse

    @property
    def flattening(self):
        return 1.0/self.__flattening_inverse

    @property
    def flattening_inverse(self):
        return self.__flattening_inverse

    @property
    def eccentricity_in_square(self):
        return (2*self.__flattening_inverse-1)/pow(self.__flattening_inverse, 2)

    @property
    def eccentricity(self):
        return math.sqrt(self.eccentricity_in_square)

    @property
    def gm(self):
        return self.__gm

    @property
    def omega(self):
        return self.__omega

    def __str__(self):
        return '{} {} {} {} {}'.format(self.__name, self.__major_axis, self.flattening_inverse, self.__gm, self.__omega)


WGS84 = Ellipsoid('WGS84', 6378137.0, 298.257223563, 3.986005e14, 7.292115e-5)
CGCS2000 = Ellipsoid('CGCS2000', 6378137.0, 298.257222101, 3.986004418e14, 7.292115e-5)

