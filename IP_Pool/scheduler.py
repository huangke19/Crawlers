# !/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import time
from multiprocessing import Process

from api import app
from checker import run_checker
from config import CHECK_CYCLE, CRAWL_CYCLE
from redis_getter import run_scheduler, redis


def check():
    while True:
        print('测试器开始运行')
        run_checker()
        time.sleep(CHECK_CYCLE)


def crawl():
    while True:
        if redis.good_ip_num() < 100:
            print('开始抓取代理')
            run_scheduler()
        time.sleep(CRAWL_CYCLE)


def run_api():
    app.run()


def main():
    check_process = Process(target=check)
    check_process.start()

    crawl_process = Process(target=crawl)
    crawl_process.start()

    api_process = Process(target=run_api)
    api_process.start()


if __name__ == '__main__':
    main()
