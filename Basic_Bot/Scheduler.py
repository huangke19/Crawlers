#!/usr/bin/python
# -*- coding: utf-8 -*-
from Basic_Bot.DataStorer import DataStorer
from Basic_Bot.Downloader import Downloader
from Basic_Bot.Parser import Parser
from Basic_Bot.UrlManager import UrlManager

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

