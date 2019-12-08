#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# @author kangao
# @since 2019/11/23

from coder.rinex.rnx_coder import RNXCoder


class RNXSP3Coder(RNXCoder):

    def __init__(self, ds):
        super(RNXSP3Coder, self).__init__(ds)

    def read_header(self):
        pass

    def read_epoch(self):
        pass

    def write_header(self, header):
        pass

    def write_epoch(self, epoch):
        pass
