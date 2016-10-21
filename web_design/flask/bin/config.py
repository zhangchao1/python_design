#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2016-07-01

es_config = {
    'url':['http://172.16.9.80:9200/'],
    'index':"ns",
    'path':'path:otv2',
    'timeout':120
}
redis_config = {
            'hostname': '172.16.9.225',
            'port'    :  6389,
            'timeout' :  600,
            'pconnect':  1
}

db_config = {
    'host'	 : '172.16.9.10',
    'username'	: 'root',
    'password':'',
    'port':3306,
    'database' :'omen'
}
encryptionKey = 'C13FD92094A3765769C7158484842BA84948F73903DE637001AB61CD2D7878EC'
validationKey = 'DD331A821B88A0BF0199560D1A0C5F16'

