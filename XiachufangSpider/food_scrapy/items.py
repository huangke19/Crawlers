# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class RecipeItem(scrapy.Item):
    rid = Field()
    name = Field()
    cate = Field()
    score = Field()
    cooked = Field()
    cook = Field()
    cover = Field()
    brief = Field()
    steps = Field()
    tips = Field()
