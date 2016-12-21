# -*- coding:utf-8 -*-

import baosteel100.apps.base.model as model
from baosteel100.libs.datatypelib import *
from baosteel100.libs.configlib import *
import  json

class ScopeModel(model.StandCURDModel):
    _coll_name = "scope"
    _columns = [
        ('name',StrDT(required= True)),
        ('homepage_id',ListIDDT(table = "homepage"))
    ]

    def init(self):
        for conf in dict(self.config("init_scope")).values():
            init_scope = {
                "name":conf.name,
                "roles":self.get_roles_fields(conf.roles),
                "add_time":utils.get_now(),
                "last_updated_user":"",
                "delete_user_id":"",
                "add_user_id":"",
                "last_updated_time":"",
            }
            object = self._new()
            del object["homepage_id"]
            object.update(init_scope)
            self.coll.update({"name":conf.name},{"$set":object},True)

    def get_roles_fields(self,roles):
        scope_roles = self.config("scope_roles")
        try:
            roles = json.loads(roles)
        except:
            pass
        if not roles or isinstance(roles,(list,tuple)):
            return roles
        # elif isinstance(roles,(dict,Mapping)):
        #     fields = roles.get("fields")
        #     if fields and fields != "__all__" and not isinstance(fields,(list,tuple)):
        #         raise TypeError(
        #             'The `fields` option must be a list or tuple or "__all__". '
        #             'Got %s.' % type(fields).__name__
        #         )
        #     assert not (fields), (
        #         "Cannot set both 'fields' and 'exclude' options "
        #     )
        #
        #     assert not (fields is None ), (
        #         "Creating a roles without either the 'fields' attribute "
        #         "or the 'exclude' attribute has been deprecated ."
        #         "You can add an explicit fields = '__all__' or just give "
        #         "a list or tuple rather then a dict."
        #     )
        #
        #     if fields is not None:
        #         for field_name in fields:
        #             assert field_name in scope_roles,(
        #                 "角色[%s]错误"%(field_name)
        #             )
        #         return fields
        #
        #     fields = scope_roles
        #
        #     return fields
        else:
            raise TypeError(
                'The `roles` option must be a list or tuple or dict. '
                'Got %s.' % type(roles).__name__
            )

    def before_create(self,object):
        object['roles'] = self.get_roles_fields(self.get_argument("roles",''))
        name= self.get_argument("name")
        if self.coll.find({"name":name}).count()!=0:
            raise ValueError(u"Scope[%s]已存在"%name)
        return object




