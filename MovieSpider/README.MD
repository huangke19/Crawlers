​	![logo](https://github.com/huangke19/MovieSpider/raw/master/logo.jpg)



# MovieSpider

> 异步爬虫只有一个追求，快！

![dd](https://github.com/huangke19/LagouSpider/raw/master/lines/bird.jpg)

## 目标

- 抓取[电影天堂](http://www.btbtdy.net/)全站所有电影的磁力链接
- 速度要快
- 要进行增量式爬取



## 网页结构

> 分析：电影网站结构非常简单，url里的数字即为电影的id，从1到13xxx，可以直接循环抓取
>

- 详情页url http://www.btbtdy.net/btdy/dy13426.html

- 磁力链页url http://www.btbtdy.net/vidlist/13415.html




## 爬虫设计

> 因为结构简单，所以设计成ID遍历式爬虫

- 请求函数 get_page
- 解析函数 parse_page
- 存储函数 save_to_mongo, save_to_redis
- 抓取流程函数 crawl
- 抓取最新电影id函数  get_newest_id
- 主运行函数 main

## 要注意的地方

> 1. 因为是id遍历式爬虫，所以会遇到很多id已经失效或者不是我们想要的信息，所以需要注意识别并处理
> 2. 异步代码比较难以编写，要注意处理函数结构和异常情况

## 去重

> 去重使用Redis数据库的集合数据结构，已正常抓取的电影的id放入crawled_movie_ids，不可用的电影的id放到bad_movie_ids，由于只存放数字，而且数据量不大，这种去重方式已经足够



## 增量式爬取

> - 每次抓取时先获取最新的电影max_id，然后遍历range(1, max_id+1)，对不属于以上两个Redis集合的id进行抓取，这样就做到了增量式抓取；
>
> - 其实也可以和两个集合中最大的数进行比较，这样也可以实现增量式，后续改进吧




## 提速 Speed Up!

- 第一步:	网络请求，网络请求的时间远远大于解析和存储时间，所以用异步来提升效率，也尝试一下aiohttp这个杀器
- 第二步:   解析，解析使用正则速度最快，不过本次解析的文本也很少啦
- 第三步:   存储，存储感觉Redis应该比MongoDB快，请指正


## 结果

> 异步效率惊人！
>
> ###### 爬取**13426**个网页，获取 60919条数据，用时96秒
>
> 请根据网站服务器并发能力自行调节asyncio信号量



![dd](https://github.com/huangke19/LagouSpider/raw/master/lines/bird.jpg)

## 问题

1. #### 数据量大的时候，爬虫爬取完成后，不能立刻结束，还要一段时间来关闭，这个是什么问题？

   解决：部分连接超时了，造成了阻塞，设置timeout参数

2. #### 爬取的数据少部分会有遗漏

   部分id不可用，或者并发数太多，服务器自动reset了请求

3. 原本不打算加delay的，但是不加delay反而慢了，加了delay跑得反而顺畅一些，why？

4. 从0到13426的爬取过程中，有的地方特别快，有的地方却开始慢下来，需要调整

5. #### reset by peer

   解决：服务器的并发连接数超过了其承载量，服务器会将其中一些连接Down掉； 

6. #### Cannot connect to host www.btbtdy.net:80 ssl:None [nodename nor servname provided, or not known]

   DNS解析错误

   解决方法：查aiohttp文档

   > *Optional* [aiodns](https://aiohttp.readthedocs.io/en/stable/glossary.html#term-aiodns) for fast DNS resolving. The library is highly recommended.
   >
   > ```
   > $ pip install aiodns
   > ```



代码将继续优化