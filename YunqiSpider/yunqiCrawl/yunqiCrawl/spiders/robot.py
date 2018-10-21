# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from yunqiCrawl.items import YunqiBookListItem, YunqiBookDetailItem


class YunqiQqComSpider(CrawlSpider):
    name = 'yunqi'
    allowed_domains = ['yunqi.qq.com']
    # start_urls = ['http://yunqi.qq.com/bk/so2/n10p1']

    rules = (
        Rule(LinkExtractor(allow=r'/bk/so2/n30p\d+'), callback='parse_book_list', follow=True),
    )

    def start_requests(self):

        urls = ('http://yunqi.qq.com/bk/so2/n30p%s' % i for i in range(12409))
        for url in urls:
            yield Request(url=url, callback=self.parse_book_list)

    def parse_book_list(self, response):
        books = response.xpath('.//div[@class="book"]')
        for book in books:
            # 小说ID
            novelId = book.xpath('./div[@class="book_info"]/h3/a/@id').extract_first()
            # 小说名字
            novelName = book.xpath('./div[@class="book_info"]/h3/a/text()').extract_first()
            # 小说链接
            novelLink = book.xpath('./div[@class="book_info"]/h3/a/@href').extract_first()

            book_info = book.xpath('./div[@class="book_info"]//dd[@class="w_auth"]')

            # 小说作者
            novelAuthor = book_info[0].xpath('./a/text()').extract_first()
            # 小说类型
            novelType = book_info[1].xpath('./a/text()').extract_first()
            # 小说状态
            novelStatus = book_info[2].xpath('./text()').extract_first()
            # 小说更新时间
            novelUpdateTime = book_info[3].xpath('./text()').extract_first()
            # 小说字数
            novelWords = book_info[4].xpath('./text()').extract_first()
            # 小说封面
            novelImageUrl = book.xpath('./a/img/@src').extract_first()

            book_list_item = YunqiBookListItem(novelId=novelId,
                                               novelName=novelName,
                                               novelLink=novelLink,
                                               novelAuthor=novelAuthor,
                                               novelType=novelType,
                                               novelStatus=novelStatus,
                                               novelUpdateTime=novelUpdateTime,
                                               novelWords=novelWords,
                                               novelImageUrl=novelImageUrl)
            yield book_list_item

            yield Request(url=novelLink, meta={'novelId': novelId}, callback=self.parse_book_detail)

    def parse_book_detail(self, response):
        if not response:
            return None
        # 小说id
        novelId = response.meta['novelId']
        # 小说标签
        novelLabel = response.xpath("//div[@class='tags']/text()").extract_first()
        # 小说总点击量
        novelAllClick = response.xpath(".//*[@id='novelInfo']/table/tr[2]/td[1]/text()").extract_first()
        # 小说总人气
        novelAllPopular = response.xpath(".//*[@id='novelInfo']/table/tr[2]/td[2]/text()").extract_first()
        # 小说总推荐
        novelAllComm = response.xpath(".//*[@id='novelInfo']/table/tr[2]/td[3]/text()").extract_first()
        # 小说月点击量
        novelMonthClick = response.xpath(".//*[@id='novelInfo']/table/tr[3]/td[1]/text()").extract_first()
        # 小说月人气
        novelMonthPopular = response.xpath(".//*[@id='novelInfo']/table/tr[3]/td[2]/text()").extract_first()
        # 小说月推荐
        novelMonthComm = response.xpath(".//*[@id='novelInfo']/table/tr[3]/td[3]/text()").extract_first()
        # 小说周点击量
        novelWeekClick = response.xpath(".//*[@id='novelInfo']/table/tr[4]/td[1]/text()").extract_first()
        # 小说周人气
        novelWeekPopular = response.xpath(".//*[@id='novelInfo']/table/tr[4]/td[2]/text()").extract_first()
        # 小说周推荐
        novelWeekComm = response.xpath(".//*[@id='novelInfo']/table/tr[4]/td[3]/text()").extract_first()
        # 小说评论总数
        novelCommentNum = response.xpath(".//*[@id='novelInfo_commentCount']/text()").extract_first()

        if not novelAllClick and not novelLabel: return

        bookDetailItem = YunqiBookDetailItem(novelId=novelId, novelLabel=novelLabel, novelAllClick=novelAllClick,
                                             novelAllPopular=novelAllPopular,
                                             novelAllComm=novelAllComm, novelMonthClick=novelMonthClick,
                                             novelMonthPopular=novelMonthPopular,
                                             novelMonthComm=novelMonthComm, novelWeekClick=novelWeekClick,
                                             novelWeekPopular=novelWeekPopular,
                                             novelWeekComm=novelWeekComm, novelCommentNum=novelCommentNum)
        yield bookDetailItem
