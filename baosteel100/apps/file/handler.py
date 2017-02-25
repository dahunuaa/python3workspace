# -*- coding:utf-8 -*-
from baosteel100.apps.base.handler import TokenHandler,MultiStandardHandler,SingleStandardHanler
from baosteel100.libs.oauthlib import get_provider
import time
import os
import baosteel100

def get_root_path():
    return os.path.dirname(os.path.abspath(baosteel100.__file__))

class UploadFileHandler(MultiStandardHandler):
    _model = "file.FileModel"

    def post(self):
        #文件的暂存路径
        host = self.request.host
        relative_path =get_root_path() + '/static/ftp/file/'#文件存放的具体硬盘路径
        upload_path = host +'/static/ftp/file/'

        if not os.path.exists(os.path.dirname(relative_path)):
            os.makedirs(os.path.dirname(relative_path))
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
            write_path = relative_path+filename
            with open(write_path,'wb') as up:
                up.write(meta['body'])
        self.result["data"] = {"file_name":filename,"file_path":filepath}
        self.finish(self.result)#此处用self.result['data']形式，回调函数是json类型，如果直接是result，回调函数的数据类型是text



handlers = [
    (r"/upload",UploadFileHandler)
]