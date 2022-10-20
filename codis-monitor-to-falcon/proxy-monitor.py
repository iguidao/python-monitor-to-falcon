#!/usr/bin/env python
# encoding: utf-8
import requests
import json
import time 
import socket

calculate_metric_dict = {
    "proxy_ops_total" : "COUNTER",
    "proxy_ops_fails" : "COUNTER",
    "proxy_ops_redis_errors" : "COUNTER",
    "proxy_ops_qps" : "GAUGE",
    "proxy_sessions_total" : "COUNTER",
    "proxy_sessions_alive" : "GAUGE",
    "proxy_runtime_general_alloc" : "GAUGE",
    "proxy_runtime_general_sys" : "GAUGE",
    "proxy_runtime_general_lookups" : "GAUGE",
    "proxy_runtime_general_mallocs" : "GAUGE",
    "proxy_runtime_general_frees" : "GAUGE",
    "proxy_runtime_heap_alloc" : "GAUGE",
    "proxy_runtime_heap_sys" : "GAUGE",
    "proxy_runtime_heap_idle" : "GAUGE",
    "proxy_runtime_heap_inuse" : "GAUGE",
    "proxy_runtime_heap_objects" : "GAUGE",
    "proxy_runtime_gc_num" : "COUNTER",
    "proxy_runtime_gc_cpu_fraction" : "GAUGE",
    "proxy_runtime_gc_total_pausems" : "COUNTER",
    "proxy_runtime_num_procs" : "GAUGE",
    "proxy_runtime_num_goroutines" : "GAUGE",
    "proxy_runtime_num_cgo_call" : "COUNTER",
    "proxy_runtime_mem_offheap" : "GAUGE",
}

def send_to_falcon(url=None, data=None):
    if data and url:
        res = requests.post(url, data=json.dumps(data))
        return res

def query_proxy(proxy_hostname):
    proxy_url = "http://%s:11081/proxy/stats" % (proxy_hostname)
    try:
        res = requests.get(proxy_url,
                           timeout=3)
        proxy_qps = res.json()
    except Exception as e:
        proxy_qps = {}
    return proxy_qps

def proxy_data(ts, host_endpoint, value, metric,ctype):
    structure = {
        'endpoint': host_endpoint,
        'metric': metric,
        'timestamp': ts,
        'step': 60,
        'value': value,
        'counterType': ctype,
        'tags': ""
    }
    return structure

def proxy_metric(proxy_stats, metric_list):
    metric = {}
    for proxy_value in metric_list:
        for i in proxy_stats[proxy_value]:
            # print(proxy_value,proxy_stats[proxy_value][i]," 的类型：",type(proxy_stats[proxy_value][i]),len(i))
            if isinstance(proxy_stats[proxy_value][i],dict):
                for i_v in proxy_stats[proxy_value][i]:
                    pkey = "proxy_"+proxy_value+"_"+i+"_"+i_v
                    metric[pkey] = proxy_stats[proxy_value][i][i_v]
            elif isinstance(proxy_stats[proxy_value][i],list):
                if proxy_value == "ops" and i == "cmd":
                    for cmd_v in proxy_stats[proxy_value][i]:
                        if cmd_v["opstr"] == "":
                            continue
                        for opstr_v in cmd_v:
                            if opstr_v == "opstr":
                                continue
                            pkey = "proxy_"+proxy_value+"_"+i+"_opstr_"+cmd_v["opstr"]+"_"+opstr_v
                            metric[pkey] = cmd_v[opstr_v]
                else:
                    break
            else:
                pkey = "proxy_"+proxy_value+"_"+i
                metric[pkey] = proxy_stats[proxy_value][i]
    return metric
def main():

    proxy_hostname = socket.gethostname()
    # proxy_hostname = "172.16.101.250"
    falcon_url="http://127.0.0.1:1988/v1/push"
    ts = int(time.time())
    falcon_data = []
    metric_list = ["ops","sessions","runtime"]
    proxy_result = query_proxy(proxy_hostname)
    if proxy_result != {}:
        metric_result = proxy_metric(proxy_result,metric_list,)
        # print(metric_result)
    else:
        metric_result = {} 
    if metric_result != {}:
        for key in  metric_result.keys():
            if key in calculate_metric_dict.keys():
                falcon_data.append(proxy_data(ts, proxy_hostname, metric_result[key], key,calculate_metric_dict[key]))
            else:
                falcon_data.append(proxy_data(ts, proxy_hostname, metric_result[key], key,"COUNTER"))
    if len(falcon_data) != 0:
        try:
            # print(falcon_data)
            send_to_falcon(falcon_url, falcon_data)
        except:
            print("no send falcon")
            pass

if __name__ == '__main__':
    main()
