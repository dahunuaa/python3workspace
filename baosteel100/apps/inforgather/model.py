# -*- coding:utf-8 -*-

import baosteel100.apps.base.model as model
import baosteel100.apps.user.model as user_model
from baosteel100.libs.datatypelib import *

class InforgatherModel(model.StandCURDModel):
    _coll_name = "inforgather"
    _columns = [
        ("gather_title",StrDT(required=True)),
        ("gather_address",StrDT(required=True)),
        ("gather_area", StrDT(required=True)),
        ("gather_oilfield", StrDT(required=True)),
        ("gather_text", StrDT(required=True)),
        ("images_list",ListDT()),
        # ("files",ListDT())
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

    def before_update(self,object):
        _object = self._get_from_id(update=True)
        images_list = self.get_argument("images_list")
        # if len(_object['images'])!=0:
        images = self.save_images(_object['add_user_jobno'], images_list)
        del object['images_list']
        object['images'] = images
        _object.update(object)
        return _object



