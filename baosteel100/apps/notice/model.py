# -*- coding:utf-8 -*-

import baosteel100.apps.base.model as model
from baosteel100.libs.datatypelib import *

class NoticeModel(model.StandCURDModel):
    _coll_name = "notice"
    _columns=[
        ("notice_title",StrDT(required=True)),
        ("notice_text",StrDT(required=True))
    ]


    def __init__(self):
        self.user_coll = model.BaseModel.get_model("user.UserModel").get_coll()
        super(NoticeModel, self).__init__()


    def before_create(self,object):
        user = self.user_coll.find_one({"_id": utils.create_objectid(object['add_user_id'])})
        object['add_user_name'] = user['name']
        self.coll.save(object)
        return object