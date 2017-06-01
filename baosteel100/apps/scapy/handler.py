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

class GetWeatherXuanhuaHandler(APIHandler):
    _model = "scapy.ScapyModel"
    def get(self):
        weather_xuanhua  = get_weather()
        self.result["data"]=weather_xuanhua
        self.finish(self.result)

class GetCctvNewsHandler(APIHandler):
    _model = "scapy.ScapyModel"
    def get(self):
        cctv_mainnews  = get_cctv_mainnews()
        self.result["data"]=cctv_mainnews
        self.finish(self.result)

class GetYangshengHandler(APIHandler):
    _model = "scapy.ScapyModel"
    def get(self):
        yangsheng_news  = get_yangsheng_news()
        self.result["data"]=yangsheng_news
        self.finish(self.result)

class GetJianfeiHandler(APIHandler):
    _model = "scapy.ScapyModel"
    def get(self):
        jianfei_news  = get_jianfei_news()
        self.result["data"]=jianfei_news
        self.finish(self.result)

class GetChufangHandler(APIHandler):
    _model = "scapy.ScapyModel"
    def get(self):
        chufang_news  = get_chufang_news()
        self.result["data"]=chufang_news
        self.finish(self.result)

class GetDetailNewsHandler(APIHandler):
    _model = "scapy.ScapyModel"
    def get(self):
        url=self.get_argument("url")
        result = get_detail_news(url)
        # self.result["data"]={"text_news":result[0],"img_news":result[1]}
        self.result["data"]=result
        self.finish(self.result)

handlers=[
    (r"/baowu/news",GetBaoWuNewsHandler),
    (r"/baowu/price",GetBaoWuPriceHandler),
    (r"/shougang/news",GetShouGangeHandler),
    (r"/weather",GetWeatherXuanhuaHandler),
    (r"/cctv_news",GetCctvNewsHandler),
    (r"/yangsheng_news",GetYangshengHandler),
    (r"/jianfei_news",GetJianfeiHandler),
    (r"/chufang_news",GetChufangHandler),
    (r"/detail_news",GetDetailNewsHandler),
]