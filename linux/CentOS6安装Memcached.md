### CentOS6安装Memcached

本文档描述了memcached在CentOS6.5下如何编译安装和设置
####编译安装
步骤如下：
1. 从官网下载memcached源文件
http://memcached.org/downloads
`wget http://memcached.org/files/memcached-1.4.36.tar.gz`

2. 安装必须的lib包和依赖
`yum install libevent-devel perl-Test-Harness`

3. 编译及安装
```
./configure
make
make test
make install
```
4. 配置自启动
在/etc/init.d下书写自启动脚本memcached

```
#!/bin/sh
# chkconfig: 35 85 21
# description:memcached service

start()
 {
 echo -n $"memcached start."
 /usr/local/bin/memcached -d -m 300 -u root -l 192.168.7.11 -p 12000 -c 256 -P /tmp/memcached.pid
 sleep 3
 /usr/local/bin/memcached -d -m 300 -u root -l 192.168.14.11 -p 12000 -c 256 -P /tmp/memcached.pid
 echo
 }

stop()
 {
 echo -n $"please use kill -9 to kill memcached manually."
 echo
 }

# See how we were called.
 case "$1" in
   start)
 start
 ;;
   stop)
 stop
 ;;
   restart)
 stop
 start
 ;;
   *)
 echo $"Usage: $0 {start|stop|restart}"
 exit 1
 esac
exit 0
```

参数解释
>-d 启动memcached服务
-m 最大内存使用，单位MB，默认64MB
-u 以？的身份运行（仅在以root运行的时候有效）
-l 连接的IP地址，默认是本机
-p 监听的端口
-c 最大同时连接数，默认是1024

5. 保存文本，并赋予执行权限
`chmod 755 memcached`

6. 增加到系统自启动
`chkconfig --add memcached`
`chkconfig memcached on`