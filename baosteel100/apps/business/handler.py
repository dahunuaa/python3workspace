# -*- coding:utf-8 -*-
from baosteel100.apps.base.handler import TokenHandler,SingleStandardHanler,MultiStandardHandler
from baosteel100.libs.loglib import get_logger
from baosteel100.libs.oauthlib import get_provider

logger = get_logger("debug")

class BusinessListHandler(MultiStandardHandler,TokenHandler):
    _model = "business.BusinessModel"
    enable_methods = ["post","get"]
    private = False;#默认为true 只能查看自己的订单


class BusinessHandler(SingleStandardHanler,TokenHandler):
    _model = "business.BusinessModel"
    enable_methods = ["get","put","delete"]

class BusinessUsersRankHandler(MultiStandardHandler,TokenHandler):
    _model = "business.BusinessModel"
    enable_methods = ["get"]
    private = False
    def _get(self):
        res=self.model.users_buss_rank()
        self.result["data"]=res

class BusinessOilfieldRankHandler(MultiStandardHandler,TokenHandler):
    _model = "business.BusinessModel"
    enable_methods = ["get"]
    private = False
    def _get(self):
        res = self.model.oilfield_buss_rank()
        self.result["data"]=res

class BusinessUpdateHandler(MultiStandardHandler,TokenHandler):
    _model = "business.BusinessModel"
    enable_methods = ["get"]
    private = False
    def _get(self):
        res = self.model.update()
        self.result["data"] = res

handlers = [
    (r"",BusinessListHandler,get_provider("business")),
    (r"/usersrank",BusinessUsersRankHandler,get_provider("business")),
    (r"/oilfieldrank",BusinessOilfieldRankHandler,get_provider("business")),
    # (r"/update",BusinessUpdateHandler,get_provider("business")),
    (r"/(.*)",BusinessHandler,get_provider("business")),


]