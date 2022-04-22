# -*- coding: utf-8 -*-
import requests
import json


class BkCmdb(object):
    """
    Tencent Cloud
    Blue Whale Interface
    """

    def __init__(self):
        self.bk_ip = 'http://172.18.9.218:33032'
        #
        self.headers = {
            'Content-Type': 'application/json',
            'HTTP_BLUEKING_SUPPLIER_ID': '0',
            'BK_USER': 'api',
        }

    # 信息查询
    def select(self, bk_host_innerip, bk_biz_id=int(3), start=int(0), limit=int(100)):
        """ 查询主机信息 """
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
        """
        状态码说明:
        1、400 网络异常
        2、404 主机不存在
        3、408 监控信息不存在
        """
        try:
            r = requests.post(url, headers=self.headers, data=data)
        except requests.exceptions.ConnectionError:
            return 400
        except requests.exceptions.Timeout:
            return 400
        except:
            return 400
        else:
            val = r.json()['data']
            if val['count'] == 0:
                return 404
            else:
                val = val['info'][0]['host']
                pop_keys = ['bk_cloud_id', 'bk_host_id']
                [val.pop(k) for k in pop_keys]
                filter_msg = "#"
                if len(val) > 0:
                    for valkey in val:
                        filter_msg += val[valkey] + "#"
                    return filter_msg
                else:
                    return 408

