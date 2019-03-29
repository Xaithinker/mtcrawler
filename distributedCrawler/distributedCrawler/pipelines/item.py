# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from pymongo import MongoClient
import configparser
import os
import sys

paths = r'E:\Documents\_2019\scrapy_project\distributedCrawler\distributedCrawler\pipelines'
paths = os.path.abspath(paths)

class CartItemPipeline(object):
    """存储至monodb"""

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(paths, 'mongodb.cfg'))
        self.client = MongoClient(self.config['DEFAULT']['MONGODB_SERVER'], int(self.config['DEFAULT']['MONGODB_PORT']))
        self.db = self.client[f"{self.config['DEFAULT']['MONGODB_DB']}"]
        self.collection = self.db['mtcollection']
    
    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item
    
    def item_scraped(self, spider):
        print('Item has insert to mongoDB')