# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MtCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class cartItem(scrapy.Item):

    datetime = scrapy.Field()

    # On pageInfo
    proId = scrapy.Field()
    title = scrapy.Field()
    avgScore = scrapy.Field()
    address = scrapy.Field()
    allCommentNum = scrapy.Field()
    avgPrice = scrapy.Field

    # detailInfo
    phone = scrapy.Field()
    openTime = scrapy.Field()
    extraInfos = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    brandId = scrapy.Field()
    brandName = scrapy.Field()


    # tags and comments
    tags = scrapy.Field()