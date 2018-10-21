import datetime
import json
import re

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

HOST = '127.0.0.1'
MONGO_PORT = 27017
mongo_conn = MongoClient(HOST, MONGO_PORT)
mongo_db = mongo_conn['mtime']
mongo_col = mongo_db['piaofang']

headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
}

def parse_movie_urls(url):
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')
        soup = soup.select_one('#hotplayContent')
        all_a = soup.find_all('a', attrs={"href": re.compile(r"http://movie.mtime.com/\d+/")})
        urls = set([url['href'] for url in all_a])
        movie_ids = [url.split('/')[-2] for url in urls]
        return movie_ids
    else:
        return None

def parse_movie_ajax(movie_id):
    url = "http://service.library.mtime.com/Movie.api"

    nowtime = datetime.datetime.now().strftime('%Y%-m%-d%H%M%S%f')
    querystring = {"Ajax_CallBack":          "true", "Ajax_CallBackType": "Mtime.Library.Services",
                   "Ajax_CallBackMethod":    "GetMovieOverviewRating", "Ajax_CrossDomain": "1",
                   "Ajax_RequestUrl":        "http%3A%2F%2Fmovie.mtime.com%2F{}%2F".format(movie_id), "t": nowtime,
                   "Ajax_CallBackArgument0": movie_id}

    response = requests.request("GET", url, headers=headers, params=querystring)
    pattern = re.compile(r'.*?({.*}).*?', re.S)
    json_text = re.findall(pattern, response.text)[0]
    infos = json.loads(json_text)

    print(infos)

    pf = dict()
    pf['名字'] = infos['value']['movieTitle']
    pf['movieId'] = infos['value']['movieRating']['MovieId']
    if infos['value'].get('boxOffice', None):
        pf['rank'] = infos['value']['boxOffice']['Rank']
        pf['总票房'] = infos['value']['boxOffice']['TotalBoxOffice']
        pf['当日票房'] = infos['value']['boxOffice']['TodayBoxOffice']
        pf['首日票房'] = infos['value']['boxOffice']['FirstDayBoxOffice']
        pf['上映天数'] = infos['value']['boxOffice']['ShowDays']
    return pf

def write_info_mongo(data):
    if data:
        mongo_col.insert(data)
    else:
        return

def main():
    url = 'http://theater.mtime.com/China_Sichuan_Province_Chengdu/'
    movie_ids = parse_movie_urls(url)
    for _id in movie_ids:
        data = parse_movie_ajax(_id)
        write_info_mongo(data)

if __name__ == '__main__':
    main()
