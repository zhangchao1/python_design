#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2016-06-15



import datetime
from IPRedisService import IPRedisService
from omen.lib.elasticsearchLib import elasticsearchLib
from omen.db.SuspensionIpModel import SuspensionIpModel
import logging
logging.basicConfig(level = logging.INFO)
class IPAnalysiseService:

    def __init__(self,redis_config={},hash_key = 'suspension:ip'):
        self.redis_config = redis_config;
        print(self.redis_config)
        self.hash_key = hash_key

    # from es get ip data to es
    # url: es host
    # index :es index
    # ip_viste_total :设置封停上限
    # rangeMinute ： 查询时间上限 ，已分钟作为单位
    # sort_type :设置排序方式
    # lte:设置查询的结束时间

    def analysise_ip_data_from_es(self,url,index,path,ip_viste_total = 5000,rangeMinute=5,sort_type = True,lte = datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')):
        print(url)
        logging.info(" analysise ip address start ")
        logging.info(" ip limit value: %s"%ip_viste_total )
        elasticsearch_service = elasticsearchLib(url)
        forbid_ip_address = []
        all_ip = elasticsearch_service.getDataByIndex(index,path,rangeMinute,sort_type,lte)
        if all_ip != "notfound":
            suspension_ip_model = SuspensionIpModel()
            forbid_ip_address = []
            for i in all_ip:
                if i[1] > ip_viste_total:
                    logging.info(" forbid ip addrss %s"%i[0])
                    forbid_ip_address.append(i[0])
        for i in  forbid_ip_address:
            i = str(i)
            ip_exist = suspension_ip_model.check_ip_is_in_db(i)
            if ip_exist:
                logging.info(" update exist ip address ")
                suspension_ip_model.update_ip_status(ip_address =i,Status= 0)
            else:
                ip_data = {}
                ip_data['Status'] = 0;
                ip_data['IpAddress'] = i
                ip_data['SuspensionTime'] = str(datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S'))
                logging.info(" add  ip address to redis")
                suspension_ip_model.add_ip_to_db(ip_data)
            self.add_violation_to_redis(self.hash_key,i)
            logging.info(" analysise ip address end ")

        #将超出上限的ip存入到redis中
    def add_violation_to_redis(self,hash_key,ip_datas):
        ip_redis_service  = IPRedisService(self.redis_config,0)
        ip_redis_service.add_ip_redis(hash_key,ip_datas)


    #将ip从对应的redis中移除
    def rem_violation_ip_from_redis(self,hash_key,ip_datas):
        logging.info(" rem  ip address from redis")
        ip_redis_service  = IPRedisService(self.redis_config,0)
        ip_redis_service.remove_ip_from_redis(hash_key,ip_datas)


# test = IPAnalysiseService()
# ip_data = test.analysise_ip_data_from_es(['http://172.16.9.80:9200/'],'ns',"path:otv2",100,30,True)

