# -*- coding:utf-8 -*-
from baosteel100.apps.base.handler import TokenHandler,SingleStandardHanler,MultiStandardHandler
from baosteel100.libs.loglib import get_logger
from baosteel100.libs.oauthlib import get_provider

logger = get_logger("debug")

class BusinessListHandler(MultiStandardHandler,TokenHandler):
    _model = "business.BusinessModel"
    enable_methods = ["post","get"]

class BusinessHandler(SingleStandardHanler,TokenHandler):
    _model = "business.BusinessModel"
    enable_methods = ["get","put"]

handlers = [
    (r"",BusinessListHandler,get_provider("business")),
    (r"/(.*)",BusinessHandler,get_provider("business"))
]