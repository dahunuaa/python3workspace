# -*- coding:utf-8 -*-

import baosteel100.apps.base.model as model
from baosteel100.libs.datatypelib import *

class LovestoryModel(model.StandCURDModel):
    _coll_name = "lovestory"
    _columns=[
        ("text",StrDT(required=True)),
        ("image_list",ListDT())
    ]

    def before_create(self,object):
        images = self.save_images(object['image_list'])
        del object['image_list']
        object['images']=images
        self.coll.save(object)
        return object

    def save_images(self,images_list):
        images=[]
        for i in images_list:
            if i=="":
                pass
            else:
                try:
                    uri = utils.family_str_to_img("lovestory/%s.png"%utils.get_uuid(),i)
                    url = self.get_host()+uri
                except:
                    url=i
                images.append(url)
        return images