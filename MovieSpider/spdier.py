#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
异步爬虫爬取电影天堂磁力链接
___ huang ke ___
___ 2018/09/13 ___
'''
import copy
import re
import sys
import time
import asyncio
import aiohttp
import redis
import requests
from pymongo import MongoClient

HOST = '127.0.0.1'
REDIS_PORT = 6379
MONGO_PORT = 27017
DELAY_TIME = 1

redis_pool = redis.ConnectionPool(host=HOST, port=REDIS_PORT, max_connections=1024, )
redis_conn = redis.Redis(connection_pool=redis_pool)

mongo_conn = MongoClient(HOST, MONGO_PORT)
mongo_db = mongo_conn.movie

NEWEST_FILM_URL = 'http://www.btbtdy.net/btfl/dy1.html'

headers = {
    'proxy-connection': "keep-alive",
    'cache-control': "no-cache",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate",
    'accept-language': "zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6",
}


async def get_page(id):
    '''
    :param id: film id
    :return:   网页源码
    '''
    mag_url = 'http://www.btbtdy.net/vidlist/%s.html'
    # conn = aiohttp.TCPConnector(verify_ssl=False)
    # async with aiohttp.ClientSession(connector=conn) as session:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(mag_url % id, headers=headers, timeout=30) as resp:
                await asyncio.sleep(DELAY_TIME)
                if resp.status == 200:
                    ids.remove(id)
                    return await resp.text()
                else:
                    ids.add(id)
                    sys.stdout.write('status code:', resp.status)
        except Exception as e:
            print(e)
            ids.add(id)


def parse_page(html, id):
    '''
    :param html: 获取到的网页源码
    :return:     电影名称和磁力链接
    '''
    if html:
        title_pattern = re.compile('title="(.*?)"')
        mag_pattern = re.compile('href="(magnet.*?)">磁力')
        titles = re.findall(title_pattern, html)
        mags = re.findall(mag_pattern, html)
        if titles and mags and len(titles) == len(mags):
            yield (titles, mags)
        else:
            redis_conn.sadd('bad_movie_ids', id)
            sys.stdout.write('id %s不可用\n' % id)
    else:
        redis_conn.sadd('bad_movie_ids', id)
        sys.stdout.write('id %s不可用\n' % id)


async def save_to_redis(gen, id):
    '''
    :param gen: data generator
    :return:    None
    '''
    if gen:
        for title, mag in gen:
            for t, m in zip(title, mag):
                redis_conn.hset('btmovie', t, m)
                redis_conn.sadd('crawled_movie_ids', id)
                sys.stdout.write('save %s %s to reids\n' % (t, m))
        mongo_conn.close()
    else:
        sys.stdout.write('save failed\n')


async def save_to_mongo(gen):
    '''
    :param gen: data generator
    :return:    None
    '''
    if gen:
        for title, mag in gen:
            for t, m in zip(title, mag):
                data = {'title': t, 'magnet': m}
                mongo_db['btbtby'].insert(data)
                sys.stdout.write('save %s to mongo' % data)
        mongo_conn.close()
    else:
        sys.stdout.write('save failed')


async def crawl(_id, sem):
    '''
    :param _id: 电影id
    :param sem: 信号数
    :return:    None
    '''
    async with sem:
        sys.stdout.write('正在爬取 %s 页\n' % _id)
        html = await  get_page(_id)
        data = parse_page(html, _id)
        await save_to_redis(data, _id)
        # await save_to_mongo(data)            # redis 和 mongo 二选一


def get_newest_id(url):
    ''' 获取最新电影编号 '''
    response = requests.get(url)
    re_pt = re.compile('<a class="pic_link" href="/btdy/dy(\d+?).html"', re.S)
    id = re.findall(re_pt, response.text)[0]
    return int(id)


def main():
    # 获取最新电影的id
    global ids
    sys.stdout.write('正在获取最新电影id\n')
    max_id = get_newest_id(NEWEST_FILM_URL)
    start = time.time()
    ids = set(range(1, max_id))

    # 对id进行去重
    sys.stdout.write('正在对id进行去重\n')
    uncrawled_ids = []
    [uncrawled_ids.append(i) for i in ids if not
    (redis_conn.sismember('crawled_movie_ids', i) or redis_conn.sismember('bad_movie_ids', i))]

    # 对新增的电影进行抓取
    if uncrawled_ids:
        sys.stdout.write('开始进行抓取\n')
    try:
        loop = asyncio.get_event_loop()
        sem = asyncio.Semaphore(100)  # 维持指定数量的信号量
        tasks = [asyncio.ensure_future(crawl(i, sem)) for i in uncrawled_ids]
        loop.run_until_complete(asyncio.wait(tasks))
        end = time.time()
        sys.stdout.write('本次下载共用时 %s 秒' % (end - start))
    except ValueError:
        sys.stdout.write("没有更新电影，下载结束")


if __name__ == '__main__':
    main()
