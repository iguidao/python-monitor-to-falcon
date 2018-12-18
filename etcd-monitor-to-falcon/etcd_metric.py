#!/usr/bin/env python
# -*- coding: utf-8 -*-

#etcd_leader_latency = [
etcd_stats_all = [
    'state',
    'recvAppendRequestCnt', 
    'recvBandwidthRate',
    'recvPkgRate',
    'sendAppendRequestCnt', 
    'sendPkgRate', 
    'sendBandwidthRate',
    'getsSuccess', 
    'getsFail', 
    'setsSuccess', 
    'setsFail', 
    'deleteSuccess', 
    'deleteFail', 
    'updateSuccess', 
    'updateFail', 
    'createSuccess', 
    'createFail', 
    'compareAndSwapSuccess', 
    'compareAndSwapFail', 
    'compareAndDeleteSuccess', 
    'compareAndDeleteFail', 
    'expireCount', 
    'watchers'
]

etcd_metrics = [
    'etcd_server_file_descriptors_used_total',
    'etcd_server_pending_proposal_total',
    'etcd_server_proposal_durations_milliseconds_sum',
    'etcd_server_proposal_durations_milliseconds_count',
    'etcd_server_proposal_failed_total',
    'etcd_snapshot_save_total_durations_microseconds_sum',
    'etcd_snapshot_save_total_durations_microseconds_count',
    'etcd_store_expires_total',
    'etcd_store_reads_total{action="get"}',
    'etcd_store_reads_total{action="getRecursive"}',
    'etcd_store_watch_requests_total',
    'etcd_store_watchers',
    'etcd_store_writes_total{action="compareAndSwap"}',
    'etcd_store_writes_total{action="create"}',
    'etcd_store_writes_total{action="delete"}',
    'etcd_store_writes_total{action="set"}',
    'etcd_store_writes_total{action="update"}',
    'etcd_wal_fsync_durations_microseconds_sum',
    'etcd_wal_fsync_durations_microseconds_count',
    'etcd_wal_last_index_saved',
    'process_cpu_seconds_total',
    'process_max_fds',
    'process_open_fds',
    'process_resident_memory_bytes',
    'process_start_time_seconds',
    'process_virtual_memory_bytes'
]

COUNTER = [
    'getsSuccess',
    'getsFail',
    'setsSuccess',
    'setsFail',
    'deleteSuccess',
    'deleteFail',
    'updateSuccess',
    'updateFail',
    'createSuccess',
    'createFail'

]

if __name__ == '__main__':
    pass
