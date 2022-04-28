# -*- coding: utf-8 -*-
import json
import requests


class BkCmdb:
    """
    Tencent Cloud
    Blue Whale Interface
    """

    def __init__(self, bk_host: str, **kw):
        self.bk_ip = bk_host

        self.headers = {
            'Content-Type': 'application/json',
            'HTTP_BLUEKING_SUPPLIER_ID': '0',
            'BK_USER': 'api',
        }

    def select_host_id(self, bk_host_innerip, bk_biz_id=int(3), start=int(0), limit=int(100)):
        """ 查询主机ID """
        url = self.bk_ip + '/api/v3/hosts/search'
        data = json.dumps({
            "page": {
                "start": start,
                "limit": limit,
                "sort": ""
            },
            "pattern": "",
            "bk_biz_id": bk_biz_id,
            "ip": {
                "flag": "bk_host_innerip|bk_host_outerip",
                "exact": 1,
                "data": [bk_host_innerip, ]
            },
            "condition": [
                {
                    "bk_obj_id": "host",
                    "fields": ['bk_host_innerip'],
                    "condition": []
                },
            ]
        })
        try:
            r = requests.post(url, headers=self.headers, data=data)
        except requests.exceptions.ConnectionError:
            return json.dumps({"ok": False, "code": 1122011, "data": "蓝鲸系统连接错误"})
        except requests.exceptions.Timeout:
            return json.dumps({"ok": False, "code": 1122012, "data": "蓝鲸系统连接超时"})
        msg = json.loads(r.text)['data']
        if int(msg['count']) == 0:
            return json.dumps({"ok": False, "code": 200, "data": ""})

        return json.dumps({"ok": True, "code": 200, "data": msg['info'][0]['host']['bk_host_id']})

    # 信息查询
    def select_host_telegraf(self, bk_host_innerip, bk_biz_id=int(3), start=int(0), limit=int(100)):
        """ 查询主机telegraf信息 """
        url = self.bk_ip + '/api/v3/hosts/search'
        data = json.dumps({
            "page": {
                "start": start,
                "limit": limit,
                "sort": ""
            },
            "pattern": "",
            "bk_biz_id": bk_biz_id,
            "ip": {
                "flag": "bk_host_innerip|bk_host_outerip",
                "exact": 1,
                "data": [bk_host_innerip, ]
            },
            "condition": [
                {
                    "bk_obj_id": "host",
                    "fields": ['bk_monitor_input1', 'bk_monitor_input2', 'bk_monitor_input3',
                               'bk_monitor_input4', 'bk_monitor_input5', 'bk_monitor_input6'],
                    "condition": []
                },
            ]
        })
        try:
            r = requests.post(url, headers=self.headers, data=data)
        except requests.exceptions.ConnectionError:
            return json.dumps({"ok": False, "code": 1122013, "data": "蓝鲸系统连接错误"})
        except requests.exceptions.Timeout:
            return json.dumps({"ok": False, "code": 1122014, "data": "蓝鲸系统连接超时"})

        dater = r.json()['data']['info'][0]['host']
        strd = ""
        for _keys in dater:
            if int(str(_keys).find('bk_monitor_input')) != int(-1):
                strd += dater[_keys] + " "
        if len(strd.strip()) == 0:
            return json.dumps({"ok": False, "code": 200, "data": strd.strip()})
        return json.dumps({"ok": True, "code": 200, "data": strd.strip()})

    def select_audit_log(self, start_time, end_time):
        """查询操作审计日志"""
        url = self.bk_ip + "/api/v3/audit/search"
        data = json.dumps({
            "condition": {
                "bk_biz_id": int(3),
                "op_target": "host",
                "op_time": [
                    start_time,
                    end_time
                ]
            },
            "start": 0,
            "limit": 200,
            "sort": "-create_time"
        })
        try:
            r = requests.post(url, headers=self.headers, data=data)
        except requests.exceptions.ConnectionError:
            return json.dumps({"ok": False, "code": 1122015, "data": ""})
        except requests.exceptions.Timeout:
            return json.dumps({"ok": False, "code": 1122016, "data": ""})

        dater = r.json()['data']

        if dater['count'] == 0:
            return json.dumps({"ok": False, "code": 200, "data": ""})

        valid = []
        for _host in dater['info']:
            if str(_host['operator']) == "api":
                pass
            else:
                valid.append(_host['content']['cur_data']['bk_host_innerip'])
        valid = list(set(valid))
        return json.dumps({"ok": True, "code": 200, "data": valid})
