# -*- coding:utf-8 -*-
import baosteel100.apps.base.model as model
from baosteel100.libs.datatypelib import *
import oauth2
import re
from baosteel100.libs.oauthlib import save_token
import json

class UserModel(model.StandCURDModel):
    _coll_name = "user"
    _columns = [
        ("login_name",StrDT()),
        ("mobile",StrDT()),
        ("password",StrDT()),
        ("role",ListDT()),
        ("name",StrDT()),
        ("email",StrDT()),
        ("login_time",DatetimeDT(default=utils.get_now())),
        ("scope",StrDT(default="normal"))
    ]

    _default_redirect_url = None

    def __init__(self):
        self.oauth_coll = model.BaseModel.get_model("oauth.OauthClientsModel").get_coll()
        super(UserModel,self).__init__()

    def init(self):
        count = self.coll.find({}).count()
        if count ==0:
            user={
                "enable_flag": 1,
                "mobile": "admin",
                "password": "e10adc3949ba59abbe56e057f20f883e",
                "email": None,
                "login_name": "admin",
                "login_time": utils.get_now(),
                "role": [

                ],
                "add_time": utils.get_now(),
                "id_card": None,
                "name": "admin",
                "scope": "admin"
            }
            self.coll.save(user)
            self._oauth2_register(utils.objectid_str(user['_id']),'e10adc3949ba59abbe56e057f20f883e')

    #生成用户
    def new(self):
        user = None
        mobile = self.get_argument("mobile")
        password = utils.generate_password(self.get_argument("password"),mobile)

        if mobile is None or password is None:
            raise ValueError(u"用户资料不完全")

        if mobile is not None:
            user = self.coll.find_one({"mobile":mobile,"enable_flag":1})
            if user is not None:
                raise ValueError(u"该手机号已经注册")
            else:
                self._arguments['login_name'] = u"%s****%s"%(mobile[0:3],mobile[-3:])
                user=self._create()
        if user is None:
            raise ValueError(u"用户创建失败")
        return utils.dump(user)

    def _create(self,user=None):

        if user is None:
            user = self._new()

        self.coll.save(user)
        self._arguments['_id'] = utils.objectid_str(user['_id'])
        self._oauth2_register(utils.objectid_str(user['_id']),
                              utils.generate_password(self.get_argument("password",""),self.get_argument("name")))
        user['token'] = self.get_oauth2_token(utils.objectid_str(user['_id']),self.get_argument("scope"))
        del user['password']
        return utils.dump(user)

    def _new(self):
        user = super(UserModel,self)._new()
        if user['name'] =='':
            user['name'] = user['mobile']
        user['password'] = utils.generate_password(user['password'],user['name'])
        return user

    def get_oauth2_token(self,client_id,scopes):
        return save_token(client_id,oauth2.grant.ClientCredentialsGrant.grant_type, client_id, scopes=[scopes])


    # 注册用户进oauth2
    def _oauth2_register(self,id = None, password = None):
        if id is None and password is None:
            id = self.get_argument('id')
            password = self.get_argument("password","")
        oauth_user = self.oauth_coll.find_one({'identifier':id})
        if oauth_user is None:
            self.oauth_coll.save({'identifier':id,
                                  'secret':password,
                                  'redirect_uris':[],
                                  'authorized_grants':[oauth2.grant.ClientCredentialsGrant.grant_type]})



    def login(self,username,password):
        if username is None or password is None:
            raise ValueError(u"用户或密码为空")
        a=utils.generate_password(password,username)
        user = self.coll.find_one({"name":username,"password":utils.generate_password(password,username),"enable_flag":1})
        if user is None:
            raise ValueError(u"用户名或密码错误")
        user['login_time']=utils.get_now()
        self.coll.save(user)
        scope = user['scope']
        user['token'] = self.get_oauth2_token(utils.objectid_str(user['_id']), scope)
        suffixs = ""
        pattern = re.compile(r'@\w+$')
        match = pattern.search(user['login_name'])
        if match:
            suffixs = match.group()

        user['suffix'] = suffixs
        del user['password']
        return utils.dump(user)

    #获取角色
    def _get_role(self):
        role_list = ['normal','admin']
        role = self.get_argument("role","")
        _roles = role.split(',')
        roles = []
        for r in _roles:
            if r in role_list:
                roles.append(r)
        return roles

    def delete(self):
        object = self._get_from_id(update = True)
        object = self.before_delete(object)
        object["enable_flag"] = 0
        object["delete_user_id"] = self._arguments["delete_user_id"]
        self.coll.save(object)
        self.after_delete(object)
        return utils.dump(object)

    def changepsw(self,username,oldpsw,newpsw):
        if username is None or oldpsw is None or newpsw is None:
            raise ValueError(u"用户名或密码为空")
        user = self.coll.find_one({"name":username})
        if not user:
            raise ValueError(u"无该用户")
        oldpsw_check = utils.generate_password(oldpsw,username)
        if oldpsw_check != user['password']:
            raise ValueError(u"原密码输入不正确")
        user['password'] = utils.generate_password(newpsw,username)
        self.coll.save(user)
        oauth = self.oauth_coll.find_one({"identifier":utils.objectid_str(user['_id'])})
        if oauth is None:
            raise ValueError(u"认证修改失败")
        oauth['secret']=utils.generate_password(newpsw,username)
        self.oauth_coll.save(oauth)







