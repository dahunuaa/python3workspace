# -*- coding:utf-8 -*-

from baosteel100.apps.base.handler import MultiStandardHandler,SingleStandardHanler

class FamilystoryListHandler(MultiStandardHandler):
    _model = "familystory.FamilystoryModel"
    enable_methods = ["get","post"]
    private = False

class FamilystoryHandler(SingleStandardHanler):
    _model = "familystory.FamilystoryModel"
    enable_methods = ["delete","get"]
    private=False

handlers =[
    (r"",FamilystoryListHandler),
    (r"/(.*)",FamilystoryHandler)
]
