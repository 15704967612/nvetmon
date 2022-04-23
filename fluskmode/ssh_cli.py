import asyncio
import json
import os

import paramiko


# 连接方法
async def ssh_connect(host: str, username: str, cmd: str):
    try:
        loop = asyncio.get_event_loop()

        def _ssh_connect():
            _private_key = paramiko.RSAKey.from_private_key_file(
                os.path.abspath(os.path.join(os.getcwd(), "keys", "id_rsa")))
            _ssh_fd = paramiko.SSHClient()
            _ssh_fd.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            _ssh_fd.connect(hostname=host, port=22, username=username, pkey=_private_key)
            stdin, stdout, stderr = _ssh_fd.exec_command(cmd)
            if len(stderr.read()) != 0:
                


            _ssh_fd.close()

        future = loop.run_in_executor(None, _ssh_connect)
        await future

    except Exception as e:
        print('ssh %s@%s: %s' % (username, host, e))
        return json.dumps({"ok": False, "code": 1122021, "data": "ssh %s@%s 连接失败" % (username, host)})


