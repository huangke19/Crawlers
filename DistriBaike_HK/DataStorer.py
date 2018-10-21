#!/usr/bin/python
# -*- coding: utf-8 -*-

class DataStorer(object):

    def __init__(self):
        pass

    def store_data(self, data):
        try:
            data = data.get('url')
            with open('hello.txt', 'a') as  f:
                f.write(data + '\n')
                f.close()
        except Exception as e:
            print(e)
