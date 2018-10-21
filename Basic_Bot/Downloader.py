#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests

from Basic_Bot.config import USER_AGENT

class Downloader(object):

    def download(self, url):
        if url is None:
            return None

        user_agent = USER_AGENT
        headers = {'User-Agent': user_agent}
        try:
            r = requests.get(url, headers=headers, timeout=4)
            if r.status_code == 200:
                r.encoding = 'utf-8'
                return r.text
            print('警告: 下载器返回状态码不是200')
            return None
        except Exception as e:
            print('下载器出错')
            print(e)
