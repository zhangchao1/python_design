#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2016-1-29

import re

class base_regular_expression:
    '''
    万能正则表达式
    '''
    def match_type(self,match_type,str):
        match_num = re.compile(match_type)
        result = match_num.match(str)
        if result:
            return  result.group()
        else:
            return  False

    ######匹配电话号码的正则########
    '''
    "^1(3\d|5[^13]|8[^4])\d{8}$"
    '''
    #####匹配邮箱的正则##########
    '''
    "^\w+@\w+\.\w+([-.]\w+)*$"
    '''

