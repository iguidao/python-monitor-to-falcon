#!/usr/bin/python
#encoding:utf-8
 
import socket
import time
from StringIO import StringIO
 
############# get zookeeper server status
class ZooKeeperServer(object):
 
    def __init__(self, host='localhost', port='2181', timeout=1):
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
 

def zk_data(endpoint, metric, ts, value, tags_name):
    structure = {
        'endpoint': endpoint,
        'metric': metric,
        'timestamp': ts,
        'step': 60,
        'value': value,
        'counterType': 'GAUGE',
        'tags': tags_name
    }
    return structure

def send_to_falcon(url=None, data=None):
    if data and url:
        res = requests.post(url, data=json.dumps(data))
        return res

zk = ZooKeeperServer()
zk_status = zk.get_stats()
endpoint=socket.gethostname()
tags_name="app=zookeeper"
falcon_data = []
ts = int(time.time())
falcon_url="http://127.0.0.1:1988/v1/push"
for key in zk_status:
    data = zk_data(endpoint, key, ts, zk_status[key], tags_name)
    falcon_data.append(data)
try:
    send_to_falcon(falcon_url, falcon_data)
except Exception as e:
    print "send faile"
