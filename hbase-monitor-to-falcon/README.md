# hbase-monitor-to-falcon

- 时间：2018-11-30
- 收集hbase监控，并上传到falcon

## 系统环境

- running inside Linux
- python (>= 2.7)
- hbase (3.4.x)

## 使用方法
1. 在本机使用
2. crontab执行即可

## 相关文档
[click me](http://abloz.com/hbase/book.html#ops.monitoring)

## Related Metrics

Metrics | Comments
--- | ---

numRegionServers | regionserver数        
numDeadRegionServers |         
clusterRequests |         
averageLoad |         
masterActiveTime |         
masterStartTime |         
 |         
Append_75th_percentile |         
Append_95th_percentile |         
Append_99th_percentile |         
Append_max |         
Append_mean |         
Append_median |         
Append_min |         
Append_num_ops |         
blockCacheCount | 内存中的Block cache item数量。这个是存储文件(HFiles)的缓存中的数量。      
blockCacheCountHitPercent |         
blockCacheEvictionCount |         
blockCacheExpressHitPercent | blockCache命中率        
blockCacheFreeSize | 内存中的Block cache memory 剩余 (单位 bytes).   
blockCacheHitCount | Number of blocks of StoreFiles (HFiles) read from the
blockCacheMissCount | StoreFiles (HFiles)请求的未在缓存中的分块数量。       
blockCacheSize | 内存中的Block cache 大小 (单位 bytes). i.e., memory in use
blockCountHitPercent |         
blockedRequestCount | 因memstore大于阈值而引发flush的次数        
checkMutateFailedCount |         
checkMutatePassedCount |         
compactedCellsCount | 合并cell个数        
compactedCellsSize |         
compactionQueueLength | 压缩队列        
Delete_75th_percentile |         
Delete_95th_percentile |         
Delete_99th_percentile |         
Delete_max |         
Delete_mean |         
Delete_median |         
Delete_min |         
Delete_num_ops |         
flushedCellsCount |         
flushedCellsSize | flush到磁盘的大小        
flushQueueLength | Current depth of the memstore flush queue. If increasing,
FlushTime_75th_percentile |         
FlushTime_95th_percentile |         
FlushTime_99th_percentile |         
FlushTime_max |         
FlushTime_mean |         
FlushTime_median |         
FlushTime_min |         
FlushTime_num_ops |         
Get_75th_percentile |         
Get_95th_percentile |         
Get_99th_percentile |         
Get_max |         
Get_mean |         
Get_median |         
Get_min |         
Get_num_ops |         
hedgedReads |         
hedgedReadWins |         
hlogFileCount | The number of write ahead logs not yet archived
hlogFileSize | WAL文件大小        
Increment_75th_percentile |         
Increment_95th_percentile |         
Increment_99th_percentile |         
Increment_max |         
Increment_mean |         
Increment_median |         
Increment_min |         
Increment_num_ops |         
majorCompactedCellsCount | 大合并cell个数        
majorCompactedCellsSize |         
memStoreSize | Regionserver管理的总memstoresize        
mobCompactedFromMobCellsCount |         
mobCompactedFromMobCellsSize |         
mobCompactedIntoMobCellsCount |         
mobCompactedIntoMobCellsSize |         
mobFileCacheAccessCount |         
mobFileCacheCount |         
mobFileCacheEvictedCount |         
mobFileCacheHitPercent |         
mobFileCacheMissCount |         
mobFlushCount |         
mobFlushedCellsCount |         
mobFlushedCellsSize |         
mobScanCellsCount |         
mobScanCellsSize |         
Mutate_75th_percentile |         
Mutate_95th_percentile |         
Mutate_99th_percentile |         
Mutate_max |         
Mutate_mean |         
Mutate_median |         
Mutate_min |         
Mutate_num_ops |         
mutationsWithoutWALCount | Count of writes submitted with a flag indicating they
mutationsWithoutWALSize |         
percentFilesLocal | 文件本地化        
readRequestCount | 读请求数        
regionCount | Regionserver管理region数量        
regionServerStartTime |         
Replay_75th_percentile |         
Replay_95th_percentile |         
Replay_99th_percentile |         
Replay_max |         
Replay_mean |         
Replay_median |         
Replay_min |         
Replay_num_ops |         
slowAppendCount |         
slowDeleteCount |         
slowGetCount | 请求完成时间超过1000ms的次数        
slowIncrementCount |         
slowPutCount |         
splitQueueLength |         
splitRequestCount | region分裂请求次数        
splitSuccessCounnt | region分裂成功次数        
SplitTime_75th_percentile |         
SplitTime_95th_percentile |         
SplitTime_99th_percentile |         
SplitTime_max |         
SplitTime_mean |         
SplitTime_median |         
SplitTime_min |         
SplitTime_num_ops |         
staticBloomSize |         
staticIndexSize | 该regionserver所管理的表索引大小        
storeCount | 该regionserver所管理的store个数        
storeFileCount | 该regionserver所管理的storefile个数        
storeFileIndexSize | Storefileindex大小        
storeFileSize | 该Regionserver管理的storefile大小        
totalRequestCount | 总请求数        
updatesBlockedTime | Number of milliseconds updates have been blocked so the
writeRequestCount | 写请求数        
 |         
GcCount | GC总次数        
GcCountConcurrentMarkSweep | ConcurrentMarkSweep总次数        
GcCountParNew |         
GcTimeMillis | GC总时间        
GcTimeMillisConcurrentMarkSweep | ConcurrentMarkSweep GC时间       
GcTimeMillisParNew | ParNew GC时间       
LogError | Total number of ERROR logs    
LogFatal | Total number of FATAL logs    
LogInfo | Total number of INFO logs    
LogWarn | Total number of WARN logs    
MemHeapCommittedM | Current heap memory committed in MB   
MemHeapMaxM | Max heap memory size in MB   
MemHeapUsedM | Current heap memory used in MB   
MemMaxM | Max memory size in MB    
MemNonHeapCommittedM | Current non-heap memory committed in MB   
MemNonHeapMaxM | Max non-heap memory size in MB   
MemNonHeapUsedM | Current non-heap memory used in MB   
ThreadsBlocked | Current number of BLOCKED threads    
ThreadsNew | Current number of NEW threads    
ThreadsRunnable | Current number of RUNNABLE threads    
ThreadsTerminated | Current number of TERMINATED threads    
ThreadsTimedWaiting | Current number of TIMED_WAITING threads    
ThreadsWaiting | Current number of WAITING threads    
 |         
authenticationFailures | Number of client connection authentication failures   
authenticationSuccesses | Number of client connections where authentication succeeded  
authorizationFailures |         
authorizationSuccesses |         
numActiveHandler | The number of RPC handlers actively servicing requests 
numCallsInGeneralQueue | The number of currently enqueued user requests  
numCallsInPriorityQueue | The number of currently enqueued priority (internal housekeeping) requests
numCallsInReplicationQueue | The number of currently enqueued operations received from replication
numOpenConnections | 该regionserver打开的连接数        
ProcessCallTime_75th_percentile |         
ProcessCallTime_95th_percentile |         
ProcessCallTime_99th_percentile |         
ProcessCallTime_max |         
ProcessCallTime_mean |         
ProcessCallTime_median |         
ProcessCallTime_min |         
ProcessCallTime_num_ops |         
QueueCallTime_75th_percentile |         
QueueCallTime_95th_percentile |         
QueueCallTime_99th_percentile |         
QueueCallTime_max |         
QueueCallTime_mean |         
QueueCallTime_median |         
QueueCallTime_min |         
QueueCallTime_num_ops |         
queueSize |         
receivedBytes | 收到数据量        
sentBytes | 发出数据量
