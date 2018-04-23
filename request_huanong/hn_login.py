# -*- coding:utf-8 -*-
__author__ = 'weikai'
import base64
import requests
from common.dama.damaUtil import dama
from request_huanong import hn_settings as se
from common.log import Logger
from common.sessionUtil import set_session
from common.OCR.orc_dama import dama_huanong

log = Logger()


class Hn_Login():
    def __init__(self, username=None, password=None):
        self.session_req = requests.session()
        self.headers = se.headers
        self.session_req.headers.update(se.headers)
        self.session_req.get("http://qcar.chinahuanong.com.cn/")
        if username is None or password is None:
            self.username = se.login_username
            self.password = se.login_password

    # 刷新获取验证码
    def __refresh_code(self, reqsss):
        code_url = "http://qcar.chinahuanong.com.cn/verifImageServlet"
        self.headers['Referer'] = "http://qcar.chinahuanong.com.cn/"
        code_resp = reqsss.get(url=code_url, headers=self.headers)
        code_base64 = base64.b64encode(code_resp.content)
        #codestr = dama("1", code_base64)
        codestr = dama_huanong(code_base64)
        log.info(u"华农登录验证码为%s" % codestr)
        return codestr

    def __login(self, reqsss, codestr):
        login_url = 'http://qcar.chinahuanong.com.cn/checkUser.do'
        headers = se.headers
        headers['Content-Type'] = "application/x-www-form-urlencoded"
        login_data = "ipAddr=&macAddr=&usercode=%s&passwd=%s&checkCode=%s" % (
            se.login_username, se.login_password, codestr)
        req = reqsss.post(url=login_url, data=login_data, headers=headers)
        if "frameset" in req.text:
            log.info(u"华农登录成功")
            # 往redis中存储session
            set_session(self.session_req, "13")
            return self.session_req
        else:
            log.error(u"华农登录失败")
            return 0

    def hn_login(self, username=None, password=None):
        try:
            # 刷新验证码
            codestr = self.__refresh_code(self.session_req)
            # 校验验证码
            count = 1
            out = self.__login(self.session_req, codestr)
            while out == 0 and count < 4:
                codestr = self.__refresh_code(self.session_req)
                count = count + 1
                out = self.__login(self.session_req, codestr)
                # self.auto_index_do(out)
            if out != 0:
                return out
        except Exception as e:
            log.info(e)


if __name__ == "__main__":
    l = Hn_Login()
    l.hn_login()
