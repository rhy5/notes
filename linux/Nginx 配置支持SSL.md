### Nginx 配置ssl支持

1.下载证书生成脚本
```
wget https://github.com/michaelliao/itranswarp.js/blob/master/conf/ssl/gencert.sh
chmod +x gencert.sh
#输入 需要支持ssl的域名 及密码
#生成如下4个文件
  www.abc.com.crt  www.abc.com.key
  www.abc.com.csr  www.abc.com.origin.key
```
2.配置nginx

```
mkdir -p /etc/nginx/ssl
cp www.abc.com.crt  /etc/nginx/ssl/
cp www.abc.com.key  /etc/nginx/ssl/

vi /etc/nginx/conf.d/default.conf

server {
    listen       80;
    server_name  www.abc.com abc.com;
    return      301 https://$server_name$request_uri;  #将http 跳转到https
    #charset koi8-r;
    #access_log  /var/log/nginx/log/host.access.log  main;

    location /status {
        stub_status on;
        access_log off;
        #allow 127.0.0.1;
        #deny all;
    }

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

server {
    listen 443 ssl ;
    server_name  www.abc.com;
    index index.html,index.htm,index.php;
    root /opt/www;
    ssl on; #开启ssl
    ssl_certificate     /etc/nginx/ssl/www.abc.com.crt; # 指定证书
    ssl_certificate_key /etc/nginx/ssl/www.abc.com.key; # 指定私钥

      location /status {
        stub_status on;
        access_log off;
        #allow 127.0.0.1;
        #deny all;
    }

    location / {
        root   /opt/www;
        index  index.html index.htm index.php;
        if (!-e $request_filename) {
        rewrite  ^(.*)$  /index.php?s=$1  last;
        break;
        }
    }

error_page  404              /404.html;

error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

    location ~ \.php$ {
        root           /opt/www;
        fastcgi_pass   127.0.0.1:9000;
        fastcgi_index  index.php;
        fastcgi_param  SCRIPT_FILENAME  /opt/www$fastcgi_script_name;
        include        fastcgi_params;
    }
}

```

3.测试 

```
/usr/sbin/nginx -t
/usr/sbin/nginx reload
#打开域名测试业务是否正常
```