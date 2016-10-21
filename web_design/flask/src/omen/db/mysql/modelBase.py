#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2016-06-13

import mysql.connector
from six import itervalues
import logging
logging.basicConfig(level = logging.INFO)
class modelBase():
    # init database
    def __init__(self,db_conifg,tablename):
        self.conn = mysql.connector.connect(pool_size = 5, user=db_conifg['username'], password=db_conifg['password'], host=db_conifg['host'], port=db_conifg['port'], database = db_conifg['database'], autocommit=True)
        self.cour = self.conn.cursor()
        self.tablename = self.escape(tablename)
        self.placeholder = '%s'
    #run excute cmd

    def excuteSqlCmd(self,query,values = [],**kwargs):
        self.cour.execute(query,values,**kwargs)
        return self.cour


    @staticmethod
    def escape(string):
        return '`%s`' % string

    # INSERT OPRATE
    def insert(self, **values):
        tablename = self.tablename
        if values:
            _keys = ", ".join(self.escape(k) for k in values)
            _values = ", ".join([self.placeholder, ] * len(values))
            sql_query = "INSERT INTO %s (%s) VALUES (%s)" % (tablename, _keys, _values)
            print(sql_query)
            print(list(itervalues(values)))
            dbcur = self.excuteSqlCmd(sql_query, list(itervalues(values)))
            logging.info("sql query : %s"%sql_query)
            return dbcur.lastrowid
        else:
            return None

    #update
    def update(self,where="1=0",where_values=[],**values):
        tablename = self.tablename
        _key_values = ", ".join([
                "%s = %s" % (self.escape(k), self.placeholder) for k in values
            ])
        sql_query = "UPDATE %s SET %s WHERE %s" % (tablename, _key_values, where)
        logging.info("sql query : %s"%sql_query)
        return self.excuteSqlCmd(sql_query, list(itervalues(values))+list(where_values))

    #select查询操作
    def select(self,where="",what = "",where_value = [],order_by="",limit =None,offset = 0,order_type = 'DESC'):
        tablename = self.tablename
        if isinstance(what, list) or isinstance(what, tuple) or what is None:
            what = ",".join(self.escape(f) for f in what) if what else '*'
        sql_query = "SELECT %s FROM %s" % (what, tablename)
        if where:
            sql_query += " WHERE %s" % where
        if order_by:
            sql_query += " ORDER BY %s %s"%(order_by,order_type)
        if limit:
            sql_query += " LIMIT %d, %d" % (offset, limit)
        logging.info("sql query : %s"%sql_query)
        dbcur = self.excuteSqlCmd(sql_query,where_value)
        fields = [f[0] for f in dbcur.description]
        for row in dbcur:
            yield dict(zip(fields, row))

    #delete
    def delete(self,where ="",where_value = []):
        tablename = self.tablename
        sql_query = "DELETE FROM %s" %tablename
        if where:
            sql_query += " WHERE %s" % where
        logging.info("sql query : %s"%sql_query)
        return self.excuteSqlCmd(sql_query,where_value)

    #关闭连接
    def __del__(self):
        self.cour.close()






