from scrapy import cmdline

name = 'xiachufang'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
