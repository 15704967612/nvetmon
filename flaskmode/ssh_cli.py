# -*- coding: utf-8 -*-
import json
import os
import time
import paramiko

from flaskmode.logger2 import Logger

logger = Logger()


# 连接方法
def ssh_connect(host: str):
    try:
        _private_key = paramiko.RSAKey.from_private_key_file(
            os.path.abspath(os.path.join(os.getcwd(), "keys", "id_rsa")))
        _ssh_fd = paramiko.SSHClient()
        _ssh_fd.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            _ssh_fd.connect(hostname=host, port=22, username="root", pkey=_private_key)
        except:
            log_msg = json.dumps({
                "datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "timestamp": time.time(),
                "ok": False,
                "code": 1122022,
                "data": "ssh root@%s Authentication failed." % host
            })
            logger.output(str(log_msg))
            _ssh_fd.close()
            return False
        _, stdout, stderr = _ssh_fd.exec_command('/opt/scripts/n9e_mon.sh', bufsize=-1, timeout=5)

        if len(stderr.read()) != 0:
            log_msg = json.dumps({
                "datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "timestamp": time.time(),
                "ok": False,
                "code": 1122021,
                "data": "ssh root@%s %s /opt/scripts/n9e_mon.sh Execute Failure" % host
            })
            logger.output(str(log_msg))
            _ssh_fd.close()
            return False
        else:
            log_msg = json.dumps({
                "datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "timestamp": time.time(),
                "ok": True,
                "code": 200,
                "data": "ssh root@%s /opt/scripts/n9e_mon.sh Execute Succeed" % host
            })
            logger.output(str(log_msg))
            _ssh_fd.close()
            return True

    except Exception as e:
        log_msg = json.dumps({
            "datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "timestamp": time.time(),
            "ok": False,
            "code": 1122022,
            "data": "ssh root@%s Connect Failure [%s]" % (host, e)
        })
        logger.output(str(log_msg))
        return False


def run_ssh(ips: list):
    for ip in ips:
        ssh_connect(ip)
