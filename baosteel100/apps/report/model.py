# -*- coding:utf-8 -*-
import baosteel100.apps.base.model as model
from baosteel100.libs.datatypelib import *
import baosteel100.report as report_util#引入这个就报404

class ReportModel(model.StandCURDModel):
    _coll_name = "report"
    _columns = []

    def business_report(self):
        business = model.BaseModel.get_model("business.BusinessModel").get_coll()
        business_data=utils.dump(business.find())#注意此处需要先将查询出来的类型转换成json类型
        report_china_name = "business"#windows上面目前路径有汉字的下载不好使
        namelist = [u'序号','出差单号','出差人员','出差总人数','出差地','编辑者','出差开始时间','出差结束时间','添加时间','最后修改时间','备注']
        fieldlist = []
        export_bus_list =[]
        for bus in business_data:
            export_bus_list.append({
                "business_order":bus["_id"],
                "business_staff":bus["business_staff"],
                "business_num":bus["business_num"],
                "business_place":bus["business_place"],
                "add_user_name":bus["add_user_name"],
                "begin_time":bus["begin_time"],
                "end_time":bus["end_time"],
                "add_time":bus["add_time"],
                "last_updated_time":bus["last_updated_time"],
                "remark":bus["remark"]
            })
        if len(export_bus_list)>0:
            fieldlist=['business_order','business_staff','business_num','business_place','add_user_name','begin_time','end_time','add_time','last_updated_time','remark']

        result = report_util.export_excel(report_china_name=[report_china_name],namelist=[namelist],result=[export_bus_list],fieldlist=[fieldlist])
        return result



