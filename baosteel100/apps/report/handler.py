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
        report_data = result["report_data"]

        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + file_names[0])
        with open(file_paths[0], 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                self.write(data)
        self.finish()


handlers = [
    (r"/business",BusinessReportHandler,get_provider("report_admin"))
]