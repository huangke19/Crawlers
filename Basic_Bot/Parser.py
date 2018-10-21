#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib.parse

class Parser(object):

    def parser(self, url, html_text):
        '''
        用于解析网页内容抽取URL和数据
        :return:返回URL和数据
        '''
        if url is None or html_text is None:
            return

        text = 'to be parsed %s' % html_text
        new_urls = self.parse_new_urls(url, text)
        new_data = self.parse_data(url, text)

        return new_urls, new_data

    def parse_new_urls(self, url, text):
        '''
        抽取新的URL集合
        :param url: 下载页面的URL
        :return: 返回新的URL集合
        '''
        new_urls = set()
        links = ['to be parse %s' % text]
        for link in links:
            new_url = 'to be done %s' % link
            new_full_url = urllib.parse.urljoin(url, new_url)
            new_urls.add(new_full_url)

        if len(new_urls) == 0:
            print('警告: 未解析到任何url')
        return new_urls

    def parse_data(self, url, text):
        '''
        抽取有效数据
        :param url:下载页面的URL
        :param text:
        :return:返回有效数据
        '''
        data = {}
        data['url'] = url
        data['items'] = 'to be parse %s' % text

        if len(data) == 0:
            print('警告: 未解析到任何url')
        return data
