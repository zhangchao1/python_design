#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2015-12-28


from elasticsearch import Elasticsearch
import datetime
import time
class base_elasticsearch:

    #####init es
    def __init__(self,url=[],timeout=300):
        self.es = Elasticsearch(url,sniffer_timeout = timeout)

    #####creat index
    def creat_index(self,index_name,body = {}):
        if self.es.indices.exists(index=index_name):
            self.es.indices.delete(index=index_name)
        self.es.indices.create(index=index_name,body=body)

    ###insert data
    def insert_data_into_es(self,index_name,doc_type,body):
        index_name = index_name + "-" + str(datetime.datetime.now().strftime('%Y.%m.%d'))
        self.es.index(index=index_name,doc_type=doc_type,body=body)

    ###search data
    def search_data_from_es(self,index_name,body):
        return self.es.search(index=index_name,body=body)



