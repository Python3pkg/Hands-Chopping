#!usr/bin/env python

import threading
from ..goods_spider.core import fetch_goods


class GoodsThread(threading.Thread):

    def __init__(self, lock, all_goods, keywords, web):
        threading.Thread.__init__(self)
        self.lock = lock
        self.keywords = keywords
        self.web = web
        self.all_goods = all_goods

    def run(self):
        result = fetch_goods(self.keywords, self.web)
        if result:
            self.append_data(result)

    def append_data(self, data):
        self.lock.acquire()
        self.all_goods.extend(data)
        self.lock.release()
