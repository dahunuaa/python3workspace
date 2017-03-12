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
        ("images_list", ListDT()),
        ("filename",StrDT()),
        ("filepath", StrDT()),
    ]

    def __init__(self):
        self.user_coll = model.BaseModel.get_model("user.UserModel").get_coll()
        super(InforgatherModel, self).__init__()

    def before_create(self,object):
        user =self.user_coll.find_one({"_id":utils.create_objectid(object['add_user_id'])})
        object['add_user_name'] = user['name']
        object["add_user_jobno"] = user['job_no']
        images = self.save_images(object['add_user_jobno'], object['images_list'])
        del object['images_list']
        object['images'] = images
        self.coll.save(object)
        return object

    def save_images(self,add_user_jobno,images_list):
        images=[]
        for i in images_list:
            if i =="":
                pass
            else:
                try:
                    uri = utils.str_to_img("inforgather/%s_%s.png"%(add_user_jobno,utils.get_uuid()),i)
                    url = self.get_host()+uri
                except:
                    url = i
                images.append(url)
        return images

    def after_create(self,object):
        msgunread_coll = model.BaseModel.get_model("msgunread.MsgunreadModel").get_coll()
        _msgunread = msgunread_coll.find()
        for i in _msgunread:
            i["gather_unread"].append(utils.objectid_str(object['_id']))
            msgunread_coll.save(i)
        return object

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







