# -*- coding:utf-8 -*-
__author__ = 'weikai'
import base64, re
import requests
import request_pingan.settings as se
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from common.dama.damaUtil import dama
from common.log import Logger
from common.sessionUtil import set_session
from common.redisUtil import CRedis
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Login(object):
    def __init__(self, username=None, password=None):
        self.log = Logger()
        self.session_req = requests.session()
        self.session_req.headers.update(se.headers)
        if username is None or password is None:
            self.username = se.login_username
            self.password = se.login_password

    # 刷新获取验证码
    def __refresh_code(self, reqsss):
        code_url = "https://icore-pts.pingan.com.cn/ebusiness/auto/rand-code-imgage.do" \
                   "?random=0.37327206414192915"
        code_resp = reqsss.get(url=code_url, headers=se.headers, verify=False)
        code_base64 = base64.b64encode(code_resp.content)
        codestr = dama("2", code_base64)
        self.log.info(u"平安登录验证码为%s", codestr)
        return codestr

    # 发送验证码
    def __validate_code(self, reqsss, codestr):
        set_code_url = "https://icore-pts.pingan.com.cn/ebusiness/auto/" \
                       "VerifyRandCodeController.do?randCode=" + codestr
        set_code_resp = reqsss.get(
            url=set_code_url,
            headers=se.headers,
            verify=False)
        set_code_result = set_code_resp.text
        if set_code_result == "true":
            self.log.info(u"平安验证码校验正确")
            return 1
        self.log.error(u"平安登录验证码错误")
        return 0

    def __use_login(self, reqsss):
        # 登录前置请求
        login_monitor_url = "https://icore-pts.pingan.com.cn/ebusiness/auto/monitor.do?" \
                            "type=insertLoginLog&flowid=&userId=STDJNDS-00001&_t=1487214110283"
        reqsss.post(
            url=login_monitor_url, headers=se.headers, verify=False)

    def __login(self, reqsss, codestr):
        login_url = 'https://icore-pts.pingan.com.cn/ebusiness/j_security_check'
        se.headers['Content-Type'] = "application/x-www-form-urlencoded"
        headers = se.headers
        login_data = "j_username=" + self.username + "&j_password=" + \
                     self.password + "&SMAUTHREASON=0&randCode=" + codestr
        req = reqsss.post(
            url=login_url,
            data=login_data,
            headers=headers,
            verify=False)
        if req.url == u'https://icore-pts.pingan.com.cn/ebusiness/':
            self.log.info(u"平安登录成功")
            # 往redis中存储session
            set_session(self.session_req, "1")
            return self.session_req

        self.log.error(u"平安登录失败")
        self.log.error(req.text)
        return 0

    def login(self):
        try:
            # 刷新验证码
            codestr = self.__refresh_code(self.session_req)
            # 校验验证码
            count = 1
            validate_code_result = self.__validate_code(self.session_req, codestr)
            while validate_code_result == 0 and count < 4:
                codestr = self.__refresh_code(self.session_req)
                validate_code_result = self.__validate_code(
                    self.session_req, codestr)
                count += 1
            # 发送登录前置请求
            self.__use_login(self.session_req)
            out = self.__login(self.session_req, codestr)
            # self.auto_index_do(out)
            if out != 0:
                #self.auto_index_do(out)
                return out
        except Exception as error:
            self.log.info(error)
            # 获取保持连接的id

    def auto_index_do(self, session):
        '''
        :param session:登录后的session
        :return:flow_id
        '''
        index_url = "https://icore-pts.pingan.com.cn/ebusiness/auto/newness/index.do"
        index_rsp = session.get(
            url=index_url,
            verify=False)
        index_rsp_text = index_rsp.text
        flow_id = re.findall(r"<div id=\"main\" flowid=\"(.+?)\">", index_rsp_text, re.S)[0]
        r = CRedis()
        r.set("pingan_keepid", flow_id)
    '''
    def send_keep_id(self, session):
        r = CRedis()
        kee_id = r.get("pingan_keepid")
        if kee_id is not None:
            keep_url = "https://icore-pts.pingan.com.cn/ebusiness/auto/keep-flow.do?flowid=" + kee_id
            rsp = session.get(
                url=keep_url, headers=se.headers, verify=False)
            self.log.info(rsp.status_code)

    def send_agentDealer(self, session):
        r = CRedis()
        kee_id = r.get("pingan_keepid")
        if kee_id is not None:
            keep_url = "https://icore-pts.pingan.com.cn/ebusiness/auto/newness/agentDealer.do?flowid=" + kee_id
            data = {"dealerCode": "210697215001",
                    "readDataFlag": "supply"}
            rsp = session.post(
                url=keep_url, data=data,headers=se.headers, verify=False)
            self.log.info(rsp.status_code)

    def send_navigators(self,session):
        r = CRedis()
        kee_id = r.get("pingan_keepid")
        url = "https://icore-pts.pingan.com.cn/ebusiness/auto/newness/save-navigators.do?flowid="+kee_id+"&platform=Win32&userAgent=Mozilla%2F5.0+(Windows+NT+6.1%3B+WOW64)+AppleWebKit%2F537.36+(KHTML%2C+like+Gecko)+Chrome%2F53.0.2785.143+Safari%2F537.36"
        rsp = session.get(
                url=url, headers=se.headers, verify=False)
        self.log.info(rsp.status_code)

    def timeout_to_continue(self, session):
        r = CRedis()
        kee_id = r.get("pingan_keepid")
        if kee_id is not None:
            url="https://icore-pts.pingan.com.cn/ebusiness/auto/newness/timeout-to-continue.do?flowid="+kee_id
            rsp = session.get(url=url, headers=se.headers, verify=False)
            self.log.info(rsp.text)
    '''
if __name__ == "__main__":
    l = Login()
    session=l.login()

