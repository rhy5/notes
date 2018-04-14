### samba 共享服务搭建

1.安装samba 
```
systemctl stop iptables.service
#关闭selinux
vi /etc/sysconfig/selinux
selinux=disabled 

yum install samba
```

2.创建共享目录 添加账户

```
mkdir -p /home/public
useradd public -M -s /sbin/nologin #添加用户 不创建home目录 同时设置不能登陆系统

passwd public #设置共享用户密码

#修改共享目录用户为public 完全控制
chown -R public.public /home/public

#开启服务自启动
systemctl enable smb

#添加smb共享用户 
smbpasswd -a public #设置密码



```
3.编辑配置smb服务

```
cp /etc/samba/smb.conf /etc/samba/smb.conf.bak

vi /etc/samba/smb.conf

[global]
        workgroup = SAMBA
        security = user #需要认证
        log file = /var/log/samba/log.%m #设置日志
        hosts allow = 192.168.100. #设置可以访问的网段
        passdb backend = tdbsam

        printing = cups
        printcap name = cups
        load printers = yes
        cups options = raw

[homes]
        comment = Home Directories
        browseable = No
        read only = No

[printers]
        comment = All Printers
        path = /var/tmp
        printable = Yes
        create mask = 0600
        browseable = No

[print$]
        comment = Printer Drivers
        path = /var/lib/samba/drivers
        write list = root
        create mask = 0664
        directory mask = 0775
[public] #配置public 共享目录
        comment = public
        path = /home/public #设置路径
        valid users = public,root #设置用户
        read only = No #可读可写
        public = no #不匿名
        writeable = yes #可写
#        create mode = 0555   ###创建后不能删除文件


```

>tdbsam：该方式则是使用一个数据库文件来建立用户数据库。数据库文件叫passdb.tdb，默认在/etc/samba目录下。passdb.tdb用户数据库可以使用smbpasswd –a来建立Samba用户，不过要建立的Samba用户必须先是系统用户。我们也可以使用pdbedit命令来建立Samba账户。pdbedit命令的参数很多，我们列出几个主要的。

pdbedit –a username：新建Samba账户。

pdbedit –x username：删除Samba账户。

pdbedit –L：列出Samba用户列表，读取passdb.tdb数据库文件。

pdbedit –Lv：列出Samba用户列表的详细信息。

pdbedit –c “[D]” –u username：暂停该Samba用户的账号。

pdbedit –c “[]” –u username：恢复该Samba用户的账号