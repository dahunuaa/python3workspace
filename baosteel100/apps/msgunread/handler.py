# -*- coding:utf-8 -*-

from baosteel100.apps.base.handler import MultiStandardHandler,SingleStandardHanler,TokenHandler
from baosteel100.libs.oauthlib import get_provider

class MsgunreadHandler(MultiStandardHandler,TokenHandler):
    _model = "msgunread.MsgunreadModel"
    enable_methods = ["put","get"]

    def _put(self):
        user_id = self.get_argument("user_id")
        msg_type = self.get_argument("type")
        msg_id = self.get_argument("msg_id")
        res = self.model.minus(user_id,msg_type,msg_id)
        self.result['data'] =res


handlers = [
    (r"/minus",MsgunreadHandler,get_provider("msgunread")),
    (r"",MsgunreadHandler,get_provider("msgunread"))
]