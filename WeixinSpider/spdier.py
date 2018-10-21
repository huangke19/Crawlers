''' 微信搜狗爬虫 '''

# 1. 爬取索引页  crawl_index_page
# 2. 爬取详情页  crawl_detail_page
# 3. 检测是否需要代理 check_proxy
# 4. 存储到数据库 store_to_mongo
import random
import re
from time import sleep
from urllib.parse import urlencode

import matplotlib.image as mpimg  # mpimg 用于读取图片
import matplotlib.pyplot as plt  # plt 用于显示图片
import pymongo
import requests
from bs4 import BeautifulSoup

mogu_url = 'http://piping.mogumiao.com/proxy/api/get_ip_al?appKey=602de1a2931f40a78513aec228e9a15f&count=1&expiryDate=0&format=1&newLine=2'

def get_proxy(url):
    r = requests.get(url)
    tmp = r.json()
    ip, port = tmp['msg'][0]['ip'], tmp['msg'][0]['port']
    host = ip + ':' + port
    return host

base_url = 'http://weixin.sogou.com/weixin?'
MONGO_URI = 'localhost'
MONGO_DB = 'weixin'
headers = {
    'Host':                      'weixin.sogou.com',
    'Connection':                'keep-alive',
    'Cache-Control':             'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent':                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, '
                                 'like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Accept':                    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':           'gzip, deflate',
    'Accept-Language':           'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
    'Cookie':                    'CXID=F9E1B4C13B456C5C3207885052B38726; SUID=2292DDAB3765860A5AF1D42700023CE7; SUV=003C177DABDD90A75AF692C7C41B1072; wuid=AAHdgfhQIAAAAAqLEyJ1mgoApwM=; sw_uuid=7116429604; sg_uuid=805865404; dt_ssuid=3151260872; pex=C864C03270DED3DD8A06887A372DA219231FFAC25A9D64AE09E82AED12E416AC; ssuid=2850715698; pgv_pvi=9436978176; usid=0C8372761537990A000000005B52FC7F; ABTEST=0|1533569192|v1; IPLOC=CN5101; weixinIndexVisited=1; JSESSIONID=aaaGLNN9jjGMVcNytxBvw; ppinf=5|1535450024|1536659624|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTklOTIlQjElRTUlQTElOTh8Y3J0OjEwOjE1MzU0NTAwMjR8cmVmbmljazoxODolRTklOTIlQjElRTUlQTElOTh8dXNlcmlkOjQ0Om85dDJsdURkNDR2WTZyckFqQ3FuVG9MdmtsWmNAd2VpeGluLnNvaHUuY29tfA; pprdig=AVITFrrFagC6LRsfLELIyms113cIX-ZYUK9BbMlGV2vZQ-015ljIdvuPJJjr9fGP2_zYfsJpzhTzUpfuidD-j6ESxYvWeXKeFFubwxXBMJSWj8WbYFkVkBh8cl7SYn_a0neqaWMSkRQeapYCrG2OHCj_l-PrOfPEnwf7gveyaBU; sgid=19-36834737-AVuFG6jA6kicmsciartRytxmw; PHPSESSID=1upv1jusprdn9ku5aj0ab68le7; SUIR=C48CC7B01B1F6F60D2C0A1891B451B18; ad=illlllllll2bK5KHlllllVmVQDYlllllz2X4WZllllGlllll4llll5@@@@@@@@@@; pgv_si=s7079841792; sct=192; ld=Kkllllllll2bqaQZlllllVmp299lllllNX3RRlllllGlllll4ylll5@@@@@@@@@@; LSTMV=240%2C76; LCLKINT=1061285; ppmdig=1535528069000000e97ca7497e0ce68dfc302ee3ac880e12; SNUID=602B6015BEB8CA30DF5A44B5BE599B10; successCount=1|Wed, 29 Aug 2018 08:07:57 GMT'}

class SogouWeixinSpider(object):

    def __init__(self, keyword):
        self.keyword = keyword
        self.client = pymongo.MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB]
        self.count = 0
        self.flag = 0

    def get_index_page(self, page):

        if self.count > 5:
            print(self.count)
            return

        params = {'query': self.keyword,
                  'type':  '2',
                  'page':  page}
        queries = urlencode(params)
        url = base_url + queries
        try:
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                self.flag += 1
                print('爬了%s个' % self.flag)
                print('正在使用本机爬取 %s 页' % page)
                text = r.text
                ip_pattern = '<p class="ip-time-p">IP.*?\d+?\.\d+\.\d+\.\d+<br>'
                if re.findall(ip_pattern, text):
                    print('不能直接用本机IP访问')
                    self.crawl_with_proxy(url)
                return r.text
            elif r.status_code == 302:
                text = self.crawl_with_proxy(url)
                return text
            else:
                print('crawl failed')
        except Exception as e:
            self.count += 1
            return self.crawl_with_proxy(url)

    def crawl_with_proxy(self, url):

        try:
            proxy = get_proxy(mogu_url)
            proxies = {'http': 'http://' + proxy}
            print('使用代理 %s 爬取' % proxies)
            print(url)

            r = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            print(r.status_code)
            r.encoding = 'utf-8'
            print(r.text)
            return r.text
        except Exception as e:
            self.count += 1
            return self.crawl_with_proxy(url)

    def parse_index_page(self, text):
        pattern = re.compile('<a target="_blank" href="(.*?)"', re.S)
        urls = re.findall(pattern, text)
        if not urls:
            print('被识别出来了，或者提取规则变了')
            return
        print(urls)
        return urls

    def crack_captcha(self, text):
        pattern = re.compile(r'onerror="setImgCode\(0\)" src="(util/seccode.php\?tc=\d+?)"', re.S)
        cap_url = re.search(pattern, text).group(1)
        fullurl = 'http://weixin.sogou.com/antispider/' + cap_url
        r = requests.get(fullurl)
        with open('code.jpeg', 'wb') as f:
            f.write(r.content)
        self.show_img('code.jpeg')
        return input('验证码: ')

    def show_img(img):
        lena = mpimg.imread(img)
        plt.imshow(lena)
        plt.axis('off')
        plt.show()

    def crawl_detail_page(self, url):
        r = requests.get(url)
        html = r.text

        soup = BeautifulSoup(html, 'lxml')
        title = soup.title.string
        title = title.strip() if title else None

        name = soup.select('.profile_nickname')
        name = name[0].get_text() if name else None

        soup = soup.select(".rich_media_content")
        if soup:
            soup = soup[0]
            text = [t.get_text() for t in soup.find_all('p') if t.get_text()]
        else:
            text = None
        return {'_id': title, 'title': title, 'name': name, 'text': text}

    def store_to_mongo(self, datas):
        if self.db.weixin.update({'title': datas['title']}, {'$set': datas}, True):
            print('Saved to Mongo', datas['title'])
        else:
            print('Saved to Mongo failed', datas['title'])

    def crawl(self, page):
        text = self.get_index_page(page)
        art_urls = self.parse_index_page(text)
        if not art_urls:
            self.crack_captcha(text)
        for i, url in enumerate(art_urls, 1):
            format_url = url.replace('amp;', '')
            data = self.crawl_detail_page(format_url)
            self.store_to_mongo(data)

if __name__ == '__main__':
    spider = SogouWeixinSpider('知乎')
    for i in range(1, 101):
        spider.crawl(i)
        sleep(random.randrange(1, 10))
