# -*- coding: utf-8 -*-

import asyncio
import atexit
import configparser
import datetime
import fcntl
import json
import logging
import os
import platform
import subprocess
import time
import random

from flask import Flask
from flask import request, jsonify, render_template, redirect

from flaskmode import bk_api
from flaskmode import logic
from flaskmode.validator import parameter
from flaskmode.ssh_cli import ssh_connect
from flaskmode.logger2 import Logger
from multiprocessing import Queue

from flask_apscheduler import APScheduler

__author__ = 'mc'

app = Flask(__name__)
app.debug = True


class SchedulerConfig(object):
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'


scheduler = APScheduler()
app.config.from_object(SchedulerConfig())

# 导入配置文件
config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname('__file__')), 'app_conf.ini'))
bk_host = config["DEFAULT"]["Cmdb_Adder"]
BkUser = bk_api.BkCmdb(bk_host)
logger = Logger()

q = Queue()


@app.route('/api/v1/mon/inputs', methods=["GET"], endpoint="mon_inputs")
@parameter('ip')
def mon_inputs():
    """获取telegraf配置信息"""
    ip = request.args.get("ip")
    host = json.loads(BkUser.select_host_id(ip))
    if not bool(host['ok']) and host['code'] == 200:
        return jsonify(dict(ok=False, code=200, data="Host不存在"))

    host_telegraf = json.loads(BkUser.select_host_telegraf(ip))
    if not host_telegraf['ok'] and host_telegraf['code'] == 200:
        return jsonify(dict(ok=False, code=200, data="TeleConf不存在"))

    return jsonify(dict(ok=True, code=200, data=host_telegraf['data']))


@app.route('/api/v1/mon/conf', methods=["GET"], endpoint="mon_files")
@parameter('name')
def mon_files():
    """获取telegraf模板文件"""
    name = request.args.get("name")
    context_dict = {"ip": request.args.get("ip"),
                    "port": request.args.get("port"),
                    "user": request.args.get("user"),
                    "password": request.args.get("password")
                    }
    filename = logic.configuration_file(name)
    if filename:
        return render_template(filename, context_dict=context_dict)
    else:
        _file_name = os.path.join(os.getcwd(), 'templates', name + '.conf')
        # Alpine
        command = "telegraf --input-filter %s config | sed -n '/\[\[inputs.%s\]\]/,$p' > %s" % (name, name, _file_name)
        # MaxOS Test
        # command = "./bin/telegraf -config ./bin/telegraf.conf --input-filter %s config | " \
        #           "sed -n '/\[\[inputs.%s\]\]/,$p' > %s" % (name, name, _file_name)
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)

        return jsonify(dict(code=3999, msg="telegraf配置模板文件不存在"))


@scheduler.task('interval', id='do_job_1', seconds=60, misfire_grace_time=900)
def production():
    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    start_time = (datetime.datetime.now() + datetime.timedelta(minutes=-1)).strftime("%Y-%m-%d %H:%M:%S")
    update_info_ip = json.loads(BkUser.select_audit_log(start_time=start_time, end_time=end_time))

    if update_info_ip['ok'] and update_info_ip['code'] == 200:
        ips = update_info_ip['data']
        for ip in ips:
            q.put(str(ip))
    else:
        ret = json.dumps({
            "datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "timestamp": time.time(),
            "ok": True,
            "code": 200,
            "data": "timer not update"
        })
        logger.output(ret)


@scheduler.task('interval', id='do_job_2', seconds=5, misfire_grace_time=900)
def consumer():
    if not q.empty():
        ip = q.get()
        ssh_connect(ip)


if __name__ != '__main__':
    scheduler.init_app(app)
    scheduler.start()
    app.run(host="0.0.0.0", port=23456, use_reloader=False)

if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    app.run(host="0.0.0.0", port=23456, use_reloader=False)
