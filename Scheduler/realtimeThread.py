# -*- coding:utf-8 -*-
__author__ = 'weikai'
import datetime, json
import threading
import traceback
import gevent
from gevent import monkey
from common.log import Logger
from request_ancheng.request_premium import get_premium
from request_cic.getCode import get_citycode
from  request_cic.request_getdata import getData, getData_CPlateNo
from request_cicc.cicc_standard_flow.flow_main import flow_main
from request_huanong.hn_entrance import hn_request
from request_pingan.entrance import pingan_request
from session import getSession
from common.mongodb.mgdboperate import inser_user_renewal, query_user_renewal, query_user_permium_time
from common.timeUtil import jq_sy_time
from common.MqSend import send_mq
from common.timeUtil import getlatedate

monkey.patch_socket()
monkey.patch_all()
monkey.patch_ssl()


# 车架号查询信息之后查询保费
def getSource(dt):
    log = Logger()
    try:
        sessiondt = ""
        companyId = dt.get('companyId', [])
        # sessiondt = getSession()
        # requestcic = sessiondt['4']
        # loginRes = sessiondt['5']
        # pingansession = sessiondt['1']
        # ancheng_session = sessiondt['12']
        # hn_session = sessiondt['13']

        requestcic = None
        loginRes = None
        pingansession = None
        ancheng_session = None
        hn_session = None

        plateNumber = dt['plateNumber']
        insureCarId = dt['insureCarId']
        sessionId = dt['sessionId']
        isPhone = dt['isPhone']
        client = dt['client']
        insuranceType = dt['insuranceType']
        insureTypeGroupId = insuranceType.get("insuranceTypeGroupId", "")
        insuranceTypeGroup = insuranceType.get("insuranceTypeGroup", "")
        carInfo = query_user_renewal(plateNumber)
        jq_sy_out = {}
        if carInfo == 0:
            carInfo = query_user_permium_time(plateNumber)
            if carInfo != 0:
                jq_sy_out = jq_sy_time(carInfo)
                log.info(json.dumps(jq_sy_out, ensure_ascii=False))
        else:
            jq_sy_out = jq_sy_time(carInfo)
            log.info(json.dumps(jq_sy_out, ensure_ascii=False))

        if jq_sy_out.get("code", "0") == "1000":
            dt['insuranceTime'] = jq_sy_out
        elif jq_sy_out.get("code", "0") == "1001" or jq_sy_out.get("code", "0") == "1002":
            cmp_id = '|'.join(str(i) for i in companyId) if len(companyId) != 0 else "1|2|4|5|12|13"
            send_mq(client, plateNumber, jq_sy_out["msg"], "2", cmp_id, sessionId, isPhone,
                    insureTypeGroupId, insuranceTypeGroup)
            return
        else:
            dt['insuranceTime'] = {"code": "1003", "msg": "数据库中未查询到信息自动生成当前时间", "syStart": getlatedate(1),
                                   "jqStart": getlatedate(1)}

        # 货车暂时只爬取人保的保费
        licenseType = dt.get('licenseType', "02")
        if licenseType == "01" and companyId and '12' not in companyId:
            log.info(u"货车暂时只爬取人保的保费")
            send_mq(client, plateNumber, "货车暂时只爬取人保的保费", "2", "2|4|5|12|13", sessionId, isPhone,
                    insureTypeGroupId, insuranceTypeGroup)
            return

        vinNo = dt.get('vinNo', '')
        insureCarId = dt.get('insureCarId', '')
        if vinNo == '' or insureCarId == '':
            return
        dt['endDate'] = dt.get("preInsureEndDate", "")

        if dt.get('identitCard', '') == '':
            dt['identitCard'] = '320123199106102810'
        dt['insuranceType'] = dt.get("insuranceType", "")

        log.info(u"程序开始运行%s" % datetime.datetime.now())
        try:

            g_list = []
            if not companyId:
                g1 = gevent.spawn(getData, requestcic, dt)
                g2 = gevent.spawn(flow_main, loginRes, dt)
                g3 = gevent.spawn(pingan_request, pingansession, dt)
                g4 = gevent.spawn(get_premium, ancheng_session, dt)
                g5 = gevent.spawn(hn_request, hn_session, dt)
                gevent.joinall([g1, g2, g3, g4, g5])

            if companyId and '4' in companyId:
                g1 = gevent.spawn(getData_CPlateNo, requestcic, dt)
                g_list.append(g1)

            if companyId and '5' in companyId:
                g2 = gevent.spawn(flow_main, loginRes, dt)
                g_list.append(g2)

            if companyId and '1' in companyId:
                g3 = gevent.spawn(pingan_request, pingansession, dt)
                g_list.append(g3)

            if companyId and '12' in companyId:
                g4 = gevent.spawn(get_premium, ancheng_session, dt)
                g_list.append(g4)

            if companyId and '13' in companyId:
                g5 = gevent.spawn(hn_request, hn_session, dt)
                g_list.append(g5)

            if g_list:
                gevent.joinall(g_list)

            print u"程序结束运行%s" % datetime.datetime.now()

        except Exception, e:
            log.error(e)
            log.error(traceback.format_exc())

    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())


# 根据车牌号进行查询保费信息
def plateNo_getSource(dt):
    log = Logger()
    try:
        requestcic = dt['4']
        loginRes = dt['5']
        pingansession = dt['1']
        ancheng_session = dt['12']
        hn_session = dt['13']
        companyId = dt.get('companyId', [])
        plateNumber = dt['licenseNo']
        sessionId = dt['sessionId']
        isPhone = dt['isPhone']
        insuranceType = dt['insuranceType']
        insureTypeGroupId = insuranceType.get("insuranceTypeGroupId", "")
        insuranceTypeGroup = insuranceType.get("insuranceTypeGroup", "")
        cdt = {}
        cdt['identitCard'] = dt['identifyNumber']
        cdt['custName'] = dt['insuredName']
        cdt['plateNumber'] = plateNumber
        cdt['vinNo'] = dt['vinNo']
        cdt['engineNo'] = dt['engineNo']
        cdt['insureCarId'] = dt['insureCarId']
        cdt['cityCode'] = get_citycode(dt['licenseNo'])
        cdt['endDate'] = dt['endDate']
        cdt['firstRegister'] = dt['enrollDate']
        cdt['vehicleBrand'] = dt['brandName']
        cdt['NSeatNum'] = dt.get('NSeatNum', 999)
        cdt['client'] = dt['client']
        client = cdt['client']
        cdt['sessionId'] = sessionId
        cdt['isPhone'] = isPhone
        cdt['insuranceType'] = insuranceType
        cdt['insuranceTime'] = dt.get("insuranceTime", {})
        cdt['licenseType'] = dt.get("licenseType", "02")
        # print(cdt)
        jq_sy_out = jq_sy_time(cdt)
        log.info(json.dumps(jq_sy_out, ensure_ascii=False))
        # print(cdt)
        if jq_sy_out.get("code", "0") == "1000":
            cdt['insuranceTime'] = jq_sy_out
        elif jq_sy_out.get("code", "0") == "1001" or jq_sy_out.get("code", "0") == "1002":
            cmp_id = '|'.join(str(i) for i in companyId) if len(companyId) != 0 else "1|2|4|5|12|13"
            send_mq(client, plateNumber, jq_sy_out["msg"], "2", cmp_id, sessionId, isPhone,
                    insureTypeGroupId, insuranceTypeGroup)
            return

        # 货车暂时只爬取人保的保费
        licenseType = dt.get('licenseType', "02")
        if licenseType == "01" and companyId and '12' not in companyId:
            log.info(u"货车暂时只爬取人保的保费")
            send_mq(client, plateNumber, "货车暂时只爬取人保的保费", "2", "2|4|5|12|13", sessionId, isPhone,
                    insureTypeGroupId, insuranceTypeGroup)
            return
        log.info(u"程序开始运行%s" % datetime.datetime.now())
        try:
            #get_premium(ancheng_session, cdt)
            # getData_CPlateNo(requestcic,cdt)
            #return
            g_list = []
            if not companyId:
                g1 = gevent.spawn(getData_CPlateNo, requestcic, cdt)
                g2 = gevent.spawn(flow_main, loginRes, cdt)
                g3 = gevent.spawn(pingan_request, pingansession, cdt)
                g4 = gevent.spawn(get_premium, ancheng_session, cdt)
                g5 = gevent.spawn(hn_request, hn_session, cdt)
                gevent.joinall([g1, g2, g3, g4, g5])

            if companyId and '4' in companyId:
                g1 = gevent.spawn(getData_CPlateNo, requestcic, cdt)
                g_list.append(g1)

            if companyId and '5' in companyId:
                g2 = gevent.spawn(flow_main, loginRes, cdt)
                g_list.append(g2)

            if companyId and '1' in companyId:
                g3 = gevent.spawn(pingan_request, pingansession, cdt)
                g_list.append(g3)

            if companyId and '12' in companyId:
                g4 = gevent.spawn(get_premium, ancheng_session, cdt)
                g_list.append(g4)

            if companyId and '13' in companyId:
                g5 = gevent.spawn(hn_request, hn_session, cdt)
                g_list.append(g5)

            if g_list:
                gevent.joinall(g_list)

            print u"程序结束运行%s" % datetime.datetime.now()

        except Exception, e:
            log.error(e)
            log.error(traceback.format_exc())

    except Exception as e:
        log.error(e)
        log.error(traceback.format_exc())
    log.info(u"程序结束运行%s" % datetime.datetime.now())
