### CDN Haproxy Nginx 获取客户端真实IP

1.架构介绍
>最前端是CDN 服务器 然后haproxy负载均衡指向nginx 目的需要获取到浏览器客户端真实IP

2.跟CDN 方技术联系 将回源IP也就是加速节点的IP列表发过来

同时将客户真实IP传过来 需要cdn方做设置

3.修改haproxy配置文件 添加如下两行

```
        option  httpclose
        option  forwardfor #except 172.16.1.21/24

```
4.修改nginx 配置

```
#查看real-ip 模块是否安装

nginx -V | grep real-ip

#确保安装OK 接着进行配置  将下列配置添加到http server location段即可
set_real_ip_from ip_range1; 
set_real_ip_from ip_range2;
real_ip_header    X-Forwarded-For;
```
>这里的ip_range1,2,…指的是高防的回源IP地址（如果高防后面还有WAF/CDN，则需要写WAF/CDN的回源IP地址，即需要写离源站最近的一层七层代理的回源IP段），需要添加多条

5.重新加载nginx配置文件

```
nginx -s reload 
或者
/etc/init.d/nginx reload
```