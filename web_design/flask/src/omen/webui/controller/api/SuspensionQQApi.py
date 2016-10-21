#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2016-06-21

from omen.webui.controller.api import api

from flask import request

import json

import time

from omen.db.SuspensionQQModel import SuspensionQQModel
from omen import wirte_log_to_file
@api.route("/api/findqq/",methods=['GET'])
def get_suspensionqq():
    suspension_qq = SuspensionQQModel()
    sort_col = request.args.get('sort_col');
    if sort_col == None:
        sort_col = 'CreatTime';
    sort_type = request.args.get('sort_type')
    if sort_type == None:
        sort_type = 'DESC'
    limit = request.args.get('max')
    if limit == None:
        limit = 5
    offset = int(request.args.get('start'))
    if offset == None:
        offset = 0;
    offset = offset*int(limit)
    data = suspension_qq.get_suspensionqq(fileds="QQ")
    info = "find suspension qq"
    wirte_log_to_file(info)
    total = len(data)
    data = suspension_qq.get_suspensionqq(limit = int(limit),offset=int(offset),sort_col=sort_col,order_type=sort_type)
    all_data = {
        "total" :total,
        "data" :data
    }
    return json.dumps(all_data)



