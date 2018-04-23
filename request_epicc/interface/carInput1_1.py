# -*- coding:utf-8 -*-
__author__ = 'weikai'
import  re

import  requests

from  request_epicc import settings as se
from common.log import  Logger

log=Logger()

#获取sessionid
# def carInput1_1(s):
#     # headers=se.headers
#     data='head.requestType=&head.requestCode=20132001&head.uuid=1234&head.sessionId=first&head.channelNo=2&proSelected=32000000&citySelected=32010000&citySelect=11000000'
#     res=s.post(url=se.carInput1_url,data=data)
#     txt=res.text
#     sessionId= re.findall(r"<input type=\"hidden\" name=\"head.sessionId\" value=\"(.+?)\" id='sessionId'>",txt,re.S)[0]
#     log.info(u'sessionid=%s' % sessionId)
#     return sessionId

def carInput1_1(citySelected,proSelected):
    headers=se.headers
    data='head.requestType=&head.requestCode=20132001&head.uuid=1234&head.sessionId=first&head.channelNo=2&proSelected='+proSelected+'&citySelected='+citySelected+'&citySelect=11000000'
    res=requests.post(url=se.carInput1_url,headers=headers,data=data)
    txt=res.text
    sessionId= re.findall(r"<input type=\"hidden\" name=\"head.sessionId\" value=\"(.+?)\" id='sessionId'>",txt,re.S)[0]
    log.info(u'sessionid=%s' % sessionId)
    return sessionId


def carInput1_2(citySelected, proSelected):
    headers = se.headers
    reqsss = requests.session();
    reqsss.headers.update(headers)
    data = 'head.requestType=&head.requestCode=20132001&head.uuid=1234&head.sessionId=first&head.channelNo=2&proSelected=' + proSelected + '&citySelected=' + citySelected + '&citySelect=11000000'
    res = reqsss.post(url=se.carInput1_url, headers=headers, data=data)
    txt = res.text
    sessionId = \
        re.findall(r"<input type=\"hidden\" name=\"head.sessionId\" value=\"(.+?)\" id='sessionId'>", txt, re.S)[0]
    log.info(u'sessionid=%s' % sessionId)
    dt = {}
    return {'sessionId': sessionId, 'request': reqsss}
