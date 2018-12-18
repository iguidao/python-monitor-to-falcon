#!/usr/bin/python
#encoding:utf-8
 
import socket
import time
import sys
import yaml
import requests
import json
from StringIO import StringIO
from optparse import OptionParser

 
############# get zookeeper server status
#class ZooKeeperServer(host_name, host_port):
class ZooKeeperServer(object):
 
    def __init__(self, host, port, timeout=1):
        self._address = (host, int(port))
        self._timeout = timeout
        self._result  = {}
 
    def _create_socket(self):
        return socket.socket()
 
 
    def _send_cmd(self, cmd):
        """ Send a 4letter word command to the server """
        s = self._create_socket()
        s.settimeout(self._timeout)
        s.connect(self._address)
        s.send(cmd)
        data = s.recv(2048)
        s.close()
        return data
 
    def get_stats(self):
        """ Get ZooKeeper server stats as a map """
        data_mntr = self._send_cmd('mntr')
        data_ruok = self._send_cmd('ruok')
        if data_mntr:
            result_mntr = self._parse(data_mntr)
	    if result_mntr.has_key('zk_version'):
		del result_mntr['zk_version']
        if data_ruok:
            result_ruok = self._parse_ruok(data_ruok)
        self._result = dict(result_mntr.items() + result_ruok.items())
         
        if not self._result.has_key('zk_followers') and not self._result.has_key('zk_synced_followers') and not self._result.has_key('zk_pending_syncs'):
           ##### the tree metrics only exposed on leader role zookeeper server, we just set the followers' to 0
           leader_only = {'zk_followers':0,'zk_synced_followers':0,'zk_pending_syncs':0}    
           self._result = dict(result_mntr.items() + result_ruok.items() + leader_only.items() )
 
        return self._result  
 
    def _parse(self, data):
        """ Parse the output from the 'mntr' 4letter word command """
        h = StringIO(data)
        result = {}
        for line in h.readlines():
            try:
                key, value = self._parse_line(line)
                result[key] = value
            except ValueError:
                pass # ignore broken lines
        return result
 
    def _parse_ruok(self, data):
        """ Parse the output from the 'ruok' 4letter word command """
        h = StringIO(data)
        result = {}
        ruok = h.readline()
        if ruok and ruok == "imok":
           result['zk_server_ruok'] = 1
        else:
           result['zk_server_ruok'] = 0
        return result
 
    def _parse_line(self, line):
        try:
            key, value = map(str.strip, line.split('\t'))
        except ValueError:
            raise ValueError('Found invalid line: %s' % line)
        if not key:
            raise ValueError('The key is mandatory and should not be empty')
        try:
            value = int(value)
        except (TypeError, ValueError):
            pass
        return key, value
 

def zk_data(endpoint, metric, ts, value):
    structure = {
        'endpoint': endpoint,
        'metric': metric,
        'timestamp': ts,
        'step': 60,
        'value': value,
        'counterType': 'GAUGE',
        'tags': ""
    }
    return structure

def send_to_falcon(url=None, data=None):
    if data and url:
        res = requests.post(url, data=json.dumps(data))
        return res

def load_yaml_data(filename=None):
    try:
        with open(filename, 'r') as f:
            data = yaml.load(f)
            return data
    except IOError:
        sys.exit()

def main(host_name, host_port):
    try:
        zk = ZooKeeperServer(host_name, host_port)
        zk_status = zk.get_stats()
    except Exception as e:
        print "zookeeper连接不上: %s" % e
        sys.exit(0)
    #endpoint=host_name
   # tags_name="app=zookeeper"
    ts = int(time.time())
    for key in zk_status:
        data = zk_data(host_name, key, ts, zk_status[key])
        falcon_data.append(data)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c","--config",dest="config_file")
    (options,args) = parser.parse_args()
    if not options.config_file:
        parser.print_help()
        sys.exit(1)
    CONFIG_FILE = options.config_file
    config_data = load_yaml_data(CONFIG_FILE)
    host_info = config_data['zk-config']
    falcon_url = config_data['falcon']['push_url']
    falcon_data = []
    for  host in host_info:
        host_name = host['host']
        host_port = host['port']
        main(host_name, host_port)
    #print falcon_data
    #send_to_falcon(falcon_url,falcon_data)
    try:
        send_to_falcon(falcon_url, falcon_data)
    except Exception as e:
        print "send faile"
