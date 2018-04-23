# -*- coding:utf-8 -*-
__author__ = 'weikai'
import json
from request_huanong.hn_settings import headers
from common.dama.damaUtil import dama
from common.log import Logger


def _get_carInof(session, vinNo):
    # 请求车管所验证码
    log = Logger()
    headers['Content-Type'] = "application/x-www-form-urlencoded; charset=UTF-8"
    url = "http://qcar.chinahuanong.com.cn/quotepriceasync/carInfoInquiryjiangsu.do"
    data = {"licenseNo": "",
            "vinNo": vinNo
            }
    rspcode = session.post(url=url, data=data, headers=headers)
    rspcode_json = rspcode.json()
    checkNo = rspcode_json['checkNo']
    checkCode = rspcode_json['checkCode']
    codestr = dama("3", checkCode)
    # 获取车管所信息
    url2 = "http://qcar.chinahuanong.com.cn/quotepriceasync/comfirmCarInfoInquiry.do"
    data2 = {"checkNo": checkNo, "checkCode": codestr}
    rsp2 = session.post(url=url2, data=data2)
    return rsp2.text


def get_carInof(session, vinNo):
    log = Logger()
    rsp = _get_carInof(session, vinNo)
    count = 1
    while u"录入的校验码有误" in rsp and count < 5:
        log.error(u"录入的校验码有误")
        rsp = _get_carInof(session, vinNo)
        count = count + 1
    if "licenseNo" in rsp:
        return json.loads(rsp)['carArr'][0]
    else:
        log.error(u"华农未获取到车管所信息 %s ", vinNo)
        return 0
