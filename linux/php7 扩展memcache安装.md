# centos php7 安装 memcache扩展

1. `wget https://github.com/websupport-sk/pecl-memcache/archive/php7.zip` 
下载php memecache扩展包

>http://pecl.php.net/package/memcache 这个是官方的 上面的是一个分支版本 

2. `unzip php7.zip` 解压文件 如果没有unzip 可以`yum install unzip` 安装即可

3. 因为 压缩包里没有 configure 及makefile 我们要用phpize 及php-config 动态添加扩展 

默认yum安装的话 是没有安装这些工具的  可以执行 `yum install php70w-devel` 来安装这些工具 

可以执行`whereis phpize` 来验证下是否安装成功 安装成功后一般在`/usr/bin/phpize` 这个路径下面

4. configure make 进行安装
```
#/usr/bin/phpize 
#./configure --with-php-config=/usr/bin/php-config
```
>提示错误：
configure: error: memcache support requires ZLIB. Use --with-zlib-dir=<DIR> to specify prefix where ZLIB include and library are located

因为memcache需要zlib的支持 所以 configure不成功 

我们执行`yum install -y zlib zlib-devel` 来进行安装zlib库

再接着 configure 

5. `make &&make install`

```
Installing shared extensions:     /usr/lib64/php/modules/
```

不出意外提示这个的话 就说明安装成功了。

然后 编辑php.ini 

`vi /etc/php.ini`

 搜索`extension_dir` 将前面的分号去掉 修改为

```
extension_dir = "/usr/lib64/php/modules/"
extension = "memcache.so"
``` 

然后重启php `service php-fpm restart`

如果提示`NOTICE: PHP message: PHP Warning:  Module 'memcache' already loaded in Unknown on line 0`

可以将`extension = "memcache.so"` 这行注释掉或者删掉。

6. `php -m |grep memcache` 验证下是否安装成功。