# -*- coding:utf-8 -*-
__author__ = 'weikai'
from Scheduler.session import getSession
from request_pingan import settings as pinganset
from request_cic import cic_settings as cicset
from request_pingan.renewal import is_renewal
from request_cic.login import  logincic

def keep_alive_session():
    try:
        sessiondt = ""
        sessiondt = getSession()
        requestcic = sessiondt['4']
        loginRes = sessiondt['5']
        pingansession = sessiondt['1']
        ancheng_session = sessiondt['12']
        hn_session = sessiondt['13']
        '''
        rsp = pingansession.get(url="https://icore-pts.pingan.com.cn/ebusiness/query/queryUserInfo.do",
                                headers=pinganset.headers,
                                verify=False)
        if "1069004717001" in rsp.text:
            print(u"pingan SESSION IS ALIVE")
        else:
            print(u"pingan SESSION IS DEATH")'
        pinganrsp = pingansession.get(url="https://icore-pts.pingan.com.cn/ebusiness/", headers=pinganset.headers,
                                      verify=False)
        if "安全退出" in pinganrsp.text:
            print(u"pingan SESSION IS ALIVE")
        else:
            print(u"pingan SESSION IS DEATH")'''

        cicrsp = requestcic.get("http://carply.cic.cn/pcis/core/header.jsp", headers=cicset.headers)
        if "今日验车码" in cicrsp.text:
            print(u"cic SESSION IS ALIVE")
        else:
            print(u"cic SESSION IS DEATH")
            logincic()
        loginRes = loginRes[0]
        ciccrsp = loginRes.get("http://b2b.ccic-net.com.cn/mss/index.jsp", headers=cicset.headers)
        if "欢迎光临" in ciccrsp.text:
            print(u"大地SESSION IS ALIVE")
        else:
            print(u"大地SESSION IS DEATH")

        hnrsp = hn_session.get("http://qcar.chinahuanong.com.cn/menu/orgMenus.do", headers=cicset.headers)
        if "暂存单管理" in hnrsp.text:
            print(u"华农SESSION IS ALIVE")
        else:
            print(u"华农SESSION IS DEATH")

        ancheng = ancheng_session.get("http://ply.e-acic.com/pcis/core/header.jsp", headers=cicset.headers)
        if "欢迎您" in ancheng.text:
            print(u"安城SESSION IS ALIVE")
        else:
            print(u"安城SESSION IS DEATH")
        #is_renewal(pingansession)
    except Exception, e:
        print(e)


if __name__ == "__main__":
    keep_alive_session()