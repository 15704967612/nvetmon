# -*- coding: utf-8 -*-
from flask import Flask
from flask import request, jsonify, render_template
from fluskmode import bk_api
from fluskmode.validator import parameter
from fluskmode import logic

__author__ = 'mc'

app = Flask(__name__)
app.debug = True
BkUser = bk_api.BkCmdb()


@app.route('/api/v1/mon/inputs', methods=["GET"], endpoint="mon_inputs")
@parameter('ip')
def mon_inputs():
    """获取telegraf配置信息"""
    ip = request.args.get("ip")
    info = BkUser.select(ip)
    if info == 400:
        return jsonify(dict(code=3990, msg="CMDB网络连接异常"))
    elif info == 404:
        return jsonify(dict(code=3991, msg="Host信息不存在"))
    elif info == 408:
        return jsonify(dict(code=3992, msg="Telegraf配置信息不存在"))
    else:
        return str(info)


@app.route('/api/v1/mon/conf', methods=["GET"], endpoint="mon_files")
@parameter('name')
def mon_files():
    """获取telegraf配置文件"""
    name = request.args.get("name")
    filename = logic.configuration_file(name)
    if filename:
        return render_template(filename)
    else:
        return jsonify(dict(code=3999, msg="telegraf配置模板文件不存在"))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=23456)
