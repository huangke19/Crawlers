import re

import requests

from config import HEADERS


def crawl_ip():
    '''
    :param site_name: 要爬取的网站名
    :param page: 要爬取的页数
    '''
    pattern = '''<td>(\d+?\.\d+?\.\d+?\.\d+?)</td>.*?<td>(\d+?)</td>'''
    url = 'http://www.ip3366.net/free/'
    # print('正在爬取{}代理第{}页'.format(s page))

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
    except Exception as e:
        print('抓取{}代理出现错误', e)


crawl_ip()
