### Centos 配置postfix 使用gmail 发送邮件

1.安装 mailx 及sendmail
```
yum -y install mailx
yum -y install sendmail
/etc/init.d/sendmail start
chkconfig sendmail on
```

2.编辑/etc/postfix/main.cf 在末尾添加如下内容 
```
smtp_sasl_security_options = noanonymous
relayhost = [smtp.gmail.com]:587
smtp_use_tls = yes
smtp_tls_CAfile = /etc/postfix/cacert.pem
smtp_sasl_auth_enable = yes
smtp_sasl_password_maps = hash:/etc/postfix/sasl/passwd
```
并设置权限
```
chmod 600 /etc/postfix/sasl/passwd

```

3.配置SASL认证 

```
mkdir -p /etc/postfix/sasl
vi /etc/postfix/sasl/passwd
#添加如下格式的内容
[smtp.gmail.com]:587 你的邮箱:密码

postmap /etc/postfix/sasl/passwd #创建查找表
```
4.生成CA证书

```
cd /etc/pki/tls/certs
make yourname.pem 

cp yourname.pem /etc/postfix/cacert.pem
```
5.重启postfix服务 并测试
```
/etc/init.d/postfix restart
echo “mail test”|mail -a /etc/hosts -s "hosts" 123456@qq.com
```

>注意如果未成功 安装yum install cyrus-sasl-plain 并登录gmail邮箱设置运行不安全的应用登陆账号为开启 重启postfix 服务 再次发送邮件测试。