#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author zhangchao 2016-06-14


from flask import Blueprint, render_template, redirect, url_for, request
from werkzeug.contrib.cache import SimpleCache
import json
omen_app = Blueprint('omen_app', __name__,)

@omen_app.route('/')
def index():
    return render_template("home.html")

@omen_app.route('/add/',methods=['POST'])
def add_ip_limit_value():
    ip_values = request.data
    cache = SimpleCache
    cache.set("limit_ip",ip_values)
    return json.dumps({'status' : 'ok'})


@omen_app.route('/serach_ip/')
def find_suspension_ip_by_time():
    return render_template("search_ip.html")

@omen_app.route('/realtime_ip/')
def suspension_ip_real_time():
    return render_template("realtime_ip.html")

@omen_app.route('/realtime_qq/')
def suspension_qq_real_time():
    return render_template("realtime_qq.html")

@omen_app.route('/realtime_api/')
def api_viste_total():
    return render_template("realtime_api.html")

@omen_app.route('/search_api/')
def search_api_viste_total():
    return render_template("search_api.html")

@omen_app.route('/all_web/realtime/visit')
def all_web_realtime_visit():
    return render_template("all_web_realtime_visit.html")
