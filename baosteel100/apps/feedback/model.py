# -*- coding:utf-8 -*-
import baosteel100.apps.base.model as model
from baosteel100.libs.datatypelib import *

class FeedbackModel(model.StandCURDModel):
    _coll_name = "feedback"
    _columns = [
        ("feedback_content",StrDT(required=True)),
        ("contact",StrDT())
    ]

