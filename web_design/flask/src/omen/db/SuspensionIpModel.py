#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2016-06-15

import datetime
import os
from omen.db.sqlite.modelBase import modelBase

class SuspensionIpModel:

        # init model
        def __init__(self):
            self.creat_table_sql = '''CREATE TABLE IF NOT EXISTS `SuspensionIp` (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  IpAddress VARCHAR ,
                                  Status INTEGER,
                                  SuspensionTime)'''
            #  KEY Status  Status creat index
            self.tablename = 'SuspensionIp'
            self.path = os.path.join("/", os.path.dirname(__file__), "sqlite_ip_data.db")
            self.suspensionIp = modelBase(self.path,self.creat_table_sql,self.tablename)


        #将ip地址存入数据库
        def add_ip_to_db(self,ip_data):
            return self.suspensionIp.insert(**ip_data)

        #判断当前ip是否存在
        def check_ip_is_in_db(self,ip_address,fileds = None):
            where = '`IpAddress` = ?'
            for item in self.suspensionIp.select(what=fileds,where = where,where_value=(ip_address,),limit=1):
                return item
            return None

        #取出所有的违禁ip
        def get_suspensionIp(self,status,limit = None,offset = None,fileds = None,sort_col =None,order_type =None):
            where = '`Status` = ?'
            data = []
            for item in self.suspensionIp.select(what=fileds,where = where,where_value=(status,),order_type=order_type,limit=limit,offset=offset,order_by=sort_col):
                data.append(item)
            return data

       #更新已经存在ip，通过status对于ip封停和解封
        def update_ip_status(self,ip_address="",ip_data = {},**kwargs):
            where = "`IpAddress` = ?"
            ip_data = dict(ip_data)
            ip_data.update(kwargs)
            ip_data['SuspensionTime']=  str(datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S'))
            return self.suspensionIp.update(where=where,where_values=(ip_address,),**ip_data)

        # 删除废弃的ip
        def delete_suspensionIp(self,ip_address):
            where = "`IpAddress` = ?"
            return self.suspensionIp.delete(where=where,where_value=(ip_address,))

# test = SuspensionIpModel()
# ip_data = {}
# # ip_data['IpAddress'] = '127.0.0.4'
# # ip_data['Status']  = 1
# # ip_data['SuspensionTime']  = datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')
# # test.add_ip_to_db(ip_data)
# print(test.get_suspensionIp(0))
