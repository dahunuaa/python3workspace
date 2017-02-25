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


handlers = [
    (r"",InforgatherListHandler,get_provider("inforgather")),
    (r"/(.*)",InforgatherHandler,get_provider("inforgather"))
]

