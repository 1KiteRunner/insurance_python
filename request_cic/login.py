# -*- coding:utf-8 -*-
__author__ = 'weikai'
import re
import requests
import request_cic.cic_settings as SE
from common.sessionUtil import set_session
from common.log import Logger

log = Logger()


def logincic():
    # username='ex_xishijuan001'
    # password='xishijuan002'
    username = 'ex_caowenjing002'
    password = '10072X'
    login_url = 'http://sso.cic.cn/cas/login?service=http%3A%2F%2Fcarply.cic.cn%2Fpcis%2Fj_spring_cas_security_check'
    headers = SE.headers
    reqsss = requests.session()
    reqsss.headers.update(headers)
    req = reqsss.get(url=login_url)

    req = req.text
    LT = re.findall(r"<input type=\"hidden\" name=\"lt\" value=\"(.+?)\" /> ", req, re.S)[0]
    execution = re.findall(r"type=\"hidden\" name=\"execution\" value=\"(.+?)\" ", req, re.S)[0]

    login_url2 = 'http://sso.cic.cn/cas/login?service=http%3A%2F%2Fcarply.cic.cn%2Fpcis%2Fj_spring_cas_security_check'
    logindata = {'username': username,
                 'lt': LT,
                 'password': password,
                 'execution': execution,
                 '_eventId': 'submit'}
    login_resp = reqsss.post(url=login_url2, data=logindata)

    if 'frmMain' in login_resp.text:
        log.info(u"cic login sucess ")
        set_session(reqsss, "4")
        return reqsss
    else:
        log.error(u"login f %s ", reqsss)
        #logincic()


if __name__ == "__main__":
    logincic()
