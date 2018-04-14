# linux 下安装softether client vpn 并配置 

1.下载 softether linux client （翻墙下）

2.解压 安装
```
tar xf 爱国.tar.gz
cd aiguo/
make 

```
按提示一步一步安装

3.配置

然后运行
```
./vpnclient statr
./vpncmd 
根据提示 选2 
然后回车 默认是localhost 
```
输入help 查看命令  或者嫌麻烦 直接执行 remoteenable 然后在windows下客户端链接进行配置

```
您可以使用下面的 66 命令:
 About                    - 显示版本信息
 AccountAnonymousSet      - 设定连接设置的用户认证种类为匿名认证
 AccountCertGet           - 获取用于连接设置的客户端证书
 AccountCertSet           - 设置连接设置的用户认证类型为用户证书认证
 AccountCompressDisable   - 禁用连接设置进行通信时的数据压缩
 AccountCompressEnable    - 启用连接设置进行通信时的数据压缩
 AccountConnect           - 使用连接设置，开始连接 VPN Server
 AccountCreate            - 创建新的连接设置
 AccountDelete            - 删除连接设置
 AccountDetailSet         - 设置接续设置的高级通信设置
 AccountDisconnect        - 断开连接中的连接设置
 AccountEncryptDisable    - 禁用连接设置进行通信时的加密
 AccountEncryptEnable     - 启用连接设置进行通信的加密
 AccountExport            - 导出连接设置
 AccountGet               - 取得连接设置的设置
 AccountImport            - 导入连接设置
 AccountList              - 获取连接设置列表
 AccountNicSet            - 设置连接设置时使用的虚拟 LAN 卡
 AccountPasswordSet       - 设定连接设置的用户证类型为密码认证
 AccountProxyHttp         - 将连接设置的连接方法设置为通过 HTTP 代理服务器连接
 AccountProxyNone         - 将连接设置的连接方法直接设置为 TCP/IP 连接
 AccountProxySocks        - 将连接设置的连接方法设置为通过 SOCKS 代理服务器连接
 AccountRename            - 更改连接设置名称
 AccountRetrySet          - 设置连接设置的连接失败或断开时建立重新连接的次数和间隔
 AccountSecureCertSet     - 将连接设置的用户认证类型设置为智能卡认证
 AccountServerCertDelete  - 删除连接设置的服务器固有证书
 AccountServerCertDisable - 禁用连接设置服务器证书验证选项
 AccountServerCertEnable  - 启用连接设置服务器证书验证选项
 AccountServerCertGet     - 获取连接设置的服务器固有证明书
 AccountServerCertSet     - 设置连接设置的服务器固有证明书
 AccountSet               - 设定连接设置连接终端
 AccountStartupRemove     - 解除连接设置的启动连接
 AccountStartupSet        - 设定连接设置的启动连接
 AccountStatusGet         - 获取当前连接设置的状态
 AccountStatusHide        - 设置成在连接到 VPN Server 时不显示连接状态和错误的画面
 AccountStatusShow        - 设置成在连接到 VPN Server 时显示连接状态和错误的画面
 AccountUsernameSet       - 设置用于连接的连接设置的用户名
 CertAdd                  - 添加信任的证明机构的证书
 CertDelete               - 删除信任的证明机构的证书
 CertGet                  - 获得新任的证明机构的证书
 CertList                 - 获取信任的证明机构的证书列表
 Check                    - 检测 SoftEther VPN 是否能正常运行
 KeepDisable              - 禁用保持互联网连接功能
 KeepEnable               - 启动 Internet 保持连接功能
 KeepGet                  - 获取保持互联网连接的功能
 KeepSet                  - 设置 Internet 保持连接功能
 MakeCert                 - 创建新的 X.509 证书和密钥 (1024 位)
 MakeCert2048             - 创建新的 X.509 证书和密钥 (2048 位)
 NicCreate                - 新的虚拟 LAN 卡的创建
 NicDelete                - 删除虚拟 LAN 卡
 NicDisable               - 禁用虚拟 LAN 卡
 NicEnable                - 启用虚拟 LAN 卡
 NicGetSetting            - 获取虚拟 LAN 卡的设置
 NicList                  - 获取虚拟 LAN 卡列表
 NicSetSetting            - 更改虚拟 LAN 卡设置
 NicUpgrade               - 升级虚拟 LAN 卡设备驱动
 PasswordGet              - 获取为连接到 VPN 客户服务的密码的设定
 PasswordSet              - 为连接到 VPN 客户服务的密码的设定
 RemoteDisable            - 禁止 VPN 客户服务的远程管理
 RemoteEnable             - 允许 VPN 客户服务的远程管理
 SecureGet                - 获取使用的智能卡种类的 ID
 SecureList               - 获取可用的智能卡种类列表
 SecureSelect             - 选择要使用的智能卡种类
 TrafficClient            - 在用户模式下，运行网络流量速度测试工具
 TrafficServer            - 在服务器模式下，运行网络流量速度测试工具
 VersionGet               - 获取 VPN 客户服务的版本信息

```

以上是命令说明

我们一般需要
 AccountCreate 
 ```
 VPN Client> AccountCreate 
AccountCreate 命令 - 创建新的连接设置
连接设置名: lovechina

终端 VPN Server 主机名和端口号: 8.8.8.8:443

终端虚拟 HUB 名称: china

连接用户名: chinese  

使用虚拟 LAN 卡名称: lovechinanetwork

命令成功完成。
 ```

 accountlist 查看列表
```
-----------------------+--------------------------------------
VPN 连接设置名称       |lovechina
状态                   |离线
VPN Server 主机名(地址)|8.8.8.8:443 (直接的 TCP/IP 连接)
虚拟 HUB 名称          |china
虚拟网络适配器名       |VPN
命令成功完成。


```
然后可以 使用
accountconnect 命令进行连接

linux下比较麻烦 需要手动添加路由

我这里提供个脚本 放在/etc/init.d/aiguo.sh chmod +x 
```
#! /bin/sh
### BEGIN INIT INFO
# Provides: vpnclient
# Required-Start: $all
# Required-Stop: $network $local_fs $remote_fs $syslog
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Start VPN Client at boot time
# chkconfig: 345 44 56
# description: Start VPN Client at boot time.
# processname: vpnclient
### END INIT INFO

# /etc/init.d/vpnclient

case "$1" in
start)
echo "Starting VPN Client"
/home/rhys/Downloads/vpnclient/vpnclient start
sleep 1
/home/rhys/Downloads/vpnclient/auto.sh
sleep 1
dhclient -4 vpn_vpn
sleep 2
route add -host 爱国IP gw 192.168.1.1
route del default
route add default gw 192.168.30.1 dev vpn_vpn
;;

stop)
echo "Stopping VPN Client"
/home/rhys/Downloads/vpnclient/vpnclient stop
route del -host 爱国IP
route del default
route add default gw 192.168.1.1 dev wlp4s0
;;

*)
echo "Usage: /etc/init.d/vpnclient/vpnclient {start|stop}"
exit 1
;;
esac

exit 0

```
下面的脚本需要根据实际情况修改下  
/home/rhys/Downloads/vpnclient/auto.sh

```
#!/usr/bin/expect
spawn /home/rhys/Downloads/vpnclient/vpncmd
expect "选择 1, 2 或 3:"
send "2\r"
expect "目标 IP 地址的主机名:"
send "\r"
expect "VPN Client>"
send "accountconnect hk\r"
send "exit\r"
interact
exit

```

启动
sudo /etc/init.d/aiguo.sh start


停止
sudo /etc/init.d/aiguo.sh stop