# -*- coding: utf-8 -*-
import asyncio
import configparser
import datetime
import json
import logging
import os
import time

from flask import Flask, current_app
from flask import request, jsonify, render_template

from fluskmode import bk_api
from fluskmode import logic
from fluskmode.schedules import SchedulerConfig, scheduler
from fluskmode.validator import parameter
from fluskmode.ssh_cli import ssh_connect

__author__ = 'mc'

app = Flask(__name__)
app.debug = False
# 导入定时器配置
app.config.from_object(SchedulerConfig())

# 导入配置文件
config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname('__file__')), 'app_conf.ini'))
host = config["DEFAULT"]["Cmdb_Adder"]

BkUser = bk_api.BkCmdb(host)


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
        task_list = [ssh_connect(host=_ip, username='admin', cmd='/opt/scripts/automon.sh') for _ip in ips]
        done, peding = asyncio.run(asyncio.wait(task_list))
    else:
        pass


if __name__ != '__main__':
    # 如果不是直接运行，则将日志输出到 gunicorn 中
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


if __name__ == '__main__':
    # 初始化定时器
    scheduler.init_app(app)
    # 启动定时器，默认后台启动了
    scheduler.start()
    # 启动app
    app.run(host="0.0.0.0", port=23456, use_reloader=False)
