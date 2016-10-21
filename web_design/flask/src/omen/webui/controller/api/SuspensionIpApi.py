#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2016-06-17

from omen.webui.controller.api import api

from flask import request

import json

import urllib2

import time

from omen.db.SuspensionIpModel import SuspensionIpModel

from omen.lib.elasticsearchLib import elasticsearchLib

from omen.webui import app
from omen import wirte_log_to_file

@api.route("/api/findip/",methods=['GET'])
def get_suspensionIp():
    suspension_ip = SuspensionIpModel()
    sort_col = request.args.get('sort_col');
    if sort_col == None:
        sort_col = 'SuspensionTime';
    sort_type = request.args.get('sort_type')
    if sort_type == None:
        sort_type = 'DESC'
    limit = request.args.get('max')
    if limit == None:
        limit = 5
    offset = int(request.args.get('start'))
    offset = offset*int(limit)
    if offset == None:
        offset = 0;
    info = "find ip :get ip status =0"
    wirte_log_to_file(info)
    total_data = suspension_ip.get_suspensionIp(0,fileds="IpAddress")
    total = len(total_data)
    data = suspension_ip.get_suspensionIp(0,limit = int(limit),offset=int(offset),sort_col=sort_col,order_type=sort_type)
    all_data = {
        "total" :total,
        "data" :data
    }
    return json.dumps(all_data)

@api.route("/api/search_ip/",methods=['GET'])
def search_suspension_ip():
     url  = app.config.get('es_host')
     timeout = app.config.get('es_timeout')
     es_lib = elasticsearchLib(url,timeout)
     search_time = request.args.get('time');
     search_index = request.args.get('index');
     search_path = request.args.get('path');
     search_rangtime= request.args.get('rangtime');
     if search_rangtime == None or search_path == None or search_time== None or search_index ==None:
         message = {
             "message":"empty value"
         }
         return json.dumps(message)
     else:
         search_time = str(search_time)
         search_time = search_time + ":00"
         search_time = time.mktime(time.strptime(search_time,'%Y-%m-%d %H:%M:%S'))
         search_time = time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(int(search_time)))
         data = []
         info = "serach ip : index->%s ,path->%s"%(search_index,search_path)
         wirte_log_to_file(info)
         data = es_lib.getDataByIndex(index=str(search_index),path=str(search_path),rangeMinute=int(search_rangtime),
                                     sort=True,lte=search_time)
         print(data)
         if data !="notfound":
            suspension_ips = {}
            for i in data:
                if i[1]>5000:
                    suspension_ips[i[0]] = i[1]
            message = {
             "message":suspension_ips
             }
            print(message)
            return json.dumps(message)
         else:
             message = {
             "message":"not found"
             }
             return json.dumps(message)

@api.route("/api/search_api_visit/",methods=['GET'])
def search_api_visit():
    url  = app.config.get('es_host')
    timeout = app.config.get('es_timeout')
    es_lib = elasticsearchLib(url,timeout)
    apiname = request.args.get('apiname');
    start = request.args.get('from');
    end = request.args.get('to')
    type = request.args.get('type')
    info = "find website: %s ----- rangetime:%s"%(apiname,type)
    wirte_log_to_file(info)
    if start == None or apiname == None or end == None or type ==None:
         message = {
             "message":"empty value"
         }
         return json.dumps(message)
    else:
        if apiname == 'all':
            apiname ="*"
        data = es_lib.get_realtime_api(index="ns-*",api_name=apiname,start=start,end=end,type=type)
        return json.dumps(data)
@api.route("/api/get_api_visit/",methods=['GET'])
def get_api_visit():
    url  = app.config.get('es_host')
    timeout = app.config.get('es_timeout')
    es_lib = elasticsearchLib(url,timeout)
    website = request.args.get('website');
    apiname = request.args.get('apiname');
    type = request.args.get('type');
    info = "find website: %s +++++++ apiname:%s  rangetime:%s"%(website,apiname,type)
    wirte_log_to_file(info)
    if type == None or apiname == None or website ==None:
         message = {
             "message":"empty value"
         }
         return json.dumps(message)
    else:
        data = es_lib.search_api_relatime(index="ns-*",website_name=website,api_name=apiname,type=type)
        if data == 'not found':
            message = {
             "message":"not found"
            }
            return json.dumps(message)
        else:
            message = {
             "message":data
            }
            return json.dumps(message)

@api.route("/api/get_all_website/",methods=['GET'])
def get_all_website():
    url  = app.config.get('es_host')
    timeout = app.config.get('es_timeout')
    es_lib = elasticsearchLib(url,timeout)
    type = request.args.get('type');
    rangetime = request.args.get('rangetime');
    if rangetime == None or type == None:
         message = {
             "message":"empty value"
         }
         return json.dumps(message)
    else:
        info = "get all website"
        wirte_log_to_file(info)
        if type == 'all':
            data = es_lib.get_all_website_name(index="*",is_all=True,rangeminute=int(rangetime))
        elif type == 'website':
            data = es_lib.get_all_website_name(index="*",is_all=False,rangeminute=int(rangetime))
        if data == 'not found':
            message = {
             "message":"not found"
            }
            return json.dumps(message)
        else:
            message = {
             "message":data
            }
            return json.dumps(message)

@api.route("/api/get_website_all_api/",methods=['GET'])
def get_website_all_api():
    url  = app.config.get('es_host')
    timeout = app.config.get('es_timeout')
    es_lib = elasticsearchLib(url,timeout)
    websitename = request.args.get('websitename');
    rangetime = request.args.get('rangetime');
    if rangetime == None or type == None:
         message = {
             "message":"empty value"
         }
         return json.dumps(message)
    else:
        data = es_lib.get_all_api_from_website(index="*",website_name=websitename,rangeminute=int(rangetime))
        if data == 'not found':
            message = {
             "message":"not found"
            }
            return json.dumps(message)
        else:
            message = {
             "message":data
            }
            return json.dumps(message)

@api.route("/api/all_china_web_visit/",methods=['GET'])
def all_china_web_visit():
    url  = app.config.get('es_host')
    timeout = app.config.get('es_timeout')
    es_lib = elasticsearchLib(url,timeout)
    type = request.args.get('type')
    if type == None:
        message = {
             "message":"empty value"
         }
        return json.dumps(message)
    else:
        if type == 'chat':
            index = 'chat-*'
        elif type == 'ns':
            index = 'ns-*'
    data = es_lib.get_all_china_visit(index=index,rangeminute=5,total=10000)
    return json.dumps(data)