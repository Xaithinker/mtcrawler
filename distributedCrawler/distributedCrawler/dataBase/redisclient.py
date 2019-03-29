# -*- coding:utf-8 -*-

"""
Redis Client
"""
import configparser
import sys
import redis
import os

paths = r'e:\Documents\_2019\scrapy_project\distributedCrawler\distributedCrawler\dataBase'
paths = os.path.abspath(paths)

config = configparser.ConfigParser()
config.read(os.path.join(paths, 'redis.cfg'))

host = config['DEFAULT']['REDIS_SERVER']
port = config['DEFAULT']['REDIS_PORT']
db = config['DEFAULT']['REDIS_DB']
pwd = config['DEFAULT']['PASSWORD']

del config

class RedisClient(object):

    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RedisClient, cls).__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwords):
        self.host = host
        self.port = port
        self.db = db
        self.pwd = pwd
        self.__pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db, password=123456)
        self.client = redis.Redis(connection_pool=self.__pool)

    @property
    def clients(self):
        return self.client

    @classmethod
    def redi(cls, *args, **kwords):
        """ @return Redis instance"""
        self = cls()
        return self.clients

redisC = RedisClient.redi