#!/usr/bin/python
# -*- coding: utf-8 -*-

class DataStorer(object):

    def __init__(self):
        pass

    def store_data(self, data):
        try:
            res = 'store data %s' % data
            return res
        except Exception as e:
            print(e)
