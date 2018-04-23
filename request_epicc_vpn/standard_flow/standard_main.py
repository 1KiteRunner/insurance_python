# -*- coding:utf-8 -*-
import base64
import codecs
import re
from trace import pickle
import time
import sys
import datetime
from jsonpath import jsonpath
import json
from common import timeUtil
from common.MqSend import send_mq
from common.dama.damaUtil import dama
from common.sessionUtil import get_session
from common.timeUtil import jq_sy_time
from my_dbUtil.dbInsert import soupDb
from request_epicc_vpn.MyAdapter import MyAdapter
from request_epicc_vpn.calcUserYears import calc_user_years

from request_epicc_vpn.getDataNew import caclAcl, caclPremium, compare_date, compare_time40
from common.log import Logger
from request_epicc_vpn.standard_flow.dt_init import dt_init
from request_epicc_vpn.translateJsonToPremiun import readJson
import traceback
from common import redisUtil

reload(sys)
sys.setdefaultencoding('utf-8')
global null, false, true
null = None
false = False
true = True
log = Logger()


def standard_main(renewal_data_dt, endDate=""):
    try:
        r = redisUtil.CRedis()

        log.error("start")
        srssion = get_session('2')
        sessBase = srssion
        req_session = pickle.loads(codecs.decode(sessBase.encode(), "base64"))
        req_session.mount('https://', MyAdapter())
        insuranceTypeList = ""
        insure_id = renewal_data_dt['insureCarId']
        client = renewal_data_dt.get('client', None)
        if isinstance(renewal_data_dt['insuranceType'], dict):
            insuranceType = renewal_data_dt['insuranceType']
            group_id = insuranceType['insuranceTypeGroupId']

        elif isinstance(renewal_data_dt['insuranceType'], list):
            insuranceTypeList = renewal_data_dt['insuranceType']
            insuranceType = insuranceTypeList[0]
            group_id = insuranceType['insuranceTypeGroupId']

        redis_dt = r.get_vin(renewal_data_dt['vinNo'], "2")
        if redis_dt is not None:
            try:
                log.info(u'人保可以从redis中获取信息')
                dt = eval(redis_dt)
                get_checkcode_url = "http://10.134.136.112:8000/prpall/business/" \
                                    "queryVehiclePMCheck.do?comCode=32012105&frameNo=" \
                                    + dt['vinNo'] + "&licenseNo="
                req_session.post(url=get_checkcode_url, verify=False).json()

                if insuranceTypeList == "":
                    price_res = caclPremium(dt, insuranceType, req_session)
                    if price_res['data'][0].get('errMessage') is not None:
                        log.error(price_res['data'][0].get('errMessage'))
                    log.error(u"开始解析保费信息")
                    PremiumInfo = readJson(
                        price_res['data'][0]['biInsuredemandVoList'][0]['prpCitemKinds'],
                        price_res['data'][0].get('ciInsureVOList', None))
                    if PremiumInfo:
                        log.info(PremiumInfo)
                        # data=[开始时间,结束时间，座位数，组合id，车辆id，公司id]
                        data_list = [dt['ciStartDate'], dt['ciEndDate'], dt['seatCount'], group_id, insure_id, '2']
                        soupDb(PremiumInfo, data_list)
                        log.info(u'人保入库成功')
                        return None
                    else:
                        log.error(u"未知错误")
                        return price_res['data'][0].get('errMessage', '未知错误')
                else:
                    for insuranceType in insuranceTypeList:
                        try:

                            insure_id = renewal_data_dt['insureCarId']
                            group_id = insuranceType['insuranceTypeGroupId']
                            price_res = caclPremium(dt, insuranceType, req_session)
                            if price_res['data'][0].get('errMessage') is not None:
                                log.error(price_res['data'][0].get('errMessage'))
                            log.error(u"开始解析保费信息")

                            PremiumInfo = readJson(price_res['data'][0]['biInsuredemandVoList'][0]['prpCitemKinds'],
                                                   price_res['data'][0].get('ciInsureVOList', None))
                            if PremiumInfo:
                                log.info(PremiumInfo)
                                # data=[开始时间,结束时间，座位数，组合id，车辆id，公司id]
                                data_list = [dt['ciStartDate'], dt['ciEndDate'], dt['seatCount'], group_id, insure_id,
                                             '2']
                                soupDb(PremiumInfo, data_list)
                                log.info(u'人保入库成功')
                                send_mq(client, dt['licenseNo'], "", "1", "2", renewal_data_dt['sessionId'],
                                        renewal_data_dt['isPhone'], insuranceType.get("insuranceTypeGroupId", "9999"),
                                        insuranceType.get("insuranceTypeGroup", "0"))
                                # return None
                            else:
                                log.error(u"未知错误")
                                log.info(u"开始发送消息")
                                send_mq(client, dt['licenseNo'], price_res['data'][0].get('errMessage', '未知错误'), "2",
                                        "2", renewal_data_dt['sessionId'], renewal_data_dt['isPhone'],
                                        insuranceType.get("insuranceTypeGroupId", "9999"),
                                        insuranceType.get("insuranceTypeGroup", "0"))
                        except Exception, e:
                            log.error(traceback.format_exc())
                            send_mq(client, dt['licenseNo'], "未知错误", "2", "2", renewal_data_dt['sessionId'],
                                    renewal_data_dt['isPhone'], insuranceType.get("insuranceTypeGroupId", "9999"),
                                    insuranceType.get("insuranceTypeGroup", "0"))
                    return None
            except:
                log.error(traceback.format_exc())
                if client is not None:
                    log.info(u"开始发送消息")
                    send_mq(client, dt['licenseNo'], "未知错误", "2", "2", renewal_data_dt['sessionId'],
                            renewal_data_dt['isPhone'], insuranceType.get("insuranceTypeGroupId", "9999"),
                            insuranceType.get("insuranceTypeGroup", "0"))
                return "未知错误"

        dt = dt_init()
        licenseType = renewal_data_dt.get('licenseType',"02")
        if licenseType == '01':
            dt['licenseType'] = licenseType
            dt['LicenseTypeDes'] = "大型汽车号牌"
            dt['licenseColorCode'] = "04"
            dt['LicenseColorCodeDes'] = "黄"
            dt['carKindCode'] = "B01"
            dt['CarKindCodeDes'] = "货车"
            dt['useNatureCode'] = "120"
            dt['clauseType'] = "F43"
            dt['tonCount'] = '10000'
        elif licenseType == "02":
            dt['licenseType'] = licenseType
            dt['LicenseTypeDes'] = "小型汽车号牌"
            dt['licenseColorCode'] = "01"
            dt['LicenseColorCodeDes'] = "蓝"
            dt['carKindCode'] = "A01"
            dt['CarKindCodeDes'] = "客车"
            dt['useNatureCode'] = "211"
            dt['clauseType'] = "F42"
            dt['tonCount'] = "0"


        sy_jq_date = jq_sy_time(renewal_data_dt)
        syStart = sy_jq_date.get('syStart',timeUtil.getlatedate(1))
        jqStart = sy_jq_date.get('jqStart',timeUtil.getlatedate(1))
        dt['ciStartDate'] = syStart
        endDate = datetime.datetime.strptime(syStart, "%Y-%m-%d").date()
        dt['ciEndDate'] = str(datetime.datetime.strptime(
                (str(endDate.year + 1) + '-' + str(endDate.month) + '-' + str(endDate.day)),
                "%Y-%m-%d").date() + datetime.timedelta(-1))
        dt['syStart'] = syStart
        dt['syEnd'] = str(datetime.datetime.strptime(
                (str(endDate.year + 1) + '-' + str(endDate.month) + '-' + str(endDate.day)),
                "%Y-%m-%d").date() + datetime.timedelta(-1))
        dt['jqStart'] = jqStart
        jqEndDate = datetime.datetime.strptime(jqStart, "%Y-%m-%d").date()
        dt['jqEnd'] = str(datetime.datetime.strptime(
                (str(jqEndDate.year + 1) + '-' + str(jqEndDate.month) + '-' + str(jqEndDate.day)),
                "%Y-%m-%d").date() + datetime.timedelta(-1))


        # if endDate == "":
        #     tomorrow = datetime.date.today() + datetime.timedelta(1)
        #     today = datetime.date.today()
        #     dt['ciStartDate'] = str(tomorrow)
        #     dt['ciEndDate'] = str(
        #         datetime.datetime.strptime((str(today.year + 1) + '-' + str(today.month) + '-' + str(today.day)),
        #                                    "%Y-%m-%d").date())
        # else:
        #     endDate = datetime.datetime.strptime(endDate, "%Y-%m-%d").date()
        #     dt['ciStartDate'] = str(endDate)
        #     endDate = datetime.datetime.strptime(
        #         (str(endDate.year + 1) + '-' + str(endDate.month) + '-' + str(endDate.day)),
        #         "%Y-%m-%d").date() + datetime.timedelta(-1)
        #     dt['ciEndDate'] = str(endDate)
        dt['vinNo'] = renewal_data_dt.get('vinNo', '')
        dt['licenseNo'] = renewal_data_dt.get('plateNumber', '')
        get_checkcode_url = "http://10.134.136.112:8000/prpall/business/queryVehiclePMCheck.do?comCode=32012105&frameNo=" + \
                            dt['vinNo'] + "&licenseNo="
        get_checkcode_res = req_session.post(url=get_checkcode_url, verify=False).json()
        checkcode_res = jsonpath(get_checkcode_res, "$.data")
        dt['checkNo'] = checkcode_res[0][0]['checkNo']
        dt['checkCode'] = checkcode_res[0][0]['checkCode']
        # dt['checkAnswer'] = request_cicc.util.pic2Str(base64.b64decode(dt['checkCode']))
        dt['checkAnswer'] = dama("3", dt['checkCode'])
        post_checkcode_url = "http://10.134.136.112:8000/prpall/business/queryVehiclePMConfirm.do?comCode=32012105&checkNo=" + \
                             dt['checkNo'] + "&checkCode=" + dt['checkAnswer']
        post_checkcode_res = req_session.post(url=post_checkcode_url, verify=False).json()
        post_checkcode_res = jsonpath(post_checkcode_res, "$.data")
        log.info(u'开始打码')
        count = 0
        log.info(post_checkcode_res[0][0].get('errMessage', ''))
        while post_checkcode_res[0][0].get('errMessage', '') is not None:
            if '未匹配到交管车辆信息' in post_checkcode_res[0][0].get('errMessage', ''):
                log.error("未匹配到交管车辆信息")
                # 返回错误信息
                if client is not None:
                    log.info(u"开始发送消息")
                    send_mq(client, dt['licenseNo'], post_checkcode_res[0][0].get('errMessage', ''), "2", "2",
                            renewal_data_dt['sessionId'], renewal_data_dt['isPhone'],
                            insuranceType.get("insuranceTypeGroupId", "9999"),
                            insuranceType.get("insuranceTypeGroup", "0"))
                return post_checkcode_res[0][0].get('errMessage', '')
            if '录入的校验码有误' in post_checkcode_res[0][0].get('errMessage', ''):
                dama("99", dt['checkCode'])
                log.error(u"验证码有误，错误的验证码为,%s" % dt['checkAnswer'])
                get_checkcode_url = "http://10.134.136.112:8000/prpall/business/queryVehiclePMCheck.do?comCode=32012105&frameNo=" + \
                                    dt['vinNo'] + "&licenseNo="
                get_checkcode_res = req_session.post(url=get_checkcode_url, verify=False).json()
                checkcode_res = jsonpath(get_checkcode_res, "$.data")
                dt['checkNo'] = checkcode_res[0][0]['checkNo']
                dt['checkCode'] = checkcode_res[0][0]['checkCode']
                # dt['checkAnswer'] = request_cicc.util.pic2Str(base64.b64decode(dt['checkCode']))
                dt['checkAnswer'] = dama("3", dt['checkCode'])
                post_checkcode_url = "http://10.134.136.112:8000/prpall/business/queryVehiclePMConfirm.do?comCode=32012105&checkNo=" + \
                                     dt['checkNo'] + "&checkCode=" + dt['checkAnswer']
                post_checkcode_res = req_session.post(url=post_checkcode_url, verify=False).json()
                post_checkcode_res = jsonpath(post_checkcode_res, "$.data")
            if count > 4:
                # 验证码重发超限
                if client is not None:
                    log.info(u"开始发送消息")
                    send_mq(client, dt['licenseNo'], "查询失败，稍后重试", "2", "2", renewal_data_dt['sessionId'],
                            renewal_data_dt['isPhone'], insuranceType.get("insuranceTypeGroupId", "9999"),
                            insuranceType.get("insuranceTypeGroup", "0"))
                return "查询失败，稍后重试"
            count = count + 1

        if post_checkcode_res[0][0].get('errMessage', '') is None:
            log.info(u'打码成功')
            dt['modelCode'] = post_checkcode_res[0][0]['modelCode']
            car_info_url = "http://10.134.136.112:8000/prpall/vehicle/vehicleQuery.do?brandName=" + dt[
                'modelCode'] + "&modelCode="
            car_info_res = req_session.post(url=car_info_url, verify=False).json()
            car_info_list = jsonpath(car_info_res, "$.data")
            if car_info_list:
                if len(car_info_list[0]) == 0:
                    log.info(u"正在重新尝试获取车辆型号")
                    dt['modelCode'] = dt['modelCode'][:-1] + dt['modelCode'][-1].lower()
                    log.info(dt['modelCode'])
                    car_info_url = "http://10.134.136.112:8000/prpall/vehicle/vehicleQuery.do?brandName=" + dt[
                        'modelCode'] + "&modelCode="
                    car_info_res = req_session.post(url=car_info_url, verify=False).json()
                    car_info_list = jsonpath(car_info_res, "$.data")

                    # cic_car_info = get_car_model(dt['vinNo'])
                    # if cic_car_info is not None:
                    #     dt['gCIndustryModelName'] = cic_car_info['gCIndustryModelName']
                    #     car_info_url = "http://10.134.136.112:8000/prpall/vehicle/vehicleQuery.do?brandName=" + dt['gCIndustryModelName'] + "&modelCode="
                    #     car_info_res = req_session.post(url=car_info_url, verify=False).json()
                    #     car_info_list = jsonpath(car_info_res, "$.data")

                if len(car_info_list[0]) > 0:
                    log.info(u'获取车型成功，正在选取最低价车型')
                    car_info_list = car_info_list[0]
                    car_info_list.sort(key=lambda obj: obj.get('priceT'))
                    car_info = car_info_list[0]

                    if post_checkcode_res[0][0].get('enrollDate', None) is not None:
                        dt['enrollDate'] = str(time.strftime("%Y-%m-%d", time.localtime(
                            int(post_checkcode_res[0][0]['enrollDate']['time']) / 1000)))
                    dt['licenseNo'] = post_checkcode_res[0][0]['id']['licenseNo']
                    dt['pmCarOwner'] = post_checkcode_res[0][0]['carOwner']
                    if licenseType=='01':
                        dt['exhaustScale'] = post_checkcode_res[0][0]['displacement']
                        dt['carLotEquQuality'] = float(car_info['vehicleQuality'])*1000
                        if post_checkcode_res[0][0].get('tonCount','0') == '0':
                            dt['tonCount'] = post_checkcode_res[0][0].get('tonCount','0')
                        else:
                            dt['tonCount'] = post_checkcode_res[0][0].get('haulage', '0')
                    else:
                        dt['exhaustScale'] = car_info['vehicleExhaust']
                    dt['engineNo'] = post_checkcode_res[0][0]['engineNo']
                    dt['brandName'] = car_info['vehicleName']
                    dt['purchasePriceOld'] = str(car_info['priceTr'])
                    log.info(u'新车购置价格是:%s' % dt['purchasePriceOld'])
                    dt['frameNo'] = dt['vinNo']
                    dt['modelCode'] = car_info['vehicleId']
                    dt['seatCount'] = car_info['vehicleSeat']
                    useYears = calc_user_years(dt['syStart'], dt['enrollDate'])
                    dt['prpCitemCar_useYears'] = useYears
                    acl_price = caclAcl(dt, req_session)
                    dt['aclPrice'] = acl_price
                    price_res = caclPremium(dt, insuranceType, req_session)

                    log.info(price_res['data'][0].get('errMessage'))
                    while price_res['data'][0].get('errMessage') is not None:


                        if '重复投保' in price_res['data'][0].get('errMessage'):
                            str1 = "\d{4}-\d{2}-\d{2}"
                            datelist = re.findall(str1, price_res['data'][0]['errMessage'], re.S)
                            if len(datelist) == 2:
                                endDate = compare_date(datelist[0], datelist[1])
                                dayGap = compare_time40(str(endDate))
                                if dayGap >= 40:
                                    log.error(u"重复投保，上期保单超过40天")
                                    if client is not None:
                                        log.info(u"开始发送消息")
                                        send_mq(client, dt['licenseNo'], price_res['data'][0]['errMessage'], "2", "2",
                                                renewal_data_dt['sessionId'], renewal_data_dt['isPhone'],
                                                insuranceType.get("insuranceTypeGroupId", "9999"),
                                                insuranceType.get("insuranceTypeGroup", "0"))
                                    return price_res['data'][0]['errMessage']
                                else:
                                    dt['syStart'] = dt['jqStart'] = str(endDate)
                                    endDate = datetime.datetime.strptime(
                                        (str(endDate.year + 1) + '-' + str(endDate.month) + '-' + str(endDate.day)),
                                        "%Y-%m-%d").date() + datetime.timedelta(-1)
                                    dt['syEnd'] = dt['jqEnd'] = str(endDate)
                                    useYears = calc_user_years(dt['syStart'], dt['enrollDate'])
                                    dt['prpCitemCar_useYears'] = useYears
                                    acl_price = caclAcl(dt, req_session)
                                    dt['aclPrice'] = acl_price
                                    price_res = caclPremium(dt, insuranceType, req_session)
                            else:
                                log.error(u"重复投保")
                                if client is not None:
                                    log.info(u"开始发送消息")
                                    send_mq(client, dt['licenseNo'], price_res['data'][0]['errMessage'], "2", "2",
                                            renewal_data_dt['sessionId'], renewal_data_dt['isPhone'],
                                            insuranceType.get("insuranceTypeGroupId", "9999"),
                                            insuranceType.get("insuranceTypeGroup", "0"))
                                return price_res['data'][0]['errMessage']

                    log.info(price_res['data'][0]['biInsuredemandVoList'][0].get('ciInsureDemandRepets'))
                    if len(price_res['data'][0]['biInsuredemandVoList'][0].get('ciInsureDemandRepets'))>0:
                        endDate = datetime.datetime.strptime(time.strftime("%Y-%m-%d", time.localtime(int(price_res['data'][0]['biInsuredemandVoList'][0].get('ciInsureDemandRepets')[0]['endDate']['time'] / 1000))),"%Y-%m-%d").date()
                        print endDate,type(endDate)
                        dayGap = compare_time40(str(endDate))
                        if dayGap >= 40:
                            log.error(u"重复投保，上期保单超过40天")
                            if client is not None:
                                log.info(u"开始发送消息")
                                send_mq(client, dt['licenseNo'], price_res['data'][0]['errMessage'], "2", "2",
                                        renewal_data_dt['sessionId'], renewal_data_dt['isPhone'],
                                        insuranceType.get("insuranceTypeGroupId", "9999"),
                                        insuranceType.get("insuranceTypeGroup", "0"))
                            return price_res['data'][0]['errMessage']
                        else:
                            dt['syStart'] = dt['jqStart'] = str(endDate)
                            endDate = datetime.datetime.strptime(
                                (str(endDate.year + 1) + '-' + str(endDate.month) + '-' + str(endDate.day)),
                                "%Y-%m-%d").date() + datetime.timedelta(-1)
                            dt['syEnd'] = dt['jqEnd'] = str(endDate)
                            useYears = calc_user_years(dt['syStart'], dt['enrollDate'])

                            dt['prpCitemCar_useYears'] = useYears
                            acl_price = caclAcl(dt, req_session)
                            dt['aclPrice'] = acl_price
                            price_res = caclPremium(dt, insuranceType, req_session)
                    log.error(u"开始解析保费信息")
                    PremiumInfo = readJson(price_res['data'][0]['biInsuredemandVoList'][0]['prpCitemKinds'],
                                           price_res['data'][0].get('ciInsureVOList', None))
                    if PremiumInfo:
                        log.info(PremiumInfo)
                        # data=[开始时间,结束时间，座位数，组合id，车辆id，公司id]
                        data_list = [dt['ciStartDate'], dt['ciEndDate'], dt['seatCount'], group_id, insure_id, '2']
                        soupDb(PremiumInfo, data_list)
                        dt['ciEndDate'] = str(dt['ciEndDate'])
                        r.set_vin(dt['vinNo'], "2", json.dumps(dt, ensure_ascii=False))
                        log.info(u'人保入库成功')
                        if insuranceTypeList != "":
                            insuranceTypeList = insuranceTypeList[1:]
                            for insuranceType in insuranceTypeList:
                                try:
                                    insure_id = renewal_data_dt['insureCarId']
                                    group_id = insuranceType['insuranceTypeGroupId']
                                    price_res = caclPremium(dt, insuranceType, req_session)
                                    if price_res['data'][0].get('errMessage') is not None:
                                        log.error(price_res['data'][0].get('errMessage'))
                                    log.error(u"开始解析保费信息")
                                    PremiumInfo = readJson(
                                        price_res['data'][0]['biInsuredemandVoList'][0]['prpCitemKinds'],
                                        price_res['data'][0].get('ciInsureVOList', None))
                                    if PremiumInfo:
                                        log.info(PremiumInfo)
                                        # data=[开始时间,结束时间，座位数，组合id，车辆id，公司id]
                                        data_list = [dt['ciStartDate'], dt['ciEndDate'], dt['seatCount'], group_id,
                                                     insure_id, '2']
                                        soupDb(PremiumInfo, data_list)
                                        log.info(u'人保入库成功')
                                        log.info(u"开始发送消息")
                                        send_mq(client, dt['licenseNo'], "", "1", "2", renewal_data_dt['sessionId'],
                                                renewal_data_dt['isPhone'],
                                                insuranceType.get("insuranceTypeGroupId", "9999"),
                                                insuranceType.get("insuranceTypeGroup", "0"))
                                        # return None
                                    else:
                                        log.error(u"未知错误")
                                        log.info(u"开始发送消息")
                                        send_mq(client, dt['licenseNo'], price_res['data'][0].get('errMessage', '未知错误'),
                                                "2", "2", renewal_data_dt['sessionId'], renewal_data_dt['isPhone'],
                                                insuranceType.get("insuranceTypeGroupId", "9999"),
                                                insuranceType.get("insuranceTypeGroup", "0"))
                                except Exception, e:
                                    log.error(traceback.format_exc())
                                    log.info(u"开始发送消息")
                                    send_mq(client, dt['licenseNo'], "未知错误", "2", "2", renewal_data_dt['sessionId'],
                                            renewal_data_dt['isPhone'],
                                            insuranceType.get("insuranceTypeGroupId", "9999"),
                                            insuranceType.get("insuranceTypeGroup", "0"))
                        return None
                    else:
                        return "未知错误"
                else:
                    log.error(u'无法获取车型')
                    if client is not None:
                        send_mq(client, dt['licenseNo'], '无法获取车型', "2", "2", renewal_data_dt['sessionId'],
                                renewal_data_dt['isPhone'], insuranceType.get("insuranceTypeGroupId", "9999"),
                                insuranceType.get("insuranceTypeGroup", "0"))
                    return ('无法获取车型')
    except Exception, e:
        log.error(traceback.format_exc())
        if client is not None:
            send_mq(client, dt['licenseNo'], '未知错误', "2", "2", renewal_data_dt['sessionId'], renewal_data_dt['isPhone'],
                    insuranceType.get("insuranceTypeGroupId", "9999"), insuranceType.get("insuranceTypeGroup", "0"))
        return "未知错误"


if __name__ == "__main__":
    standard_main()
#     r = redisUtil.CRedis()
#     dt = """{
#     "frameNo": "LDC643T24F3333320",
#     "vinNo": "LDC643T24F3333320",
#     "aclPrice": "53642.40",
#     "taxPlatFormTime": "2016-1-8",
#     "checkCode": "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",
#     "checkAnswer": "ayy1",
#     "operationTimeStamp": "2017-05-03 18:37:21",
#     "agentCode": "320021101233",
#     "enrollDate": "2015-06-23",
#     "purchasePriceOld": "61800",
#     "randomProposalNo": "6358560951487830052655 ",
#     "operator_homephone": "13809040202",
#     "licenseNo": "苏FG705U",
#     "ciStartDate": "2017-06-12",
#     "exhaustScale": 1.587,
#     "brandName": "东风雪铁龙DC7162LYCM轿车",
#     "ciEndDate": "2018-06-11",
#     "prpCitemCar_useYears": "1",
#     "seatCount": 5,
#     "engineNo": "2601465",
#     "pmCarOwner": "俞萍",
#     "useYear": "9",
#     "makeCom": "32012105",
#     "checkNo": "72PICC320017001493807837056333",
#     "operatorCode": "A320100906",
#     "modelCode": "XTAAFD0120",
#     "today": "2017-05-03",
#     "operatorProjectCode": "KBDAA201632010000000501,KBDAA201632010000000873"
# }"""
#     print r.set_vin("LDC643T24F3333320", "2", dt)
