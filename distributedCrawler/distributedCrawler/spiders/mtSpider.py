#/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
from distributedCrawler.scrapy_redis.spiders import RedisSpider
import time
import re
from scrapy.http import Request, Response, TextResponse
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from datetime import datetime
from ..items import MtCrawlerItem
from ..utils import randList, regex
from ..sett import setting, Settings
from urllib.parse import urljoin
from functools import partial
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class CartSpider(RedisSpider):
    sett = Settings.copy(setting)
    name = "mtcrawler"
    start_urls = sett['LOGINURL']

    def __init__(self):
        self.user_agent = randList(self.sett['USERAGENTS'])
        self.headers = {'Host': 'bj.meituan.com', 'User-Agent': self.user_agent}

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, headers=self.headers, callback=self.parse_onepage)

    def parse_onepage(self, response):
        """ next_page and some entrance url with some messages """

        pageCount = response.xpath('//ul[@class="pagination clear"]/li[7]')
        for i in range(2, pageCount):
            url = urljoin(response.url, 'pn{}/'.format(i))
            headers = self.headers
            headers['Referer'] = 'http://bj.meituan.com/meishi/sales/pn{}/'.format(i-1)
            time.sleep(2) # no need to be so fast because onePage consumes much time or there will be much urls in queue
            yield Request(url, headers=headers)

        # the whole information of one page
        PoiLists = '(?<="poiInfos":\[)(.+?)(?=\]},)'
        PoiListsObj = re.compile(PoiLists)
        poList = re.findall(PoiListsObj, response.text)
        info = poList[0]

        # In this page, there are part of Items
        itemloader = ItemLoader(item=MtCrawlerItem())

        li_item = ["id", "title", "score", "addr", "comnum", "price"]
        item_name = ["proId", "title", "avgScore", "address", "allCommentNum", "avgPrice"]

        poiInfos = list(zip(*[regex(x, info) for x in li_item])) # [(), ()...]

        for val in poiInfos:
            for i in range(len(val)):
                itemloader.add_value(item_name[i], val[i])

        # id for the entrance url
        for id in regex('id', info):
            url = 'http://www.meituan.com/meishi/' + '{}/'.format(id)
            headers = self.headers
            yield Request(url, callback=self.parse_item, headers=headers)
    
    def parse_item(self, response):
        """ parse the details such as the number of comments etc """
        text = response.text
        detailInfo = '(?<="detailInfo":{)(.+)(?=(},"photos"))'
        detailInfoObj = re.compile(detailInfo)
        detailInfo = re.findall(detailInfoObj, text)
        info = detailInfo[0][0] # [('')] -> str

        # parse the item in detailInfo
        itemloader = ItemLoader(item=MtCrawlerItem())
        p_regex = partial(regex, source=info)

        li_item = ['phone', 'openTime', 'extraInfos', 'longitude', 'brandId', 'brandName']
        
        for name in li_item:
            itemloader.add_value(name, *p_regex(name)) # regex() -> list. so unpack list -> str

        """
        # TODO:查询评论
        id = re.findall('\d+', response.url)[0]
        # Ajax请求url如下。offset为页码，tag为对应不同标签的评价内容。其余固定。
        url = 'http://www.meituan.com/meishi/api/poi/getMerchantComment?'
        'id=36235&userId=&offset=10&pageSize=10&sortType=1&tag=%E4%B8%8A%E8%8F%9C%E5%BF%AB'
        formdata = {
            'id': id,
            'userId': '',
            'offset': '...',
            'pageSize': 10,
            'sortType': 1,
            'tag': '...'
        }
        """
