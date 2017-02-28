# -*- coding:utf-8 -*-
from baosteel100.libs.datatypelib import *
import baosteel100.apps.base.model as model

class LikeModel(model.StandCURDModel):
    _coll_name = "like"
    _columns = [
        ("user_id",StrDT(required=True)),
        ("buss_like",ListDT()),
        ("gather_like",ListDT()),
        ("guide_like",ListDT()),
        ("buss_like_detail",ListDT()),
        ("guide_like_detail",ListDT()),
        ("gather_like_detail",ListDT())
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

    def like_list(self,user_id):
        buss_coll = model.BaseModel.get_model("business.BusinessModel").get_coll()
        guide_coll = model.BaseModel.get_model("inforguide.InforguideModel").get_coll()
        gather_coll = model.BaseModel.get_model("inforgather.InforgatherModel").get_coll()
        like_coll=self.coll.find_one({"user_id":user_id})
        guide_like_detail=[]
        buss_like_detail=[]
        gather_like_detail=[]
        for i in like_coll["guide_like"]:
            _guide=guide_coll.find_one({"_id":utils.create_objectid(i)})
            guide_like_detail.append(_guide)
        for j in like_coll["buss_like"]:
            _buss = buss_coll.find_one({"_id":utils.create_objectid(j)})
            buss_like_detail.append(_buss)
        for k in like_coll["gather_like"]:
            _gather = gather_coll.find_one({"_id":utils.create_objectid(k)})
            gather_like_detail.append(_gather)

        like_coll=utils.dump(like_coll)
        buss_like_detail=utils.dump(buss_like_detail)
        guide_like_detail=utils.dump(guide_like_detail)
        gather_like_detail=utils.dump(gather_like_detail)
        return like_coll,buss_like_detail,guide_like_detail,gather_like_detail
