# Codis-monitor-to-falcon

- 时间：2022-10-20
- 其中 proxy-monitor.py 是收集codis的proxy监控，并上传到falcon

## proxy-monitor.py 的使用
### 系统环境
- running inside Linux
- python (>= 2.7)
- codis proxy (proxy-admin-port 11081)

### 使用方法
1. 放到运行codis proxy的机器上，crontab执行即可

### 相关文档
[click me](https://github.com/CodisLabs/codis/blob/release3.1/pkg/proxy/metrics.go)

### Proxy Metrics

Metrics | Comments
--- | ---
proxy_ops_cmd_opstr_DEL_calls | ? 
proxy_ops_cmd_opstr_DEL_fails | ? 
proxy_ops_cmd_opstr_DEL_redis_errtype | ? 
proxy_ops_cmd_opstr_DEL_usecs | ? 
proxy_ops_cmd_opstr_DEL_usecs_percall | ? 
proxy_ops_cmd_opstr_EXPIRE_calls | ? 
proxy_ops_cmd_opstr_EXPIRE_fails | ? 
proxy_ops_cmd_opstr_EXPIRE_redis_errtype | ? 
proxy_ops_cmd_opstr_EXPIRE_usecs | ? 
proxy_ops_cmd_opstr_EXPIRE_usecs_percall | ? 
proxy_ops_cmd_opstr_GET_calls | ? 
proxy_ops_cmd_opstr_GET_fails | ? 
proxy_ops_cmd_opstr_GET_redis_errtype | ? 
proxy_ops_cmd_opstr_GET_usecs | ? 
proxy_ops_cmd_opstr_GET_usecs_percall | ? 
proxy_ops_cmd_opstr_MGET_calls | ? 
proxy_ops_cmd_opstr_MGET_fails | ? 
proxy_ops_cmd_opstr_MGET_redis_errtype | ? 
proxy_ops_cmd_opstr_MGET_usecs | ? 
proxy_ops_cmd_opstr_MGET_usecs_percall | ? 
proxy_ops_cmd_opstr_PEXPIRE_calls | ? 
proxy_ops_cmd_opstr_PEXPIRE_fails | ? 
proxy_ops_cmd_opstr_PEXPIRE_redis_errtype | ? 
proxy_ops_cmd_opstr_PEXPIRE_usecs | ? 
proxy_ops_cmd_opstr_PEXPIRE_usecs_percall | ? 
proxy_ops_cmd_opstr_PING_calls | ? 
proxy_ops_cmd_opstr_PING_fails | ? 
proxy_ops_cmd_opstr_PING_redis_errtype | ? 
proxy_ops_cmd_opstr_PING_usecs | ? 
proxy_ops_cmd_opstr_PING_usecs_percall | ? 
proxy_ops_cmd_opstr_QUIT_calls | ? 
proxy_ops_cmd_opstr_QUIT_fails | ? 
proxy_ops_cmd_opstr_QUIT_redis_errtype | ? 
proxy_ops_cmd_opstr_QUIT_usecs | ? 
proxy_ops_cmd_opstr_QUIT_usecs_percall | ? 
proxy_ops_cmd_opstr_SADD_calls | ? 
proxy_ops_cmd_opstr_SADD_fails | ? 
proxy_ops_cmd_opstr_SADD_redis_errtype | ? 
proxy_ops_cmd_opstr_SADD_usecs | ? 
proxy_ops_cmd_opstr_SADD_usecs_percall | ? 
proxy_ops_cmd_opstr_SETEX_calls | ? 
proxy_ops_cmd_opstr_SETEX_fails | ? 
proxy_ops_cmd_opstr_SETEX_redis_errtype | ? 
proxy_ops_cmd_opstr_SETEX_usecs | ? 
proxy_ops_cmd_opstr_SETEX_usecs_percall | ? 
proxy_ops_cmd_opstr_SMEMBERS_calls | ? 
proxy_ops_cmd_opstr_SMEMBERS_fails | ? 
proxy_ops_cmd_opstr_SMEMBERS_redis_errtype | ? 
proxy_ops_cmd_opstr_SMEMBERS_usecs | ? 
proxy_ops_cmd_opstr_SMEMBERS_usecs_percall | ? 
proxy_ops_fails | client到proxy的fails
proxy_ops_qps | proxy的qps
proxy_ops_redis_errors | proxy到redis的error
proxy_ops_total | ? 
proxy_runtime_gc_cpu_fraction | ? 
proxy_runtime_gc_num | ? 
proxy_runtime_gc_total_pausems | ? 
proxy_runtime_general_alloc | ? 
proxy_runtime_general_frees | ? 
proxy_runtime_general_lookups | ? 
proxy_runtime_general_mallocs | ? 
proxy_runtime_general_sys | ? 
proxy_runtime_heap_alloc | ? 
proxy_runtime_heap_idle | ? 
proxy_runtime_heap_inuse | ? 
proxy_runtime_heap_objects | ? 
proxy_runtime_heap_sys | ? 
proxy_runtime_mem_offheap | ? 
proxy_runtime_num_cgo_call | ? 
proxy_runtime_num_goroutines | ? 
proxy_runtime_num_procs | ? 
proxy_sessions_alive | proxy的活跃链接
proxy_sessions_total | ? 
