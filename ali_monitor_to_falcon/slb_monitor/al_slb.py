#!/usr/bin/env python
#encoding: utf-8
from aliyunsdkcore import client
from aliyunsdkcms.request.v20180308 import QueryMetricLastRequest 
from optparse import OptionParser
import time
import datetime
import json
import os
import sys
import requests
from traceback import print_exc
import yaml
from os import path

clt = client.AcsClient('your_access_key','your_access_secret','your_region_id')
BASE_DIR = path.dirname(path.abspath(__file__))

def load_yaml_data(filename=None):
    try:
        with open(filename, 'r') as f:
            data = yaml.load(f)
            return data
    except IOError:
        print_exc()


def query_metric(project,metric,instance_id,**kwargs):
    request = QueryMetricLastRequest.QueryMetricLastRequest()
    request.set_accept_format('json')
    request.set_Project(project)
    request.set_Metric(metric)
    request.set_Dimensions("{'instanceId':'%s'}" % instance_id)
    while True:
        try:
            data = json.loads(clt.do_action_with_exception(request))
            break
        except:
            time.sleep(1)
    return data

def slb_data(ts, metric, value, tags):
    structure = {
        'metric':metric.lower(),
        'timestamp':int(ts),
        'step':60,
        'counterType':'GAUGE',
        'tags':tag,
        'value':value,
        'endpoint':'slb-all'
    }
    return structure

def send_to_falcon(url=None, data=None):
    if data and url:
        res = requests.post(url, data=json.dumps(data))
        return res

def handler_response(metric,data,field,unit,tag):
    datapoint = json.loads(data['Datapoints'])
    if unit == "bits":
        value = value / 1000000
        unit = "Mbps"
    metric_num = len(datapoint)
    for number in range(metric_num):
        ts = str(datapoint[number]['timestamp'] / 1000)
        value = datapoint[number].get(field)
        port = datapoint[number].get('port')
        if not port:
            metric_name = metric + '.' + unit
        else:
            metric_name = metric + '.' + port + '.' + unit
        push_data=slb_data(ts, metric_name, value, tag)
        all_data.append(push_data)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f","--file",dest="metric_file")
    parser.add_option("-c","--config",dest="config_file")
    (options,args) = parser.parse_args()
    if not options.config_file:
        parser.print_help()
        sys.exit(1)
    CONFIG_FILE = BASE_DIR + '/%s' % options.config_file
    METRIC_FILE = BASE_DIR + '/%s' % options.metric_file
    config_data = load_yaml_data(CONFIG_FILE)
    metric_data = load_yaml_data(METRIC_FILE)
    project = config_data['project']
    host_info = config_data['host']
    falcon_url = config_data['falcon']['push_url']
    metric_list = metric_data['metric_list']
    all_data = []
    for host_name in host_info:
        instance_id = host_name['instance_id']
        tag = host_name['tag']
        for metric_info in metric_list:
            data = query_metric(project, metric_info['metric'], instance_id)
            handler_response(metric_info['metric'],
                             data,
                             metric_info['field'],
                             metric_info['unit'],
                             tag)
    try:
        send_to_falcon(falcon_url, all_data)
    except Exception as e:
        print e
