#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import requests
import time
import json
import sys
import yaml
from optparse import OptionParser
from StringIO import StringIO
from  nginx_metric import ( 
    nginx_metric,
    COUNTER
)

def stats_result(ip, port, value):
    res = requests.get("http://{ip}:{port}/{value}".format(ip=ip, port=port, value=value),
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

def nginx_data(endpoint, metric, ts, value, counter_type):
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

def get_keys(nginx_name, ts, nginx_result, nginx_traps):
    falcon_data = []
    for key in nginx_traps:
        nginx_value = nginx_result.get(key, {})
        if nginx_value == {}:
            continue
        metric = 'ngx_' + key
        if key in COUNTER:
            falcon_data.append(nginx_data(nginx_name, metric, ts, nginx_value, "COUNTER"))
        else:
            falcon_data.append(nginx_data(nginx_name, metric, ts, nginx_value, "GAUGE"))
           

    return falcon_data

def text_switch(data):
    h = StringIO(data)
    result = {}
    nginx_line = 1
    for line in h.readlines():
        if nginx_line == 1:
            value = line.split()
            result["active"] = int(value[2])
        if nginx_line == 3:
            value = line.split()
            result["accepts"] = int(value[0])
            result["handled"] = int(value[1])
            result["requests"] = int(value[2])
        if  nginx_line == 4:
            value = line.split()
            result["reading"] = int(value[1])
            result["writing"] = int(value[3])
            result["waiting"] = int(value[5])

        nginx_line+=1
    return result
  


def send_to_falcon(url=None, data=None):
    if data and url:
        res = requests.post(url, data=json.dumps(data))
        return res

def main(host_info):
    ts = int(time.time())
    falcon_data = []
    for  host in host_info:
        nginx_name = host['host']
        nginx_port = host['port']
        nginx_url = host['url']
        try:
            nginx_stats_result = stats_result(nginx_name, nginx_port, nginx_url)
        except:
            continue
        nginx_value = text_switch(nginx_stats_result)
        stats_data = get_keys(nginx_name, ts, nginx_value, nginx_metric)
        falcon_data.extend(stats_data)
    return falcon_data

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c","--config",dest="config_file")
    (options,args) = parser.parse_args()
    if not options.config_file:
        parser.print_help()
        sys.exit(1)
    CONFIG_FILE = options.config_file
    config_data = load_yaml_data(CONFIG_FILE)
    host_info = config_data['nginx-config']
    falcon_url = config_data['falcon']['push_url']
    falcon_data = main(host_info) 

    try:
        send_to_falcon(falcon_url, falcon_data)
    except:
        print "send faile"
        pass
