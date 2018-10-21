''' 爬虫启动入口 '''

from Basic_Bot.Scheduler import SpiderMan

if __name__ == "__main__":
    spider_man = SpiderMan()
    start_url = '请自行替换'
    spider_man.crawl(start_url)

# todo 修改解析规则
# todo 修改存储规则
