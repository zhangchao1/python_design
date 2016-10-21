#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2016-06-21

import datetime
from omen.lib.elasticsearchLib import elasticsearchLib
from omen.db.SuspensionQQModel import SuspensionQQModel
import logging
logging.basicConfig(level = logging.INFO)
class AddSuspensionQQService:

    def add_suspension_qq(self,url,index,path,re_pattern = "\d{5,}-{4}.{5,17}-{4}"):
        logging.info(" add_suspension_qq start ")
        elasticsearch_service = elasticsearchLib(url)
        suspension_qq_model = SuspensionQQModel()
        suspension_qq = elasticsearch_service.get_suspension_qq(index=index,path=path,re_pattern=re_pattern)
        if suspension_qq != 'notfound':
            for i in suspension_qq:
                check_qq_is_exist = suspension_qq_model.check_qq_is_in_db(i)
                if check_qq_is_exist:
                    if check_qq_is_exist['Password'] == suspension_qq[i]:
                        continue
                    else:
                        suspension_qq_model.update_qq_password(qq=i,Password = suspension_qq[i])
                else:
                    qq_data = {}
                    qq_data['QQ'] = i;
                    qq_data['Password'] = suspension_qq[i]
                    qq_data['CreatTime'] = str(datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S'))
                    logging.info(" add qq to db")
                    suspension_qq_model.add_qq_to_db(qq_data=qq_data)
# test = AddSuspensionQQService()
# test.add_suspension_qq(['http://172.16.9.80:9200/'],"*","path:otv2")
