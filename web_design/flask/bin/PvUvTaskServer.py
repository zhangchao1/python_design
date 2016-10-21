#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2016-06-14

import os, sys
parentdir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src");
if parentdir not in sys.path:
    sys.path.insert(0, parentdir);

from omen.tasks.getliveSourceTask import getliveSourceTask

import config

import argparse

#config#

url = config.es_config['url']

def get_parameters():
    parameters = argparse.ArgumentParser(description = "get pv")
    parameters.add_argument("-s",)
    parameters.add_argument("-p",)
    parameters.add_argument("-i",)
    args = parameters.parse_args()
    return args

command_lines = get_parameters()

getliveSource_task = getliveSourceTask(url = url,index = 'ns-2016.07.20',path = command_lines.p,
                                       host = command_lines.i,source = command_lines.s,
                                       encryptionKey= config.encryptionKey,
                                       validationKey = config.validationKey,
                                       db_config = config.db_config)
def run():
        getliveSource_task.add_data_to_db()

if __name__ == '__main__':

    run();