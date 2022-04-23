# -*- coding: utf-8 -*-
# encoding:utf-8
# validator.py
import re
from flask import request, jsonify

__author__ = 'mc'


def __check_ip(ipaddr):
    compile_ip = re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}| \
                            2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    if compile_ip.match(ipaddr):
        return True
    else:
        return False


def __check_name(name):
    compile_name = re.compile('^([a-zA-Z]\w.+$)')
    if compile_name.match(name):
        return True
    else:
        return False


def parameter(tag: str):
    """检查参数合法性"""

    def _parameter(func):

        def _check(*args, **kwargs):
            if len(request.args.keys()) == 0:
                return jsonify(dict(code=4010, msg="请输入参数"))
            # if len(request.args.keys()) > 1:
            #     return jsonify(dict(code=4011, msg="参数不合法"))
            if tag == "ip":
                ip = request.args.get("ip", "")
                if not ip:
                    return jsonify(dict(code=4012, msg="缺少IP参数"))
                if not __check_ip(ip):
                    return jsonify(dict(code=4013, msg="IP格式错误"))
            elif tag == "name":
                name = request.args.get("name", "")
                if not name:
                    return jsonify(dict(code=4022, msg="缺少name参数"))
                if not __check_name(name):
                    return jsonify(dict(code=4023, msg="Name格式错误"))

            return func(*args, **kwargs)

        return _check

    return _parameter
