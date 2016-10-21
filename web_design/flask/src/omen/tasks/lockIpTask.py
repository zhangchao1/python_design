#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2016-06-16


from omen.service.IPAnalysiseService import IPAnalysiseService

import datetime

class lockIpTask:
    def __init__(self,url,index,path,redis_config,ip_viste_total = 5000,rangeMinute=5,sort_type = True,lte = datetime.datetime.now().
                 strftime('%Y.%m.%d %H:%M:%S')):
        self.url = url
        self.index = index
        self.path = path
        self.ip_viste_total = ip_viste_total
        self.rangeMinute = rangeMinute
        self.sort_type = sort_type
        self.lte = lte
        self.redis_config = redis_config

    def run(self):
        ip_analysise_service = IPAnalysiseService(self.redis_config)
        print(self.url)
        ip_analysise_service.analysise_ip_data_from_es(self.url,self.index,self.path,self.ip_viste_total,self.rangeMinute,
                                                       self.sort_type,self.lte)


