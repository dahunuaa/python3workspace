# -*- coding:utf-8 -*-

import baosteel100.apps.base.model as model
import baosteel100.apps.user.model as user_model
from baosteel100.libs.datatypelib import *

class InforgatherModel(model.StandCURDModel):
    _coll_name = "inforgather"
    _columns = [
        ("gather_title",StrDT(required=True)),
        ("gather_address",StrDT(required=True)),
        ("gather_area", StrDT(required=True)),
        ("gather_oilfield", StrDT(required=True)),
        ("gather_text", StrDT(required=True)),
        ("images",ListDT()),
        ("files",ListDT())
    ]

    def before_create(self,object):
        object["add_user_name"]=user_model.UserModel.get_username_by_id(object['add_user_id'])
        self.coll.save(object)
        return object


