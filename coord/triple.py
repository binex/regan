#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# @author kangao
# @since 2019/11/23

import math

__LEN__ = 3


class Triple(object):

    def __init__(self, elements=None):
        if not elements:
            elements = [0.0, 0.0, 0.0]
        self.__elements = elements

    def __len__(self):
        return __LEN__

    def __getitem__(self, i):
        return self.__elements[i]

    def __setitem__(self, key, value):
        self.__elements[key] = value

    def __str__(self):
        return '({}, {}, {})'.format(self[0], self[1], self[2])

    def __repr__(self):
        return '{}({}, {}, {})'.format(type(self).__name__, self[0], self[1], self[2])

    def __add__(self, triple):
        if not isinstance(triple, Triple):
            raise Exception('triple type is invalid, type=%s' % type(triple))
        result_triple = self.clone()
        result_triple[0] += triple[0]
        result_triple[1] += triple[1]
        result_triple[2] += triple[2]
        return result_triple

    def __sub__(self, triple):
        if not isinstance(triple, Triple):
            raise Exception('triple type is invalid, type=%s' % type(triple))
        result_triple = self.clone()
        result_triple[0] -= triple[0]
        result_triple[1] -= triple[1]
        result_triple[2] -= triple[2]
        return result_triple

    def __mul__(self, element):
        if isinstance(element, Triple):
            return self.dot(element)
        result_triple = self.clone()
        result_triple[0] *= element
        result_triple[1] *= element
        result_triple[2] *= element
        return result_triple

    def __div__(self, factor):
        if (not isinstance(factor, int) and not isinstance(factor, float)) or factor == 0:
            raise Exception('factor must be number and not zero.')
        result_triple = self.clone()
        factor = factor*1.0
        result_triple[0] /= factor
        result_triple[1] /= factor
        result_triple[2] /= factor
        return result_triple

    def __eq__(self, triple):
        if type(triple) == type(self):
            return abs(triple[0]-self[0]) < 1e-15 and abs(triple[1]-self[1]) < 1e-15 and abs(triple[2]-self[2]) < 1e-15
        return False

    def clone(self):
        triple = object.__new__(self.__class__)
        triple.__init__()
        triple[0] = self[0]
        triple[1] = self[1]
        triple[2] = self[2]
        return triple

    def distance(self):
        sum = 0.0
        for element in self:
            sum += pow(element, 2)
        return math.sqrt(sum)

    def dot(self, triple):
        return self[0]*triple[0] + self[1]*triple[1] + self[2]*triple[2]

    def cross(self, triple):
        result = Triple()
        result[0] = self[1]*triple[2] - self[2]*triple[1]
        result[1] = self[2]*triple[0] - self[0]*triple[2]
        result[2] = self[0]*triple[1] - self[1]*triple[0]
        return result

    def r1(self, theta):
        triple = self.clone()
        sin_theta = math.sin(theta)
        cos_theta = math.cos(theta)
        triple[0] = self[0]
        triple[1] = self[1]*cos_theta - self[2]*sin_theta
        triple[2] = self[1]*sin_theta + self[2]*cos_theta
        return triple

    def r2(self, theta):
        triple = self.clone()
        sin_theta = math.sin(theta)
        cos_theta = math.cos(theta)
        triple[0] = self[0]*cos_theta + self[2]*sin_theta
        triple[1] = self[1]
        triple[2] = -self[0]*sin_theta + self[2]*cos_theta
        return triple

    def r3(self, theta):
        triple = self.clone()
        sin_theta = math.sin(theta)
        cos_theta = math.cos(theta)
        triple[0] = self[0]*cos_theta - self[1]*sin_theta
        triple[1] = self[0]*sin_theta + self[1]*cos_theta
        triple[2] = self[2]
        return triple

