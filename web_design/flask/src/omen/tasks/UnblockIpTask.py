#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2016-06-15

import time

from omen.db.SuspensionIpModel import  SuspensionIpModel

from omen.service.IPAnalysiseService  import IPAnalysiseService

import logging

logging.basicConfig(level = logging.INFO)

class UnblockIpTask:

    def __init__(self,redis_config={},clocktime =24,suspension_key = 'suspension:ip'):
        self.redis_config = redis_config;
        self.clock_ip_time = clocktime
        self.suspension_key = suspension_key

    #解禁ip
    def unblockIp(self):
        logging.info("start unblock ip ")
        suspension_ip_model = SuspensionIpModel()
        all_suspension_ip = suspension_ip_model.get_suspensionIp(0)
        ip_analysise_service = IPAnalysiseService(self.redis_config)
        currnet_time = self._fromatTime(time.time())
        for i in all_suspension_ip:
            logging.info("unblock ip address %s"%i['IpAddress'])
            ip_SuspensionTime = self._fromatTime(time.mktime(time.strptime(i['SuspensionTime'],'%Y.%m.%d %H:%M:%S')))
            if currnet_time -ip_SuspensionTime > self.clock_ip_time*60000*60:
                suspension_ip_model.update_ip_status(ip_address=i['IpAddress'],Status= 1)
                ip_analysise_service.rem_violation_ip_from_redis(self.suspension_key,i['IpAddress'])
            else:
                continue
        logging.info("end unblock ip ")
    #格式化时间
    def _fromatTime(self,fromat_time):
        fromat_time = str(fromat_time)
        fromat_time = fromat_time.split(".")
        fromat_time = int(fromat_time[0])*1000
        return fromat_time


