# -*- coding:utf-8 -*-
from baosteel100.apps.base.handler import TokenHandler,MultiStandardHandler,SingleStandardHanler
from baosteel100.libs.oauthlib import get_provider

class NoticereadListHandler(TokenHandler,MultiStandardHandler):
    _model = "noticeread.NoticereadModel"
    enable_methods = ['post','get']
    private = False

class NoticeHandler(SingleStandardHanler,TokenHandler):
    _model = "notice.NoticereadModel"
    enable_methods = ['get','put','delete']
    private = False

handlers = [
    (r"",NoticereadListHandler,get_provider("noticeread")),
    (r"/(.*)",NoticeHandler,get_provider("noticeread"))
]
