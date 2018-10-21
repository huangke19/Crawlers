#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

class Parser(object):

    def parser(self, url, html_text):
        '''
        用于解析网页内容抽取URL和数据
        :return:返回URL和数据
        '''
        if url is None or html_text is None:
            return

        text = html_text
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
        pattern = re.compile('<a target=_blank href="/(item/.*?)".*?</a>', re.S)
        links = re.findall(pattern, text)
        for link in links:
            new_url = url.split('item/')[0] + link
            new_urls.add(new_url)
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
        title_pattern = re.compile('<h1 >(.*?)</h1>.*?', re.S)
        summar_pattern = re.compile('<div class="para" label-module="para">(.*?)</div>', re.S)
        title = re.findall(title_pattern, text)
        summary = re.findall(summar_pattern, text)
        data['title'] = title[0]
        data['sammary'] = summary[0]

        if len(data) == 0:
            print('警告: 未解析到任何url')

        return data
