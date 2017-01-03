# -*- coding:utf-8 -*-
import baosteel100.apps.base.model as model
from baosteel100.libs.datatypelib import *

class BusinessModel(model.StandCURDModel):
    _coll_name = "business"
    _columns = [
        ("business_staff",ListDT(required=True)),#出差人员
        ("staff_num",IntDT()),#出差人数根据business_staff确定
        ("business_place",StrDT(required=True)),
        ("business_reason",StrDT(required=True)),
        ("begin_time",StrDT(required=True)),
        ("end_time",StrDT(required=True)),
        ("remark",StrDT())
    ]

    def __init__(self):
        self.user_coll = model.BaseModel.get_model("user.UserModel").get_coll()
        super(BusinessModel, self).__init__()

    def before_create(self,object):
        object['staff_num']=len((object['business_staff']))
        user =self.user_coll.find_one({"_id":utils.create_objectid(object['add_user_id'])})
        object['add_user_name'] = user['name']
        self.coll.save(object)
        return object

