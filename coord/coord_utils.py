#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# @author kangao
# @since 2019/11/23
from position import Cartesian
from position import Geodetic
from ellipsoid import Ellipsoid
import math


def geodetic_to_cartesian(geodetic, ellipsoid):
    if not isinstance(geodetic, Geodetic) or not isinstance(ellipsoid, Ellipsoid):
        raise Exception('Geodetic position type and ellipsoid is expected.')
    n = calc_prime_vertical(geodetic.b, ellipsoid)
    cos_phi = math.cos(geodetic.b)
    sin_phi = math.sin(geodetic.b)
    cos_lambda = math.cos(geodetic.l)
    sin_lambda = math.sin(geodetic.l)
    cartesian = Cartesian()
    cartesian.x = (n + geodetic.h) * cos_phi * cos_lambda
    cartesian.y = (n + geodetic.h) * cos_phi * sin_lambda
    cartesian.z = ((1-ellipsoid.eccentricity_in_square)*n + geodetic.h) * sin_phi
    return cartesian


def cartesian_to_geodetic(cartesian, ellipsoid):
    if not isinstance(cartesian, Cartesian) or not isinstance(ellipsoid, Ellipsoid):
        raise Exception('Cartesian position type and ellipsoid is expected.')
    geodetic = Geodetic()
    geodetic.l = math.atan2(cartesian.y, cartesian.x)
    p = math.sqrt(pow(cartesian.x, 2) + pow(cartesian.y, 2))
    z_p = cartesian.z / p
    phi_0 = math.atan2(z_p, 1-ellipsoid.eccentricity_in_square)
    while True:
        n_i = calc_prime_vertical(phi_0, ellipsoid)
        h_i = p/math.cos(phi_0) - n_i
        phi_i = math.atan2(z_p, 1-ellipsoid.eccentricity_in_square*n_i/(n_i+h_i))
        if abs(phi_i - phi_0) < 1e-15:
            break
        else:
            phi_0 = phi_i
    geodetic.b = phi_0
    geodetic.h = h_i
    return geodetic


def calc_prime_vertical(phi, ellipsoid):
    e_sin_phi_in_square = ellipsoid.eccentricity_in_square * pow(math.sin(phi), 2)
    return ellipsoid.major_axis/math.sqrt(1-e_sin_phi_in_square)


def deg_to_rad(deg):
    return deg*math.pi/180.0


def rad_to_deg(rad):
    return rad*180/math.pi

