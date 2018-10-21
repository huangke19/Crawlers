# !/usr/bin/python
# -*- coding: utf-8 -*-

''' 知道创宇面试题 '''
import copy
import re
import sys
from time import sleep

import requests
import logging.config
from argparse import ArgumentParser
from pymongo import MongoClient

HOST = '127.0.0.1'
PORT = 27017
DELAY = 1

logging.basicConfig(filename='robot.log', filemode='a',
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

LOG_LEVEL = {
    1: logger.debug,
    2: logger.info,
    3: logger.warning,
    4: logger.error,
    5: logger.critical
}

start_url = 'https://www.sina.com.cn/'
uncrawled_url = set()

class Spider(object):

    def __init__(self, log, args):
        self.log = log
        self.args = args

    def get_content(self, url):
        '''
        :param url: 地址
        :return:    页面数据
        '''
        try:
            r = requests.get(url, timeout=5)
            r.encoding = 'utf-8'
            print(r.status_code)
            return r.text
        except Exception as e:
            self.log(e)
            uncrawled_url.add(url)
            return None

    def get_new_urls(self, html):
        '''
        :param html: 页面获取的数据
        :return:     解析的二级地址url
        '''
        # todo
        if html:
            pattern = re.compile('href="(https?://.*sina.*?.html)')
            urls = re.findall(pattern, html)
            print(urls[:4])
            if urls:
                return urls
            else:
                return []
        else:
            return None

    def crawl_one_page(self, url, key=None):
        ''' 主运行函数 '''
        html = self.get_content(url)
        urls = self.get_new_urls(html)
        if key:
            if re.search(key, html):
                print('find the key')
                return urls, html
            else:
                print('not find the key')
                return [], []
        else:
            return urls, html

    def crawl_all_pages(self):
        pass

class DataBase(object):

    def __init__(self, HOST, PORT, dbname, colname, log):
        self.host = HOST
        self.port = PORT
        self.conn = MongoClient(HOST, PORT)
        self.db = self.conn[dbname]
        self.collection = self.db[colname]
        self.log = log

    def save_to_mongo(self, url, html):
        data_dict = {'url': url, 'html': html}
        try:
            self.collection.insert(data_dict)
        except Exception as e:
            self.log(e)
            return

class MyParser(ArgumentParser):

    def __init__(self):
        super().__init__()
        self.description = '请输入爬虫参数'

    def get_parser(self):
        self.add_argument('-u', dest='url', type=str, help='url地址')
        self.add_argument('-d', dest='depth', type=int, default=2, help='爬取深度')
        self.add_argument('-thread', dest='thread', default=10, help='线程池大小')
        self.add_argument('-dbfile', dest='dbname', help='数据库名')
        self.add_argument('-f', dest='logfile', help='日志文件')
        self.add_argument('-k', dest='key', help='页面内的关键词')
        self.add_argument('-l', dest='loglevel', type=int, default=3, help='日志等级')
        self.add_argument('--testself', dest='test', help='程序自测 ')
        return self.parse_args()

class Timer():

    def __init__(self):
        self.sleep = sleep(10)

    def mysleep(self):
        return self.sleep

def main():
    parser = MyParser()
    args = parser.get_parser()
    depth = args.depth
    url = args.url if args.url else start_url
    key = args.key
    # key = '抖音'
    dbname = args.dbname if args.dbname else 'sina'
    colname = 'sina'
    # timer = Timer()

    log = LOG_LEVEL[args.loglevel]
    spider = Spider(log, args)
    mongo = DataBase(HOST, PORT, dbname, colname, log)

    flag = 0
    tc_list = [url]  # 待爬队列
    for i in range(0, depth):
        urls = copy.deepcopy(tc_list)  # 将待爬urls放入urls
        tc_list = []  # 清空待爬队列
        for url in urls:
            flag += 1
            # timer.sleep()
            sleep(4)
            sys.stdout.write('正在爬第个 %s 网页 \n' % flag)
            new_url, data = spider.crawl_one_page(url, key)

            if new_url and data:
                [tc_list.append(url) for url in new_url]
                mongo.save_to_mongo(url, data)
            elif (not new_url) and data:
                mongo.save_to_mongo(url, data)
            else:
                continue

if __name__ == '__main__':
    main()
