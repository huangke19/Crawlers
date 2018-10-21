#!/usr/bin/python
# -*- coding: utf-8 -*-

from DataStorer import DataStorer
from Downloader import Downloader
from Parser import Parser
from UrlManager import UrlManager

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
                self.manager.add_new_urls(new_urls)
                self.output.store_data(data)
                print("已经抓取%s个链接" % self.manager.old_urls_size())
            except Exception:
                print("crawl failed")

if __name__ == "__main__":
    spider_man = SpiderMan()
    start_url = input('请输入爬虫的起始url: ')
    spider_man.crawl(start_url)
