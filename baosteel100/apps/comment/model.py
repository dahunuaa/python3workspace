# -*- coding:utf-8 -*-

import baosteel100.apps.base.model as model
from baosteel100.libs.datatypelib import *

class CommentHandler(model.StandCURDModel):
    _coll_name = "comment"
    _columns = [
        ("comment_type",StrDT(required=True,default="buss_comment")),
        ("text_id",StrDT(required=True)),
        ("user_id",StrDT(required=True)),#工号/手机号
        ("text",StrDT(required=True)),
    ]


    def __init__(self):
        self.user_coll = model.BaseModel.get_model("user.UserModel").get_coll()
        super(CommentHandler, self).__init__()


    def before_create(self, object):
        user = self.user_coll.find_one({"_id": utils.create_objectid(object['add_user_id'])})
        object['add_user_name'] = user['name']
        self.coll.save(object)
        return object

    def before_delete(self,object):
        user_id = self.get_argument("user_id")
        if user_id != object['user_id']:
            raise ValueError(u"你无权限删除该评论！")
        return object


