# -*- coding:utf-8 -*-
import baosteel100.apps.base.model as model
from baosteel100.libs.datatypelib import *

class SignModel(model.StandCURDModel):
    _coll_name = "sign"
    _columns=[
        ("addresses",StrDT()),
        ("address",DictDT()),
        ("lat",StrDT()),
        ("long", StrDT()),
    ]

    def __init__(self):
        self.user_coll = model.BaseModel.get_model("user.UserModel").get_coll()
        super(SignModel, self).__init__()

    def before_create(self,object):
        user =self.user_coll.find_one({"_id":utils.create_objectid(object['add_user_id'])})
        object['add_user_name'] = user['name']
        object["add_user_jobno"]=user["job_no"]
        self.coll.save(object)
        return object

