# -*- coding:utf-8 -*-
import baosteel100.apps.base.model as model
from baosteel100.libs.datatypelib import *

class MsgunreadModel(model.StandCURDModel):
    _coll_name = "msgunread"
    _columns = [
        ("user_id",StrDT(required=True)),
        ("buss_unread",ListDT()),
        ("gather_unread",ListDT()),
        ("guide_unread",ListDT())
    ]

    def __init__(self):
        self.user_coll = model.BaseModel.get_model("user.UserModel").get_coll()
        super(MsgunreadModel,self).__init__()#此处必须加上self

    def init(self):
        user_coll = self.user_coll.find()
        for i in user_coll:
            _mobile = i["mobile"]
            _unread = self.coll.find_one({"user_id":_mobile})
            if not  _unread:
                msgunread = {
                    "user_id":_mobile,
                    "buss_unread":[],
                    "gather_unread":[],
                    "guide_unread":[],
                }
                self.coll.save(msgunread)

    def minus(self,user_id,type,msg_id):
        _msgunread=self.coll.find_one({"user_id":user_id})
        if type=="bussiness":
            if msg_id in _msgunread["buss_unread"]:
                _msgunread["buss_unread"].remove(msg_id)
        elif type == "inforgather":
            if msg_id in _msgunread["gather_unread"]:
                _msgunread["gather_unread"].remove(msg_id)
        elif type == "inforguide":
            if msg_id in _msgunread["guide_unread"]:
                _msgunread["guide_unread"].remove(msg_id)
        else:
            raise ValueError(u"类型错误")
        self.coll.save(_msgunread)
        return utils.dump(_msgunread)


