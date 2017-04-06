# -*- coding:utf-8 -*-
from baosteel100.apps.base.handler import TokenHandler,MultiStandardHandler,SingleStandardHanler
from baosteel100.libs.oauthlib import get_provider

class ReplycommentListHandler(MultiStandardHandler,TokenHandler):
    _model = "reply_comment.ReplycommentHandler"
    enable_methods = ["post","get"]
    private = False

class ReplycommentHandler(SingleStandardHanler,TokenHandler):
    _model = "reply_comment.ReplycommentHandler"
    enable_methods = ["get","delete"]
    private = False

handlers = [
    (r"",ReplycommentListHandler,get_provider("reply_comment")),
    (r"/(.*)",ReplycommentHandler,get_provider("reply_comment"))
]