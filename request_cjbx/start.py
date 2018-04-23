# -*- coding:utf-8 -*-
__author__ = 'weikai'
import traceback
from parse2 import parse_query_all
from request_data import query_car, query_detail, policy_info
from common.log import Logger
from common.mongodb.mongoUtils import mg_update_insert
import datetime
from request_cjbx.login import get_cjbx_session
import gevent
from gevent import monkey
import json

log = Logger()
monkey.patch_socket()
monkey.patch_ssl()
monkey.patch_all()


# licenseType = “01”大型汽车号牌   "02" 小型汽车号牌 “15”挂车号牌  暂时只支持这些 默认处理为02
def cjbx_start(palte_number, licensetype="02"):
    try:
        session = get_cjbx_session()
        out1 = query_detail(palte_number, session=session, licensetype=licensetype)
        if out1 != 0:
            # 获取车辆详细信息
            html = query_car(palte_number, session=session, licensetype=licensetype)
            alldt = parse_query_all(html)
            alldt['CAR_INFO'] = out1
            # 取出前两条保险详情
            if len(alldt) != 0 and len(alldt['SY']) != 0:
                if len(alldt['SY']) > 1:
                    g1 = gevent.spawn(policy_info, alldt['SY'][0]['INSURE_CODE'], session)
                    g2 = gevent.spawn(policy_info, alldt['SY'][1]['INSURE_CODE'], session)
                    gevent.joinall([g2, g1])
                    alldt['SY'][0]['INSURANCE_TYPE'] = g1.value.get('insuranceType', {})
                    alldt['SY'][0]['INFO'] = g1.value.get('Info', {})
                    alldt['SY'][1]['INSURANCE_TYPE'] = g2.value.get('insuranceType', {})
                    alldt['SY'][1]['INFO'] = g2.value.get('Info', {})
                else:
                    insuranceType = policy_info(alldt['SY'][0]['INSURE_CODE'], session=session)
                    alldt['SY'][0]['INSURANCE_TYPE'] = insuranceType.get('insuranceType', {})
                    alldt['SY'][0]['INFO'] = insuranceType.get('Info', {})
            mg_update_insert('InsuranceInfo', {'BODY.PALTE_NO': palte_number}, alldt)
            mydata = parse_body(alldt)
            log.info(json.dumps(mydata, ensure_ascii=False))
            return mydata
        else:
            log.error(u"未查询到用户信息 %s " % palte_number)
            return 0
    except Exception, e:
        log.error(e)
        log.error(traceback.format_exc())
        return 0


def parse_body(body):
    syEnd = syStart = ""
    jqStart = jqEnd = ""
    COMPANY = ""
    insuranceType = {}
    endDate = SY_END_DATE = JQ_END_DATE = ""
    if len(body.get('SY', [])) != 0:
        syStart = body.get('SY', [])[0].get('START_DATE', "")
        syEnd = body.get('SY', [])[0].get('END_DATE', "")
        COMPANY = body.get('SY', [])[0].get('COMPANY', "")
        SY_END_DATE = body.get('SY', [])[0].get('END_DATE', "")
        insuranceType = body.get('SY', [])[0].get('INSURANCE_TYPE', {})
    if len(body.get('JQ', [])) != 0:
        jqStart = body.get('JQ', [])[0].get('START_DATE', "")
        jqEnd = body.get('JQ', [])[0].get('END_DATE', "")
        COMPANY = body.get('JQ', [])[0].get('COMPANY', "")
        SY_END_DATE = body.get('JQ', [])[0].get('END_DATE', "")

    if SY_END_DATE == "":
        SY_END_DATE = _getlatedate(0)
    if JQ_END_DATE == "":
        JQ_END_DATE = _getlatedate(0)
    datetmp = _compare_date(str(JQ_END_DATE), str(SY_END_DATE))
    datamax = _compare_date(datetmp, _getlatedate(0))
    endDate = datamax

    out = {
        "licenseNo": body.get('CAR_INFO', {}).get('PLATE_NUMBER', ''),
        "vinNo": body.get('CAR_INFO', {}).get('FRAME_NUMBER', ''),
        "endDate": endDate,
        "CCardDetail": body.get('CAR_INFO', {}).get('VEHICLE_TYPE', ''),
        "brandName": body.get('CAR_INFO', {}).get('CHINESE_BRAND', '') + " " + body.get('CAR_INFO', {}).get(
            'VEHICLE_MODEL', ''),
        "insuredName": body.get('CAR_INFO', {}).get('OWNER_NAME', ''),
        "identifyNumber": "",
        "CUsageCde": "",
        "NNewPurchaseValue": "",
        "insuredAddress": "",
        "mobile": "",
        "enrollDate": body.get('CAR_INFO', {}).get('INITIAL_REGISTRATION_DATE', ''),
        "engineNo": body.get('CAR_INFO', {}).get('INITIAL_REGISTRATION_DATE', ''),
        "CModelCde": "",
        "NSeatNum": body.get('CAR_INFO', {}).get('SEATING_CAPACITY', '5'),
        "COMPANY_ID": COMPANY,
        "insuranceType": insuranceType,
        "insuranceTime": {'syEnd': syEnd,
                          'syStart': syStart,
                          'jqStart': jqStart,
                          'jqEnd': jqEnd}
    }

    return out


# 日期比较 返回值 为大的日期
def _compare_date(str_date1, str_date2):
    str_date1 = str_date1.split(" ")[0]
    str_date2 = str_date2.split(" ")[0]
    str_date1 = datetime.datetime.strptime(str_date1, "%Y-%m-%d")
    str_date2 = datetime.datetime.strptime(str_date2, "%Y-%m-%d")
    if str_date1.date() >= str_date2.date():
        return str(str_date1.date())
    else:
        return str(str_date2.date())


def _getlatedate(i, str_date=''):
    if str_date == '':
        nowdate = datetime.date.today()  #
        tomorrow = nowdate + datetime.timedelta(days=i)
        return str(tomorrow)
    else:
        str_date = datetime.datetime.strptime(str_date, "%Y-%m-%d").date()
        tomorrow = str_date + datetime.timedelta(days=i)
        return str(tomorrow)


if __name__ == "__main__":
    # {"BODY.PALTE":"苏BD6X35"}
    # print cjbx_start("苏JL5099",licensetype="01")
    #for i in ['苏A91192', '苏A89607', '苏AH7385', '苏AH7377', '苏A91192', '苏A89288', '苏A89288', '苏A90198', '苏A89607',
            #  '苏AH7385', '苏AH7377', '苏A91192']:
    cjbx_start("苏A89607", licensetype="01")
