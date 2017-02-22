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
        noticeread = self.user_coll.find()
        for i in noticeread:
            _mobile = i['mobile']
            notice_read = {
                "user_id":_mobile,
                "unread_msg":[],
            }
            self.coll.save(notice_read)




