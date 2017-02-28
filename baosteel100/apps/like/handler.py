# -*- coding:utf-8 -*-
from baosteel100.apps.base.handler import MultiStandardHandler,SingleStandardHanler,TokenHandler
from baosteel100.libs.oauthlib import get_provider

class LikeHandler(MultiStandardHandler,TokenHandler):
    _model = "like.LikeModel"
    enable_methods = ["put","get"]

    def _put(self):
        user_id = self.get_argument("user_id")
        type = self.get_argument("type")
        like_id = self.get_argument("like_id")
        res = self.model.alter(user_id,type,like_id)
        self.result["data"] = res

handlers = [
    (r"/add",LikeHandler,get_provider("like")),
    (r"",LikeHandler,get_provider("file"))
]
