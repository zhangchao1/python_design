#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2016-06-16

import os, sys
parentdir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src");
if parentdir not in sys.path:
    sys.path.insert(0, parentdir);

from omen.tasks.UnblockIpTask import UnblockIpTask
from omen.tasks.lockIpTask import lockIpTask
from omen.tasks.getliveSourceTask import getliveSourceTask
from omen.service.AddSuspensionQQService import AddSuspensionQQService
import config
#####config#######
url = config.es_config['url']
index =config.es_config['index']
path = config.es_config['path']
redis_config = config.redis_config
##################
unblock_ip_task = UnblockIpTask(redis_config=redis_config)
lock_ip_task = lockIpTask(url=url,index=index,path=path,redis_config = redis_config)

def run():
    unblock_ip_task.unblockIp()
    lock_ip_task.run()
    AddSuspensionQQService().add_suspension_qq(url,index="*",path = path)

if __name__ == '__main__':
    while 1:
        run();
