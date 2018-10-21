import requests
import json
import re
from multiprocessing.pool import Pool
from urllib.parse import urlencode

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
}

def get_index_page(offset, keyword):
    params = {'offset':   offset,
              'format':   'json',
              'keyword':  keyword,
              'autoload': 'true',
              'count':    '20',
              'cur_tab':  '1',
              'from':     'search_tab'}
    url = 'https://www.toutiao.com/search_content/?' + urlencode(params)

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except ConnectionError:
        return None

def parse_index_urls(res):
    if res and 'data' in res.keys():
        for item in res.get('data'):
            title = item.get('title')
            article_url = item.get('article_url')
            if title and article_url:
                yield {
                    'title':       title,
                    'article_url': article_url
                }

def get_page_detail(url):
    new_url = url.replace('group/', 'a')
    res = requests.get(new_url, headers=headers)
    if res.status_code == 200:
        html = res.text
        return html
    else:
        return None

def parse_details(html):
    url_pattern = re.compile('gallery: JSON.parse(.*?)siblingList', re.S)
    url_items = re.findall(url_pattern, html)
    try:
        tmp = url_items[0].strip()[2:-3].replace('\\', '')
        urls_json = json.loads(tmp)
        pic_urls = urls_json.get('sub_images')
        images = [item.get("url") for item in pic_urls]
        return images
    except IndexError:
        return None

def main(offset):
    res = get_index_page(offset, '街拍')
    url_gen = parse_index_urls(res)
    for item in url_gen:
        title = item.get('title')
        url = item.get('article_url')
        html = get_page_detail(url)
        if html:
            image_urls = parse_details(html)
            if image_urls:
                print(title, image_urls)
            else:
                continue
        else:
            continue

if __name__ == '__main__':
    main(0)
    # pool = Pool()
    # pool.map(main, [i * 10 for i in range(10)])
