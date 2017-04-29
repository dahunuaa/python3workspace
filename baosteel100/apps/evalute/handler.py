# -*- coding:utf-8 -*-
from baosteel100.libs.oauthlib import get_provider
from baosteel100.apps.base.handler import MultiStandardHandler,TokenHandler,SingleStandardHanler

class EvaluteHandler(MultiStandardHandler,TokenHandler):
    _model = "evalute.EvaluteModle"
    enable_methods = ["post","get"]
    private = False

class EvaluteSingleHandler(SingleStandardHanler,TokenHandler):
    _model = "evalute.EvaluteModle"
    enable_methods = ["put","get"]
    private = False

handlers=[
    (r"",EvaluteHandler,get_provider("evalute")),
    (r"/(.*)",EvaluteSingleHandler,get_provider("evalute"))
]