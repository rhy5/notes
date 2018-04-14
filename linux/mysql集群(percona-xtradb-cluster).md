### percona-xtradb-cluster 环境搭建

参考文档 https://www.percona.com/doc/percona-xtradb-cluster/5.7/install/yum.html 


1.准备
    
    系统：centos 6.9
    selinux:关闭  （或者将selinux模式从enforcing 改为 permissive）
    iptables：关闭 （或者iptables 允许 3306，4444，4567，4568 几个端口相互通讯）
    pxc1:   192.168.44.151  node1
    pxc2:   192.168.44.152  node2
    pxc3:   192.168.44.153  node3

2.安装
    
- 安装仓库包 `yum install http://www.percona.com/downloads/percona-release/redhat/0.1-4/percona-release-0.1-4.noarch.rpm`

- 安装软件 `yum install Percona-XtraDB-Cluster-57` 
>需要socat 及libev.so.4()(64bit) 依赖

socat 安装
```
wget –no-cache http://www.convirture.com/repos/definitions/rhel/6.x/convirt.repo -O /etc/yum.repos.d/convirt.repo
yum makecache
yum install socat
```
libev.so.4()(64bit) 安装

```
wget  ftp://rpmfind.net/linux/dag/redhat/el6/en/x86_64/dag/RPMS/libev-4.15-1.el6.rf.x86_64.rpm
rpm -ivh libev-4.15-1.el6.rf.x86_64.rpm
```

>将3个节点安装好之后对mysql root密码进行修改 及添加必要的账户

```
service mysql start
grep 'temporary password' /var/log/mysqld.log
```
对mysql进行简单的配置
```
mysql -uroot -p #登陆 mysql 更改root密码 

mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'rootPass';
Query OK, 0 rows affected (0.00 sec)

后面需要用到的账户 提前设置好
mysql> CREATE USER 'sstuser'@'localhost' IDENTIFIED BY 'passw0rd';
mysql> GRANT RELOAD, LOCK TABLES, PROCESS, REPLICATION CLIENT ON *.* TO
  'sstuser'@'localhost';
mysql> FLUSH PRIVILEGES;
```

3.配置节点

- 配置node1 
```
vi /etc/percona-xtradb-cluster.conf.d/wsrep.cnf
```
如下配置
```
[mysqld]
# Path to Galera library
wsrep_provider=/usr/lib64/galera3/libgalera_smm.so

# Cluster connection URL contains IPs of nodes
#If no IP is found, this implies that a new cluster needs to be created,
#in order to do that you need to bootstrap this node
wsrep_cluster_address=gcomm://192.168.44.151,192.168.44.152,192.168.44.153 #编辑同步的3个节点IP

# In order for Galera to work correctly binlog format should be ROW
binlog_format=ROW

# MyISAM storage engine has only experimental support
default_storage_engine=InnoDB #数据库引擎

# Slave thread to use
wsrep_slave_threads= 8

wsrep_log_conflicts

# This changes how InnoDB autoincrement locks are managed and is a requirement for Galera
innodb_autoinc_lock_mode=2

# Node IP address
wsrep_node_address=192.168.44.151 #当前节点IP
# Cluster name
wsrep_cluster_name=pxc-cluster #集群名称

#If wsrep_node_name is not specified,  then system hostname will be used
wsrep_node_name=pxc1 #当前节点名称 一般机器名就行

#pxc_strict_mode allowed values: DISABLED,PERMISSIVE,ENFORCING,MASTER
pxc_strict_mode=ENFORCING 

# SST method
wsrep_sst_method=xtrabackup-v2

#Authentication for SST method
wsrep_sst_auth="sstuser:passw0rd" #之前添加的sstuser账户密码 用来进行sst传输的账户

```

4.启动第一个节点

```
/etc/init.d/mysql bootstrap-pxc
```

5.添加节点
- 同第一个节点一样的配置文件 注意特别的地方 
```
# Node IP address 
wsrep_node_address=192.168.44.151 #当前节点IP
#If wsrep_node_name is not specified,  then system hostname will be used
wsrep_node_name=pxc1 #当前节点名称 一般机器名就行
```
这两个地方要更改为当前机器的ip及名称 其他的跟node1 保持一致即可

6.启动其他节点

```
/etc/init.d/mysql start
```

7.验证是否同步 

>将 创建 添加数据 及查询分别 在不同node上执行 验证是否同步

```
mysql@pxc2> CREATE DATABASE percona;
Query OK, 1 row affected (0.01 sec)

mysql@pxc3> USE percona;
Database changed

mysql@pxc3> CREATE TABLE example (node_id INT PRIMARY KEY, node_name VARCHAR(30));
Query OK, 0 rows affected (0.05 sec)

mysql@pxc1> INSERT INTO percona.example VALUES (1, 'percona1');
Query OK, 1 row affected (0.02 sec)

mysql@pxc2> SELECT * FROM percona.example;
+---------+-----------+
| node_id | node_name |
+---------+-----------+
|       1 | percona1  |
+---------+-----------+
1 row in set (0.00 sec)

```