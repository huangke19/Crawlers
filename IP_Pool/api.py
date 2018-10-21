# !/usr/bin/python
# -*- coding: utf-8 -*-

''' 通过Flask提供接口 '''

from flask import Flask

from db import Redis_KEY
from redis_getter import redis

__all__ = ['app']
app = Flask(__name__)


@app.route("/")
def welcome():
    return "This is my IP Proxy Pool"


@app.route('/get')
def get_ip():
    ip = get_new_ip()
    if ip:
        return ip
    return 'no more proxy ip'


@app.route('/count')
def count_ip():
    if redis.good_ip_num():
        return '当前可用IP数:  %s' % redis.good_ip_num()
    else:
        return '当前没有可用IP'


def get_new_ip():
    raw_ip = redis._random()
    if raw_ip:
        ip = str(raw_ip, encoding='utf-8')
        return ip
    return None


if __name__ == '__main__':
    app.run()
