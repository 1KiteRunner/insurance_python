# coding: utf8
import base64
import codecs
import json
import time
import pickle
import requests
import settings as se
from request_cjbx.func import get_request, post_request, update_new_session
from request_epicc.utils import pic2Str
# 禁用安全请求警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def login_ssl():
    try:
        millis = int(round(time.time() * 1000))
        headers = se.headers
        with open('cookie.txt') as f:
            TWFID = f.readline()
            print TWFID

        headers["Cookie"] = "TWFID={0}".format(TWFID)

        url_yzm = "https://vpn.cjbx.com.cn/web/0/http/1/88.32.0.232:88/sinoiais/pages/login/RandomNumUtil.jsp?d={0}".format(
            str(millis))

        code_resp = get_request(url=url_yzm, headers=headers)

        # 验证码
        codestr = None
        if code_resp:
            code_base64 = base64.b64encode(code_resp.content)
            codestr = pic2Str(base64.b64decode(code_base64))

        if not codestr:
            print u"获取验证码异常"

        print codestr

        url_login1 = "https://vpn.cjbx.com.cn/web/0/http/1/88.32.0.232:88/sinoiais/checklogin/checkLoginInfo.do"
        data_1 = {
            "sysUserCode": "CJCXwm01",
            "sysPassWord": "2DDFE7",
            "random": codestr
        }
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        login_1_resp = post_request(url=url_login1, data=data_1, headers=headers)
        if not login_1_resp:
            return

        print login_1_resp.text

        response_body = login_1_resp.content.decode()
        response_body = json.loads(response_body)
        print response_body
        print type(response_body)
        msg = response_body.get('msg')
        count =0
        if msg != 'success' and count <5:
            print u'验证码错误'
            count=count+1
            return login_ssl()

        # 如果验证码返回错误不执行第二步
        url_login2 = "https://vpn.cjbx.com.cn/web/1/http/1/88.32.0.232:88/sinoiais/login.html"
        data_2 = {
            "sysUser.userCode": "CJCXwm01",
        }

        login_2_resp = post_request(url=url_login2, data=data_2, headers=headers)
        # print login_2_resp.text

        # req_session.adapters.pop('https://')
        # log1_session = codecs.encode(pickle.dumps(req_session), "base64").decode()
        # update_new_session("11", {"11": log1_session})

    except Exception as e:
        print e





if __name__ == "__main__":
    login_ssl()
