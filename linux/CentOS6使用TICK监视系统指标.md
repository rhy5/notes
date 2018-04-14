### CentOS6使用TICK监视系统指标

#### 添加TICK repo
vi /etc/yum.repos.d/influxdata.repo
```
[influxdb]
name = InfluxData Repository - RHEL 6Server
baseurl = https://repos.influxdata.com/rhel/6Server/x86_64/stable/
enabled = 1
gpgcheck = 1
gpgkey = https://repos.influxdata.com/influxdb.key
```

#### 安装InfluxDB并配置身份验证
InfluxDB是一个开源数据库，优化了快速，高可用性存储和检索时间序列数据。 InfluxDB非常适合运行监控，应用程序度量和实时分析
yum install influxdb
chkconfig influxdb on
service influxdb start
启动InfluxDB控制台
influx
创建新的管理用户sammy，密码Mama3860
CREATE USER "sammy" WITH PASSWORD 'Mama3860' WITH ALL PRIVILEGES
验证是否已创建用户
show users
退出InfluxDB控制台
exit
配置身份验证
vi /etc/influxdb/influxdb.conf
找到[http]部分，取消注释auth-enabled选项，并将其值设置为true，另开放http endpoint
```
    [http]
      # Determines whether HTTP endpoint is enabled.
      enabled = true

      # The bind address used by the HTTP service.
      bind-address = ":8086"

      # Determines whether HTTP authentication is enabled.
      auth-enabled = true
```
重新启动InfluxDB服务
service influxdb restart

#### 安装和配置Telegraf
Telegraf是一个开源代理，可以收集运行系统或其他服务的指标和数据。 Telegraf然后将数据写入InfluxDB或其他输出。
yum install telegraf
编辑器中打开Telegraf配置文件
vi /etc/telegraf/telegraf.conf
找到[outputs.influxdb]部分，根据需要修改urls = ["http://localhost:8086"]并提供用户名和密码
```
    [[outputs.influxdb]]
      ## The full HTTP or UDP endpoint URL for your InfluxDB instance.
      ## Multiple urls can be specified as part of the same cluster,
      ## this means that only ONE of the urls will be written to each interval.
      # urls = ["udp://localhost:8089"] # UDP endpoint example
      urls = ["http://localhost:8086"] # required
      ## The target database for metrics (telegraf will create it if not exists).
      database = "telegraf" # required

      ...

      ## Write timeout (for the InfluxDB client), formatted as a string.
      ## If not provided, will default to 5s. 0s means no timeout (not recommended).
      timeout = "5s"
      username = "sammy"
      password = "Mama3860"
      ## Set the user agent for HTTP POSTs (can be useful for log differentiation)
      # user_agent = "telegraf"
      ## Set UDP payload size, defaults to InfluxDB UDP Client default (512 bytes)
      # udp_payload = 512
```
启动telegraf
chkconfig telegraf on
service telegraf start
打开InfluxDB控制台，看看Telegraf在数据库中存储了哪些测量，连接您先前配置的用户名和密码
influx -username 'sammy' -password 'Mama3860'
show databases
切换到telegraf数据库
use telegraf
显示Telegraf通过执行此命令收集的各种测量
show measurements

#### 安装Kapacitor
Kapacitor是一个数据处理引擎。它允许您插入自己的自定义逻辑，以使用动态阈值处理警报，匹配模式的度量或识别统计异常。我们将使用Kapacitor从InfluxDB读取数据，生成警报，并将这些警报发送到指定的电子邮件地址。
yum install kapacitor
vi /etc/kapacitor/kapacitor.conf
找到[[influxdb]]部分，并提供用于连接到InfluxDB数据库的用户名和密码
```
# Multiple InfluxDB configurations can be defined.
# Exactly one must be marked as the default.
# Each one will be given a name and can be referenced in batch queries and InfluxDBOut nodes.
[[influxdb]]
  # Connect to an InfluxDB cluster
  # Kapacitor can subscribe, query and write to this cluster.
  # Using InfluxDB is not required and can be disabled.
  enabled = true
  default = true
  name = "localhost"
  urls = ["http://localhost:8086"]
  username = "sammy"
  password = "Mama3860"
```
启动kapacitor
chkconfig kapacitor on
service kapacitor start
验证Kapacitor是否正在运行，检查Kapacitor的任务列表
kapacitor list tasks
您将看到一个空的任务列表

#### 安装和配置Chronograf
Chronograf是一个图形和可视化应用程序，它提供了可视化监控数据和创建警报和自动化规则的工具。它包括对模板的支持，并且具有用于公共数据集的智能预配置仪表板库。我们将配置它连接到我们已经安装的其他组件
yum install chronograf
启动chronograf
chkconfig chronograf on
service chronograf start
现在，您可以通过在Web浏览器中访问http://192.168.11.40:8888/访问Chronograf界面