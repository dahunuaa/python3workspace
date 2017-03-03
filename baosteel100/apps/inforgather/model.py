# -*- coding:utf-8 -*-

import baosteel100.apps.base.model as model
from baosteel100.libs.datatypelib import *
import baosteel100.apps.user.model as user_model

class InforgatherModel(model.StandCURDModel):
    _coll_name = "inforgather"
    _columns = [
        ("gather_title",StrDT(required=True)),
        ("gather_address",StrDT(required=True)),
        ("gather_area", StrDT(required=True)),
        ("gather_oilfield", StrDT(required=True)),
        ("gather_text", StrDT(required=True)),
        ("filename",StrDT()),
        ("filepath", StrDT()),
    ]

    def __init__(self):
        self.user_coll = model.BaseModel.get_model("user.UserModel").get_coll()
        super(InforgatherModel, self).__init__()

    def before_create(self,object):
        user =self.user_coll.find_one({"_id":utils.create_objectid(object['add_user_id'])})
        object['add_user_name'] = user['name']
        self.coll.save(object)
        return object

    def after_create(self,object):
        msgunread_coll = model.BaseModel.get_model("msgunread.MsgunreadModel").get_coll()
        _msgunread = msgunread_coll.find()
        for i in _msgunread:
            i["gather_unread"].append(utils.objectid_str(object['_id']))
            msgunread_coll.save(i)
        return object

    def after_delete(self,object):
        msg_id = utils.objectid_str(object["_id"])
        msgunread_coll = model.BaseModel.get_model("msgunread.MsgunreadModel").get_coll()
        _msgunread = msgunread_coll.find()
        for i in _msgunread:
            if msg_id in i["gather_unread"]:
                i["gather_unread"].remove(msg_id)
                msgunread_coll.save(i)
        return object

    def unread_msg(self):
        user_mobile = user_model.UserModel.get_user_mobile_by_token(self._arguments["access_token"])
        msgunread_coll = model.BaseModel.get_model("msgunread.MsgunreadModel").get_coll()
        msgunread = msgunread_coll.find_one({"user_id":user_mobile["mobile"]})
        return msgunread

    def classify(self):
        dongbei_count=self.coll.find({"gather_area":"东北"}).count()
        xinan_count=self.coll.find({"gather_area":"西南"}).count()
        zhonghaiyu_count=self.coll.find({"gather_area":"中海油"}).count()
        huabei_count=self.coll.find({"gather_area":"华北"}).count()
        huazhong_count=self.coll.find({"gather_area":"华中"}).count()
        huadong_count=self.coll.find({"gather_area":"华东"}).count()
        xinjiang_count=self.coll.find({"gather_area":"新疆"}).count()
        result = {"dongbei":dongbei_count,"xinan":xinan_count,"zhonghaiyou":zhonghaiyu_count,
                 "huabei": huabei_count,"huazhong":huazhong_count,"huadong":huadong_count,"xinjiang":xinjiang_count}
        return result







