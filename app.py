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
import time

from flask import Flask
from flask import request, jsonify, render_template

from flaskmode import bk_api
from flaskmode import logic
from flaskmode.schedules import SchedulerConfig, scheduler
from flaskmode.validator import parameter
from flaskmode.ssh_cli import ssh_connect
from flaskmode.logger2 import Logger

__author__ = 'mc'

app = Flask(__name__)
app.debug = False
# 导入定时器配置
# app.config.from_object(SchedulerConfig())

# 导入配置文件
config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname('__file__')), 'app_conf.ini'))
bk_host = config["DEFAULT"]["Cmdb_Adder"]
BkUser = bk_api.BkCmdb(bk_host)
logger = Logger()


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
    filename = logic.configuration_file(name)
    if filename:
        return render_template(filename)
    else:
        return jsonify(dict(code=3999, msg="telegraf配置模板文件不存在"))


def timer():
    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    start_time = (datetime.datetime.now() + datetime.timedelta(minutes=-1)).strftime("%Y-%m-%d %H:%M:%S")
    update_info_ip = json.loads(BkUser.select_audit_log(start_time=start_time, end_time=end_time))
    if update_info_ip['ok'] and update_info_ip['code'] == 200:
        ips = update_info_ip['data']
        for _ip in ips:
            ssh_connect(host=_ip, username='root', cmd='/opt/scripts/n9e_mon.sh')
    else:
        log_msg = json.dumps({
            "datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "timestamp": time.time(),
            "ok": True,
            "code": 200,
            "data": "timer not update"
        })
        logger.output(log_msg)


def _init_ok(app):

    def _init_tasks():
        app.config.from_object(SchedulerConfig())
        scheduler.init_app(app)
        scheduler.start()
        app.run(host="0.0.0.0", port=23456, use_reloader=False)

    def _init_app():
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
        # app.run(host="0.0.0.0", port=23456, use_reloader=False)

    if platform.system() != 'Windows':
        f = open("scheduler.lock", "wb")

        def unlock():
            fcntl.flock(f, fcntl.LOCK_UN)
            f.close()

        atexit.register(unlock)

        _init_app()

        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            _init_tasks()

        except Exception as e:
            print(e)
        pass


if __name__ != '__main__':
    _init_ok(app)


if __name__ == '__main__':
    _init_ok(app)

