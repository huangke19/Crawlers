#!/usr/bin/python
# -*- coding: utf-8 -*-
from multiprocessing.managers import BaseManager

# 创建类似的QueueManager:
from DataStorer import DataStorer
from Downloader import Downloader
from Parser import Parser
from UrlManager import UrlManager

class QueueManager(BaseManager):
    pass

# 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

# 连接到服务器，也就是运行task_master.py的机器:
server_addr = '127.0.0.1'
print('Connect to server %s...' % server_addr)

# 端口和验证码注意保持与task_master.py设置的完全一致:
m = QueueManager(address=(server_addr, 8001), authkey=b'abc')
m.connect()

# 获取Queue的对象:
task = m.get_task_queue()

class SpiderMan(object):

    def __init__(self):
        self.manager = UrlManager()
        self.downloader = Downloader()
        self.parser = Parser()
        self.output = DataStorer()

    def crawl(self, start_url):
        self.manager.add_new_url(start_url)

        while (self.manager.has_new_url() and self.manager.old_urls_size() < 100):
            try:
                new_url = self.manager.get_new_url()
                html = self.downloader.download(new_url)
                new_urls, data = self.parser.parser(new_url, html)
                for url in new_urls:
                    task.put(url)
                self.output.store_data(data)
                print("已经抓取%s个链接" % self.manager.old_urls_size())
            except Exception:
                print("crawl failed")

if __name__ == '__main__':
    spider = SpiderMan()
    while not task.empty():
        url = task.get()
        spider.crawl(url)
