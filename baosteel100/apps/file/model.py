# -*- coding:utf-8 -*-
import baosteel100.apps.base.model as model
from baosteel100.libs.datatypelib import *
import os
from baosteel100.libs.utils import *

class FileModel(model.StandCURDModel):
    _coll_name = "file"
    _columns = [
        ("file_name",StrDT()),
        ("file_path",StrDT())

    ]



