#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib.parse
import requests

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/68.0.3440.106 Safari/537.36'

class UrlManager(object):

    def __init__(self):
        self.new_urls = set()  # 未爬取URL集合
        self.old_urls = set()  # 已爬取URL集合

    def has_new_url(self):
        return self.new_urls_size() != 0

    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    def add_new_url(self, url):
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def new_urls_size(self):
        return len(self.new_urls)

    def old_urls_size(self):
        return len(self.old_urls)

class Downloader(object):

    def download(self, url):
        if url is None:
            return None

        user_agent = USER_AGENT
        headers = {'User-Agent': user_agent}
        try:
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                r.encoding = 'utf-8'
                return r.text
            return None
        except Exception as e:
            print(e)

class Parser(object):

    def parser(self, url, html_text):
        if url is None or html_text is None:
            return

        text = 'to be parsed %s' % html_text
        new_urls = self.parse_new_urls(url, text)
        new_data = self.parse_data(url, text)

        return new_urls, new_data

    def parse_new_urls(self, url, text):
        new_urls = set()
        links = ['to be parse %s' % text]
        for link in links:
            new_url = 'to be done %s' % link
            new_full_url = urllib.parse.urljoin(url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    def parse_data(self, url, text):
        data = {}
        data['url'] = url
        data['items'] = 'to be parse %s' % text
        return data

class DataStorer(object):

    def __init__(self):
        pass

    def store_data(self, data):
        pass

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
    start_url = ''
    spider_man.crawl(start_url)
