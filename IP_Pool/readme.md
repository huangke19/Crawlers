![proxy](https://github.com/huangke19/IP_Pool/raw/master/proxy.png))



# IP_Pool

![dd](https://github.com/huangke19/LagouSpider/raw/master/lines/bird.jpg)

## 功能描述

- 通过Flask提供接口
- 通过requests抓取免费代理放入Redis
- 通过aiohttp库对代理进行异步检测
- 通过评分机制筛选淘汰不可用IP
- 不同进程负责不同的功能，当可用IP数量小于30时会开启新一轮抓取



## 项目结构：

| 文件      | 作用            |
| --------- | --------------- |
| api.py    | Flask提供的接口 |
| ipChecker | 检查IP是否可用  |
| spider.py | 抓取免费代理    |
| db.py     | 数据库配置      |
| config.py | 配置参数        |



## 使用说明

下载源码:

```shell
git clone https://github.com/huangke19/IP_Pool
```

安装依赖:

```shell
pip install -r requirements.txt
python scheduler.py
```



通过api访问http://127.0.0.1:5000 查看。



## Api

| api    | method | Description      |
| ------ | ------ | ---------------- |
| /      | GET    | api介绍          |
| /get   | GET    | 随机获取一个代理 |
| /count | GET    | 查看当前可用IP数 |

#### 

## Example

```python
import requests

ip = requests.get("http://127.0.0.1:5000/get").text
print(ip)
```

[Errno 54] Connection reset by peer
https://segmentfault.com/q/1010000005647542



## 检测策略

- 请求异常的直接删除
- 请求返回码不是200的进行减分重试
- 连续5次请求返回码不是200的删除