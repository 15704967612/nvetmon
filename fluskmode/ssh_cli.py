# -*- coding: utf-8 -*-
import json
import os
import time
import paramiko

from fluskmode.logger2 import Logger

logger = Logger()


# 连接方法
def ssh_connect(host: str, username: str, cmd: str):
    try:
        _private_key = paramiko.RSAKey.from_private_key_file(
            os.path.abspath(os.path.join(os.getcwd(), "keys", "id_rsa")))
        _ssh_fd = paramiko.SSHClient()
        _ssh_fd.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        _ssh_fd.connect(hostname=host, port=22, username=username, pkey=_private_key)
        _, stdout, stderr = _ssh_fd.exec_command(cmd)

        if len(stderr.read()) != 0:
            log_msg = json.dumps({
                "datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "timestamp": time.time(),
                "ok": False,
                "code": 1122021,
                "data": "ssh %s@%s %s 执行失败" % (username, host, cmd)
            })
            Logger.output(log_msg)
        else:
            log_msg = json.dumps({
                "datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "timestamp": time.time(),
                "ok": True,
                "code": 200,
                "data": "ssh %s@%s %s 执行成功" % (username, host, cmd)
            })
            logger.output(log_msg)

        _ssh_fd.close()

    except Exception as e:
        log_msg = json.dumps({
            "datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "timestamp": time.time(),
            "ok": False,
            "code": 1122022,
            "data": "ssh %s@%s 连接失败 [%s]" % (username, host, e)
        })
        Logger.output(log_msg)
