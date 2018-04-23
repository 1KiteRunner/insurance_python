# -*- coding:utf-8 -*-
__author__ = 'weikai'
from request_huanong.hn_settings import headers
from common.log import Logger
import jsonpath
import json
from request_huanong.hn_parse import hn_parse_renrwal


def is_hn_renewal(session, licenseNo="", vinNo=""):
    log = Logger()
    try:
        url = "http://qcar.chinahuanong.com.cn/quotepriceasync/getOldPolicy.do"
        headers['Content-Type'] = "application/x-www-form-urlencoded; charset=UTF-8"
        data = {"licenseNo": licenseNo,
                "vinNo": vinNo,
                "engineNo": ""
                }
        rsp = session.post(url=url, data=data, headers=headers)
        if u"发生异常" in rsp.text:
            return 0
        else:
            if len(rsp.json()) != 0:
                log.info(u"是华农续保用户")
                return rsp.json()
            else:
                return 0
    except Exception as e:
        log.error(e)
        return 0


def hn_renewal_userinfo(session, policyNo):
    # 0507 JQ
    # 0506 SY
    log = Logger()
    try:
        url = "http://qcar.chinahuanong.com.cn/quotepriceasync/getPolicyInfo.do?policyNo=" + policyNo
        rsp = session.get(url=url)
        if 'licenseNo' in rsp.text:
            return rsp.json()
        else:
            return False
    except Exception as e:
        log.error(e)
        return False


def get_hn_userinfo(session, licenseNo="", vinNo=""):
    log = Logger()
    try:
        rsp1 = is_hn_renewal(session, licenseNo, vinNo)
        policyNo = ""
        rsp2 = ""
        syStart = syEnd = jqStart = jqEnd = ""
        if rsp1 != 0:
            JQ = jsonpath.jsonpath(rsp1, "$.[?(@.riskCode=='0507')]")
            SY = jsonpath.jsonpath(rsp1, "$.[?(@.riskCode=='0506')]")

            if JQ != False:
                jq_policyNo = JQ[0]['policyNo']
                jqStart=JQ[0]['startDate']
                jqEnd=JQ[0]['endDate']
                JQ_RSP = hn_renewal_userinfo(session, jq_policyNo)
            if SY != False:
                sy_policyNo = SY[0]['policyNo']
                syStart=JQ[0]['startDate']
                syEnd=JQ[0]['endDate']
                SY_RSP = hn_renewal_userinfo(session, sy_policyNo)

            if JQ_RSP != False:
                rsp2 = JQ_RSP
            else:
                rsp2 = SY_RSP
            insuranceType = hn_parse_renrwal(JQ_RSP, SY_RSP)
            out = {
                "licenseNo": licenseNo,
                "vinNo": rsp2['car']['vinNo'],
                "endDate": rsp2['base']['endDate'],
                "CCardDetail": rsp2['car']['vehicleStyle'],
                "brandName": rsp2['car']['modelName'],
                "insuredName": rsp2['persons'][0]['insuredName'],
                "identifyNumber": rsp2['persons'][0]['identifyNumber'],
                "CUsageCde": "",
                "NNewPurchaseValue": rsp2['car']['purchasePrice'],
                "insuredAddress": rsp2['persons'][0]['insuredAddress'],
                "mobile": rsp2['persons'][0]['mobile'],
                "enrollDate": rsp2['car']['enrollDate'],
                "engineNo": rsp2['car']['engineNo'],
                "CModelCde": rsp2['car']['modelCode'],
                "NSeatNum": "",
                "COMPANY_ID": "13",
                "insuranceType": insuranceType,
                "insuranceTime": {'syEnd': syEnd,
                                  'syStart': syStart,
                                  'jqStart': jqStart,
                                  'jqEnd': jqEnd}
            }
            return out
    except Exception as e:
        log.error(e)
        return 0


if __name__ == "__main__":
    from common.sessionUtil import get_session

    session = get_session("13")
    print json.dumps(get_hn_userinfo(session, licenseNo=u"苏JLS055"), ensure_ascii=False)
