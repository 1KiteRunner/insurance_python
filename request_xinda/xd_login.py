# -*- coding:utf-8 -*-
__author__ = 'weikai'
import re
import requests
import request_xinda.settings as SE
from common.sessionUtil import set_session
from common.log import Logger

log = Logger()


def xd_login():
    username = '03129002'
    #跟信达协商了，每50天自动改密码，密码规则类似人保，前面的字母不变，后缀数字按年+月来自动顺延 QWEasd1706
    password = 'QWEasd123'
    login_url = 'http://10.75.1.10:8001/prpall/UICentralControl?SelfPage=/common/pub/UILogonInput.jsp'
    headers = SE.HEADERS_XINDA
    reqsss = requests.session()
    reqsss.headers.update(headers)

    logindata = "UserCode=" + username + "&Password=" + password + "&ComCode=03120000&MacAddress=&RiskCode=0500&ClassCode=&ClassCodeSelect=05&RiskCodeSelect=0500&image.x=42&image.y=9"
    login_resp = reqsss.post(url=login_url, data=logindata)

    if 'parent.fraCode.window.location' in login_resp.text:
        log.info(u"xinda login sucess ")
        set_session(reqsss, "14")
        return reqsss
    else:
        log.error(u"login f %s ", reqsss)


if __name__ == "__main__":
    xd_login()
