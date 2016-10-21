#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2016-06-15

from redis import Redis
import redis

class IPRedisService(object):
    def __init__(self, redis_config={},db=0):
        self.pool = redis.ConnectionPool(host = redis_config['hostname'], port = redis_config['port'], db = db);
        self.redis = redis.Redis(connection_pool=self.pool)
        print(self.redis)

    #add ip to redis
    def add_ip_redis(self,hash_key,ip_address):
        return self.redis.sadd(hash_key,ip_address)

    #remove ip from redis
    def remove_ip_from_redis(self,hash_key,ip_address):
            return self.redis.srem(hash_key,ip_address)
