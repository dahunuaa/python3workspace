# -*- coding:utf-8 -*-
from baosteel100.apps.base.handler import MultiStandardHandler,SingleStandardHanler,TokenHandler
from baosteel100.libs.oauthlib import get_provider

class Keywordshandler(MultiStandardHandler,TokenHandler):
    _model = "keywords.KeyWordsModel"
    enable_methods = ["post","get"]
    private=False

    def _get(self):
        res = self.model.keywords_rank()
        self.result["data"]=res
handlers=[
    (r"",Keywordshandler,get_provider("keywords"))
]