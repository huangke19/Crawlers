![logo](https://github.com/huangke19/XiachufangSpider/raw/master/logo.png)



# 下厨房Spider



## 目标

抓取下厨房全站菜谱



## 网站结构分析

经过观察分析，有两种方式可以爬取，一种是从首页进入各大分类，然后从进入分类分别开爬

第二种是直接使用ID遍历式爬取

本次爬取决定选择第二种



## 调试

scrapy shell url

## 解析

使用xpath

## 清洗

使用itemloader的清洗功能

## 查看解析结果

 scrapy parse --spider=xiachufang https://www.xiachufang.com/recipe/103299381/

## 检查字段

在parse的doc中创建contract

scrapy check xiachufang



process_item里必须传spider参数



## 加入启动和调试脚本

```python
from scrapy import cmdline

name = 'xiachufang'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
```





问题：

1. key_error   检查item和spider里是否匹配
2. unicode.strip，在Python3里没有unicode，改成str
3. process_item里必须传spider参数



# 反爬

## 429封IP

激活代理IP中间件，但失效的IP怎么去除呢？爬取失败的url又如何处理？

使用开源代理，付费的蘑菇代理，使用tor