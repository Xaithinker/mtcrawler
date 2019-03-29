# -*- coding:utf-8 -*-

"""
西刺代理

"""
import requests
from ..dataBase import redisC, mongo_connection # no need mongo  now
from ..utils import randList
from ..sett import setting, Settings
from lxml import etree
from urllib.parse import urlparse, urljoin
import time
from datetime import datetime
import random

rediss = redisC() # redis instance
del redisC

class Proxy(object):


    session = requests.Session()
    sett = Settings.copy(setting)

    url_count = None
    #__next_url = None
    def __init__(self):
        self.user_agent = randList(self.sett['USERAGENTS'])
        self.headers = {'Host':'www.xicidaili.com', 'Referer':'https://www.xicidaili.com/articles/', 'User-Agent':self.user_agent, 'If-None-Match': 'W/"44be6b7e031c0e22db730f33820223b3"'}
        self.proxy = {
                    "http": 'socks5://127.0.0.1:9150',
                    "https": 'socks5://127.0.0.1:9150',
                    }

    def crawl(self):
        while True:
            try:
                url_count = 3638
                num = random.randint(1, url_count)
                url = 'https://www.xicidaili.com/nn/' + str(num)
                with self.session.get(url, headers=self.headers, hooks=dict(response=Proxy.parseIP), proxies=self.proxy, allow_redirects=False) as r:
                    if r.status_code == 200:
                        time.sleep(60) # about one minute to refresh the list
                        rediss.ltrim('ip', 1, 0)
                        self.crawl()
                        print('Successfully')
            except Exception as e:
                print(f'Exception occurs: {e}')
                self.crawl()

    @staticmethod
    def parseIP(r, *args, **kwargs):
        root_node = etree.HTML(r.content.decode(r.encoding))

        # IP:PORT
        ip_list = root_node.xpath(r"//td[2]/text()")
        port = root_node.xpath(r"//td[3]/text()")

        assert len(ip_list) == len(port)

        ip = (f'{x}:{y}' for x, y in zip(ip_list, port))
        for val in ip:
            #print(val)
            rediss.lpush('ip', val)