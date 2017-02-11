# -*- coding:utf-8 -*-

from baosteel100.apps.base.handler import TokenHandler,SingleStandardHanler,MultiStandardHandler
from baosteel100.libs.loglib import get_logger
from baosteel100.libs.oauthlib import get_provider

logger = get_logger("debug")

class FeedbackListHandler(MultiStandardHandler,TokenHandler):
    _model = "feedback.FeedbackModel"
    enable_methods = ['post','get']

class FeedbackHandler(SingleStandardHanler,TokenHandler):
    _model = "feedback.FeedbackModel"
    enable_methods = ['get','delete']

handlers = [
    (r"",FeedbackListHandler,get_provider("feedback")),
    (r"/(.*)",FeedbackHandler,get_provider("feedback_admin"))
]