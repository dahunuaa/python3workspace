# -*- coding:utf-8 -*-
import baosteel100.apps.base.model as model
from baosteel100.libs.datatypelib import *
import baosteel100.libs.utils as utils

class NoticereadModel(model.StandCURDModel):
    _coll_name = "noticeread"
    _columns = [
        ("user_id",StrDT(required=True)),
        ("unread_msg",ListDT())
    ]

    def __init__(self):
        self.user_coll = model.BaseModel.get_model("user.UserModel").get_coll()
        super(NoticereadModel,self).__init__()

    def init(self):
        user_coll = self.user_coll.find()
        for i in user_coll:
            _mobile = i['mobile']
            _new_notice=self.coll.find_one({"user_id":_mobile})
            if not _new_notice:
                notice_read = {
                    "user_id":_mobile,
                    "unread_msg":[],
                }
                self.coll.save(notice_read)



    def minus(self,user_id,msg_id):
        notice_coll = model.BaseModel.get_model("notice.NoticeModel").get_coll()
        _msg = notice_coll.find_one({"_id": utils.create_objectid(msg_id)})
        if not _msg:
            raise ValueError(u"没有该消息")
        _noticeread = self.coll.find_one({"user_id": user_id})
        if msg_id in _noticeread["unread_msg"]:
            _noticeread["unread_msg"].remove(msg_id)
        else:
            raise ValueError(u"该用户未读消息中无该消息")
        self.coll.save(_noticeread)
        return utils.dump(_noticeread)








