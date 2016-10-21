#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2016-06-14


from flask import Flask

def register_blueprint(app):
    from omen.webui.controller.index import omen_app
    app.register_blueprint(omen_app)
    from omen.webui.controller.api import api
    app.register_blueprint(api)
app = Flask(__name__)
register_blueprint(app)
