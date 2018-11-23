# jstorm-monitor-to-falcon

- 时间：2018-11-23
- 收集jstormr监控，并上传到falcon

## 系统环境

- running inside Linux
- python (>= 2.7)
- jstorm-ui


## 使用方法
1. 修改文件中的jstorm_host的ip地址为jstorm的ui地址和端口
2. 修改文件中的cluster_jstorm后面的jstorm集群名字
3. crontab执行即可

## 相关文档
[click me](https://github.com/alibaba/jstorm)

## Related Metrics

Metrics | Comments
--- | ---

RecvTps | 
SendTps | 
HeapMemory | 
Failed | 
Acked | 
MemoryUsed | 
Emitted | 
CpuUsedRatio | 
ProcessLatency | 
