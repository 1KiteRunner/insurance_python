# -*- coding:utf-8 -*-
__author__ = 'weikai'
from request_ancheng.login import login_ancheng
import codecs
import cPickle as pickle
from request_cic.login import logincic
from request_cicc.interface.login import login
from insert_session import insert_srssion
import datetime
import traceback
from request_pingan.login import Login
from request_cic import cic_settings as se
from common.sessionUtil import get_session
from request_ancheng.login import login_ancheng
from request_huanong.hn_login import Hn_Login


def __loginSession():
    sess = {}
    log1 = logincic()
    loginpingan = Login()

    if log1 is not None:
        log1_session = codecs.encode(pickle.dumps(log1), "base64").decode()
        loginRes = login()
        log2_seeion = codecs.encode(pickle.dumps(loginRes), "base64").decode()
        pingan_session = loginpingan.login()
        pingan_session = codecs.encode(
            pickle.dumps(pingan_session), "base64").decode()
    else:
        log1_session = None
        print('session4 login unsucess')
    sess['4'] = log1_session  # 中华联合
    sess['5'] = log2_seeion  # 大地保险
    sess['1'] = pingan_session
    return sess


def getSession():
    sessiondt = get_session(["1", "4", "5", "12", "13"])
    pingansession = sessiondt[0]
    sessio4 = sessiondt[1]
    sessio5 = sessiondt[2]
    ancheng_session = sessiondt[3]
    hn_session = sessiondt[4]


    # 测试session是否有效
    if sessio4 is not None:
        CUST_DATA = 'plateNo=' + '' + '&frmNo=' + 'LBELMBKC2EY568468'
        getcodeinfo_url = 'http://carply.cic.cn/pcis/policy/universal/quickapp/actionservice.ai'
        getcodeinfo_data = 'ADAPTER_TYPE=JSON_TYPE&SERVICE_TYPE=ACTION_SERVIC&CODE_TYPE=CODE_TYPE&BEAN_HANDLE=baseAction&ACTION_HANDLE=perform&SERVICE_NAME=vhlPlatformCommonAction&SERVICE_MOTHOD=getJsCheckInfo&DW_DATA=%255B%255D&HELPCONTROLMETHOD=common&SCENE=UNDEFINED&BIZ_SYNCH_CONTINUE=false&CUST_DATA=' + CUST_DATA
        headers = se.headers
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        try:
            getcodeinforesp = sessio4.post(
                url=getcodeinfo_url,
                data=getcodeinfo_data,
                headers=headers)
        except Exception as e:
            print(e)
            sessio4 = logincic()
        print('curru_url = %s' % getcodeinforesp.url)
    else:
        sessio4 = logincic()

    if sessio5 is None:
        sessio5 = login()

    if pingansession is None:
        loginpingan = Login()
        pingansession = loginpingan.login()

    if ancheng_session is None:
        ancheng_session = login_ancheng()

    if hn_session is None:
        hn = Hn_Login()
        hn_session = hn.hn_login()
    return {'4': sessio4, '5': sessio5, "1": pingansession, "12": ancheng_session, "13": hn_session}


# 如果有一个session失败都不会去插入表


def runSession():
    try:
        print("run session start" + str(datetime.datetime.now()))
        loginpingan = Login()
        hn = Hn_Login()

        log1 = logincic()
        loginRes = login()
        pingan_session = loginpingan.login()
        ancheng = login_ancheng()
        hn_session = hn.hn_login()
        print("run session end " + str(datetime.datetime.now()))
    except Exception as e:
        print(e)
        print(traceback.format_exc())


if __name__ == "__main__":
    runSession()
