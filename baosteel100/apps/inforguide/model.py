# -*- coding:utf-8 -*-

import baosteel100.apps.base.model as model
import baosteel100.apps.user.model as user_model
from baosteel100.libs.datatypelib import *

class InforguideModel(model.StandCURDModel):
    _coll_name = "inforguide"
    _columns = [
        ("guide_title",StrDT(required=True)),
        ("guide_type",StrDT(required=True)),
        ("guide_text", StrDT(required=True)),
        ("images_list",ListDT()),
        ("filename", StrDT()),
        ("filepath", StrDT()),
    ]

    def before_create(self,object):
        user=user_model.UserModel.get_username_by_id(object['add_user_id'])
        object["add_user_name"] =user['name']
        object["add_user_jobno"]=user['job_no']
        images = self.save_images(object['add_user_jobno'],object['images_list'])
        del object['images_list']
        object['images']=images
        self.coll.save(object)
        return object

    def after_create(self,object):
        msgunread_coll = model.BaseModel.get_model("msgunread.MsgunreadModel").get_coll()
        _msgunread = msgunread_coll.find()
        for i in _msgunread:
            i["guide_unread"].append(utils.objectid_str(object['_id']))
            msgunread_coll.save(i)
        return object

    def save_images(self,add_user_jobno,images_list):
        images=[]
        for i in images_list:
            if i =="":
                pass
            else:
                try:
                    uri = utils.str_to_img("inforguide/%s_%s.png"%(add_user_jobno,utils.get_uuid()),i)
                    url = self.get_host()+uri
                except:
                    url = i
                images.append(url)
        return images

    def before_update(self,object):
        _object = self._get_from_id(update=True)
        images_list = self.get_argument("images_list")
        images = self.save_images(_object['add_user_jobno'], images_list)
        del object['images_list']
        object['images'] = images
        _object.update(object)
        return _object

    def after_delete(self,object):
        msg_id = utils.objectid_str(object["_id"])
        msgunread_coll = model.BaseModel.get_model("msgunread.MsgunreadModel").get_coll()
        _msgunread = msgunread_coll.find()
        for i in _msgunread:
            if msg_id in i["guide_unread"]:
                i["guide_unread"].remove(msg_id)
                msgunread_coll.save(i)
        return object

    def unread_msg(self):
        user_mobile = user_model.UserModel.get_user_mobile_by_token(self._arguments["access_token"])
        msgunread_coll = model.BaseModel.get_model("msgunread.MsgunreadModel").get_coll()
        msgunread = msgunread_coll.find_one({"user_id":user_mobile["mobile"]})
        return msgunread

    def classify(self):
        result = utils.dump(self.coll.aggregate([{"$group":{"_id":"$guide_type",
                                                    "num":{"$sum":1}}},
                                                  {"$sort":{"num":-1}}
                                                  ]))

        # bijixiaojie_count = self.coll.find({"guide_type":"笔记小结"}).count()
        # yonghuxinxi_count = self.coll.find({"guide_type":"用户信息"}).count()
        # chanpinxinxi_count = self.coll.find({"guide_type": "产品信息"}).count()
        # hangyexinxi_count = self.coll.find({"guide_type": "行业信息"}).count()
        # gongsixinwen_count = self.coll.find({"guide_type": "公司新闻"}).count()
        # result = {"bijixiaojie":bijixiaojie_count,"yonghuxinxi":yonghuxinxi_count,"chanpinxinxi":chanpinxinxi_count,
        #           "hangyexinxi":hangyexinxi_count,"gongsixinwen":gongsixinwen_count}
        return result



