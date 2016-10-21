#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2016-07-19

from omen.lib.elasticsearchLib import elasticsearchLib

from omen.lib.cryptoLib import cryptoLib

from omen.db.StarLongzhuModel import StarLongzhuModel

import time

import random

import  re

class getliveSourceTask:

    #init es
    def __init__(self,url,index,path,host,source,encryptionKey,validationKey,db_config):

        self.index = str(index)
        self.host = host
        self.path = path
        self.source = source
        self.es = elasticsearchLib(url)
        self.encryptionKey = encryptionKey;
        self.validationKey = validationKey
        self.crypto_lib = cryptoLib(encryptionKey,validationKey)
        self.star_longzhu = StarLongzhuModel(db_config)

    def _formatTime(self,lteTime,type="%Y.%m.%d %H:%M:%S"):

         format_time = time.mktime(time.strptime(lteTime,type))
         format_time = str(format_time)
         format_time = format_time.split(".")
         format_time = int(format_time[0])*1000
         return format_time

    def _unixTimeToLocalTime(self,unixtime):
        return time.strftime('%Y-%m-%d %H:%M:%S ',time.localtime(unixtime/1000))


    def _getbody(self):
        body ={
  "size": 10000,
  "sort": [
    {
      "@timestamp": {
        "order": "desc",
        "unmapped_type": "boolean"
      }
    }
  ],
  "highlight": {
    "pre_tags": [
      "@kibana-highlighted-field@"
    ],
    "post_tags": [
      "@/kibana-highlighted-field@"
    ],
    "fields": {
      "*": {}
    },
    "require_field_match": False,
    "fragment_size": 2147483647
  },
  "query":
      {
    "filtered": {
      "query": {
        "query_string": {
          "query": "(referer:\"from=%s\" OR referer:\"from=lplqqbrowser\")  AND path:%s"%(self.source,self.path),
          "analyze_wildcard": True
        }
      }
  }
}
}
        return body

    def _getOrginData(self):
        body = self._getbody()
        print(body)
        data = self.es.search_data_from_es(index_name=self.index,body=body)
        if data != 'not found':
            orgin_data = data[u'hits'][u'hits']
            all_data = []
            for i in orgin_data:
                value = {}
                value['ip'] = i['_source']['clientip']
                value['path'] = i['_source']['path']
                referer = str(i['_source']['referer']);
                referer = referer.split("?")
                if "star.longzhu.com" in referer[0]:
                    host = re.split('com',referer[0])
                    value['host'] = host[0] + "com"
                    domain = host[1].split("/",1)
                    domain = domain[1]
                    value['domain'] = domain
                if "http://longzhu.com/" in referer[0]:
                    value['host'] = "http://longzhu.com/"
                    value['domain'] = "unkonw"
                if "cn" in referer[0]:
                    host = re.split('com',referer[0])
                    value['host'] = host[0] + "cn"
                    domain = "unkonw"
                    value['domain'] = domain
                source = referer[1].split("=")
                value['source'] = source[1]
                if i['_source'].has_key('cookies'):
                    userinfo = str(i['_source']['cookies']).split(";")
                    if "pluguest" in str(i['_source']['cookies']):
                        for k in userinfo:
                            if "pluguest" in k:
                                p1u_id = str(k).split("=")
                                value['pluguest'] = p1u_id[1]
                                break
                            else:
                                continue
                    else:
                        value['pluguest'] = self.get_random_data()
                    if "p1u_id" in str(i['_source']['cookies']):
                        for k in userinfo:
                            if "p1u_id" in k:
                                p1u_id = str(k).split("=")
                                uid = self.crypto_lib.decrypt(p1u_id[1])
                                value['uid'] = int(uid)
                                break
                            else:
                                continue
                    else:
                        value['uid'] = -1
                else:
                    value['pluguest'] = self.get_random_data()
                    value['uid'] = -1
                value['browsername'] = i['_source']['browser']['name']
                visittime = str(i['_source']['@timestamp'])
                visittime = visittime.split(".")
                visittime = self._unixTimeToLocalTime(self._formatTime(visittime[0],"%Y-%m-%dT%H:%M:%S"))
                value['visttime'] = visittime
                all_data.append(value)
            return all_data
        else:
            return None

    def add_data_to_db(self):
        all_data = self._getOrginData()
        if all_data != None:
            for i in all_data:
                self.star_longzhu.add_es_data_to_db(i)
        else:
            "find no data"

    def get_random_data(self):
        time_datas = str(time.time())
        time_data = time_datas.split(".")
        time_string = time_data[0] + time_data[1]
        random_data = str(random.randint(10000,99999))
        return time_string + random_data




