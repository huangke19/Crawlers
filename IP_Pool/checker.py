# !/usr/bin/python
# -*- coding: utf-8 -*-

''' aiohttp 检测器'''

import asyncio
import sys
from asyncio import TimeoutError

from aiohttp import ClientConnectionError, ClientError
from aiohttp import ClientSession

from config import HEADERS, TEST_URL
from redis_getter import redis

ips = redis._all()


async def check_ip(ip):
    if isinstance(ip, bytes):
        ip = ip.decode('utf-8')
    proxy = 'http://%s' % ip
    print('正在测试: %s' % proxy)

    # conn = aiohttp.TCPConnector(verify_ssl=False)
    # async with ClientSession(connector=conn) as session:
    async with ClientSession() as session:
        try:
            async  with session.get(TEST_URL, headers=HEADERS, proxy=proxy,
                                    timeout=10, allow_redirects=False) as response:
                if response.status == 200:
                    redis._set_max(ip)
                    print('ip %s可用' % proxy)
                else:
                    redis._decrease(ip)
                    print('响应码不是200 %s减一分' % ip)
        except (ClientError, ClientConnectionError, TimeoutError) as e:
            redis.delete(ip)
            print('请求失败: %s %s' % (ip, e))


def run_checker():
    loop = asyncio.get_event_loop()
    try:
        for i in range(0, len(ips), 500):
            test_ips = ips[i:i + 500]
            tasks = [check_ip(ip) for ip in test_ips]
            loop.run_until_complete(asyncio.wait(tasks))
            # time.sleep(1)
    except Exception:
        print('测试器发生错误')
