# -*- coding:utf-8 -*-

from baosteel100.apps.base.handler import MultiStandardHandler,SingleStandardHanler,TokenHandler
from baosteel100.libs.oauthlib import get_provider
from baosteel100.libs.loglib import get_logger
import tornado.web
import baosteel100.libs.file as file_model

logger = get_logger("debug")

class InforgatherListHandler(MultiStandardHandler,TokenHandler):
    _model = "inforgather.InforgatherModel"
    enable_methods = ["post","get"]
    private = False

class InforgatherHandler(SingleStandardHanler,TokenHandler):
    _model = "inforgather.InforgatherModel"
    enable_methods = ["get","put","delete"]

class FileUploadHandler(TokenHandler):
    def post(self):
        import time
        file_type = self.get_argument("file_type",'normal')
        url = '/static/ftp/files/'
        upload_path = url + time.strftime('%Y%m%d')
        file = self.request.files['file']


handlers = [
    (r"",InforgatherListHandler,get_provider("inforgather")),
    (r"/(.*)",InforgatherHandler,get_provider("inforgather"))
]

