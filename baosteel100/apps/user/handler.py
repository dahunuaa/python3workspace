# -*- coding:utf-8 -*-

from baosteel100.apps.base.handler import APIHandler,TokenHandler,SingleStandardHanler,MultiStandardHandler
from baosteel100.libs.loglib import get_logger
from baosteel100.libs.oauthlib import get_provider

logger = get_logger("debug")

class UserRegisterHandler(MultiStandardHandler):
    _model = "user.UserModel"
    enable_methods = ['post']

    def _post(self):
        res = self.model.new()
        self.result["data"]=res

class UserLoginHandler(MultiStandardHandler):
    _model = "user.UserModel"
    enable_methods = ['post']

    def _post(self):
        mobile = self.get_argument('mobile',None)
        password = self.get_argument('password',None)
        if mobile is None or password is None:
            raise ValueError(u"用户名或密码为空")
        res = self.model.login(mobile,password)
        self.result['data']=res

class UserPswResetHandler(MultiStandardHandler):
    _model = "user.UserModel"
    enable_methods = ['post']

    def _post(self):
        mobile = self.get_argument("mobile",None)
        oldpsw = self.get_argument("oldpsw",None)
        newpsw = self.get_argument("newpsw",None)
        if mobile is None or newpsw  is None:
            raise ValueError(u"手机号或密码为空")
        res = self.model.changepsw(mobile,oldpsw,newpsw)
        self.result['data'] = res


class UserListHandler(MultiStandardHandler,TokenHandler):
    _model = "user.UserModel"
    enable_methods = ['get','post','put','delete']


class UserHandler(SingleStandardHanler,TokenHandler):
    _model = "user.UserModel"
    enable_methods = ['get']


handlers = [
    (r"/register",UserRegisterHandler),
    (r"/login",UserLoginHandler),
    (r'/psw/reset',UserPswResetHandler),
    (r"",UserListHandler,get_provider("user_admin")),
    (r"/(.*)",UserHandler,get_provider("user_admin"))
]