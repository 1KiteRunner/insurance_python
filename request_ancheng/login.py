# coding:utf8
import codecs
import pickle
import sys

import requests
from bs4 import BeautifulSoup

import settings as se
from common.log import Logger
from common.redisUtil import CRedis


reload(sys)

sys.setdefaultencoding('utf-8')

log = Logger()


def login_ancheng(flag=1):
    # 获取页面的lt和execution
    url_login_1 = "http://ply.e-acic.com/cas/login?service=http%3A%2F%2Fply.e-acic.com%2Fpcis%2Fj_spring_security_check"

    headers = se.HEADERS
    session = requests.session()
    session.headers.update(headers)
    ret_1 = session.get(url=url_login_1)

    html = ret_1.text

    soup = BeautifulSoup(html, 'html.parser')

    lt = soup.find("input", attrs={"name": "lt"})["value"]
    execution = soup.find("input", attrs={"name": "execution"})["value"]

    # 登录账号密码
    url_login_2 = "http://ply.e-acic.com/cas/login?service=http%3A%2F%2Fply.e-acic.com%2Fpcis%2Fj_spring_security_check"

    username = "132021892"
    password = "1121"

    logindata = {'username': username,
                 'lt': lt,
                 'password': password,
                 'execution': execution,
                 '_eventId': 'submit'}

    session.post(url_login_2, data=logindata)

    # 将session入库
    session.adapters.pop('https://')
    login_session = codecs.encode(pickle.dumps(session), "base64").decode()

    # 验证是否登陆成功
    url_login_3 = "http://ply.e-acic.com/pcis/core/pcis_main.jsp"

    ret_3 = session.get(url=url_login_3)

    # print r_3.text

    if "mainFrame" in ret_3.text:
        # print "ancheng login sucess"
        r = CRedis()
        r.set_session_redis(login_session, '12')
        log.info(u"ancheng login sucess ")
    else:
        # print "ancheng login fail"
        log.info(u"ancheng login fail ")
        if flag < 5:
            flag += 1
            return login_ancheng(flag)
        else:
            return None

    return session


if __name__ == "__main__":
    login_ancheng()
