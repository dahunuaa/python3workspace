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

class LikelistHandler(MultiStandardHandler,TokenHandler):
    _model = "like.LikeModel"
    enable_methods = ["get"]

    def _get(self):
        user_id = self.get_argument("user_id")
        res = self.model.like_list(user_id)
        self.result["data"]["like_coll"]=res[0]
        self.result["data"]["buss_like_detail"]=res[1]
        self.result["data"]["guide_like_detail"]=res[2]
        self.result["data"]["gather_like_detail"]=res[3]


handlers = [
    (r"/alter",LikeHandler,get_provider("like")),
    (r"/list",LikelistHandler,get_provider("like")),
    (r"",LikeHandler,get_provider("like"))
]
