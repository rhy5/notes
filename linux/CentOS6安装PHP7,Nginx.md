### CentOS安装PHP7,Nginx

1. 安装REMI、EPEL、Webtatic源
**CentOS6**

```
yum install epel-release
rpm -Uvh http://rpms.famillecollet.com/enterprise/remi-release-6.rpm
rpm -Uvh https://mirror.webtatic.com/yum/el6/latest.rpm

```
**CentOS7**
```
yum install epel-release
rpm -Uvh http://rpms.famillecollet.com/enterprise/remi-release-7.rpm
rpm -Uvh https://mirror.webtatic.com/yum/el7/webtatic-release.rpm
```

2. 安装PHP7
```
yum install php70w
查看可安装的php模块
yum search php70w
yum install php70w-mysql php70w-xml php70w-soap php70w-xmlrpc php70w-pdo php70w-bcmath
yum install php70w-mbstring php70w-json php70w-gd php70w-mcrypt php70w-pdo_dblib
```

3. 安装Nginx
`yum install nginx`
配置自启动和启动服务
```
systemctl enable nginx.service
systemctl start nginx.service
```
4. 安装PHP-FPM
`yum install php70w-fpm`

5. 修改Nginx配置文件，创建虚拟主机
vi /etc/nginx/conf.d/default.conf

```
server {
    listen       80;
    server_name  www.666123.com 666123.com ag.qq7567.com al88.qq7567.com qq7567.com www.qq7567.com;

    #charset koi8-r;
    #access_log  /var/log/nginx/log/host.access.log  main;

    location / {
        root   /opt/www;
        index  index.html index.htm index.php;
        if (!-e $request_filename) {
        rewrite  ^(.*)$  /index.php?s=$1  last;
        break;
        }
    }

    error_page  404              /404.html;

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

    # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
    #
    location ~ \.php$ {
        root           /opt/www;
        fastcgi_pass   127.0.0.1:9000;
        fastcgi_index  index.php;
        fastcgi_param  SCRIPT_FILENAME  /opt/www$fastcgi_script_name;
        include        fastcgi_params;
    }

}


```

6. 重启服务
service nginx restart
service php-fpm restart

7. 验证
```
php -v
nginx -v
```

`vi /opt/www/index.php`
```
&lt;?php
phpinfo();
?&gt;
```




