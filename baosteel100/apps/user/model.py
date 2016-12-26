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
        ("permission",StrDT(default="normal")),
        ("email",StrDT()),
        ("login_time",DatetimeDT(default=utils.get_now())),
        ("scope",StrDT())
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
                "password": "3e50b4886e092bceaba34e449e6d8337",
                "email": None,
                "login_name": "Admin",
                "login_time": utils.get_now(),
                "role": [

                ],
                "add_time": utils.get_now(),
                "id_card": None,
                "name": "Admin",
                "scope": "superuser"
            }
            self.coll.save(user)
            self._oauth2_register(utils.objectid_str(user['_id']),'3e50b4886e092bceaba34e449e6d8337')

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



    def login(self,username,password,system):
        if username is None or password is None:
            raise ValueError(u"用户或密码为空")
        user = self.coll.find_one({"name":username,"password":utils.generate_password(password,username),"system":system,"enable_flag":1})
        if user is None:
            raise ValueError(u"用户名或密码错误")
        user['login_time']=utils.get_now()
        self.coll.save(user)
        user['auth'] = self.get_user_info(utils.objectid_str(user['_id']))['scope']
        scope = self.get_user_info(utils.objectid_str(user['_id']))['scope']['scope']
        user['token'] = self.get_oauth2_token(utils.objectid_str(user['_id']), scope)
        suffixs = ""
        pattern = re.compile(r'@\w+$')
        match = pattern.search(user['login_name'])
        if match:
            suffixs = match.group()

        user['suffix'] = suffixs
        del user['password']
        return utils.dump(user)

    def get_user_info(self, user_id):
        user = self.get_one(user_id)
        scope = self.get_scope(user_id)
        if scope is not None:
            user['scope'] = scope
        else:
            res = {"value": user['scope'], "scope":user['scope'],"expired_time": None, "redirect_url": self.get_default_redirect_url(),
                   "address": {}}
            user['scope'] = res
        del user['password']
        return utils.dump(user)

    def get_scope(self, user_id):
        auth_model = model.BaseModel.get_model("auth.AuthModel")
        try:
            auth = auth_model.get_scopes(user_id)
            admin_url = auth.get("admin_url", self.get_default_admin_url())
            if type(admin_url) == str:
                admin_url = json.loads(admin_url)

            res = {"value": auth['bank_account_name'],
                   "scope":auth['scopes'],
                   "expired_time": auth['expires_at'],
                   "redirect_url": auth.get("redirect_url", self.get_default_redirect_url()),
                   "address": {
                       "province": auth.get("office_province", ""),
                       "city": auth.get("office_city", ""),
                       "area": auth.get("office_area", ""),
                       "detail_address": auth.get("office_detail_address", ""),
                       "address": auth.get("address", ""),
                   },
                   "admin_url": admin_url
                   }
            return utils.dump(res)
        except Exception as e:
            return None

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

    def changepsw(self,username,newpsw):
        if username is None or newpsw is None:
            raise ValueError(u"用户名或密码为空")
        user = self.coll.find_one({"name":username})
        if not user:
            raise ValueError(u"无该用户")
        user['psw'] = utils.generate_password(newpsw,username)
        self.coll.save(user)
        oauth = self.oauth_coll.find_one({"identifier":utils.objectid_str(user['_id'])})
        if oauth is None:
            raise ValueError(u"认证修改失败")
        oauth['secret']=utils.generate_password(newpsw,username)
        self.oauth_coll.save(oauth)







