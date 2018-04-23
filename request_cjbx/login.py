# -*- coding:utf-8 -*-
__author__ = 'weikai'
import base64
import time
import socket
import json
import traceback
import codecs
import cPickle as pickle

import requests

from request_epicc.utils import pic2Str
from common.log import Logger
import request_cjbx.settings as se
from common.redisUtil import CRedis

headers = se.headers


def _Get_RandomNum(session_req):
    log = Logger()
    try:
        millis = int(round(time.time() * 1000))
        url = "http://32.0.192.232:88/sinoiais/pages/login/RandomNumUtil.jsp?d={0}".format(
            str(millis))
        code_resp = session_req.get(url=url, headers=headers)
        # 验证码
        codestr = None
        if code_resp:
            code_base64 = base64.b64encode(code_resp.content)
            codestr = pic2Str(base64.b64decode(code_base64))
        if not codestr:
            log.info("获取验证码异常")

        log.info("codestr=%s" % codestr)
        return codestr
    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())
        return None


def _checkLoginInfo(session_req, codestr):
    log = Logger()
    try:
        url = "http://32.0.192.232:88/sinoiais/checklogin/checkLoginInfo.do"
        headers['Content-Type'] = "application/x-www-form-urlencoded"
        data_1 = {
            "sysUserCode": "CJCXwm01",
            "sysPassWord": "2DDFE7",
            "random": codestr
        }

        login_1_resp = session_req.post(url=url, data=data_1, headers=headers)
        if "success" in login_1_resp.text:
            log.info(u"登录成功")
            return 1
        elif "randomError" in login_1_resp.text:
            log.error(u"验证码错误")
            return 0
        else:
            return 2
    except Exception as e:
        log.error(u"登录失败")
        log.error(traceback.format_exc())
        return 2


def _login_html(session_req):
    log = Logger()
    url = "http://32.0.192.232:88/sinoiais/login.html"
    headers['Content-Type'] = "application/x-www-form-urlencoded"
    data_2 = {
        "sysUser.userCode": "CJCXwm01",
    }
    login_2_resp = session_req.post(url=url, data=data_2, headers=headers)
    return login_2_resp


def get_sinoiais(session):
    url = "http://32.0.192.232:88/sinoiais/"
    rsp = session.get(url=url, headers=headers)
    return rsp


def login_cjbx():
    session_req = requests.session()
    session_req.headers.update(headers)
    # 设置代理
    # session_req.proxies = {'http':'118.178.232.65:808'}
    # 获取首页 拿到cookie
    rsp = get_sinoiais(session_req)
    # 获取验证码
    codestr = _Get_RandomNum(session_req)
    # 校验验证码
    out = _checkLoginInfo(session_req, codestr)
    count = 1
    if out == 1:
        _login_html(session_req)
        set_cjbx_session(session_req)
        return rsp
    elif out == 0:
        while count < 5:
            count = count + 1
            login_cjbx()


def set_cjbx_session(session):
    log = Logger()
    r = CRedis()
    base64_session = codecs.encode(pickle.dumps(session), "base64").decode()
    try:
        # file_object = open('session.txt', 'w')
        # file_object.write(base64_session)
        r.set("99_COMPANY", base64_session)
    except Exception as e:
        log.error("session error")
        log.error(traceback.format_exc())


def get_cjbx_session():
    log = Logger()
    try:
        r = CRedis()
        session = ""
        # file_object = open('session.txt')
        sessionbase64 = r.get("99_COMPANY")
        if sessionbase64 == None:
            session = login_cjbx()
        else:
            session = pickle.loads(codecs.decode(sessionbase64.encode(), "base64"))

        iplist = socket.gethostbyname_ex(socket.gethostname())
        if se.proxy not in json.dumps(iplist):
            session.proxies = se.proxies
        return session
    except Exception as e:
        log.error("session error")
        log.error(traceback.format_exc())


if __name__ == "__main__":
    login_cjbx()
    # session=get_cjbx_session()
    # print(1)
