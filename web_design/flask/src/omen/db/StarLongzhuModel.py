#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2016-06-15

from omen.db.mysql.modelBase import modelBase

class StarLongzhuModel:

    def __init__(self,db_config):
        self.tableName = 'star_longzhu'
        self.star_longzhu = modelBase(db_config,self.tableName)

    def add_es_data_to_db(self,data):
        return self.star_longzhu.insert(**data)
