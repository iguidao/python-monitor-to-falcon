#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import requests
import time
import yaml
import socket
import json
from StringIO import StringIO
from decimal import Decimal
from optparse import OptionParser
from  hbase_metric import hbase_metric

def load_yaml_data(filename=None):
    try:
        with open(filename, 'r') as f:
            data = yaml.load(f)
            return data
    except IOError:
        sys.exit()

def get_json(ip, port):
    res = requests.get("http://{ip}:{port}/jmx".format(ip=ip, port=port),timeout=10)
    indices = res.json()
    return indices

def hbase_data(endpoint, metric, ts, value, tag):
    structure = {
        'endpoint': endpoint,
        'metric': metric,
        'timestamp': ts,
        'step': 60,
        'value': value,
        'counterType': "GAUGE",
        'tags': tag
    }
    return structure

def get_keys(HOSTNAME, ts, hbase_dic, attr, hbase_role, hbase_cluster):
    falcon_data = []
    tag = "cluster=%s,role=%s" % ( hbase_cluster, hbase_role )
    for key in hbase_metric:
        hbase_value = hbase_dic.get(key, {})
        if hbase_value == {}:
            continue
        metric = 'hbase.' + attr + '.' + key
        falcon_data.append(hbase_data(HOSTNAME, metric, ts, hbase_value, tag))

    return falcon_data

def send_to_falcon(url=None, data=None):
    if data and url:
        res = requests.post(url, data=json.dumps(data))
        return res

def main(host_infoi, ts, falcon_url):
    hbase_falcon_data = []
    for hbase_info in host_info:
        hbase_host = hbase_info['host']
        hbase_port = hbase_info['port']
        hbase_role = hbase_info['role']
        hbase_cluster = hbase_info['cluster']
        HOSTNAME = socket.gethostbyaddr(hbase_host)[0].split('.')[0]
        try:
            hbase_get_result = get_json(hbase_host, hbase_port)
        except:
            print "连接地址失败：http://%s:%s/jmx " % (hbase_host, hbase_port)
            continue
        if hbase_role == "master":
            try:
                hbase_master_dic = filter(lambda x: x['name']=='Hadoop:service=HBase,name=Master,sub=Server', hbase_get_result['beans'])[0];
                master_hbase_metric = get_keys(HOSTNAME, ts, hbase_master_dic, "master",  hbase_role, hbase_cluster)
                hbase_falcon_data = hbase_falcon_data + master_hbase_metric
            except Exception as e:
                print "获取'Hadoop:service=HBase,name=Master,sub=Server' 数据失败： %s" % e
        elif hbase_role == "regionserver":
            try:
                hbase_region_dic = filter(lambda x: x['name']=='Hadoop:service=HBase,name=RegionServer,sub=Server', hbase_get_result['beans'])[0];
                region_hbase_metric = get_keys(HOSTNAME, ts, hbase_region_dic, "regionserver",  hbase_role, hbase_cluster)
                hbase_falcon_data = hbase_falcon_data + region_hbase_metric
            except Exception as e:
                print "获取'Hadoop:service=HBase,name=RegionServer,sub=Server' 数据失败： %s" % e
            try:
                hbase_region_ipc_dic = filter(lambda x: x['name']=='Hadoop:service=HBase,name=RegionServer,sub=IPC', hbase_get_result['beans'])[0];
                region_ipc_hbase_metric = get_keys(HOSTNAME, ts, hbase_region_ipc_dic, "regionserver",  hbase_role, hbase_cluster)
                hbase_falcon_data = hbase_falcon_data + region_ipc_hbase_metric
            except Exception as e:
                print "获取'Hadoop:service=HBase,name=RegionServer,sub=IPC' 数据失败： %s" % e
        else:
            print "配置文件写错了吧，不认识你这个role: %s" % hbase_role
            continue
   
        try:
            hbase_jvm_dic = filter(lambda x: x['name']=="Hadoop:service=HBase,name=JvmMetrics", hbase_get_result['beans'])[0];
            two_hbase_metric = get_keys(HOSTNAME, ts, hbase_jvm_dic, "jvmmetrics", hbase_role, hbase_cluster)
            hbase_falcon_data = hbase_falcon_data + two_hbase_metric
        except Exception as e:
            print "获取'Hadoop:service=HBase,name=JvmMetrics' 数据失败 %s " % e
    #print len(hbase_falcon_data)
    try:
        send_to_falcon(falcon_url, hbase_falcon_data)
    except:
        print "上传falcon失败。"
        pass

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c","--config",dest="config_file")
    (options,args) = parser.parse_args()
    if not options.config_file:
        parser.print_help()
        sys.exit(1)
    CONFIG_FILE = options.config_file
    config_data = load_yaml_data(CONFIG_FILE)
    host_info = config_data['hbase-config']
    ts = int(time.time())
    falcon_url = config_data['falcon']['push_url']
    
    main(host_info, ts, falcon_url)

