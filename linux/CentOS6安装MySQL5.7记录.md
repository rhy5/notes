### CentOS安装MySQL5.7记录

安装源
`yum install http://dev.mysql.com/get/mysql57-community-release-el6-9.noarch.rpm`

安装MySQL5.7
`yum install mysql-community-server`

设置自启动和开启服务
`chkconfig mysqld on`
`service mysqld start`

修改root默认密码
MySQL5.7 启动后，在/var/log/mysqld.log文件中给root生成了一个默认密码
`grep 'temporary password' /var/log/mysqld.log`

登录MySQL并修改密码
`mysql -uroot -p`
`mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'Mama3860!';`

添加远程登录用户
这里是新增用户admin
`mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'Mama3860!' WITH GRANT OPTION;`
`mysql> FLUSH PRIVILEGES;`

配置默认编码为utf8
`vi /etc/my.cnf
```
[mysqld]
# 在myslqd下添加如下键值对
character_set_server=utf8
init_connect='SET NAMES utf8'
```
重启 MySQL 服务，使配置生效
`service mysqld restart`
查看字符集
`mysql> SHOW VARIABLES LIKE 'character%';`




