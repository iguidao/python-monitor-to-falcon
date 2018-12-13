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
import yaml
import signal
from os import path
from traceback import print_exc

def handler(signum, frame):
    raise AssertionError

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
    try:
        data = json.loads(clt.do_action_with_exception(request))
    except:
        data = {}
    return data

def slb_data(ts, metric, value, slb_endpoint):
    structure = {
        'metric':str(metric.lower()),
        'timestamp': int(ts),
        'step': 60,
        'counterType': 'GAUGE',
        'tags': "",
        'value': value,
        'endpoint': slb_endpoint
    }
    return structure

def send_to_falcon(url=None, data=None):
    if data and url:
        res = requests.post(url, data=json.dumps(data))
        return res

def handler_response(metric,data,field,unit,slb_name):
    ali_data = []
    slb_endpoint = "slb-%s" % slb_name
    datapoint = json.loads(data['Datapoints'])
    metric_num = len(datapoint)
    for number in range(metric_num):
        ts = str(datapoint[number]['timestamp'] / 1000)
        value = datapoint[number].get(field)
        if unit == "bits":
            value = value / 1000000
            unit = "mbps"
        port = datapoint[number].get('port')
        if not port:
            metric_name = metric + '.' + unit
        else:
            metric_name = metric + '.' + port + '.' + unit
        push_data=slb_data(ts, metric_name, value, slb_endpoint)
        ali_data.append(push_data)
    return ali_data

if __name__ == '__main__':
    BASE_DIR = path.dirname(path.abspath(__file__))
    #print time.time()
    parser = OptionParser()
    parser.add_option("-f","--file",dest="metric_file")
    parser.add_option("-c","--config",dest="config_file")
    (options,args) = parser.parse_args()
    if not options.config_file or not options.metric_file:
        parser.print_help()
        sys.exit(1)
    CONFIG_FILE = BASE_DIR + '/%s' % options.config_file
    METRIC_FILE = BASE_DIR + '/%s' % options.metric_file
    config_data = load_yaml_data(CONFIG_FILE)
    metric_data = load_yaml_data(METRIC_FILE)
    project = config_data['project']
    host_info = config_data['host']
    ali_access_key = config_data['ali_access_key']
    ali_access_secret = config_data['ali_access_secret']
    ali_region_id = config_data['ali_region_id']
    falcon_url = config_data['falcon']['push_url']
    metric_list = metric_data['metric_list']
    clt = client.AcsClient(ali_access_key, ali_access_secret, ali_region_id)
    all_data = []
    for host_name in host_info:
        instance_id = host_name['instance_id']
        slb_name = host_name['name']
        for metric_info in metric_list:
            try:
                signal.signal(signal.SIGALRM, handler)
                signal.alarm(1)
                data = query_metric(project, metric_info['metric'], instance_id)
                signal.alarm(0)
            except AssertionError:
                continue
            if not data:
                continue
            ali_data = handler_response(metric_info['metric'],
                             data,
                             metric_info['field'],
                             metric_info['unit'],
                             slb_name)
            all_data.extend(ali_data)
    try:
        #print all_data
        send_to_falcon(falcon_url, all_data)
    except Exception as e:
        print e
