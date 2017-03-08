# -*- coding:utf-8 -*-
from baosteel100.apps.base.handler import TokenHandler,MultiStandardHandler,SingleStandardHanler
from baosteel100.libs.oauthlib import get_provider

class SignListHandler(MultiStandardHandler,TokenHandler):
    _model = "sign.SignModel"
    enable_methods = ["get","post"]
    private = False

class SignHandler(SingleStandardHanler,TokenHandler):
    _model = "sign.SignModel"
    enable_methods = ["get","delete"]


handlers=[
    (r"",SignListHandler,get_provider("sign")),
    (r"/(.*)",SignHandler,get_provider("sign")),
]