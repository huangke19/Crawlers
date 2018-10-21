# !/usr/bin/python
# -*- coding: utf-8 -*-

''' 调用爬取 '''
import sys
import time

from config import PROXY_SITES
from db import RedisClient
from spider import crawl_ip

redis = RedisClient()


def over_limit():
    if redis._count() > 10000:
        return True
    else:
        return False


def run_scheduler():
    page = 1
    while not over_limit() and page < 50 \
            and redis.good_ip_num() < 100:
        for name in PROXY_SITES:
            ips = crawl_ip(name, page)
            for ip in ips:
                redis._add(ip)
        time.sleep(5)
        page += 1
        print('page:', page)
