# !/usr/bin/python
# -*- coding: utf-8 -*-

# Redis Host
HOST = 'localhost'
# Redis PORT
PORT = 6379

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

TEST_URL = "http://baidu.com/"
# TEST_URL = "http://www.httpbin.org/"
# TEST_URL = "https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D"

Proxy_NUM = 100
CHECK_TIME = 5
CHECK_CYCLE = 30
CRAWL_CYCLE = 120

XICI_PATTERN = '<td>(\d+?\.\d+?\.\d+?\.\d+?)</td>.*?(\d+?)</d?'
_89IP_PATTERN = '.*?(\d+?\.\d+?\.\d+?\.\d+?).*?(\d+?)'
_66IP_PATTERN = '<tr><td>(\d+?\.\d+?\.\d+?\.\d+?)</td><td>(\d+?)</td>'
KUAIDAILI_PATTERN = ''' <td data-title="IP">(.*?)</td>
                    <td data-title="PORT">(\d+?)</td>'''
IP3366_PATTERN = '''<td>(\d+?\.\d+?\.\d+?\.\d+?)</td>.*?<td>(\d+?)</td>'''

XICI_URL1 = 'http://www.xicidaili.com/nt/%s'
XICI_URL2 = 'http://www.xicidaili.com/wn/%s'
XICI_URL3 = 'http://www.xicidaili.com/wt/%s'
_66IP_URL = 'http://www.66ip.cn/%s.html'
_89IP_URL = 'http://www.89ip.cn/index_%s.html'
KUAIDAILI_URL = 'https://www.kuaidaili.com/free/inha/%s/'
IP3366_URL = 'http://www.ip3366.net/free/?stype=1&page=%s'

IP_SITES = {
    'xici1': {'pattern': XICI_PATTERN, 'url': XICI_URL1},
    'xici2': {'pattern': XICI_PATTERN, 'url': XICI_URL2},
    'xici3': {'pattern': XICI_PATTERN, 'url': XICI_URL3},
    '_89': {'pattern': _89IP_PATTERN, "url": _89IP_URL},
    '_66': {'pattern': _66IP_PATTERN, "url": _66IP_URL},
    'kuaidaili': {'pattern': KUAIDAILI_PATTERN, "url": KUAIDAILI_URL},
    'ip3366': {'pattern': IP3366_PATTERN, "url": IP3366_URL},

}

PROXY_SITES = [
    'xici1',
    'xici2',
    'xici3',
    '_89',
    '_66',
    'kuaidaili',
    'ip3366'
]

'''
https://proxy.mimvp.com/free.php?proxy=in_hp
http://www.coobobo.com/free-http-proxy
http://ip.zdaye.com/
http://www.mayidaili.com/free/anonymous/%E9%AB%98%E5%8C%BF
http://http.taiyangruanjian.com/
http://http.zhimaruanjian.com/
'''
