# ElasticSearch-monitor

收集elasticsearch监控发送到falcon

## 系统环境

- running inside Linux
- python ( >= 2.7 )
- elasticsearch ( >= 2.3 )

## 需要模块环境

- pip install requests


## 配置文件更改

1. 编辑conf/conf.yaml文件，替换你的falcon地址和elasticsearch集群地址，模板为两个集群
```

# falcon config
falcon:
    push_url: http://127.0.0.1:1988/v1/push

# Elasticsearch clusters
es-clusters:
  - {One_host: "HOST-NAME-01", PORT: "9200", cluster_name: "CLUSTER-NAME-01", Back_host: "HOST-NAME-02"}
  - {One_host: "HOST-NAME-01", PORT: "9200", cluster_name: "CLUSTER-NAME-02", Back_host: "HOST-NAME-02"}
  
```
 
2. 编辑settings.py文件更改自己的监控项

3. 启动方式
>\# crontab -e
  ```
* * * * * python es-monitor.py

  ```

## 相关文档
[click me](https://github.com/RosenLo/elasticsearch-agent)


## Related Metrics

Metrics | Comments
--- | ---
es.status | status of cluster, the status may be one of three values:`green`/`yellow`/`red`
es.active_primary_shards | indicates the number of primary shars in your cluster
es.active_shards | an aggregate total of all shards across all indices
es.initializing_shards | a count of shards that are being freshly created
es.number_of_nodes | self-descriptive
es.number_of_data_nodes | self-descriptive
es.relocating_shards | the number of shards that are currently moving from on node to another node
es.unassigned_shards | shards that exist in the cluster state, but cannot be found in the cluster itself
es.task_max_waiting_in_queue_millis | the maximun time that a task is waiting in the queue
es.thread_pool.bulk.active | the number of threads active in the bulk thread pool
es.thread_pool.bulk.queue | the number of threads queued in the bulk thread pool 
es.thread_pool.bulk.rejected | the number of threads rejected in the bulk thread pool 
es.thread_pool.search.active | the number of threads active in the search thread pool
es.thread_pool.search.queue | the number of threads queued in the search thread pool
es.thread_pool.search.threads | the number of threads rejected in the search thread pool
es.thread_pool.index.active | the number of threads active in the index thread pool
es.thread_pool.index.queue | the number of threads queued in the index  thread pool
es.thread_pool.index.rejected | the number of threads rejected in the index thread pool
es.process.cpu.percent | CPU usage in percent, or -1 if not known at the time the stats are computed
es.cache.filter.evictions | field缓存里面被驱逐的数据量
es.cache.filter.size | field缓存区大小
es.docs.count | 集群中所有分片的文档
es.docs.deleted | 集群中所有分片的删除的文档
es.fielddata.evictions | fielddata缓存里面被驱逐的数据量
es.fielddata.size | fielddata缓存区大小
es.flush.total | 从开始indexflush到磁盘次数(进行一次提交并删除事务日志的操作叫做flush)
es.flush.total.time | indexflush到磁盘花费时间
es.get.current | 当前正在运行的get请求数
es.get.exists.time | 文档存在时花费在get请求上的时间
es.get.exists.total | 文档存在时get请求次数
es.get.missing.time | 文档丢失时花费在get请求上的时间
es.get.missing.total | 文档丢失时get请求次数
es.get.time | 花费在get请求上的总时间
es.get.total | 总的get请求次数
es.http.current_open | 当前打开的http连接数
es.http.total_opened | 打开http的总连接数
es.id_cache.sizeid | 缓存的大小
es.indexing.delete.current | 当前从一个index中删除的文档数量
es.indexing.delete.time | 从一个index中删除文档花费的总时间
es.indexing.delete.total | 从一个index中删除的文档数量
es.indexing.index.current | 当前一个index中被索引的文档数量
es.indexing.index.time | 从一个index索引文档所花费的时间
es.indexing.index.total | 一个index中被索引的文档数量
es.merges.current | 当前的活跃段合并数量
es.merges.current.docs | 当前跨段合并的文档数量
es.merges.current.size | 当前被合并的段的大小
es.merges.total | 所有段的合并数量
es.merges.total.docs | 跨所有合并段的文档数量
es.merges.total.size | 所有合并段的大小
es.merges.total.time | 花在合并段上的时间
es.pendingtaskspriority_high | 高优先级的未完成的task数量
es.pendingtaskspriority_urgent | 紧急优先未完成的task数量
es.pendingtaskstotal | 总的未完成的task数量
es.primaries.docs.count | 主分片上的文档总量
es.primaries.docs.deleted | 主分片上删除的文档总量
es.primaries.flush.total | 主分片上从开始时间indexflush到磁盘次数
es.primaries.flush.total.time | 主分片上indexflush到磁盘花费时间
es.primaries.get.current | 主分片上当前正在运行的get请求数
es.primaries.get.exists.time | 主分片上文档存在时花费在get请求上的时间
es.primaries.get.exists.total | 主分片上文档存在时get请求次数
es.primaries.get.missing.time | 主分片上文档丢失时花费在get请求上的时间
es.primaries.get.missing.total | 主分片上文档丢失时get请求次数
es.primaries.get.time | 主分片上花费在get请求上的总时间
es.primaries.get.total | 主分片上总的get请求次数
es.primaries.indexing.delete.current | 主分片上当前从一个index中删除的文档数量
es.primaries.indexing.delete.time | 主分片上从一个index中删除文档花费的总时间
es.primaries.indexing.delete.total | 主分片上从一个index中删除的文档数量
es.primaries.indexing.index.current | 主分片上当前一个index中被索引的文档数量
es.primaries.indexing.index.time | 主分片上从一个index索引文档所花费的时间
es.primaries.indexing.index.total | 主分片上一个index中被索引的文档数量
es.primaries.merges.current | 主分片上当前的活跃段合并数量
es.primaries.merges.current.docs | 主分片上当前跨段合并的文档数量
es.primaries.merges.current.size | 主分片上当前被合并的段的大小
es.primaries.merges.total | 主分片上所有段的合并数量
es.primaries.merges.total.docs | 主分片上跨所有合并段的文档数量
es.primaries.merges.total.size | 主分片上所有合并段的大小
es.primaries.merges.total.time | 主分片上花在合并段上的时间
es.primaries.refresh.total | 主分片上index刷新总数量
es.primaries.refresh.total.time | 主分片上index刷新花费的总时间
es.primaries.search.fetch.current | 当前运行在主分片上查询取回操作的数量
es.primaries.search.fetch.time | 在主分片上查询取回操作的总时间
es.primaries.search.fetch.total | 在主分片上查询取回操作的数量
es.primaries.search.query.current | 当前运行在主分片上查询操作的数量
es.primaries.search.query.time | 在主分片上查询操作的总时间
es.primaries.search.query.total | 在主分片上查询操作的数量
es.primaries.store.size | 所有主分片的大小/bytes
es.refresh.total | 总的index刷新次数
es.refresh.total.time | 总的index刷新花费的时间
es.search.fetch.current | 当前运行的查询取回操作的数量
es.search.fetch.open_contexts | 活跃查询次数
es.search.fetch.time | 查询取回操作的总时间
es.search.fetch.total | 查询取回操作的数量
es.search.query.current | 当前运行查询操作的数量
es.search.query.time | 查询操作的总时间
es.search.query.total | 查询操作的数量
es.store.size | 总的存储大小/bytes
es.transport.rx_count | 在集群通信中接受的包的总数量
es.transport.rx_size | 在集群通信中接受的数据大小/bytes
es.transport.server_open | 为集群通信打开的连接数
es.transport.tx_count | 在集群通信中发送的包的总数量
es.transport.tx_size | 在集群通信中发送的数据大小/bytes
es.jvm.mem.non_heap_user_in_btyes | 加载类使用的大小
