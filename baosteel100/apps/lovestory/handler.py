# -*- coding:utf-8 -*-

from baosteel100.apps.base.handler import MultiStandardHandler,SingleStandardHanler

class LovestoryListHandler(MultiStandardHandler):
    _model = "lovestory.LovestoryModel"
    enable_methods = ["get","post"]
    private = False

class LovestoryHandler(SingleStandardHanler):
    _model = "lovestory.LovestoryModel"
    enable_methods = ["delete","get"]
    private=False

handlers =[
    (r"",LovestoryListHandler),
    (r"/(.*)",LovestoryHandler)
]
