# -*- coding:utf-8 -*-

from baosteel100.apps.base.handler import TokenHandler,SingleStandardHanler,MultiStandardHandler
from baosteel100.libs.oauthlib import get_provider
from baosteel100.libs.loglib import get_logger

logger = get_logger("debug")
class NoticeListHandler(TokenHandler,MultiStandardHandler):
    _model = "notice.NoticeModel"
    enable_methods = ["post","get"]
    private = False



class Noticehandler(TokenHandler,SingleStandardHanler):
    _model = "notice.NoticeModel"
    enable_methods = ["get","put","delete"]
    private = False

handlers = [
    (r"",NoticeListHandler,get_provider("notice")),
    (r"/(.*)",Noticehandler,get_provider("notice"))
]
