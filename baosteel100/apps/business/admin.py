# -*- coding:utf-8 -*-
from baosteel100.apps.base.handler import TokenHandler,MultiStandardHandler,SingleStandardHanler
from baosteel100.libs.loglib import get_logger
from baosteel100.libs.oauthlib import get_provider

logger = get_logger("debug")

class AdminBusinessListHandler(MultiStandardHandler,TokenHandler):
    _model = "business.BusinessModel"
    private = False

class AdminBussinessHandler(SingleStandardHanler,TokenHandler):
    _model = "business.BusinessModel"
    private = False

handlers = [
    (r"",AdminBusinessListHandler,get_provider("business_admin")),
    (r"/(.*)",AdminBussinessHandler,get_provider("business_admin"))
]
