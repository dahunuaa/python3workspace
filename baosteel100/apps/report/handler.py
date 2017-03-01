# -*- coding:utf-8 -*-
from baosteel100.apps.base.handler import MultiStandardHandler,TokenHandler
from baosteel100.libs.oauthlib import get_provider
import baosteel100.libs.utils as utils
# import baosteel100.report as report_util#引入这个就报404

class BusinessReportHandler(MultiStandardHandler,TokenHandler):
    _model = "report.ReportModel"
    enable_methods = ["get"]

    def get(self):
        page = 1
        page_size = 10000
        result = self.model.report()
        file_names = result["filename"]
        file_paths = result["file_path"]
        report_data = result["report_data"]

        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + file_names[0])
        print(file_paths[0])
        with open(file_paths[0], 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                self.write(data)
        return utils.dump(result)


        # report_china_name = "出差信息表"
        # namelist = [u'序号','出差单号','出差人员','出差总人数','出差地','编辑者','出差开始时间','出差结束时间','添加时间','最后修改时间','备注']
        # fieldlist = []
        # export_bus_list =[]
        # for bus in business_data:
        #     export_bus_list.append({
        #         "business_order":bus["_id"],
        #         "business_staff":bus["business_staff"],
        #         "business_num":bus["business_num"],
        #         "business_place":bus["business_place"],
        #         "add_user_name":bus["add_user_name"],
        #         "begin_time":bus["begin_time"],
        #         "end_time":bus["end_time"],
        #         "add_time":bus["add_time"],
        #         "last_updated_time":bus["last_updated_time"],
        #         "remark":bus["remark"]
        #     })
        # if len(export_bus_list)>0:
        #     fieldlist=['business_order','business_staff','business_num','business_place','add_user_name','begin_time','end_time','add_time','last_updated_time','remark']
        #
        # result = report_util.export_excel(report_china_name=[report_china_name],namelist=[namelist],result=[export_bus_list],fieldlist=[fieldlist])
        # file_names = result["filename"]
        # file_paths = result["file_path"]
        # report_data = result["report_data"]
        #
        # self.set_header('Content-Type', 'application/octet-stream')
        # self.set_header('Content-Disposition', 'attachment; filename=' + file_names[0])
        # with open(file_paths[0], 'rb') as f:
        #     while True:
        #         data = f.read(1024)
        #         if not data:
        #             break
        #         self.write(data)
        # # self.finish()

handlers = [
    (r"/business",BusinessReportHandler,get_provider("report_admin"))
]