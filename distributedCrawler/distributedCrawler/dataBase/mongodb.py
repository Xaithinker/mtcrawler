# -*- coding:utf-8 -*-

from pymongo import MongoClient
import configparser
import os

paths = r'E:\Documents\_2019\scrapy_project\distributedCrawler\distributedCrawler\pipelines'
paths = os.path.abspath(paths)
config = configparser.ConfigParser()
config.read(os.path.join(paths, 'mongodb.cfg'))

del paths

client = MongoClient(config['DEFAULT']['MONGODB_SERVER'], int(config['DEFAULT']['MONGODB_PORT']))
db = client[f"{config['DEFAULT']['MONGODB_DB']}"]

del config

mongo_connection = db['xicidaili']
