# zookeeper-monitor-to-falcon

- 时间：2018-11-21
- 收集zookeeper监控，并上传到falcon

## 系统环境

- running inside Linux
- python (>= 2.7)
- zookeeper (3.4.x)


## 使用方法
1. 在本机使用
2. crontab执行即可

## 相关文档
[click me](https://blog.csdn.net/reblue520/article/details/52352689)

## Related Metrics

Metrics | Comments
--- | ---
zk_avg_latency | 平均延时
zk_max_latency | 最大延时
zk_min_latency | 最小延时
zk_packets_received | 收包数  
zk_packets_sent | 发包数
zk_num_alive_connections | 连接数
zk_outstanding_requests | 堆积请求数
zk_server_state | leader/follower 状态
zk_znode_count | znode数量
zk_watch_count | watch数量
zk_ephemerals_count | 临时节点（znode）
zk_approximate_data_size | 数据大小
zk_open_file_descriptor_count | 打开的文件描述符数量
zk_max_file_descriptor_count | 最大文件描述符数量
zk_followers | follower数量
zk_synced_followers | 同步的follower数量
zk_pending_syncs | 准备同步数
zk_server_ruok | zookeeper是否正常（1正常，0不正常）
