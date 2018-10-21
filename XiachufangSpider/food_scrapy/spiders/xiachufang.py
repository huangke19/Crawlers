#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join

from food_scrapy.items import RecipeItem

class XiachufangSpider(scrapy.Spider):
    name = 'xiachufang'
    handle_httpstatus_list = [404, 429, 502]
    allowed_domains = ['xiachufang.com']

    def start_requests(self):
        meta = {'dont_redirect': True, "handle_httpstatus_list": [302, 301]}
        urls = ['https://www.xiachufang.com/recipe/%s/' % i for i in range(100002567, 101790129)]
        for url in urls:
            yield Request(url=url, meta=meta, callback=self.parse)

    def parse(self, response):
        ''' 解析函数，加上字段检测
        @url https://www.xiachufang.com/recipe/103299381/
        @returns items 1
        @scrapes rid name cate cooked cook cover brief steps tips
        '''
        l = ItemLoader(item=RecipeItem(), response=response)

        l.add_value('rid', response.url.split('/')[-2])
        l.add_xpath('name', '//h1[1]/text()', Join(), MapCompose(str.strip))
        l.add_xpath('cate', '//div[@class="recipe-cats"]/a/text()')
        l.add_xpath('score', '//span[@itemprop="ratingValue"]/text()')
        l.add_xpath('cooked', '//div[contains(@class,"cooked")]/span[1]/text()')
        l.add_xpath('cook', '//span[@itemprop="name"]/text()')
        l.add_xpath('cover', '//div/div/img/@src')
        l.add_xpath('brief', '//div[@itemprop="description"]/text()', Join(), MapCompose(str.strip))
        steps = [[s.xpath('p/text()').extract(), s.xpath('img/@src').extract()] for s in
                 response.xpath('//div[@class="steps"]//li')]
        l.add_value('steps', steps)
        l.add_xpath('tips', '//div[@class="tip"]/text()', Join(), MapCompose(str.strip))

        return l.load_item()
