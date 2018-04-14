### MySQL5.7双主复制配置

#### 配置my.cnf
vi /etc/my.cnf
```
[mysqld]
log_bin
binlog-format=ROW
log_slave_updates=true

datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid

character_set_server=utf8
init_connect='SET NAMES utf8'
max_connections = 5000
max_connect_errors = 20000
transaction_isolation = READ-COMMITTED
explicit_defaults_for_timestamp = 1
tmp_table_size =  16777216
max_allowed_packet = 8388608

#老报超时，我就设置大了一点
interactive_timeout = 57600
#老报超时，我就设置大了一点
wait_timeout = 57600


read_buffer_size = 16777216
read_rnd_buffer_size = 33554432
sort_buffer_size =  67108864
join_buffer_size =  67108864
query_cache_size = 0
query_cache_type = 0

#另外一台设置为2
server-id = 1
#另外一台设置为2
auto_increment_offset=1
auto_increment_increment=2

#需要同步表，多个需多行
binlog-do-db = bc
replicate-do-db = bc
binlog-ignore-db = monitor_db
replicate-ignore-db = mysql
replicate-ignore-db = sys
replicate-ignore-db = monitor_db

#害怕遇到错误停止同步，忽略所有错误
slave-skip-errors=all
#zabbix数据不是很重要，容许crash丢数据
sync_binlog = 0

master_info_repository = TABLE
relay_log_info_repository = TABLE

#开启gtid，这是一个新特性，我们的复制是基于GTID的，所以打开
gtid_mode = on
enforce_gtid_consistency = 1
binlog_gtid_simple_recovery = 1

# slave
slave-parallel-type = LOGICAL_CLOCK
#日志老报一个错误，先关闭并行了
slave-parallel-workers = 0
#slave-parallel-workers = 16

#nnodb settings设置项
#内存的75%比较合适
innodb_buffer_pool_size =8G
innodb_buffer_pool_instances = 8
innodb_buffer_pool_load_at_startup = 1
innodb_buffer_pool_dump_at_shutdown = 1
innodb_lru_scan_depth = 2000
innodb_lock_wait_timeout = 10000
innodb_io_capacity = 4000
innodb_io_capacity_max = 8000
innodb_flush_method = O_DIRECT
innodb_flush_neighbors = 1
innodb_log_file_size = 2G
innodb_log_buffer_size = 16777216
innodb_purge_threads = 4
innodb_large_prefix = 1
innodb_thread_concurrency = 80
innodb_print_all_deadlocks = 1
innodb_strict_mode = 1
innodb_sort_buffer_size = 67108864
innodb_flush_log_at_trx_commit = 2
innodb_read_io_threads = 8
innodb_write_io_threads = 8


[mysqld-5.7]
innodb_buffer_pool_dump_pct = 40
innodb_page_cleaners = 4
innodb_undo_log_truncate = 1
innodb_max_undo_log_size = 1G
innodb_purge_rseg_truncate_frequency = 128
binlog_gtid_simple_recovery=1
log_timestamps=system
transaction_write_set_extraction=MURMUR32
show_compatibility_56=on

```

#### 增加同步用户
两台MySQL同时添加同步用户
```
mysql> create user 'sstuser'@'192.168.3.%' identified by 'Mama3860!';
mysql> GRANT REPLICATION SLAVE ON *.* TO 'sstuser'@'192.168.3.%';
mysql> flush privileges;
```
查看GTID mode是否已打开
```
mysql> show global variables like '%gtid%';
```
GTID同步数据不用再记录对方的log文件和位置了，用master_auto_position=1就行

在两台Mysql上都运行，IP得互指
```
mysql> change master to master_host='192.168.3.21', master_user='sstuser',master_password='Mama3860!',master_auto_position=1;
mysql> start slave;
mysql> show slave status\G ;
```

上面输出结果中
Master_Log_File:
Read_Master_Log_Pos: 4
表示同步的文件和位置

显示下面表示工作正常
Slave_IO_Running: Yes
Slave_SQL_Running: Yes

