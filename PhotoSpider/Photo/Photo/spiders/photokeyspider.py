# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request

from Photo import settings
from Photo.items import PhotoItem


class PhotospiderSpider(scrapy.Spider):
    name = 'keyimages'
    allowed_domains = ['images.so.com']
    start_urls = ['http://images.so.com/']

    def start_requests(self):
        search_key = input('输入要搜索的关键词: ')
        base_url = 'http://images.so.com/j?q=' + search_key + '&src=srp&correct=menghia&pn=60&ch=&sn={}'
        for i in range(1, settings.MAX_PAGE + 1):
            url = base_url.format(i * 60)
            self.log(url)
            yield Request(url)

    def parse(self, response):
        self.log(response.status)
        res = json.loads(response.text)
        for image in res.get('list'):
            item = PhotoItem()
            item['id'] = image.get('imagekey', 'common')
            item['url'] = image.get('img')
            item['title'] = image.get('title')
            item['thumb'] = image.get('thumb')
            yield item
