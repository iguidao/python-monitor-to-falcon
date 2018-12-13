#!/usr/bin/env python
# encoding: utf-8

import json
import re
import sys
import time
import yaml
import socket
import requests
from optparse import OptionParser

from es_metric import (
    traps1,
    traps2,
    GAUGE,
    COUNTER
)


def load_yaml_data(filename=None):
    try:
        with open(filename, 'r') as f:
            data = yaml.load(f)
            return data
    except IOError:
        print "打开文件失败"

def es_data(endpoint, metric, timestamp, value, counter_type, tags):
    structure = {
        'endpoint': endpoint,
        'metric': metric,
        'timestamp': timestamp,
        'step': 60,
        'value': value,
        'counterType': counter_type,
        'tags': tags
    }
    return structure

def get_keys(stats, traps, ts, HOSTNAME, cluster_name):
    stats_data_gauge = {}
    stats_data_timer = {}
    tags = "cluster_name = %s" % cluster_name
    falcon_data = []

    for key in traps:
        if key == 'status':
            value = stats.get(key, '')
            if value == 'green':
                stats[key] = 1
            elif value == 'yellow':
                stats[key] = 2
            elif value == 'red':
                stats[key] = 0

        c = key.split('.')
        s = stats
        while len(c):
            s = s.get(c.pop(0), {})

        if s == {}:
            continue

        metric = 'es.' + key
        if key in GAUGE:
            falcon_data.append(es_data(HOSTNAME, metric, ts, s, 'GAUGE', tags))
        elif key in COUNTER:
            falcon_data.append(es_data(HOSTNAME, metric, ts, s, 'COUNTER', tags))

    return falcon_data

def send_to_falcon(url=None, data=None):
    if data and url:
        res = requests.post(url, data=json.dumps(data))
        return res

def health_result(ip, port):
    res = requests.get("http://{ip}:{port}/_cluster/health".format(ip=ip, port=port), timeout=10)
    health = res.json()
    return health


def node_result(ip, port):
    res = requests.get("http://{ip}:{port}/_nodes/stats".format(ip=ip, port=port), timeout=10)
    node = res.json()
    return node

def check_result(ip, port):
    res = requests.get("http://{ip}:{port}".format(ip=ip, port=port), timeout=10)
    indices = res.status_code
    return indices

def main(CONFIG_FILE):
    data_time =  int(time.time())
    node = {}
    if_ip = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    indices = {}
    falcon_data = []
    data = load_yaml_data(CONFIG_FILE)
    cluster_list = data['es-clusters']
    url = data['falcon']['push_url']
    for i in cluster_list:
        PORT = i['PORT'] 
        ONE_HOST = i['One_host']
        BACK_HOST = i['Back_host']
        try:
            if check_result(ONE_HOST,PORT) == 200 :
                HOSTNAME=ONE_HOST
            elif check_result(BACK_HOST,PORT) == 200 :
                HOSTNAME=BACK_HOST
            else:
                print "this %s and %s not fount!!!` \n", (ONE_HOST, BACK_HOST)
                continue
        except:
            continue
            
        IP = socket.gethostbyname(HOSTNAME)
        cluster_name = i['cluster_name'] 
        try:
            data_time = data_time
            health = health_result(IP, PORT)
            falcon_data = get_keys(health, traps1, data_time, HOSTNAME, cluster_name)
            node_stats = node_result(IP, PORT)
            for node_id in node_stats.get('nodes', {}).keys():
                ip_addr = node_stats['nodes'][node_id]['host']
                if if_ip.match(ip_addr):
                    HOSTNAME = socket.gethostbyaddr(ip_addr)[0].split('.')[0]
                    node = node_stats['nodes'][node_id]
                    falcon_data2 = get_keys(node, traps2, data_time, HOSTNAME, cluster_name)
                    falcon_data.extend(falcon_data2)
            try:
                #print url, falcon_data
                send_to_falcon(url, falcon_data)
            except Exception as e:
                print "falcon field %s" % e

        except (requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout,
                ) as e:
            print "获取es数据失败:%s " % e
            sys.exit(1)

        except Exception as e:
            print "加载json失败:%s " % e
            sys.exit(1)

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-c","--config",dest="config_file")
    (options,args) = parser.parse_args()
    if not options.config_file:
        parser.print_help()
        sys.exit(1)
    CONFIG_FILE = options.config_file
    main(CONFIG_FILE)
