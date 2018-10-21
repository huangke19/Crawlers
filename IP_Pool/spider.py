# !/usr/bin/python
# -*- coding: utf-8 -*-

'''  通用爬取，通过传入代理IP网站名和页数进行IP的抓取 '''

import re
import sys

import requests

from config import HEADERS, IP_SITES


def crawl_ip(site_name, page):
    '''
    :param site_name: 要爬取的网站名
    :param page: 要爬取的页数
    '''
    pattern = IP_SITES[site_name]['pattern']
    url = IP_SITES[site_name]['url'] % page
    print('正在爬取{}代理第{}页'.format(site_name, page))

    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            pattern = re.compile(pattern, re.S)
            items = re.findall(pattern, res.text)
            if not items:
                print('未解析到真实内容，可能需要调整解析方式')
                return None
            for i, port in items:
                IP = '%s:%s' % (i, port)
                print('抓到ip %s' % IP)
                yield IP
    except Exception as e:
        print('抓取{}代理出现错误'.format(site_name), e)

# crawl_ip('_89', 1)
