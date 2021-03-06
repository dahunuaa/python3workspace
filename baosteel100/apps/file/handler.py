# -*- coding:utf-8 -*-
from baosteel100.apps.base.handler import TokenHandler,MultiStandardHandler,SingleStandardHanler
from baosteel100.libs.oauthlib import get_provider
import time
import os
import baosteel100
import baosteel100.libs.utils as utils
def get_root_path():
    return os.path.dirname(os.path.abspath(baosteel100.__file__))

class UploadFileHandler(MultiStandardHandler,TokenHandler):
    _model = "file.FileModel"

    def post(self):
        #文件的暂存路径
        host = "http://"+self.request.host
        relative_path =get_root_path() + '/static/ftp/file/'#文件存放的具体硬盘路径
        upload_path = host +'/static/ftp/file/'

        if not os.path.exists(os.path.dirname(relative_path)):
            os.makedirs(os.path.dirname(relative_path))
        #提取表单中‘name’为‘file’的文件元数据
        file_metas=self.request.files['file']
        for meta in file_metas:
            filename=meta['filename']
            newfilename=self.user_id+'_'+str(utils.get_local_timestamp())
            filepath=os.path.join(upload_path,filename)#将filename改为newfilename
            file = {
                "file_name" :filename,
                "file_path":filepath,
                "add_time":time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),
                "add_user_id":self.user_id,
            }
            self.coll.save(file)
            #有些文件需要已二进制的形式存储，实际中可以更改
            write_path = relative_path+filename#将filename改为newfilename
            with open(write_path,'wb') as up:
                up.write(meta['body'])
        self.result["data"] = {"file_name":filename,"file_path":filepath}
        self.finish(self.result)#此处用self.result['data']形式，回调函数是json类型，如果直接是result，回调函数的数据类型是text

class DownloadFilesHandler(TokenHandler,MultiStandardHandler):
    _model = "file.FileModel"
    def get(self):
        path = get_root_path() + '/static/ftp/file/'
        zip_name = os.path.join(get_root_path()+'/static/ftp/wenjian_'+time.strftime("%Y%m%d") + '.zip')
        utils.zip_folder(path,zip_name)
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + os.path.split(zip_name)[1])
        with open(zip_name, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                self.write(data)
        os.remove(zip_name)
        self.finish()

class DownloadImagesHandler(TokenHandler,MultiStandardHandler):
    _model = "file.FileModel"
    def get(self):
        path = get_root_path() + '/static/ftp/image/'
        zip_name = os.path.join(get_root_path()+'/static/ftp/tuku_'+time.strftime("%Y%m%d") + '.zip')
        utils.zip_folder(path,zip_name)
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + os.path.split(zip_name)[1])
        with open(zip_name, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                self.write(data)
        os.remove(zip_name)
        self.finish()

handlers = [
    (r"/upload",UploadFileHandler,get_provider("file")),
    (r"/download/images",DownloadImagesHandler,get_provider("file")),
    (r"/download/files",DownloadFilesHandler,get_provider("file")),
]