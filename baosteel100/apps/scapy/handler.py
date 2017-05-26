#-*- coding:utf-8 -*-
from baosteel100.apps.base.handler import APIHandler
from baosteel100.apps.scapy.libs import *

class GetBaoWuNewsHandler(APIHandler):
    _model = "scapy.ScapyModel"

    def get(self):
        news = get_pretty_news()
        self.result["data"]=news
        self.finish(self.result)

class GetBaoWuPriceHandler(APIHandler):
    _model = "scapy.ScapyModel"

    def get(self):
        data = get_shareprice()
        company = get_pricedata()
        table = get_pricetable(data, company)
        self.result["data"]=table
        self.finish(self.result)

class GetShouGangeHandler(APIHandler):
    _model = "scapy.ScapyModel"

    def get(self):
        news=get_detail_shougang_news()
        self.result["data"]=news
        self.finish(self.result)

handlers=[
    (r"/baowu/news",GetBaoWuNewsHandler),
    (r"/baowu/price",GetBaoWuPriceHandler),
    (r"/shougang/news",GetShouGangeHandler),
]