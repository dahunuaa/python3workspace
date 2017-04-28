# -*- coding:utf-8 -*-

from baosteel100.apps.base.handler import MultiStandardHandler,SingleStandardHanler,TokenHandler
from baosteel100.libs.oauthlib import get_provider
from baosteel100.libs.loglib import get_logger

logger = get_logger("debug")

class InforgatherListHandler(MultiStandardHandler,TokenHandler):
    _model = "inforgather.InforgatherModel"
    enable_methods = ["post","get"]
    private = False

class InforgatherHandler(SingleStandardHanler,TokenHandler):
    _model = "inforgather.InforgatherModel"
    enable_methods = ["get","put","delete"]
    private = False

class InforgatherClassifyHandler(MultiStandardHandler,TokenHandler):
    _model = "inforgather.InforgatherModel"
    enable_methods = ["get"]
    private = False

    def get(self):
        self.result["data"] = self.model.classify()
        self.finish(self.result)

class KeywordRankHandler(MultiStandardHandler,TokenHandler):
    _model = "inforgather.InforgatherModel"
    enable_methods = ["get"]
    private = False

    def _get(self):
        result = self.model.key_words_rank()
        self.result["data"]=result

handlers = [
    (r"",InforgatherListHandler,get_provider("inforgather")),
    (r"/classify",InforgatherClassifyHandler,get_provider("inforgather")),
    (r"/keywordrank",KeywordRankHandler,get_provider("inforgather")),
    (r"/(.*)",InforgatherHandler,get_provider("inforgather"))
]

