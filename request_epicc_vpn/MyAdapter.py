# -*- coding:utf-8 -*-
__author__ = 'weikai'
import ssl
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import  settings as se

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize,block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

if __name__=="__main__":
    headers=se.headers_
    login_url="https://10.134.136.112:8888/casserver/login?service=http%3A%2F%2F10.134.136.112%3A80%2Fportal%2Findex.jsp"
    s = requests.Session()
    s.mount('https://', MyAdapter())  # 所有的https连接都用ssl.PROTOCOL_SSLV3去连接
    rsp=s.get(url=login_url,headers=headers,verify=False)
    print(rsp.text)
