# -*- coding:utf-8 -*-
import baosteel100.apps.base.model as model
from baosteel100.libs.datatypelib import *
import baosteel100.report as report_util#引入这个就报404
import baosteel100.libs.utils as utils

class ReportModel(model.StandCURDModel):
    _coll_name = "report"
    _columns = []

    def business_report(self,time_desc,start_time,end_time):
        business_coll = model.BaseModel.get_model("business.BusinessModel").get_coll()
        query_params= report_util.change_time(time_desc,start_time,end_time)
        business = business_coll.find(query_params).sort("add_time", -1)
        business_data=utils.dump(business)#注意此处需要先将查询出来的类型转换成json类型
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
        data = business_data
        return result,data

    def inforgather_report(self,time_desc,start_time,end_time):
        inforgather = model.BaseModel.get_model("inforgather.InforgatherModel").get_coll()
        query_params = report_util.change_time(time_desc, start_time, end_time)
        inforgather = inforgather.find(query_params).sort("add_time", -1)
        inforgather_data=utils.dump(inforgather)#注意此处需要先将查询出来的类型转换成json类型
        report_china_name = "inforgather"#windows上面目前路径有汉字的下载不好使
        namelist = [u'序号','情报单号','搜集人','标题','地址','油田区块','油田','内容','添加时间','最后修改时间','文件名','下载地址']
        fieldlist = []
        export_bus_list =[]
        for gather in inforgather_data:
            export_bus_list.append({
                "gather_order":gather["_id"],
                "add_user_name":gather["add_user_name"],
                "gather_title":gather["gather_title"],
                "gather_address":gather["gather_address"],
                "gather_area":gather["gather_area"],
                "gather_oilfield":gather["gather_oilfield"],
                "gather_text":gather["gather_text"],
                "add_time":gather["add_time"],
                "last_updated_time":gather["last_updated_time"],
                "filename":gather["filename"],
                "filepath":gather["filepath"]
            })
        if len(export_bus_list)>0:
            fieldlist=['gather_order','add_user_name','gather_title','gather_address','gather_area','gather_oilfield','gather_text','add_time','last_updated_time','filename','filepath']

        result = report_util.export_excel(report_china_name=[report_china_name],namelist=[namelist],result=[export_bus_list],fieldlist=[fieldlist])
        data = inforgather_data
        return result,data

    def inforguide_report(self,time_desc,start_time,end_time):
        inforguide = model.BaseModel.get_model("inforguide.InforguideModel").get_coll()
        query_params = report_util.change_time(time_desc, start_time, end_time)
        inforguide = inforguide.find(query_params).sort("add_time", -1)
        inforguide_data=utils.dump(inforguide)#注意此处需要先将查询出来的类型转换成json类型
        report_china_name = "inforguide"#windows上面目前路径有汉字的下载不好使
        namelist = [u'序号','单号','搜集人','标题','分类','内容','添加时间','最后修改时间','图片地址']
        fieldlist = []
        export_bus_list =[]
        for guide in inforguide_data:
            export_bus_list.append({
                "guide_order":guide["_id"],
                "add_user_name":guide["add_user_name"],
                "guide_title":guide["guide_title"],
                "guide_type":guide["guide_type"],
                "guide_text":guide["guide_text"],
                "add_time":guide["add_time"],
                "last_updated_time":guide["last_updated_time"],
                "images":str(guide["images"]) ,
            })
        if len(export_bus_list)>0:
            fieldlist=['guide_order','add_user_name','guide_title','guide_type','guide_text','add_time','last_updated_time','images']

        result = report_util.export_excel(report_china_name=[report_china_name],namelist=[namelist],result=[export_bus_list],fieldlist=[fieldlist])
        data = inforguide_data
        return result,data

    def notice_report(self,time_desc,start_time,end_time):
        notice = model.BaseModel.get_model("notice.NoticeModel").get_coll()
        query_params = report_util.change_time(time_desc, start_time, end_time)
        notice = notice.find(query_params).sort("add_time", -1)
        notice_data=utils.dump(notice)#注意此处需要先将查询出来的类型转换成json类型
        report_china_name = "notice"#windows上面目前路径有汉字的下载不好使
        namelist = [u'序号','单号','发布人','标题','内容','发布时间','最后修改时间']
        fieldlist = []
        export_bus_list =[]
        for notice in notice_data:
            export_bus_list.append({
                "notice_order":notice["_id"],
                "add_user_name":notice["add_user_name"],
                "notice_title":notice["notice_title"],
                "notice_text":notice["notice_text"],
                "add_time":notice["add_time"],
                "last_updated_time":notice["last_updated_time"],
            })
        if len(export_bus_list)>0:
            fieldlist=['notice_order','add_user_name','notice_title','notice_text','add_time','last_updated_time']

        result = report_util.export_excel(report_china_name=[report_china_name],namelist=[namelist],result=[export_bus_list],fieldlist=[fieldlist])
        data = notice_data
        return result,data






