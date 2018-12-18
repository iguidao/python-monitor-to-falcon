#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import requests
import time
import json
import yaml
from optparse import OptionParser
from StringIO import StringIO
from decimal import Decimal
from  etcd_metric import ( 
    etcd_stats_all,
    etcd_metrics,
    COUNTER
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

def load_yaml_data(filename=None):
    try:
        with open(filename, 'r') as f:
            data = yaml.load(f)
            return data
    except IOError:
        sys.exit()

def etcd_data(endpoint, metric, ts, value, counter_type):
    structure = {
        'endpoint': endpoint,
        'metric': metric,
        'timestamp': ts,
        'step': 60,
        'value': value,
        'counterType': counter_type,
        'tags': ""
    }
    return structure

def get_keys(etcd_name, ts, etcd_result, etcd_traps, url_value=None):
    falcon_data = []
    for key in etcd_traps:
        if key == 'state' and url_value == "self":
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
        if key in COUNTER:
            falcon_data.append(etcd_data(etcd_name, metric, ts, etcd_value, "COUNTER"))
        else:
            falcon_data.append(etcd_data(etcd_name, metric, ts, etcd_value, "GAUGE"))
           

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

def main(etcd_name, etcd_port):
    #HOSTNAME = socket.gethostname()
    #etcd_name = "127.0.0.1"
    #etcd_port = "2379"
    #falcon_url="http://127.0.0.1:1988/v1/push"
    stats_value = ["self", "store"]
    ts = int(time.time())
    stats_all_data = []
    for url_value in stats_value:
        try:
            etcd_stats_result = stats_result(etcd_name, etcd_port, url_value)
        except:
            continue
        stats_data = get_keys(etcd_name, ts, etcd_stats_result, etcd_stats_all, url_value)
        stats_all_data = stats_all_data + stats_data
    try:
        etcd_metric_result = metrics_result(etcd_name, etcd_port)
    except:
        etcd_metric_result = ""
    metric_dic_result = text_switch(etcd_metric_result)
    metric_data = get_keys(etcd_name, ts, metric_dic_result, etcd_metrics)
   # falcon_data = stats_all_data + metric_data 
    falcon_data.extend(stats_all_data + metric_data)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c","--config",dest="config_file")
    (options,args) = parser.parse_args()
    if not options.config_file:
        parser.print_help()
        sys.exit(1)
    CONFIG_FILE = options.config_file
    config_data = load_yaml_data(CONFIG_FILE)
    host_info = config_data['etcd-config']
    falcon_url = config_data['falcon']['push_url']
    falcon_data = []
    for  host in host_info:
        etcd_name = host['host']
        etcd_port = host['port']
        main(etcd_name, etcd_port)
    #main()

    #print falcon_data
    try:
        send_to_falcon(falcon_url, falcon_data)
    except:
        print "send faile"
        pass
