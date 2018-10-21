#!/usr/bin/python
# -*- coding: utf-8 -*-

''' 酷我听书app爬虫，获取app内所有小说的详细信息'''

import sys

import requests
from pymongo import MongoClient

mongo_conn = MongoClient('127.0.0.1', 27017, connect=False)
db = mongo_conn.kuwo
curser = db.novel

# 主页url
index_url = 'http://ts.kuwo.cn/service/getlist.v31.php?act=get_header&uid=13657560984&version=8.5.3.0&device_id=Avu4' \
            'n1VFxmMSdNPdRGa1a91ydzE7-6ISB6yu54uwtG7_&token=&channelId=qq&kw_id=-1'

# 小说大类的分类接口
novel_url = 'http://ts.kuwo.cn/service/catlist.v34.php?act=first_cat&id=%s&uid=13657560984&version=8.5.3.0&device_id=' \
            'Avu4n1VFxmMSdNPdRGa1a91ydzE7-6ISB6yu54uwtG7_&token=&channelId=qq&kw_id=-1'

# 小说子类（都市、言情）下的书籍目录
novel_sub_url = 'http://ts.kuwo.cn/service/getlist.v31.php?act=cat&id={}&type=hot&uid=13657560984&version=8.5.3.0&device_id=Avu4n1VFxmMSdNPdRGa1a91ydzE7-6ISB6yu54uwtG7_&token=&channelId=qq&kw_id=-1'

# 指定书籍的所有音频信息
book_info_url = 'http://tingshu.kuwo.cn/api/tsdata?m=getChapters&id={}'


def get_top_index(url):
    ''' 获取主页下的总分类目录 '''
    try:
        r = requests.get(url)
        r.encoding = 'utf-8'
        cates = r.json().get('list')
        return cates
    except Exception:
        sys.stdout.write("获取主页分类失败")
        return None


def get_novel_index(id):
    '''
    获取小说分类下的目录
    id: 小说大类的id
    '''
    url = novel_url % id
    try:
        r = requests.get(url)
        r.encoding = 'utf-8'
        novel_cats = r.json().get('cats')
        return novel_cats
    except Exception:
        sys.stdout.write("获取小说分类失败")
        return None


def get_sub_books(id):
    ''' 获取小说分类下文学类的所有书籍 '''
    url = novel_sub_url.format(id)
    try:
        r = requests.get(url)
        r.encoding = 'utf-8'
        lit_books = r.json().get('list')
        return lit_books
    except Exception:
        sys.stdout.write("获取小说子类下书籍失败")
        return None


def get_book_info(id):
    ''' 获取书籍的详细信息 '''
    url = book_info_url.format(id)
    r = requests.get(url)
    r.encoding = 'utf-8'
    chapters = r.text
    return chapters


def main():
    cates = get_top_index(index_url)
    novel_cat_id = cates[0].get('Id')
    sub_cats = get_novel_index(novel_url % novel_cat_id)
    for cat in sub_cats:
        cat_name = cat.get("Name")
        curser = db[cat_name]
        id = cat.get("Id")
        books = get_sub_books(id)
        for book in books:
            curser.insert(book)
    return None


if __name__ == '__main__':
    main()
