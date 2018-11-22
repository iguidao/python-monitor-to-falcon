#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""{"leader":"2998b57f5ea51c6b","followers":{"2a5fb1d2700e7390":{"latency":{"current":0.001134,"average":0.001811088994566386,"standardDeviation":0.0014273669646051007,"minimum":0.000653,"maximum":2.538844},"counts":{"fail":0,"success":72434561}},"82e636fcd3e2c73c":{"latency":{"current":0.001518,"average":0.0019875461865150796,"standardDeviation":0.0014614747902608216,"minimum":0.000648,"maximum":1.658805},"counts":{"fail":0,"success":74746164}}}}
"""

import socket
import requests
import time
from StringIO import StringIO
from decimal import Decimal
from  etcd_metric import ( 
    #etcd_leader_latency, 
    #etcd_leader_counts, 
    #etcd_self, 
    #etcd_store, 
    etcd_stats_all,
    etcd_metrics
)

def stats_result(ip, port, value):
    res = requests.get("http://{ip}:{port}/v2/stats/{value}".format(ip=ip, port=port, value=value),
                       timeout=10)
    indices = res.json()
    return indices

def metrics_result(ip, port):
    res = requests.get("http://{ip}:{port}/metrics".format(ip=ip, port=port),
                       timeout=10)
    indices = res.text
    return indices

def etcd_data(endpoint, metric, ts, value):
    structure = {
        'endpoint': endpoint,
        'metric': metric,
        'timestamp': ts,
        'step': 60,
        'value': value,
        'counterType': "GAUGE",
        'tags': ""
    }
    return structure

def get_keys(HOSTNAME, ts, etcd_result, etcd_traps):
    falcon_data = []
    for key in etcd_traps:
        if key == 'state':
            value = etcd_result.get(key, '')
            if value == "StateLeader":
                etcd_result[key] = 1
            elif value == "StateFollower":
                etcd_result[key] = 2
            else:
                etcd_result[key] = 0
        etcd_value = etcd_result.get(key, {})
        if etcd_value == {}:
            continue
        metric = 'etcd.' + key
        falcon_data.append(etcd_data(HOSTNAME, metric, ts, etcd_value))

    return falcon_data

def text_switch(data):
    h = StringIO(data)
    exclude_text = "#"
    result = {}
    for line in h.readlines():
        if exclude_text in line:
            continue
        try:
            key, value = map(str.strip, str(line).split())
            value =  Decimal(value).quantize(Decimal('0'))
            result[key] = int(value)
        except ValueError:
            pass # ignore broken lines
    return result

def send_to_falcon(url=None, data=None):
    if data and url:
        res = requests.post(url, data=json.dumps(data))
        return res

def main():
    HOSTNAME = socket.gethostname()
    etcd_host = "127.0.0.1"
    etcd_port = "2379"
    falcon_url="http://127.0.0.1:1988/v1/push"
    stats_value = ["self", "store"]
    ts = int(time.time())
    stats_all_data = []
    falcon_data = []
    for url_value in stats_value:
        try:
            etcd_stats_result = stats_result(etcd_host, etcd_port, url_value)
        except:
            continue
        stats_data = get_keys(HOSTNAME, ts, etcd_stats_result, etcd_stats_all)
        stats_all_data = stats_all_data + stats_data
    try:
        etcd_metric_result = metrics_result(etcd_host, etcd_port)
    except:
        etcd_metric_result = ""
    metric_dic_result = text_switch(etcd_metric_result)
    metric_data = get_keys(HOSTNAME, ts, metric_dic_result, etcd_metrics)
    falcon_data = stats_all_data + metric_data 
    try:
        send_to_falcon(falcon_url, falcon_data)
    except:
        pass

if __name__ == '__main__':
    main()

