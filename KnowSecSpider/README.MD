# 知道创宇爬虫题



#### 使用python编写一个网站爬虫程序，支持参数如下：

spider.py -u url -d deep -f logfile -l loglevel(1-5)  --testself -thread number --dbfile  filepath  --key=”HTML5”



 

#### 参数说明：

- [ ] -u 指定爬虫开始地址

- [ ] -d 指定爬虫深度

--thread 指定线程池大小，多线程爬取页面，可选参数，默认10

- [ ] --dbfile 存放结果数据到指定的数据库（sqlite）文件中

- [ ] --key 页面内的关键词，获取满足该关键词的网页，可选参数，默认为所有页面

- [ ] -l 日志记录文件记录详细程度，数字越大记录越详细，可选参数，默认spider.log

--testself 程序自测，可选参数

 

#### 功能描述：

1、指定网站爬取指定深度的页面，将包含指定关键词的页面内容存放到sqlite3数据库文件中

2、程序每隔10秒在屏幕上打印进度信息

3、支持线程池机制，并发爬取网页

4、代码需要详尽的注释，自己需要深刻理解该程序所涉及到的各类知识点

5、需要自己实现线程池

 

提示1：使用re  urllib/urllib2  beautifulsoup/lxml2  threading optparse Queue  sqlite3 logger  doctest等模块

提示2：注意是“线程池”而不仅仅是多线程

提示3：爬取sina.com.cn两级深度要能正常结束

 

建议程序可分阶段，逐步完成编写，例如：

版本1:Spider1.py -u url -d deep

版本2：Spider3.py -u url -d deep -f logfile -l loglevel(1-5)  --testself

版本3：Spider3.py -u url -d deep -f logfile -l loglevel(1-5)  --testself -thread number

版本4：剩下所有功能



 

# 爬虫设计

#### 参考资料：《代码大全》第五章

《代码大全》有言，在软件架构的层次上，可以通过把整个系统分解为多个子系统来降低问题的复杂度。

《代码大全》又有言，一个程序中的设计层次

- 系统（1）首先被组织成子系统（2）

- 子系统进一步被分解为类（3）

- 然后类又被分解为子程序和数据（4）

- 每个子程序内部也要进行设计


将此爬虫看作一个软件系统，对其按如上思路进行分析

#### 第一层：软件系统

本爬虫是一个整站爬取类爬虫系统

#### 第二层：分解为子系统或包

识别出所有的主要子系统

1. 爬虫系统
2. 参数解析系统
3. 日志系统
4. 线程池系统
5. 测试系统

#### 第三层：分解为类

1. 爬虫需要成为一个类
2. 线程池需要成为一个类

#### 第四层：分解为子程序



- #### 爬虫类

  crawl_one_page

  ###### 爬取流程 ：

  ```python
  tc_list = [start_url]	# 待爬队列
  
  for i in range(depth):
      urls = copy.deepcopy(tc_list)	# 将待爬urls放入urls
      tc_list = []					# 清空待爬队列
      for url in urls:
          new_url, data = crawl(url)
          tc_list.append(new_url)
  ```




- #### 日志系统

  ```python
  logging.basicConfig(filename='robot.log', filemode='a',
                      format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
  logger = logging.getLogger(__name__)
  
  LOG_LEVEL = {
      1: logger.info,
      2: logger.warning,
      3: logger.error,
      4: logger.critical,
      5: logger.log,
  }
  ```

  to be done

- #### 线程池系统

- #### 参数解析系统

  ```python
  class MyParser(ArgumentParser):
  
      def __init__(self):
          super().__init__()
          self.description = '可选爬虫参数'
  
      def get_parser(self):
          self.add_argument('-u', dest='url', help='url地址')
          self.add_argument('-d', dest='depth', help='爬取深度')
          self.add_argument('-thread', dest='thread', default=10, help='线程池大小')
          self.add_argument('-dbfile', dest='dbname', help='数据库名')
          self.add_argument('-f', dest='logfile', help='日志文件')
          self.add_argument('-k', dest='key', default='all', help='页面内的关键词')
          self.add_argument('-l', dest='loglevel', help='日志等级')
          self.add_argument('--testself', dest='test', help='程序自测 ')
          return self.parse_args()
  ```

- #### 测试系统

- #### 数据类

  1. 初始化时连接mongodb
  2. save_to_mongo





