# -*- coding:utf-8 -*-
from baosteel100.apps.base.handler import MultiStandardHandler,TokenHandler
from baosteel100.libs.oauthlib import get_provider
import baosteel100.libs.utils as utils

class BusinessReportHandler(MultiStandardHandler,TokenHandler):
    _model = "report.ReportModel"
    enable_methods = ["get"]

    def get(self):
        result = self.model.business_report()
        file_names = result["filename"]
        file_paths = result["file_path"]
        self.result["data"]={"download_path":result["download_path"],"file_name":file_names,"file_path":file_paths}
        self.finish(self.result)

        #以下注释内容可以直接在浏览器下载该文件
        # self.set_header('Content-Type', 'application/octet-stream')
        # self.set_header('Content-Disposition', 'attachment; filename=' + file_names[0])
        # with open(file_paths[0], 'rb') as f:
        #     while True:
        #         data = f.read(1024)
        #         if not data:
        #             break
        #         self.write(data)
        # self.finish(self.result)

class InforgatherReportHandler(MultiStandardHandler,TokenHandler):
    _model = "report.ReportModel"
    enable_methods = ["get"]

    def get(self):
        result = self.model.inforgather_report()
        file_names = result["filename"]
        file_paths = result["file_path"]
        self.result["data"]={"download_path":result["download_path"],"file_name":file_names,"file_path":file_paths}
        self.finish(self.result)

class InforguideReportHandler(MultiStandardHandler,TokenHandler):
    _model = "report.ReportModel"
    enable_methods = ["get"]

    def get(self):
        result = self.model.inforguide_report()
        file_names = result["filename"]
        file_paths = result["file_path"]
        self.result["data"]={"download_path":result["download_path"],"file_name":file_names,"file_path":file_paths}
        self.finish(self.result)

class NoticeReportHandler(MultiStandardHandler,TokenHandler):
    _model = "report.ReportModel"
    enable_methods = ["get"]

    def get(self):
        result = self.model.notice_report()
        file_names = result["filename"]
        file_paths = result["file_path"]
        self.result["data"]={"download_path":result["download_path"],"file_name":file_names,"file_path":file_paths}
        self.finish(self.result)


handlers = [
    (r"/business",BusinessReportHandler,get_provider("report_admin")),
    (r"/inforgather",InforgatherReportHandler,get_provider("report_admin")),
    (r"/inforguide",InforguideReportHandler,get_provider("report_admin")),
    (r"/notice",NoticeReportHandler,get_provider("report_admin")),
]