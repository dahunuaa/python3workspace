# -*- coding:utf-8 -*-

import baosteel100.apps.base.model as model
from baosteel100.libs.datatypelib import *

class NoticeModel(model.StandCURDModel):
    _coll_name = "notice"
    _columns=[
        ("notice_title",StrDT(required=True)),
        ("notice_text",StrDT(required=True))
    ]