# slb_monitor_to_falconn

- 时间：2018-11-15
- 收集阿里云SLB监控，并上传到falcon

## 系统环境

- running inside Linux
- python (>= 2.7)

### 阿里云官方SDK

- pip install aliyuncli
- pip install -Iv aliyun-python-sdk-cms==5.0.0
- aliyuncli configure
- pip install aliyun-python-sdk-core
- pip install aliyun-python-sdk-cms

### 配置文件更改

1. 编辑`al_slb.py` 替换你的阿里云认证信息
>\# vim al_slb.py
  ```
  clt = client.AcsClient('your_access_key','your_access_secret','your_region_id')
  ```
2. 编辑`conf.yaml` 更改你的falcon地址和slb信息
>\# vim conf.yaml
  ```
falcon:
    push_url: http://127.0.0.1:1988/v1/push
project: 'acs_slb_dashboard'
host:
    - { instance_id: 'SLB-ID', tag: 'slb=SLB_MAME' }
    - { instance_id: 'SLB-ID', tag: 'slb=SLB-NAME' }

  ```

3. 选择metric，可以默认配置，在配置文件metric_all.yaml文件中

4. 启动方式
>\# crontab -e
  ```
* * * * * python al_slb.py

  ```

## 相关文档
[click me](https://help.aliyun.com/document_detail/28622.html?spm=a2c4g.11186623.6.685.2bb83da6imuTkb)

## Related Metrics
### 四层监控指标
Metrics | Comments
--- | ---
Metric | 描述
HeathyServerCount | 后端健康ECS实例个数
UnhealthyServerCount | 后端异常ECS实例个数
PacketTX | 端口每秒流出数据包数
PacketRX | 端口每秒流入数据包数
TrafficRXNew | 端口每秒流入数据量
TrafficTXNew | 端口每秒流出数据量
ActiveConnection | 端口当前活跃连接数，既客户端正在访问SLB产生的连接
InactiveConnection | 端口当前非活跃连接数，既访问SLB后未断开的空闲的连接
NewConnection | 端口当前新建连接数
MaxConnection | 端口当前并发连接数
DropConnection | 监听每秒丢失连接数
DropPacketRX | 监听每秒丢失入包数
DropPacketTX | 监听每秒丢失出包数
DropTrafficRX | 监听每秒丢失入bit数
DropTrafficTX | 监听每秒丢失出bit数
InstanceActiveConnection | 实例每秒活跃连接数
InstanceDropConnection | 实例每秒丢失连接数
InstanceDropPacketRX | 实例每秒丢失入包数
InstanceDropPacketTX | 实例每秒丢失出包数
InstanceDropTrafficRX | 实例每秒丢失入bit数
InstanceDropTrafficTX | 实例每秒丢失出bit数
InstanceInactiveConnection | 实例每秒非活跃连接数
InstanceMaxConnection | 实例每秒最大并发连接数
InstanceNewConnection | 实例每秒新建连接数
InstancePacketRX | 实例每秒入包数
InstancePacketTX | 实例每秒出包数
InstanceTrafficRX | 实例每秒入bit数
InstanceTrafficTX | 实例每秒出bit数
### 七层监控指标
Metrics | Comments
--- | ---
Metric | 描述
Qps | 端口维度的QPS
Rt | 端口维度的请求平均延时
StatusCode2xx | 端口维度的slb返回给client的2xx状态码统计
StatusCode3xx | 端口维度的slb返回给client的3xx状态码统计
StatusCode4xx | 端口维度的slb返回给client的4xx状态码统计
StatusCode5xx | 端口维度的slb返回给client的5xx状态码统计
StatusCodeOther | 端口维度的slb返回给client的other状态码统计
UpstreamCode4xx | 端口维度的rs返回给slb的4xx状态码统计
UpstreamCode5xx | 端口维度的rs返回给client的5xx状态码统计
UpstreamRt | 端口维度的rs发给proxy的平均请求延迟
InstanceQps | 实例维度的QPS
InstanceRt | 实例维度的请求平均延时
InstanceStatusCode2xx | 实例维度的slb返回给client的2xx状态码统计
InstanceStatusCode3xx | 实例维度的slb返回给client的3xx状态码统计
InstanceStatusCode4xx | 实例维度的slb返回给client4xx状态码统计
InstanceStatusCode5xx | 实例维度的slb返回给client的5xx状态码统计
InstanceStatusCodeOther | 实例维度的slb返回给client的Other状态码统计
InstanceUpstreamCode4xx | 实例维度的rs返回给slb的4xx状态码统计
InstanceUpstreamCode5xx | 实例维度的rs返回给slb的5xx状态码统计
InstanceUpstreamRt | 实例维度的rs发给proxy的平均请求延迟
