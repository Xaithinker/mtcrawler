# -*- coding:utf-8 -*-

import threading
import requests 

def testnet(ip):

    proxyli = [{'http': 'http://' + ip + '/'}, {'https': 'http://' + ip + '/'}]

    def func(proxy):
        try:
            r = requests.get('http://httpbin.org/ip', proxies=proxy)
            if r.status_code == 200:
                return True
        except:
            return False

    for p in proxyli:
        t = threading.Thread(target=func, args=(p))
        t.start()
        t.join()

    return True

testIP = testnet