# -*- coding:utf-8 -*-
from baosteel100.libs.datatypelib import *
import baosteel100.apps.base.model as model

class LikeModel(model.StandCURDModel):
    _coll_name = "like"
    _columns = [
        ("user_id",StrDT(required=True)),
        ("buss_like",ListDT()),
        ("gather_like",ListDT()),
        ("guide_like",ListDT())
    ]

    def __init__(self):
        self.user_coll = model.BaseModel.get_model("user.UserModel").get_coll()
        super(LikeModel, self).__init__()

    def init(self):
        user_coll = self.user_coll.find()
        for i in user_coll:
            _mobile = i["mobile"]
            _like = self.coll.find_one({"user_id":_mobile})
            if not  _like:
                like = {
                    "user_id":_mobile,
                    "buss_like":[],
                    "gather_like":[],
                    "guide_like":[],
                }
                self.coll.save(like)

    def alter(self,user_id,type,like_id):
        _like = self.coll.find_one({"user_id":user_id})
        if type =="bussiness":
            if like_id in _like["buss_like"]:
                _like["buss_like"].remove(like_id)
            else:
                _like["buss_like"].append(like_id)
        if type =="inforgather":
            if like_id in _like["gather_like"]:
                _like["gather_like"].remove(like_id)
            else:
                _like["gather_like"].append(like_id)
        if type =="inforguide":
            if like_id in _like["guide_like"]:
                _like["guide_like"].remove(like_id)
            else:
                _like["guide_like"].append(like_id)
        self.coll.save(_like)
        return utils.dump(_like)