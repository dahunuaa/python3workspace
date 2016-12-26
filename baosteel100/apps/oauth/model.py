# -*- coding:utf-8 -*-
import baosteel100.apps.base.model as model

class OauthClientsModel(model.StandCURDModel,model.Singleton):
    _coll_name = "oauth_clients"


class OauthAccessTokenModel(model.StandCURDModel,model.Singleton):
    _coll_name = "oauth_access_token"