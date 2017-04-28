# -*- coding:utf-8 -*-
import baosteel100.apps.base.model as model
from baosteel100.libs.datatypelib import *

class KeyWordsModel(model.StandCURDModel):
    _coll_name="keywords"
    _columns=[
        ("author_name",StrDT()),
        ("author_id",StrDT()),
        ("keyword",StrDT())
    ]

    def keywords_rank(self):
        result=utils.dump(self.coll.aggregate([{"$group":{"_id":"$keyword",
                                                          "num":{"$sum":1},
                                                          }},
                                               {"$sort": {"num": -1}, }
                                               ]))
        return result