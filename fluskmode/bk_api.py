# -*- coding: utf-8 -*-
import json
import requests


class BkCmdb:
    """
    Tencent Cloud
    Blue Whale Interface
    """

    def __init__(self, host: str, **kw):
        self.bk_ip = host

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
                data = ""
                if len(val) > 0:
                    for _key in val:
                        data += val[_key] + " "
                    data = str(data.strip())
                    return data
                else:
                    return 408
