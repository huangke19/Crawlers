#!/usr/bin/python
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo as pymongo
from scrapy.exceptions import DropItem

from food_scrapy.items import RecipeItem
from food_scrapy.settings import MONGODB_SERVER, MONGODB_DB, MONGODB_PORT, MONGODB_COLLECTION

class FoodScrapyPipeline(object):

    def __init__(self):
        client = pymongo.MongoClient(MONGODB_SERVER, MONGODB_PORT)
        db = client[MONGODB_DB]
        self.collection = db[MONGODB_COLLECTION]

    def process_item(self, item, spider):
        if item and isinstance(item, RecipeItem):
            # 插入数据库集合中
            recipe_item = dict(item)
            print(recipe_item)
            self.collection.insert(recipe_item)
        else:
            raise DropItem
