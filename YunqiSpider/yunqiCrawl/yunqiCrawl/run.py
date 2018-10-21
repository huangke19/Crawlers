from scrapy import cmdline

name = 'yunqi'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
