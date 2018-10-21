# !/usr/bin/python
# -*- coding: utf-8 -*-

''' 定义redis的初始化和各种操作 '''

import random

import redis

from config import HOST, PORT

Redis_KEY = 'good_ips'


class RedisClient(object):

    def __init__(self):
        self.redis_pool = redis.ConnectionPool(host=HOST, port=PORT, max_connections=20)
        self.conn = redis.StrictRedis(connection_pool=self.redis_pool)

    def _add(self, ip, score=90):
        ''' 将ip的分数加1 '''
        if not self.conn.zscore(Redis_KEY, ip):
            self.conn.zadd(Redis_KEY, score, ip)
        else:
            pass

    def _decrease(self, ip):
        ''' 将ip的分数减1 '''
        score = self.conn.zscore(Redis_KEY, ip)
        if not score:
            return
        if score > 85:
            self.conn.zincrby(Redis_KEY, ip, -1)
        else:
            self.conn.zrem(Redis_KEY, ip)

    def _random(self):
        ''' 分数从高到低的取可用ip'''
        for i in range(100, 0, -1):
            result = self.conn.zrangebyscore(Redis_KEY, i, i)
            if result:
                return random.choice(result)
            else:
                continue
        return None

    def _set_max(self, ip):
        ''' 将ip分数设到100 '''
        self.conn.zadd(Redis_KEY, 100, ip)

    def _count(self):
        ''' 获取IP数量 '''
        return self.conn.zcard(Redis_KEY)

    def _all(self):
        ''' 获取所有的IP '''
        return self.conn.zrangebyscore(Redis_KEY, 0, 100)

    def good_ip_num(self):
        ''' 获取所有的IP '''
        return len(self.conn.zrangebyscore(Redis_KEY, 100, 100))

    def delete(self, ip):
        self.conn.zrem(Redis_KEY, ip)
