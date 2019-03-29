# -*- coding:utf-8 -*-


from .redisclient import redisC
from .mongodb import mongo_connection

__all__ = ['redisC', 'mongo_connection']