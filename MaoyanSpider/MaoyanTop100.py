''' 猫眼电影Top100 爬虫'''
import json
import re
from multiprocessing.pool import Pool

import requests
from requests.exceptions import RequestException

# 1.抓取单面内容          get_one_page()
# 2.正则表达式获取信息     parse_one_page()
# 3.保存信息              write_to_file()
# 4. 开启循环/线程        pool

URL = 'http://maoyan.com/board/4?offset=%s'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/68.0.3440.106 Safari/537.36'}

def get_one_page(url, headers):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        print('something wrong')

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name">'
                         + '<a.*?>(.*?)</a>.*?"star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)  # 不加re.S无法匹配换行符
    items = re.findall(pattern, html)
    for item in items:
        print(item)
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time':  item[4].strip()[5:],
            'score': item[5] + item[6]
        }

def write_to_file(content):
    with open('result.txt', 'a', encoding='utf8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()
        # encoding='utf8' ensure_ascii=False 保证写入txt的都是中文而不是ASCII码

def main(offset):
    url = URL % str(offset)
    html = get_one_page(url, HEADERS)
    for i in parse_one_page(html):
        write_to_file(i)

if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i * 10 for i in range(10)])
