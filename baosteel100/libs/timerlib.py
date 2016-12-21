# -*- coding: utf-8 -*-
#
# @author: zhao jie
# Created on 2016-11-23
#
import httplib2,datetime
import baosteel100.apps.base.model as model

from baosteel100.libs.options import config

def run_gps_timer():
    gps_model = model.BaseModel.get_model("gps.GpsModel").get_coll()
    gps_list = gps_model.find()
    for gps in gps_list:
        gps_no = gps.get("gps_no","")
        url = '%s%s'% (config.gps_url,gps_no)
        response,content = get_http_response(url,"json")
        msg = content.get("Msg","")
        if msg == "ok":
            ret = content.get("Ret","")
            if ret == 0:
                data = content.get("Data","")
                data.update({"add_time":datetime.datetime.now()})
                gps_l = gps["gps_list"]
                gps_l.append(data)
                gps_model.save(gps)

def run_http_timer():
    urls = config.http_url
    fail_message = ""
    http_model = model.BaseModel.get_model("http.HttpModel").get_coll()
    for system_name,url in urls.iteritems():
        http_m = http_model.find_one({"system_name":system_name})
        status = "通信正常"
        try:
            response,content = get_http_response(url,"http")
        except Exception:
            status = "通信失败"
            fail_message += ("链接%s出现了问题" % url)
        if http_m is None:
            http_m = {}

        data = {"status":status,"add_time":datetime.datetime.now()}
        http_m["status"] = status
        http_m["last_updated_time"] = datetime.datetime.now()
        http_m["system_name"] = system_name
        http_m["system_url"] = url
        search_list = http_m.get("search_list",[])
        search_list.append(data)
        http_m["search_list"] = search_list
        http_model.save(http_m)

    if fail_message:
        print (fail_message)
        #给短信接口接入

def get_http_response(url,type):
    conn = httplib2.Http(timeout=3)
    response,content = conn.request(uri=url,method="GET")
    if type == "json":
        return response,eval(content)
    else:
        return response,content


if __name__ == '__main__':
    run_http_timer()