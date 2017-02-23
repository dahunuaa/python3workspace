# -*- coding:utf-8 -*-

import baosteel100.apps.base.model as model
from baosteel100.libs.datatypelib import *
import  baosteel100.libs.utils as utils

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

    def after_create(self,object):
        noticeread_coll = model.BaseModel.get_model("noticeread.NoticereadModel").get_coll()
        _noticeread = noticeread_coll.find()
        for i in _noticeread:
            i["unread_msg"].append(utils.objectid_str(object['_id']))
            noticeread_coll.save(i)
        return object

    def after_delete(self,object):
        msg_id = utils.objectid_str(object["_id"])
        noticeread_coll = model.BaseModel.get_model("noticeread.NoticereadModel").get_coll()
        _noticeread = noticeread_coll.find()
        for i in _noticeread:
            if msg_id in i["unread_msg"]:
                i["unread_msg"].remove(msg_id)
                noticeread_coll.save(i)
        return object

