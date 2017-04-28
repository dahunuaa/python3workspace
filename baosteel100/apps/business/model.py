# -*- coding:utf-8 -*-
import baosteel100.apps.base.model as model
from baosteel100.libs.datatypelib import *
import baosteel100.apps.user.model as user_model


class BusinessModel(model.StandCURDModel):
    _coll_name = "business"
    _columns = [
        ("business_staff",StrDT(required=True)),#出差人员
        ("business_num",StrDT(required=True)),
        ("business_place",StrDT(required=True)),
        ("business_reason",StrDT(required=True)),
        ("begin_time",StrDT(required=True)),
        ("end_time",StrDT(required=True)),
        ("remark",StrDT())
    ]

    def __init__(self):
        self.user_coll = model.BaseModel.get_model("user.UserModel").get_coll()
        super(BusinessModel, self).__init__()#继承BusinessModel超类的__init__为了继续使用其超类的功能

    def before_create(self,object):
        # object['staff_num']=len((object['business_staff']))
        user =self.user_coll.find_one({"_id":utils.create_objectid(object['add_user_id'])})
        object['add_user_name'] = user['name']
        self.coll.save(object)
        return object

    def after_create(self,object):
        msgunread_coll = model.BaseModel.get_model("msgunread.MsgunreadModel").get_coll()
        _msgunread = msgunread_coll.find()
        for i in _msgunread:
            i["buss_unread"].append(utils.objectid_str(object['_id']))
            msgunread_coll.save(i)
        return object

    def after_delete(self,object):
        msg_id = utils.objectid_str(object["_id"])
        msgunread_coll = model.BaseModel.get_model("msgunread.MsgunreadModel").get_coll()
        _msgunread = msgunread_coll.find()
        for i in _msgunread:
            if msg_id in i["buss_unread"]:
                i["buss_unread"].remove(msg_id)
                msgunread_coll.save(i)
        return object

    def unread_msg(self):
        user_mobile = user_model.UserModel.get_user_mobile_by_token(self._arguments["access_token"])
        msgunread_coll = model.BaseModel.get_model("msgunread.MsgunreadModel").get_coll()
        msgunread = msgunread_coll.find_one({"user_id":user_mobile["mobile"]})
        return msgunread

    def users_buss_rank(self):
        result=utils.dump(self.coll.aggregate([{"$group":{"_id":"$add_user_id",
                                                          "name":{"$last":"$add_user_name"},#添加额外字段
                                                          "num":{"$sum":1}}},
                                               ]))
        return result

    def oilfield_buss_rank(self):
        result=utils.dump(self.coll.aggregate([{"$group":{"_id":"$business_place",
                                                          "num":{"$sum":1},
                                                          }},
                                               {"$sort":{"num":-1},}
                                               ]))
        return result








