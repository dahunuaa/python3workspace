# -*- coding:utf-8 -*-

from baosteel100.apps.base.handler import MultiStandardHandler,SingleStandardHanler,TokenHandler
from baosteel100.libs.oauthlib import get_provider
from baosteel100.libs.loglib import get_logger

logger = get_logger("debug")

class InforguideListHandler(MultiStandardHandler,TokenHandler):
    _model = "inforguide.InforguideModel"
    enable_methods = ["post","get"]
    private = False

class InforguideHandler(SingleStandardHanler,TokenHandler):
    _model = "inforguide.InforguideModel"
    enable_methods = ["get","put","delete"]

handlers = [
    (r"",InforguideListHandler,get_provider("inforguide")),
    (r"/(.*)",InforguideHandler,get_provider("inforguide"))
]

