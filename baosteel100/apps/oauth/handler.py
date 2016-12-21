# -*- coding:utf-8 -*-
from oauth2.web.tornado import OAuth2Handler
from baosteel100.apps.base.handler import TokenHandler,MultiStandardHandler
from baosteel100.apps.base.model import BaseModel
from baosteel100.libs.oauthlib import get_provider

class OauthHandler(MultiStandardHandler,TokenHandler):
    _model = "oauth.OauthAccessTokenHandler"
    enable_methods = ["post"]

    def _post(self):
        user_model = BaseModel.get_model("user.UserModel")
        user = user_model.get_user_infor(self.user_id)
        self.result["data"] = user

handlers = [
    (r'',OauthHandler,get_provider('normal')),
    (r'/token',OAuth2Handler,get_provider())
]