#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from config import USER_AGENT

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
