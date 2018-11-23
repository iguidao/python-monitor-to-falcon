#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import requests
import time
import json
from decimal import Decimal

def metrics_result(ip, port, cluster_name):
    res = requests.get("http://{ip}:{port}/api/v2/cluster/{cluster_name}/metrics".format(ip=ip, port=port, cluster_name=cluster_name),
                       timeout=10)
    indices = res.json()
    return indices

def jstorm_data(HOSTNAME, metric, ts, value, tags):
    structure = {
        'endpoint': HOSTNAME,
        'metric': metric,
        'timestamp': ts,
        'step': 60,
        'value': value,
        'counterType': "GAUGE",
        'tags': tags
    }
    return structure

def send_to_falcon(url=None, data=None):
    if data and url:
        res = requests.post(url, data=json.dumps(data))
        return res

def main():
    jstorm_host = "127.0.0.1"
    jstorm_port = "8080"
    HOSTNAME = socket.gethostbyaddr(jstorm_host)[0].split('.')[0]
    falcon_url="http://127.0.0.1:1988/v1/push"
    ts = int(time.time())
    cluster_jstorm = ["jstorm_1", "jstorm_2", "jstorm_3"]
    falcon_data = []
    for cluster_name in cluster_jstorm:
        try:
            jstorm_result = metrics_result(jstorm_host, jstorm_port, cluster_name)
        except:
            continue
        for j_info in  jstorm_result['metrics']:
            if j_info == "":
                break
            metric = "jstorm.%s" % j_info['name']
            #value =  j_info['data'][-1]
            value =  Decimal(j_info['data'][-1]).quantize(Decimal('0'))
            tags = "cluster=%s" % cluster_name
            falcon_data.append(jstorm_data(HOSTNAME, metric, ts, int(value), tags))
    try:
        send_to_falcon(falcon_url, falcon_data)
    except:
        print "no send falcon"
        pass

if __name__ == '__main__':
    main()
