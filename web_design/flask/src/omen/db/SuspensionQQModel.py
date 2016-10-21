#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2016-06-21

import datetime
import os
from omen.db.sqlite.modelBase import modelBase
class SuspensionQQModel:

    def __init__(self):
        self.creat_table_sql = '''CREATE TABLE IF NOT EXISTS `SuspensionQQ` (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  QQ VARCHAR ,
                                  Password INTEGER,
                                  CreatTime)'''
        #  KEY Status  Status creat index
        self.tablename = 'SuspensionQQ'
        self.path = os.path.join("/", os.path.dirname(__file__), "sqlite_ip_data.db")
        self.suspensionIp = modelBase(self.path,self.creat_table_sql,self.tablename)

    #将qq数据存入数据库
    def add_qq_to_db(self,qq_data):
        return self.suspensionIp.insert(**qq_data)

    #取出所有的违禁QQ
    def get_suspensionqq(self,limit = None,offset = None,fileds = None,sort_col =None,order_type =None):
        data = []
        for item in self.suspensionIp.select(what=fileds,order_type=order_type,limit=limit,offset=offset,order_by=sort_col):
            data.append(item)
        return data

    #更新已经存在QQ
    def update_qq_password(self,qq="",ip_data = {},**kwargs):
        where = "`QQ` = ?"
        ip_data = dict(ip_data)
        ip_data.update(kwargs)
        ip_data['CreatTime']=  str(datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S'))
        return self.suspensionIp.update(where=where,where_values=(qq,),**ip_data)

    #检查对应的qq是否存在在库中
    def check_qq_is_in_db(self,qq,fileds = None):
        where = '`QQ` = ?'
        for item in self.suspensionIp.select(what=fileds,where = where,where_value=(qq,),limit=1):
            return item
        return None

