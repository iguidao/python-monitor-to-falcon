# nginx-monitor-to-falcon
 
- 时间：2018-12-18
- 收集nginx监控，并上传到falcon

## 系统环境

- running inside Linux
- python (>= 2.7)
- nginx --with-http_stub_status_module 模块


## 使用方法
1. 在本机使用
2. crontab执行即可

## 相关文档
[click me](http://nginx.org/en/docs/http/ngx_http_stub_status_module.html)

## Related Metrics

Metrics | Comments
--- | ---
Active | 当前活动客户端连接数，包括等待连接。
accepts | 已接受的客户端连接总数
handled | 成功的客户端连接数
requests | 客户端请求数
Reading | nginx正在读取请求标头的当前连接数
Writing | nginx响应写回客户端的当前连接数
Waiting | 当前等待请求的空闲客户端连接数
