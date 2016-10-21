#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2016-06-13

from elasticsearch import Elasticsearch
import json
import datetime
import operator
import time
import re
from omen import wirte_log_to_file

class elasticsearchLib:
    # init

    #es查询时间，时间间隔数据
    timsSpan = {
        '1m':'0.1m',
        '5m':'0.5m',
        '15m':'1m',
        '30m':'1m',
        '1h' :'2m',
        '4h' :'8m',
        '1d' :'1h',
        '4d' :'4h',
        '7d' :'6h'
    }
    rangeSpan = {
        '1m':1,
        '5m':5,
        '15m':15,
        '30m':30,
        '1h' :60,
        '4h' :240,
        '1d' :1440,
        '4d' :4320,
        '7d' :8640
    }

    def __init__(self,url = [],timeout=60):
        if len(url)>1:
            self.es = Elasticsearch(url,sniffer_timeout=timeout,sniff_on_start=True,sniff_on_connection_fail=True,maxsize=25)
        else:
            self.es = Elasticsearch(url,sniffer_timeout=timeout)
    #search data from es
    def getDataByIndex(self,index,path,rangeMinute =5,sort = True,lte = datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')):
        lte = self._formatTime(lte)
        lte = str(lte)
        lte = lte.split(".")
        lte = int(lte[0])*1000
        index_time = time.strftime('%Y.%m.%d',time.localtime(lte/1000))
        body = {
            "query": {
            "filtered": {
            "query": {
                 "query_string": {
                "query": "*",
                "analyze_wildcard": True
                }
            },
            "filter": {
                "bool": {
                    "must": [
            {
                "query": {
                "query_string": {
                  "query": "*",
                  "analyze_wildcard": True
                }
              }
            },
            {
              "range": {
                "@timestamp": {
                  "gte": self._range(lte,rangeMinute),
                  "lte": lte,
                  "format": "epoch_millis"
                    }
                 }
                }
            ],
          "must_not": []
            }
         }
        }
        },
            "size": 0,
            "aggs": {
            "2": {
            "terms": {
            "field": "geoip.ip",
            "size": 10,
            "order": {
            "_count": "desc"
                        }
                    }
                }
            }
        }
        print(body)
        index = index + "-%s"%index_time
        print(index)
        info = "get ip_data: index->%s,body->%s"%(index,str(body))
        wirte_log_to_file(info)
        try:
            all_data = self.es.search(index = index,body = body)
            ip = all_data['aggregations'];
            ip_sum = ip['2']['buckets']
            ip_data = {}
            for i in ip_sum:
                ip_data[i['key']] = i['doc_count']
            ip_data = sorted(ip_data.iteritems(),key= lambda x:x[1],reverse=sort)
            info = "get all_ip: %s"%(str(ip_data))
            wirte_log_to_file(info)
            return ip_data
        except Exception as e:
            return "notfound"

    # 获取当前时间到上一段的时间的unix时间
    def _range(self,nowtime,rangenum =0):

        return nowtime - rangenum*60*1000

    def _formatTime(self,lteTime,type="%Y.%m.%d %H:%M:%S"):
        return time.mktime(time.strptime(lteTime,type))

    # all_data[u'hits'][u'hits'][3][u'_source'][u'cookies']
    def get_suspension_qq(self,index,path,re_pattern):
        lte = str(time.time())
        lte = lte.split(".")
        lte = int(lte[0])*1000
        gte = self._range(lte,5)
        body= {
            "query": {
            "filtered": {
            "query": {
                "query_string": {
                "analyze_wildcard": True,
                "query": path
            }
        },
        "filter": {
                "bool": {
                "must": [
                {
                    "range": {
                    "@timestamp": {
                    "gte": gte,
                    "lte": lte,
                    "format": "epoch_millis"
                    }
                }
                }
            ],
            "must_not": []
            }
         }
        }
        },
    "aggs": {}
    }
        print(body);
        print(index);
        info = "get suspension_qq: index->%s,body->%s"%(index,str(body))
        wirte_log_to_file(info)
        try:
            all_data = self.es.search(index = index,body = body)
            all_data = all_data['hits']['hits']
            qq_number = {}
            match_num = re.compile(re_pattern)
            for i in all_data:
                if i['_source'].has_key('cookies'):
                    qq_n = match_num.search(str(i['_source']['cookies']))
                    if qq_n:
                        suspension_user = qq_n.group()
                        print(suspension_user)
                        suspension_user = suspension_user.split("----",2)
                        qq_number[suspension_user[0]] = suspension_user[1]
                else:
                    continue
            info = "get qq : %s"%(qq_number)
            wirte_log_to_file(info)
            return qq_number
        except Exception as e:
            return "notfound"

    def get_realtime_api(self,index,api_name,start,end,type):
        lte = self._formatTime(end,"%Y-%m-%d %H:%M:%S")
        lte = str(lte)
        lte = lte.split(".")
        lte = int(lte[0])*1000
        lte = lte-1000
        print(lte)
        gte = self._formatTime(start,"%Y-%m-%d %H:%M:%S")
        gte = str(gte)
        gte = gte.split(".")
        gte = int(gte[0])*1000
        print(gte)
        body = {
                "size": 0,
                "sort": [
                {
                    "@timestamp": {
                    "order": "desc",
                    "unmapped_type": "boolean"
                }
            }
        ],
            "query": {
            "filtered": {
            "query": {
            "query_string": {
            "analyze_wildcard": True,
            "query": "site:%s"%api_name
            }
        },
        "filter": {
        "bool": {
          "must": [
            {
              "range": {
                "@timestamp": {
                  "gte": gte,
                  "lte": lte,
                  "format": "epoch_millis"
                 }
                }
             }
            ],
          "must_not": []
         }
         }
         }
        },
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
    "aggs": {
            "2": {
            "date_histogram": {
            "field": "@timestamp",
            "interval": self.timsSpan[type],
            "time_zone": "Asia/Shanghai",
            "min_doc_count": 0,
            "extended_bounds": {
            "min": gte,
            "max": lte
            }
        }
        }
    },
    "fields": [
        "*",
        "_source"
        ],
        "script_fields": {},
        "fielddata_fields": [
        "@timestamp"
        ]
    }
        print(body)
        info = "get realtime_api : index->%s,body->%s"%(index,str(body))
        wirte_log_to_file(info)
        all_data = self.es.search(index=index,body = body)
        all_data = all_data['aggregations']['2']['buckets']
        api_count = []
        print(all_data)
        for i in all_data:
            if type == '15m' or type == '30m'or type == '1h' or type == '4h' or type=='5m' or type=='1m':
                key = time.strftime("%H:%M:%S",time.localtime(i['key']/1000))
            elif type == '1d' or type == '4d'or type == '7d':
                key = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(i['key']/1000))
            value = i['doc_count']
            value_all = key + '?' +str(value)
            api_count.append(value_all)
        info = "realtime_api : %s"%(str(api_count))
        wirte_log_to_file(info)
        return api_count

    def search_api_relatime(self,index,website_name,api_name,type):
        lte = str(time.time())
        lte = lte.split(".")
        lte = int(lte[0])*1000
        gte = self._range(lte,self.rangeSpan[type])
        body = {
            "size": 0,
            "query": {
            "filtered": {
            "query": {
                "query_string": {
            "analyze_wildcard": True,
            "query": 'site:%s AND path:%s'%(website_name,api_name)
            }
        },
        "filter": {
            "bool": {
            "must": [
                {
                "range": {
                    "@timestamp": {
                    "gte": gte,
                    "lte": lte,
                    "format": "epoch_millis"
                    }
                }
            }
          ],
          "must_not": []
        }
      }
    }
  },
  "aggs": {
    "2": {
      "date_histogram": {
        "field": "@timestamp",
        "interval": self.timsSpan[type],
        "time_zone": "Asia/Shanghai",
        "min_doc_count": 1,
        "extended_bounds": {
          "min": gte,
          "max": lte
        }
      }
    }
  }
}
        print(body)
        info = "api_relatime : index->%s body->%s"%(index,str(body))
        wirte_log_to_file(info)
        try:
            all_data = self.es.search(index=index,body=body)
            all_data = all_data['aggregations']['2']['buckets']
            api_count = []
            for i in all_data:
                if type == '15m' or type == '30m'or type == '1h' or type == '4h' or type=='5m' or type=='1m':
                    key = time.strftime("%H:%M:%S",time.localtime(i['key']/1000))
                elif type == '1d' or type == '4d'or type == '7d':
                    key = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(i['key']/1000))
                value = i['doc_count']
                value_all = key + '?' +str(value)
                api_count.append(value_all)
            info = "api_relatime : %s"%(str(api_count))
            wirte_log_to_file(info)
            return api_count
        except Exception as e:
            return 'not found'

    def get_all_website_name(self,index,is_all = True,rangeminute =20):
        lte = str(time.time())
        lte = lte.split(".")
        lte = int(lte[0])*1000
        gte = self._range(lte,rangeminute)
        body = {
        "size": 0,
                "query": {
                "filtered": {
                "query": {
                "query_string": {
                "query": "*",
                "analyze_wildcard": True
            }
        },
            "filter": {
            "bool": {
            "must": [
            {
                "range": {
                    "@timestamp": {
                    "gte": gte,
                    "lte": lte,
                    "format": "epoch_millis"
                    }
                }
                }
            ],
            "must_not": []
            }
        }
        }
    },
    "aggs": {
        "2": {
        "terms": {
            "field": "site",
            "size": 200,
            "order": {
            "_count": "desc"
            }
        }
        }
        }
        }
        print(body)
        info = "all_website_name : index->%s body->%s"%(index,str(body))
        wirte_log_to_file(info)
        try:
            all_data = self.es.search(index=index,body=body)
            all_data = all_data['aggregations']['2']['buckets']
            all_web_site = []
            if is_all:
                all_web_site.append("all")
            for i in all_data:
                all_web_site.append(i['key'])
            info = "all_website_name : %s"%(str(all_web_site))
            wirte_log_to_file(info)
            return all_web_site
        except Exception as e:
            return 'not found'

    def get_all_api_from_website(self,index,website_name,rangeminute =20,total=100):
        lte = str(time.time())
        lte = lte.split(".")
        lte = int(lte[0])*1000
        gte = self._range(lte,rangeminute)
        body = {
            "size": 0,
            "query": {
            "filtered": {
            "query": {
                "query_string": {
                "analyze_wildcard": True,
                "query": "*"
            }
        },
        "filter": {
            "bool": {
            "must": [
                {
                "range": {
                    "@timestamp": {
                    "gte": gte,
                    "lte": lte,
                    "format": "epoch_millis"
                    }
                }
                }
            ],
                "must_not": []
            }
        }
        }
    },
        "aggs": {
        "2": {
            "filters": {
                "filters": {
                website_name: {
                    "query": {
                    "query_string": {
                    "query": website_name,
                    "analyze_wildcard": True
                 }
             }
          }
        }
      },
      "aggs": {
        "3": {
          "terms": {
            "field": "path",
            "size": total,
            "order": {
              "_count": "desc"
            }
          }
        }
      }
    }
  }
}
        print(body)
        try:
            all_data = self.es.search(index=index,body=body)
            all_data = all_data['aggregations']['2']['buckets'][website_name]['3']['buckets']
            all_api_for_web_site = []
            for i in all_data:
                all_api_for_web_site.append(i['key'])
            return all_api_for_web_site
        except Exception as e:
            return 'not found'

    def get_all_china_visit(self,index,rangeminute=1,total = 1000):
        lte = str(time.time())
        lte = lte.split(".")
        lte = int(lte[0])*1000
        gte = self._range(lte,rangeminute)
        body = {
  "size": 0,
  "query": {
    "filtered": {
      "query": {
        "query_string": {
          "query": "geoip.country_name:China",
          "analyze_wildcard": True
        }
      },
      "filter": {
        "bool": {
          "must": [
            {
              "range": {
                "@timestamp": {
                  "gte": gte,
                  "lte": lte,
                  "format": "epoch_millis"
                }
              }
            }
          ],
          "must_not": []
        }
      }
    }
  },
  "aggs": {
    "2": {
      "terms": {
        "field": "geoip.city_name",
        "size": 0,
        "order": {
          "_count": "desc"
        }
      },
      "aggs": {
        "3": {
          "terms": {
            "field": "geoip.longitude",
            "size": 0,
            "order": {
              "_count": "desc"
            }
          },
          "aggs": {
            "4": {
              "terms": {
                "field": "geoip.latitude",
                "size": 0,
                "order": {
                  "_count": "desc"
                }
              }
            }
          }
        }
      }
    }
  }
}
        print(body)
        info = "get_all_china_visit : index->%s body->%s"%(index,str(body))
        wirte_log_to_file(info)
        high_item = []
        middle_item = []
        min_item = []
        all_count = {}
        first_item_count = []
        final_data = {}
        try:
            all_data = self.es.search(index=index,body=body)
            all_data = all_data[u'aggregations'][u'2'][u'buckets']
            for i in range(0,len(all_data)):
                first_item_count.append(all_data[i]['doc_count'])
                all_count[i] = all_data[i]['doc_count']
            item_count = list(set(first_item_count))
            item_count = sorted(item_count)
            item_len = len(item_count)
            middle_len = int(item_len*0.33)
            max_len = int(item_len*0.67)
            middle_count = item_count[middle_len]
            max_count = item_count[max_len]
            for i in range(0,len(all_data)):
                value = {}
                geoCoord = []
                value['name'] =  all_data[i]['key']
                value['value'] = all_data[i]['doc_count']
                geoCoord.append(all_data[i]['3']['buckets'][0]['key'])
                geoCoord.append(all_data[i]['3']['buckets'][0]['4']['buckets'][0]['key'])
                value['geoCoord'] = geoCoord
                if  value['value'] > max_count:
                    high_item.append(value)
                elif  value['value'] > middle_count and value['value'] < max_count:
                    middle_item.append(value)
                elif  value['value'] < middle_count and  value['value'] > 0 :
                    min_item.append(value)
            total_count = sum(e for  k,e in all_count.items())
            final_data['is_success']= True
            sum_data = {}
            sum_data['low'] = min_item
            sum_data['middle'] = middle_item
            sum_data['high'] = high_item
            final_data['data'] = sum_data
            final_data['msg'] = 'suceess'
            final_data['total'] = total_count
            return final_data
        except Exception as e:
            final_data['is_success']= False
            return final_data

    def search_data_from_es(self,index_name,body={}):
        try:
            all_data =  self.es.search(index=index_name,body=body)
            return all_data
            # es_data =  self.es.search(
            #      index=index_name,
            #      doc_type='logs',
            #      from_ = 0,
            #      size = 1,
            #      body=body
            # )
            # _size = 100;
            # import math;
            # totalCount = es_data['hits']['total']
            # _totalPage = math.ceil(totalCount /_size)
            # _currentPage = 0;
            # while (_currentPage > _totalPage):
            #     _from = _currentPage * _size
            #     es_data =  self.es.search(
            #         index=index_name,
            #         doc_type='logs',
            #         from_ = _from,
            #         size = _size,
            #         body=body
            #     )
            #     yield es_data
        except Exception as e:
            return 'not found'


