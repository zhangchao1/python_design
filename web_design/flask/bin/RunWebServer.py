#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2016-06-14

import os, sys
parentdir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src");
if parentdir not in sys.path:
    sys.path.insert(0, parentdir);
import config
from omen.webui import app

def run():
    app.config['es_host']  = config.es_config['url']
    app.config['es_timeout']  = config.es_config['timeout']
    app.run()
run()
