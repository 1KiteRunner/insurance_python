# -*- coding:utf-8 -*-
import sys
from selenium import webdriver
import os
import time

from common.log import Logger
from common.sessionUtil import get_session
from login_ssl import login_ssl

import pickle
import codecs
import re

from MyAdapter import MyAdapter
log=Logger()


reload(sys)
sys.setdefaultencoding('utf-8')
IEdriver = "C:\Program Files (x86)\Internet Explorer\IEDriverServer.exe"

name = 'nanj-667'
pwd = '70611370'

name2 = 'A320100906'
pwd2 = 'Wdm201701'

def checkVPN(ip="10.134.136.112"):
    ip = "10.134.136.112"
    result = os.system('ping -n 4 -w 1 %s' % ip)

    return result

def killTask(name):
    for i in name:
        log.error("关闭进程")
        cmd = "taskkill /f /im %s" % i
        f = os.popen(cmd)

def login_vpn():
    try:
        os.environ["webdriver.ie.driver"] = IEdriver
        driver = webdriver.Ie()
        driver.implicitly_wait(15)
        url = "https://vpn.piccjs.com/remote-sale"
        login_url = 'https://vpn.piccjs.com/prx/000/http/10.134.136.112/portal'
        driver.get(url)
        driver.get("javascript:document.getElementById('overridelink').click();")
        try:
            driver.switch_to_alert().accept()
        except Exception,e:
            print e
        time.sleep(2)
        driver.execute_script('document.getElementById("uname").value = "%s";' % name)
        driver.execute_script('document.getElementById("pwd").value = "%s";' % pwd)
        driver.find_element_by_xpath('//*[@id="loginbtn"]').click()
        time.sleep(15)
        result = checkVPN()
        if result == 1:
            log.error("vpn连接异常，正在重新连接")
            killTask(["IEDriverServer.exe", "iexplore.exe"])
            login_vpn()
        else:
            log.error("vpn连接正常")
            return True
    except Exception,e:
        log.error("VPN登录失败，正在重新登录")
        return False

def check_session():
    srssion = get_session('2')
    if srssion is not None:
        sessBase = srssion
        req_session = pickle.loads(codecs.decode(sessBase.encode(), "base64"))
        req_session.mount('https://', MyAdapter())
        try:
            if_renewal_url = "http://10.134.136.112:8000/prpall/business/selectRenewalPolicyNo.do"
            req_session.post(if_renewal_url,verify=False).json()
            return True
        except Exception,e:
            log.error(e)
            return False
    else:
        return False

def check_relogin():
    result = checkVPN()
    if result == 1:
        log.error("vpn连接异常，正在重新连接")
        killTask(["IEDriverServer.exe", "iexplore.exe"])
        result = login_vpn()
        if result:
            login_ssl()
    else:
        result = check_session()
        if result:
            log.info("检测到session正常")
        else:
            log.error("session失效，正在重新登录")
            login_ssl()

    # try:
    #     driver.switch_to_alert().accept()
    # except Exception,e:
    #     print e
    # driver.get(login_url)
    # driver.get("javascript:document.getElementById('overridelink').click();")
    # driver.execute_script('document.getElementById("username1").value = "%s";' % name2)
    # driver.execute_script('document.getElementById("password1").value = "%s";' % pwd2)
    # driver.find_element_by_xpath('//*[@id="button"]').click()
    # driver.get("http://10.134.136.112:8000/prpall/index.jsp?calogin")
    # driver.switch_to.frame('main')
    # driver.switch_to.frame('page')
    # return driver.get_cookies()

def getCookie():
    login_vpn()
    # cookieStr=""
    # for cookie in  cookies:
    #     cookieStr = cookieStr+cookie['name']+"="+cookie['value']+";"
    # myheaders={
    #     "Accept": "application/x-ms-application, image/jpeg, application/xaml+xml, image/gif, image/pjpeg, application/x-ms-xbap, */*",
    #     "Accept-Language": "zh-CN",
    #     "User-Agent":"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    #     "Accept-Encoding": "gzip, deflate",
    #     "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    #     "Cookie": cookieStr
    # }
    # req_session = requests.session()
    # req_session.headers.update(myheaders)
    # log1_session = codecs.encode(pickle.dumps(req_session), "base64").decode()
    # updata_session("2",{"2":log1_session})
if __name__=="__main__":
    check_relogin()
    # licenseNoList = [u"苏AQ6C06",u"苏AB1P05",u"苏AB2R68",u"苏AB0P61",u"苏AB9N73",u"苏AK0C77",u"苏AB2Q60",u"苏AB9N35",u"苏AB3Q98",u"苏AK8A77",u"苏AB0Q87",u"苏B768TD",u"苏ACT331"]
    # licenseNoList = [u'苏AY9H66']
    # for licenseNo in licenseNoList:
    #     print json.dumps(getCookie(),ensure_ascii=False,indent=4)
    # print json.dumps(carDic,ensure_ascii=False,indent=4)
    # print json.dumps(personDic,ensure_ascii=False,indent=4)
    # print time.time()-startTime


