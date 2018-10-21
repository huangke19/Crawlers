![logo](https://github.com/huangke19/KuwoSpider/raw/master/logo.jpg)

## 酷我听书app爬虫



## 接口抓包

使用wireshark和网易mumu安卓模拟器进行抓包

### wireshark过滤器

```shell
http.host contains "kuwo.cn" and http
```

#### 主页分类接口

```python
index_url = 'http://ts.kuwo.cn/service/getlist.v31.php?act=get_header&uid=13657560984&version=8.5.3.0&device_id=Avu4' \
            'n1VFxmMSdNPdRGa1a91ydzE7-6ISB6yu54uwtG7_&token=&channelId=qq&kw_id=-1'
```

#### 小说大类接口

```python
novel_url = 'http://ts.kuwo.cn/service/catlist.v34.php?act=first_cat&id=%s&uid=13657560984&version=8.5.3.0&device_id=' \
            'Avu4n1VFxmMSdNPdRGa1a91ydzE7-6ISB6yu54uwtG7_&token=&channelId=qq&kw_id=-1'
```

#### 小说子类（都市、言情）下的书籍目录接口

```python
novel_sub_url = 'http://ts.kuwo.cn/service/getlist.v31.php?act=cat&id={}&type=hot&uid=13657560984&version=8.5.3.0&device_id=Avu4n1VFxmMSdNPdRGa1a91ydzE7-6ISB6yu54uwtG7_&token=&channelId=qq&kw_id=-1'
```

#### 指定书籍的所有音频信息

```python
book_info_url = 'http://tingshu.kuwo.cn/api/tsdata?m=getChapters&id={}'
```

![logo](https://github.com/huangke19/KuwoSpider/raw/master/res.png)



