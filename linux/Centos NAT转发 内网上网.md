### Centos NAT 转发 内网上网

1.环境介绍

```
    3台主机 1台 双网卡 有外网IP 2台内网ip 不能上网
    server1 wan 8.8.8.8 lan 10.0.0.1 可以上网
    server2 lan 10.0.0.2    不能上网
    server3 lan 10.0.0.3    不能上网

    目的 将server1 作为NAT服务器 使其他两台不能上网的服务器可以上网

```

2.配置server1 开启ip_forward 
```
    vi /etc/sysctl.conf 
        修改net.ipv4.ip_forward 的值为1 
    sysctl -p
        使配置生效 
```
3.配置 server2 和server3的网关为server1的lan 地址

```
vi /etc/sysconfig/network-scripts/ifcfg-xxx #先执行ifconfig看具体网卡名称进行编辑
添加 GATEWAY=10.0.0.1
```

4.配置server1 的NAT转发 编辑iptables规则

```
iptables -t nat -A POSTROUTING -s 10.0.0.2 -j MASQUERADE
iptables -t nat -A POSTROUTING -s 10.0.0.3 -j MASQUERADE
```  
5.检查iptables 规则是否有冲突 同时保存iptables 并验证是否生效

```
#重启server2 server3 网卡
service network restart

#ping 测试是否可以上网
ping www.yahoo.com
ping 114.114.114.114
#排错 检查iptables 规则链是否冲突
#查看nat表的规则链
iptables -t nat -L -n 
    REJECT     all  --  anywhere             anywhere            reject-with icmp-host-prohibited

#若存在上述规则 就需要删除
#先查看下上述规则的编号
iptables -L -n --line-number

#删除上述规则
iptables -D forward 1

#保存 iptables 
service iptables save

#重启系统 验证是否生效

```


