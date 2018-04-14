### Percona-Xtrabd-Haproxy 部署

1.参考mysql集群(percona-xtradb-cluster).md 完成基本环境的 搭建 在此不再叙述

2.添加 监控账户 随便一台mysql服务器 添加账户 会自动同步到其他mysql服务器

```
mysql> grant process on *.* to 'clustercheckuser'@'localhost' identified by 'clustercheckpassword!';
Query OK, 0 rows affected (0.00 sec)

mysql> flush privileges;
Query OK, 0 rows affected (0.00 sec)
```

>注意 如果要修改默认账户密码 同时也要修改/usr/bin/clustercheck 脚本中的账户密码 要保持一致

3.通过xinetd 将/usr/bin/clustercheck 注册为一个服务 先安装xinetd
```
yum install xinetd 

ls /etc/xinetd.d/mysqlchk

#确定mysqlchk的内容如下 

# default: on
# description: mysqlchk
service mysqlchk
{
# this is a config for xinetd, place it in /etc/xinetd.d/
disable = no
flags = REUSE
socket_type = stream
port = 9200 #如果haproxy 配置的检查端口改变 同时也要修改这里的端口号
wait = no
user = nobody
server = /usr/bin/clustercheck
log_on_failure += USERID
only_from = 0.0.0.0/0 
# recommended to put the IPs that need
# to connect exclusively (security purposes)
per_source = UNLIMITED
}

#接着编辑/etc/services 将mysqlchk注册为服务
vi /etc/services 

#添加如下内容到文件底部 注意端口号要跟haproxy 及mysqlchk保持一致
mysqlchk 9200/tcp # mysqlchk 

```
>以上操作需要在所有的mysql cluster服务器上执行

4.配置haproxy服务器 

```
global
log 127.0.0.1 local0
log 127.0.0.1 local1 notice
maxconn 4096
chroot /usr/share/haproxy
user haproxy
group haproxy
daemon

defaults
log global
mode http
option tcplog
option dontlognull
retries 3
option redispatch
maxconn 2000
contimeout 5000
clitimeout 50000
srvtimeout 50000

frontend pxc-front
bind *:3307 #mysql 端口
mode tcp
default_backend pxc-back

frontend stats-front
bind *:80   #监控后台的访问端口 自行修改
mode http
default_backend stats-back

frontend pxc-onenode-front
bind *:3306 #mysql端口
mode tcp
default_backend pxc-onenode-back

backend pxc-back
mode tcp
balance leastconn #算法
option httpchk #必须开启这个选项才能利用clustercheck 这个脚本去检查mysql cluster的健康状况
server c1 10.116.39.76:3306 check port 9200 inter 12000 rise 3 fall 3 #修改为对应的IP地址及端口 及名字 端口号跟上面mysqlchk保持一致即可
server c2 10.195.206.117:3306 check port 9200 inter 12000 rise 3 fall 3 #修改为对应的IP地址及端口 及名字 端口号跟上面mysqlchk保持一致即可
server c3 10.202.23.92:3306 check port 9200 inter 12000 rise 3 fall 3 #修改为对应的IP地址及端口 及名字 端口号跟上面mysqlchk保持一致即可

backend stats-back
mode http
balance roundrobin
stats uri /haproxy/stats #haproxy状态监控页面地址
stats auth pxcstats:secret #修改自己的账户密码 可添加多个账户
stats auth pxcstats:secret #修改自己的账户密码 可添加多个账户

backend pxc-onenode-back
mode tcp
balance leastconn
option httpchk #必须开启这个选项
server c1 10.116.39.76:3306 check port 9200 inter 12000 rise 3 fall 3   #修改为对应的IP地址及端口 及名字 端口号跟上面mysqlchk保持一致即可
server c2 10.195.206.117:3306 check port 9200 inter 12000 rise 3 fall 3 backup #修改为对应的IP地址及端口 及名字 端口号跟上面mysqlchk保持一致即可
server c3 10.202.23.92:3306 check port 9200 inter 12000 rise 3 fall 3 backup #修改为对应的IP地址及端口 及名字 端口号跟上面mysqlchk保持一致即可
```


5.重启haproxy 及xinetd服务  登陆haproxy监控后台查看 同时 停止随便其中一台的mysql服务 观察 监控变化 添加数据验证是否同步
