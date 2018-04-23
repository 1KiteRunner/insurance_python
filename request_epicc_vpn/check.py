# -*- coding:utf-8 -*-
#检查VPN是否还在线如果不在线会重新登录更新数据库中的session
import os
from request_epicc_vpn.login import login_vpn

from login_ssl import login_ssl
IEdriver = "C:\Program Files (x86)\Internet Explorer\IEDriverServer.exe"

name = 'nanj-617'
pwd = '201701'

name2 = 'A320100906'
pwd2 = 'c464465851'

def checkVPN(ip="10.134.136.112"):
    ip = "10.134.136.112"
    result = os.system('ping -n 4 -w 1 %s' % ip)
    return result

def killTask(name):
    for i in name:
        cmd = "taskkill /f /im %s" % i
        f = os.popen(cmd)

def check_relogin():
    result = checkVPN()
    if result==1:
        killTask(["IEDriverServer.exe","iexplore.exe"])
        result = login_vpn()
        if result:
            login_ssl()
    #
    # try:
    #     srssion = get_session()
    #     sessBase = srssion['2']
    #     req_session = pickle.loads(codecs.decode(sessBase.encode(), "base64"))
    #     licenseNo = u'苏bz970w'
    #     mydata = "prpCrenewalVo.policyNo=&prpCrenewalVo.othFlag=&prpCrenewalVo.engineNo=&prpCrenewalVo.frameNo=&prpCrenewalVo.vinNo=&prpCrenewalVo.licenseNo=" + urllib.quote(licenseNo.encode('gb2312')) + "&prpCrenewalVo.licenseColorCode=&prpCrenewalVo.licenseType=02"
    #     req_session.post("http://10.134.136.112:8000/prpall/business/selectRenewal.do?pageSize=10&pageNo=1",data=mydata)
    # except Exception,e:
    #     killTask(["IEDriverServer.exe", "iexplore.exe"])
    #     cookie = getCookie()
    #     updata_session("2", {"2": cookie})

if __name__=="__main__":
    check_relogin()