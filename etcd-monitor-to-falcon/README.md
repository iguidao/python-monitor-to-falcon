# etcd-monitor-to-falcon

- 时间：2018-11-22
- 收集etcdr监控，并上传到falcon
 
## 系统环境

- running inside Linux
- python (>= 2.7)
- etcd (>= 2.x)


## 使用方法
1. 在本机使用
2. crontab执行即可(python etcd-monitor.py -c conf.yaml)

## 相关文档
[click me](https://coreos.com/etcd/docs/latest/v2/api.html)

## Related Metrics

Metrics | Comments
--- | ---
state | 领导者（1）或追随者（2） 
recvAppendRequestCnt | 节点已处理的附加请求数
recvBandwidthRate | 节点每秒接收的字节数（仅限跟随者）
recvPkgRate | 节点每秒接收的请求数（仅限跟随者）
sendAppendRequestCnt | 节点已发送的请求数
sendPkgRate | 此节点每秒发送的请求数（仅限leader）
sendBandwidthRate | 节点每秒发送的字节数（仅限leader）
getsSuccess | get成功次数
getsFail | get错误次数
setsSuccess | set成功次数
setsFail | set错误次数
deleteSuccess | delete成功次数
deleteFail | delete错误次数
updateSuccess | update成功次数
updateFail | update错误次数
createSuccess | create成功次数
createFail | create错误次数
compareAndSwapSuccess | 
compareAndSwapFail | 
compareAndDeleteSuccess | 
compareAndDeleteFail | 
expireCount | 
watchers | 
etcd_server_file_descriptors_used_total | 
etcd_server_pending_proposal_total | 
etcd_server_proposal_durations_milliseconds_sum | 
etcd_server_proposal_durations_milliseconds_count | 
etcd_server_proposal_failed_total | 
etcd_snapshot_save_total_durations_microseconds_sum | 
etcd_snapshot_save_total_durations_microseconds_count | 
etcd_store_expires_total | 
etcd_store_reads_total{action="get"} | 
etcd_store_reads_total{action="getRecursive"} | 
etcd_store_watch_requests_total | 
etcd_store_watchers | 
etcd_store_writes_total{action="compareAndSwap"} | 
etcd_store_writes_total{action="create"} | 
etcd_store_writes_total{action="delete"} | 
etcd_store_writes_total{action="set"} | 
etcd_store_writes_total{action="update"} | 
etcd_wal_fsync_durations_microseconds_sum | 
etcd_wal_fsync_durations_microseconds_count | 
etcd_wal_last_index_saved | 
process_cpu_seconds_total | 
process_max_fds | 
process_open_fds | 
process_resident_memory_bytes | 
process_start_time_seconds | 
process_virtual_memory_bytes | 
