# -*- coding:utf-8 -*-
from common.sessionUtil import set_session

__author__ = 'weikai'

import requests,re
from MyAdapter import MyAdapter
import  settings as se
import sys
from selenium import webdriver
import os
import requests
import urllib
from bs4 import BeautifulSoup
import pickle
import codecs
import time
import json
import datetime
from request_epicc_vpn.dbUtil import updata_session
import urllib
from common.log import Logger

log=Logger()

def login_ssl():
    try:
        #访问首页
        headers=se.headers_
        login_url="https://10.134.136.112:8888/casserver/login?service=http%3A%2F%2F10.134.136.112%3A80%2Fportal%2Findex.jsp"
        index_request = requests.Session()
        index_request.headers.update(headers)
        index_request.mount('https://', MyAdapter())
        index_html_resp=index_request.get(url=login_url,headers=headers,verify=False)
        index_html_body=index_html_resp.text
        LT=re.findall(r"<input type=\"hidden\" name=\"lt\" value=\"(.+?)\" />",index_html_body,re.S)[0]
        print(LT)
        #请求登陆获取ticket
        login_url2="https://10.134.136.112:8888/casserver/login?service=http%3A%2F%2F10.134.136.112%3A80%2Fportal%2Findex.jsp"
        headers['Content-Type']="application/x-www-form-urlencoded"
        index_request.headers.update(headers)
        # headers['Referer']="https://10.134.136.112:8888/casserver/login?service=http%3A%2F%2F10.134.136.112%3A80%2Fportal%2Findex.jsp"
        body="PTAVersion=&toSign=&Signature=&rememberFlag=1&userMac=&key=yes&errorKey=null&loginMethod=nameAndPwd&username="+se.username+"&password="+se.password+"&lt="+LT+"&_eventId=submit&pcguid=&button.x=25&button.y=10"
        ticket_res=index_request.post(url=login_url2,data=body,verify=False)
        print ticket_res.url
        #print(ticket_res.text)

        index_request.adapters.pop('https://')
        log1_session = codecs.encode(pickle.dumps(index_request), "base64").decode()
        set_session(log1_session,'2')
        # updata_session("2", {"2": log1_session})
    except Exception,e:
        print e
        print "第二层登录失败，正在重新登录"
        login_ssl()

if __name__=="__main__":
    login_ssl()
    # try:
    #     licenseNo = u'苏A21P07'
    #     srssion = get_session()
    #     sessBase = srssion['2']
    #     req_session = pickle.loads(codecs.decode(sessBase.encode(), "base64"))
    #     if_renewal_url = "http://10.134.136.112:8000/prpall/business/selectRenewalPolicyNo.do?licenseNo=" + urllib.quote(licenseNo.encode('gb2312')) + "&licenseFlag=1&licenseType=02"
    #     if_renewal_res = req_session.post(if_renewal_url).json()
    #     print(if_renewal_res)
    # except Exception,e:
    #     log.error(e)

