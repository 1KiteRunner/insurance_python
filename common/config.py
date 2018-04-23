# -*- coding:utf-8 -*-
__author__ = 'weikai'
import socket
import json

# 距离多少天可以查询保费
days = 41
# REDIS HOST
# REDIS_HOST = "120.55.189.14"
# REDIS_PASSWORD = 'qwer12344321qwer'

REDIS_HOST = "54.222.246.139"
REDIS_PASSWORD = 'qwer12344321qwer'
# session缓存时间 20分钟
SESSIONTIME = 1200

# 自己的打码
DAMA_IP = "http://52.80.31.10:8088/"
# 内网地址
# DAMA_IP="http://10.0.1.233:8080/"
queryCode = "verificationCode/verificationCode/queryCode"
reportverificationCode = "verificationCode/verificationCode/reportverificationCode"

iplist = socket.gethostbyname_ex(socket.gethostname())

server = ["54.223.113.173",
          "54.223.171.99",
          "54.223.59.95",
          "54.223.201.101",
          "52.80.31.10",
          "54.223.230.150"]

for i in server:
    if i in json.dumps(iplist):
        MYSQLHOST = "10.0.1.244"
        break

# MYSQL配置
# 10.0.1.244
MYSQLHOST = '54.222.246.139'
MYSQLUSER = 'insurance'
MYSQLPASSWORD = 'insurance'
MYSQLDB = 'insurance'
# 代理配置


# mongodb配置
mongo_user = 'superuser'
mongo_password = 'nanMI2016'
mongo_uri = '52.80.31.10:27017'

# 核保开关 0关 1开
HEBAO_KEY = 1
