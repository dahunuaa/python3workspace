# -*- coding:utf-8 -*-
from baosteel100.apps.base.handler import TokenHandler,MultiStandardHandler,SingleStandardHanler
from baosteel100.libs.oauthlib import get_provider
import time
import os
import baosteel100.libs.utils as utils
import baosteel100.apps.base.model as model


class UploadFileHandler(MultiStandardHandler,TokenHandler):
    _model = "file.FileModel"

    def post(self):
        #文件的暂存路径
        upload_path = utils.get_root_path() +'/static/ftp/file/'
        if not os.path.exists(os.path.dirname(upload_path)):
            os.makedirs(os.path.dirname(upload_path))
        #提取表单中‘name’为‘file’的文件元数据
        file_metas=self.request.files['file']
        for meta in file_metas:
            filename=meta['filename']
            filepath=os.path.join(upload_path,filename)
            file = {
                "file_name" :filename,
                "file_path":filepath,
                "add_time":time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),
                "add_user_id":self.user_id,
            }
            self.coll.save(file)
            #有些文件需要已二进制的形式存储，实际中可以更改
            with open(filepath,'wb') as up:
                up.write(meta['body'])
            self.write('finished!')
        result = {"success":1,"data":{"file_name":filename,"file_path":filepath}}
        self.finish(result)



handlers = [
    (r"/upload",UploadFileHandler,get_provider("file")),
]