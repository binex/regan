#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# @author kangao
# @since 2019/11/23

from triple import Triple


class Cartesian(Triple):

    def __init__(self, elements=None):
        super(Cartesian, self).__init__(elements)

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, x):
        self[0] = x

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, y):
        self[1] = y

    @property
    def z(self):
        return self[2]

    @z.setter
    def z(self, z):
        self[2] = z


class Geodetic(Triple):

    def __init__(self, elements=None):
        super(Geodetic, self).__init__(elements)

    @property
    def b(self):
        return self[0]

    @b.setter
    def b(self, b):
        self[0] = b

    @property
    def l(self):
        return self[1]

    @l.setter
    def l(self, l):
        self[1] = l

    @property
    def h(self):
        return self[2]

    @h.setter
    def h(self, h):
        self[2] = h
