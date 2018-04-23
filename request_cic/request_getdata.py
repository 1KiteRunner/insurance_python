# -*- coding:utf-8 -*-
from common.redisUtil import CRedis

__author__ = 'wk'
import traceback
import json
import urllib
import sys

import requests

from parse import parseCarInfo, parseCardata, parseFee, parse_renewal_data
import utils
from feebody2 import getFeebody, compare_date
from vhlPlatform import *
from calcNActualValue import calcNActualValue
from my_dbUtil.dbInsert import soupDb
from translate import getPriumeInf
from common.log import *
from common.MqSend import send_mq, send_mq_update_carinfo
from common import config, redisUtil
from request_cic import cic_settings as SE
from common.sessionUtil import get_session

reload(sys)
sys.setdefaultencoding('utf8')
log = Logger()

r = redisUtil.CRedis()


def is_cic_renewal(requesteicc, CPlateNo=None, vino=None):
    headers = SE.headers
    headers['content-type'] = 'application/x-www-form-urlencoded'
    url = 'http://carply.cic.cn/pcis/actionservice.ai'
    CPlateNo2 = urllib.quote(urllib.quote(CPlateNo))
    body_CPlateNo = 'SERVICE_TYPE=ACTION_SERVIC&CODE_TYPE=UTF-8&BEAN_HANDLE=baseAction&ACTION_HANDLE=perform&SERVICE_NAME=policyAppBizAction&SERVICE_MOTHOD=hasPlyByCPlateNo&DW_DATA=%253Cdata%253E%253C%252Fdata%253E&HELPCONTROLMETHOD=common&SCENE=UNDEFINED&BIZ_SYNCH_LOCK=&BIZ_SYNCH_MODULE_CODE=&BIZ_SYNCH_NO=&BIZ_SYNCH_DESC=&BIZ_SYNCH_CONTINUE=false&CUST_DATA=CPlateNo%253d' + CPlateNo2 + '%2523%2523%2523CEngNo%253d%2523%2523%2523CFrmNo%253d%2523%2523%2523COrigPlyNo%253d%2523%2523%2523CProdNo%253d0360'
    boy_vino = ''
    renewal_resp = requesteicc.post(url=url, headers=headers, data=body_CPlateNo)
    is_ture = re.findall(r"RESULT_MSG:\'(.+?)\',", renewal_resp.text, re.S)[0]
    if is_ture == 'true':
        log.info("CPlateNo= %s 是 中华联合 CIC续保用户 " % CPlateNo)
        return 1
    else:
        return 0


# 车架号查询不到车辆信息时通过车管所返回的gCNoticeType 快速查询码 查询车辆信息
def vehicleList_code(requesteicc, gCNoticeType):
    headers = SE.headers
    headers['content-type'] = 'application/x-www-form-urlencoded'
    url = "http://114.251.1.161/zccx/vehicleList.shtml?qtype=2&pageno=1"
    data = "fieldName=&orderByType=&innerFlag=&jyFlag=&qtype=2&strqcpp=&cxid=&strqccx=&cxppid=&cxcxid=&fsearchCode=&cxingmc=&cxingbm=&cxingcj=" + gCNoticeType + "&importFlag=&vehicleClass=&fvinRoot=&plateNo=&firstRegisterDate=&car_engineNumber=&car_engineModel=&car_displacement=&car_power=&car_curbWeight=&car_ratedCapacity=&car_totalMassTraction=&car_ratedLoad=&car_emissionsStandards=&car_powerType=&pageno=1&pagesize=15&maxPagesize=200&gotoPage=&hvinRoot=&hvinFlag=&requestSource=http%3A%2F%2Fcarply.cic.cn%2Fpcis%2FofferAcceptResult&plateNo=&firstRegisterDate="
    rsp = requesteicc.post(url=url, data=data, headers=headers)
    carlist = parseCarInfo(rsp.text)
    return carlist


# 返回续保用户信息
def renewal_data(requesteicc, CPlateNo=None, vino=None):
    headers = SE.headers
    headers['content-type'] = 'application/x-www-form-urlencoded'
    url = 'http://carply.cic.cn/pcis/actionservice.ai'
    body = ''
    CPlateNo = CPlateNo.encode()
    if CPlateNo != None:
        CPlateNo2 = urllib.quote(urllib.quote(CPlateNo))
        body_CPlateNo = 'SERVICE_TYPE=ACTION_SERVIC&CODE_TYPE=UTF-8&BEAN_HANDLE=baseAction&ACTION_HANDLE=perform&SERVICE_NAME=policyAppBizAction&SERVICE_MOTHOD=getPlyListByCPlateNo&DW_DATA=%253Cdata%253E%253CdataObjs%2520type%253D%2522ONE_SELECT%2522%2520%2520dwName%253D%2522policy.ply_plyListForCPlateNo_DW%2522%2520dwid%253D%2522dwid0.5329886837252121%2522%2520pageCount%253D%25221%2522%2520pageNo%253D%25221%2522%2520pageSize%253D%252215%2522%2520rsCount%253D%25220%2522%252F%253E%253C%252Fdata%253E&HELPCONTROLMETHOD=common&SCENE=UNDEFINED&BIZ_SYNCH_LOCK=&BIZ_SYNCH_MODULE_CODE=&BIZ_SYNCH_NO=&BIZ_SYNCH_DESC=&BIZ_SYNCH_CONTINUE=false&CUST_DATA=CPlateNo%253d' + CPlateNo2 + '%2523%2523%2523CEngNo%253d%2523%2523%2523CFrmNo%253d%2523%2523%2523COrigPlyNo%253d%2523%2523%2523CProdNo%253d0360'
        body = body_CPlateNo
    elif vino != None:
        vino2 = urllib.quote(urllib.quote(vino))
        boy_vino = 'SERVICE_TYPE=ACTION_SERVIC&CODE_TYPE=UTF-8&BEAN_HANDLE=baseAction&ACTION_HANDLE=perform&SERVICE_NAME=policyAppBizAction&SERVICE_MOTHOD=getPlyListByCPlateNo&DW_DATA=%253Cdata%253E%253CdataObjs%2520type%253D%2522ONE_SELECT%2522%2520%2520dwName%253D%2522policy.ply_plyListForCPlateNo_DW%2522%2520dwid%253D%2522dwid0.5329886837252121%2522%2520pageCount%253D%25221%2522%2520pageNo%253D%25221%2522%2520pageSize%253D%252215%2522%2520rsCount%253D%25220%2522%252F%253E%253C%252Fdata%253E&HELPCONTROLMETHOD=common&SCENE=UNDEFINED&BIZ_SYNCH_LOCK=&BIZ_SYNCH_MODULE_CODE=&BIZ_SYNCH_NO=&BIZ_SYNCH_DESC=&BIZ_SYNCH_CONTINUE=false&CUST_DATA=CPlateNo%253d%2523%2523%2523CEngNo%253d%2523%2523%2523CFrmNo%253d' + vino2 + '%2523%2523%2523COrigPlyNo%253d%2523%2523%2523CProdNo%253d0360'
        body = boy_vino
    elif CPlateNo == None and vino == None:
        return u'CPlateNo or vino cant None'
    renewal_resp = requesteicc.post(url=url, headers=headers, data=body)
    is_ture = re.findall(r"RESULT_MSG:\'(.+?)\',", renewal_resp.text, re.S)[0]
    if is_ture == u'没有符合条件的记录！':
        return 0
    elif is_ture == u'查询完毕！':
        log.info("CPlateNo= %s 是CIC续保用户 " % CPlateNo)
        renewal_data_dt = parse_renewal_data(renewal_resp.text)
        return renewal_data_dt


# 通过车架号查询用户的保费
def getData(requesteicc, data, cardict=None):
    searchVin = data['vinNo']
    insureCarId = data['insureCarId']
    isPhone = data['isPhone']
    sessionId = data['sessionId']
    client = data['client']
    CPlateNo = data['plateNumber']

    insuranceType = data.get("insuranceType", {})
    if isinstance(insuranceType, list):
        insuranceTypeGroupId = insuranceType[0].get("insuranceTypeGroupId", "")
        insuranceTypeGroup = insuranceType[0].get("insuranceTypeGroup", "")
    else:
        insuranceTypeGroupId = insuranceType.get("insuranceTypeGroupId", "")
        insuranceTypeGroup = insuranceType.get("insuranceTypeGroup", "")
        # 先查询redis中是否有信息
        log.info(u"START  FROM REDIS GET CIC USERINFO")
        # 获取消息体
        r = CRedis()
        feedict = r.get_vin(searchVin, "4")
        if feedict != None:
            # 设置保险类型
            feedict = eval(feedict)
            log.info(u"CIC FROM REDIS GET USERINFO %s " % searchVin)
            feedict['insuranceType'] = insuranceType
            post_fee(requesteicc, feedict, data)
            return
    '''
    endDate = data.get("preInsureEndDate", "")
    if endDate == "":
        endDate = data.get("endDate", "")
    if endDate != "":
        min_time = compare_time40(endDate)
        if min_time > config.days:
            log.error("中华联合保险查询在40天内的 车牌号为 %s 保险结束时间为 %s" % (CPlateNo, endDate))
            send_mq(client, CPlateNo, "中华联合保险查询在40天内的 车牌号为 %s 保险结束时间为 %s" % (CPlateNo, endDate), "2", "4", sessionId,
                    isPhone, insuranceTypeGroupId, insuranceTypeGroup)
            return "中华联合保险查询在40天内的 车牌号为 %s 保险结束时间为 %s" % (CPlateNo, endDate)
        if min_time < 0:
            endDate = utils.getlatedate(1)
    '''
    headers = SE.headers
    if cardict == None:
        cardict = getCarInof(requesteicc, searchVin)
        if isinstance(cardict, dict):
            # 发送车辆信息 更新数据库
            send_mq_update_carinfo(client, cardict)
        else:
            # 未查询到交管信息
            send_mq(client, CPlateNo, cardict, "2", "4", sessionId, isPhone, insuranceTypeGroupId, insuranceTypeGroup)
            return
    # 获取查询车辆精确信息的MD5
    res3 = requesteicc.get(
        url='http://carply.cic.cn/pcis/policy/universal/quickapp/quick_offer.jsp?isOffer=1&prodNo=0360&dptCde=32010101&CUnionMrk=0')
    res_body = res3.text
    if res3.status_code == 200:
        md5byJy = re.findall(r"md5byJy = \"(.+?)\";", res_body, re.S)[0]
    else:
        res_body = requesteicc.get(
            url='http://carply.cic.cn/pcis/policy/universal/quickapp/quick_offer.jsp?isOffer=1&prodNo=0360&dptCde=32010101&CUnionMrk=0')
        res_body = res3.text
        md5byJy = re.findall(r"md5byJy = \"(.+?)\";", res_body, re.S)[0]

    ######################请求车辆信息##################################

    request114 = requests.session();
    headers114 = SE.headers
    request114.headers.update(headers114)
    # 车架号
    # searchVin='LMVHEKFD6EA029484'
    # searchVin='LFV2A11K8F4192886'
    validNo = md5byJy
    # vehicleId='I0000000000000000230000000000033'
    search_url = 'http://114.251.1.161/zccx/search?regionCode=00000000&jyFlag=0&businessNature=A&operatorCode=0000000000&returnUrl=http://carply.cic.cn/pcis/offerAcceptResult&vname=&searchVin=' + searchVin + '&vinflag=1&validNo=' + validNo
    repon114 = request114.get(url=search_url)
    if "没有找到符合条件的数据" in repon114.text:
        log.error("中华联合通过车架号未查询到车辆信息 %s" % searchVin)
        carlist = vehicleList_code(request114, cardict['gCNoticeType'])
    else:
        carlist = parseCarInfo(repon114.text)

    if len(carlist) != 0:
        gCSearchCode = vehicleId = carlist[len(carlist) - 1]['vehicleId']
        vehicleCode = carlist[len(carlist) - 1]['vehicleCode']
        ######################选择车辆##################################
        getVehicleForReturn_url = 'http://114.251.1.161/zccx/getVehicleForReturn.shtml?vehicleCode=' + vehicleId + '&vehicleId=' + vehicleId + '&hvinRoot=' + searchVin + '&hvinFlag=1'
        getVehicleForReturnrsp = request114.post(url=getVehicleForReturn_url)
        # log.info(getVehicleForReturnrsp.text)
        dt = parseCardata(getVehicleForReturnrsp.text)
    else:
        log.error("通过车架号以及车辆快速查询码无法车辆信息无法查询 %s " % CPlateNo)
        send_mq(client, CPlateNo, "%s 通过车架号以及车辆快速查询码无法车辆信息无法查询" % CPlateNo, "2", "4", sessionId, isPhone,
                insuranceTypeGroupId, insuranceTypeGroup)
        return


    #####################新车购置浮动上线###############
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    ModeCode = vehicleCode.replace(' ', '').replace(u'\r', '').replace(u'\n', '')
    getOfferPrice_url = 'http://carply.cic.cn/pcis/policy/universal/quickapp/actionservice.ai'
    getOfferPricedata = 'ADAPTER_TYPE=JSON_TYPE&SERVICE_TYPE=ACTION_SERVIC&CODE_TYPE=CODE_TYPE&BEAN_HANDLE=baseAction&ACTION_HANDLE=perform&SERVICE_NAME=offerDataLoadAction&SERVICE_MOTHOD=getOfferPrice&DW_DATA=%255B%255D&HELPCONTROLMETHOD=common&SCENE=UNDEFINED&BIZ_SYNCH_CONTINUE=false&CUST_DATA=dptCde%253D32010101%2523%2523%2523prodNo%253D0360_0332%2523%2523%2523modelCde%253D' + ModeCode
    getOfferPriceresp = requesteicc.post(url=getOfferPrice_url, data=getOfferPricedata, headers=headers)
    getOfferPriceresp = getOfferPriceresp.json()
    gNOfferPurChasePriceMax = getOfferPriceresp['JSON_OBJ']['maxPrice']  # 新车购置价浮动上限
    gNOfferPurChasePriceMin = getOfferPriceresp['JSON_OBJ']['minPrice']  # 新车购置价浮动下
    #####################请求车管所信息#############################################

    # cardict=getCarInof(requesteicc,searchVin)


    ##############################################
    checkNo = cardict['checkNo']
    codestr = cardict['gCValidateCode']
    gCFstRegYm = cardict['CFstRegYm']
    gNDisplacement = cardict['gNDisplacement']
    gCPlateTyp = cardict['gCPlateTyp']
    gNNewPurchaseValue = gNOfferPurChasePriceMax  # 新车购置价
    plateNo = cardict['gCPlateNo'].encode('utf-8')
    # 从车辆列表中选择的座位数
    seat = dt['seat']
    # 选择车型的座位数 与车管所不同
    car_seat = cardict.get("gNSeatNum", "")

    if car_seat != "" and car_seat != seat:
        seat = car_seat
    # 车管所查询出的信息 座位数出现为0
    if car_seat == 0:
        seat = dt['seat']

    if int(seat) <= 6:
        SY_seatcode = '302001001'
        JQ_seatcode = '302001001'
    elif int(seat) > 6 and int(seat) < 10:
        SY_seatcode = '302001008'
        JQ_seatcode = '302001022'
    elif int(seat) >= 10:
        SY_seatcode = '302001016'
        JQ_seatcode = '302001022'
    else:
        SY_seatcode = '302001001'
        JQ_seatcode = '302001001'
    gNDiscussActualValue = calcNActualValue(gCFstRegYm, gNNewPurchaseValue, SY_seatcode)
    gNDiscussActualValue = str((gNDiscussActualValue))
    # 协商实际价值



    feedict = {"gNNewPurchaseTaxValue": dt['purchasePriceTax'],  # 新车购置价
               "gNKindredPrice": dt['kindredPrice'],
               "gNKindredPriceTax": dt['kindredPriceTax'],
               "gNNewPurchaseValue": round(float(dt['purchasePrice']), 2),
               "gNDiscussActualValue": gNDiscussActualValue,
               "gCFrmNo": dt['hvinRoot'],
               "gCMonDespRate": "307007001",  # 月折旧率
               "gNActualValue": gNDiscussActualValue,
               "gNOfferPurChasePriceMax": gNOfferPurChasePriceMax,
               "gNOfferPurChasePriceMin": gNOfferPurChasePriceMin,
               "gCIndustryModelCode": dt['hyVehicleCode'],
               "gCIndustryModelName": urllib.unquote(urllib.unquote(dt['hyVehicleName']).__str__()),  # 要转码
               "gCNoticeType": dt['vehicleFgwCode'],
               "gCProdPlace": dt['importF'].encode("utf-8"),  # 中文需要转为012
               "gCFamilyCode": dt['familyCode'],
               "gCFamilyName": dt['familyName'].encode("utf-8"),
               "gCFstRegYm": gCFstRegYm,
               "gCModelNme": dt['vehicleName'].encode("utf-8"),
               "gCBrandId": dt['brandName'].encode("utf-8"),
               "gCModelCde": dt['vehicleCode'],
               "gCSearchCode": checkNo,
               "gCValidateCode": codestr,
               "gCPlateNo": plateNo,
               "gCEngNo": cardict['CEngNo'],
               "gNDisplacement": str(float(dt['displacement']) / 1000),
               "gCPlateTyp": cardict['gCPlateTyp'],
               "gCCarAge": "306002",  # age
               "gNSeatNum": seat,
               "gNPoWeight": cardict['NCurbWt'],
               "RVehlcleTonnage": int(float((cardict.get("RVehlcleTonnage", "0")))),
               "lNVhlActVal": gNDiscussActualValue,
               "lNDeductible_036001": "2000",
               "lNVhlActVal_036005": gNDiscussActualValue,
               "lNVhlActVal_036007": gNDiscussActualValue,
               "gCRegVhlTyp": cardict['gCRegVhlTyp'],
               "NCurbWt": cardict['NCurbWt'],
               "hCAppNme": cardict['hCAppNme'].encode("utf-8"),
               "jCGender": "1061",
               "jCOwnerAge": "341060",
               "JQgCVhlTyp": JQ_seatcode,  # 车辆类型代码
               "SYgCVhlTyp": SY_seatcode,  # 车辆类型代码
               "insuranceType": insuranceType,  # 保险类型
               "endDate": dt.get("endDate", utils.getlatedate(1)),
               "syStart": dt.get("insuranceTime", {}).get("syStart", utils.getlatedate(1)),
               "jqStart": dt.get("insuranceTime", {}).get("jqStart", utils.getlatedate(1))
               }
    ####################################计算费用###############################################
    if isinstance(insuranceType, list):
        for i in insuranceType:
            feedict['insuranceType'] = i
            post_fee(requesteicc, feedict, data)
    else:
        post_fee(requesteicc, feedict, data)


# 通过车牌号查询用户的保费
def getData_CPlateNo(requesteicc, renewal_data_dt):
    headers = SE.headers
    # searchVin = data['vinNo']
    # insureCarId = renewal_data_dt['insureCarId']
    CPlateNo = renewal_data_dt['plateNumber']
    searchVin = renewal_data_dt['vinNo']
    client = renewal_data_dt['client']
    isPhone = renewal_data_dt['isPhone']
    sessionId = renewal_data_dt['sessionId']
    insuranceType = renewal_data_dt["insuranceType"]
    if isinstance(insuranceType, list):
        insuranceTypeGroupId = insuranceType[0].get("insuranceTypeGroupId", "")
        insuranceTypeGroup = insuranceType[0].get("insuranceTypeGroup", "")
    else:
        insuranceTypeGroupId = insuranceType.get("insuranceTypeGroupId", "")
        insuranceTypeGroup = insuranceType.get("insuranceTypeGroup", "")

        # 从redis中查询消息
        log.info(u"START  FROM REDIS GET CIC USERINFO")
        # 获取消息体
        r = CRedis()
        feedict = r.get_vin(searchVin, "4")
        if feedict != None:
            # 设置保险类型
            feedict = eval(feedict)
            log.info(u"CIC FROM REDIS GET USERINFO %s " % searchVin)
            feedict['insuranceType'] = insuranceType
            post_fee(requesteicc, feedict, renewal_data_dt)
            return

    '''
    endDate = renewal_data_dt.get("endDate", "")
    # 判断保险结束时间 如果结束时间距离今天超过40天不进行查询
    if endDate != "":
        min_time = compare_time40(endDate)
        if min_time > config.days:
            log.error("中华联合保险查询在40天内的 车牌号为 %s 保险结束时间为 %s" % (CPlateNo, endDate))
            send_mq(client, CPlateNo, "中华联合保险查询在40天内的 车牌号为 %s 保险结束时间为 %s" % (CPlateNo, endDate), "2", "4", sessionId,
                    isPhone, insuranceTypeGroupId, insuranceTypeGroup)
            return "中华联合保险查询在40天内的 车牌号为 %s 保险结束时间为 %s" % (CPlateNo, endDate)
        if min_time < 0:
            renewal_data_dt['endDate'] = utils.getlatedate(1)
            endDate = utils.getlatedate(1)
    else:
        renewal_data_dt['endDate'] = utils.getlatedate(1)
    '''
    cardict = getCarInof(requesteicc, searchVin)
    if isinstance(cardict, dict):
        # 发送车辆信息 更新数据库
        send_mq_update_carinfo(client, cardict)
    else:
        # 未查询到交管信息
        send_mq(client, CPlateNo, cardict, "2", "4", sessionId, isPhone, insuranceTypeGroupId, insuranceTypeGroup)
        return

    # 获取查询车辆精确信息的MD5

    res3 = requesteicc.get(
        url='http://carply.cic.cn/pcis/policy/universal/quickapp/quick_offer.jsp?isOffer=1&prodNo=0360&dptCde=32010101&CUnionMrk=0')
    res_body = res3.text
    if res3.status_code == 200:
        md5byJy = re.findall(r"md5byJy = \"(.+?)\";", res_body, re.S)[0]
    else:
        res_body = requesteicc.get(
            url='http://carply.cic.cn/pcis/policy/universal/quickapp/quick_offer.jsp?isOffer=1&prodNo=0360&dptCde=32010101&CUnionMrk=0')
        res_body = res3.text
        md5byJy = re.findall(r"md5byJy = \"(.+?)\";", res_body, re.S)[0]

    ######################请求车辆信息##################################
    request114 = requests.session();
    headers114 = SE.headers
    request114.headers.update(headers114)
    # 车架号
    # searchVin='LMVHEKFD6EA029484'
    # searchVin='LFV2A11K8F4192886'
    validNo = md5byJy
    # vehicleId='I0000000000000000230000000000033'
    search_url = 'http://114.251.1.161/zccx/search?regionCode=00000000&jyFlag=0&businessNature=A&operatorCode=0000000000&returnUrl=http://carply.cic.cn/pcis/offerAcceptResult&vname=&searchVin=' + searchVin + '&vinflag=1&validNo=' + validNo
    repon114 = request114.get(url=search_url)
    if "没有找到符合条件的数据" in repon114.text:
        log.error("%s 通过车架号未查询到车辆信息 %s" % (CPlateNo, searchVin))
        carlist = vehicleList_code(request114, cardict['gCNoticeType'])
    else:
        carlist = parseCarInfo(repon114.text)
    if len(carlist) != 0:
        gCSearchCode = vehicleId = carlist[len(carlist) - 1]['vehicleId']
        vehicleCode = carlist[len(carlist) - 1]['vehicleCode']
        ######################选择车辆##################################
        getVehicleForReturn_url = 'http://114.251.1.161/zccx/getVehicleForReturn.shtml?vehicleCode=' + vehicleId + '&vehicleId=' + vehicleId + '&hvinRoot=' + searchVin + '&hvinFlag=1'
        getVehicleForReturnrsp = request114.post(url=getVehicleForReturn_url)
        # log.info(getVehicleForReturnrsp.text)
        dt = parseCardata(getVehicleForReturnrsp.text)
    else:
        log.error("%s 中华联合通过车架号以及车辆快速查询码无法车辆信息无法查询")
        send_mq(client, CPlateNo, "%s 中华联合通过车架号以及车辆快速查询码无法车辆信息无法查询" % CPlateNo, "2", "4", sessionId, isPhone,
                insuranceTypeGroupId, insuranceTypeGroup)
        return


    #####################新车购置浮动上线###############
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    ModeCode = vehicleCode.replace(' ', '').replace(u'\r', '').replace(u'\n', '')
    getOfferPrice_url = 'http://carply.cic.cn/pcis/policy/universal/quickapp/actionservice.ai'
    getOfferPricedata = 'ADAPTER_TYPE=JSON_TYPE&SERVICE_TYPE=ACTION_SERVIC&CODE_TYPE=CODE_TYPE&BEAN_HANDLE=baseAction&ACTION_HANDLE=perform&SERVICE_NAME=offerDataLoadAction&SERVICE_MOTHOD=getOfferPrice&DW_DATA=%255B%255D&HELPCONTROLMETHOD=common&SCENE=UNDEFINED&BIZ_SYNCH_CONTINUE=false&CUST_DATA=dptCde%253D32010101%2523%2523%2523prodNo%253D0360_0332%2523%2523%2523modelCde%253D' + ModeCode
    getOfferPriceresp = requesteicc.post(url=getOfferPrice_url, data=getOfferPricedata, headers=headers)
    getOfferPriceresp = getOfferPriceresp.json()
    gNOfferPurChasePriceMax = getOfferPriceresp['JSON_OBJ']['maxPrice']  # 新车购置价浮动上限
    gNOfferPurChasePriceMin = getOfferPriceresp['JSON_OBJ']['minPrice']  # 新车购置价浮动下
    #####################请求车管所信息#############################################

    # cardict=getCarInof(requesteicc,searchVin)


    ##############################################
    checkNo = cardict['checkNo']
    codestr = cardict['gCValidateCode']
    gCFstRegYm = cardict['CFstRegYm']
    gNDisplacement = cardict['gNDisplacement']
    gCPlateTyp = cardict['gCPlateTyp']
    gNNewPurchaseValue = gNOfferPurChasePriceMax  # 新车购置价
    plateNo = cardict['gCPlateNo'].encode('utf-8')
    seat2 = dt['seat']
    seat = cardict['gNSeatNum']
    # 座位数 续保信息 与 车型搜索出的信息不一致
    # seat2 = renewal_data_dt.get('NSeatNum', 999)
    if seat == "":
        seat = seat2

    if int(seat) <= 6:
        SY_seatcode = '302001001'
        JQ_seatcode = '302001001'
    elif int(seat) > 6 and int(seat) < 10:
        SY_seatcode = '302001008'
        JQ_seatcode = '302001022'
    elif int(seat) >= 10:
        SY_seatcode = '302001016'
        JQ_seatcode = '302001022'
    else:
        SY_seatcode = '302001001'
        JQ_seatcode = '302001001'
    gNDiscussActualValue = calcNActualValue(gCFstRegYm, gNNewPurchaseValue, SY_seatcode)
    gNDiscussActualValue = str((gNDiscussActualValue))
    # 协商实际价值
    feedict = {"gNNewPurchaseTaxValue": dt['purchasePriceTax'],  # 新车购置价
               "gNKindredPrice": dt['kindredPrice'],
               "gNKindredPriceTax": dt['kindredPriceTax'],
               "gNNewPurchaseValue": dt['purchasePrice'],
               "gNDiscussActualValue": gNDiscussActualValue,
               "gCFrmNo": dt['hvinRoot'],
               "gCMonDespRate": "307007001",  # 月折旧率
               "gNActualValue": gNDiscussActualValue,
               "gNOfferPurChasePriceMax": gNOfferPurChasePriceMax,
               "gNOfferPurChasePriceMin": gNOfferPurChasePriceMin,
               "gCIndustryModelCode": dt['hyVehicleCode'],
               "gCIndustryModelName": urllib.unquote(urllib.unquote(dt['hyVehicleName']).__str__()),
               # dt['hyVehicleName'],  # 要转码
               "gCNoticeType": dt['vehicleFgwCode'],
               "gCProdPlace": dt['importF'].encode("utf-8"),  # 中文需要转为012
               "gCFamilyCode": dt['familyCode'],
               "gCFamilyName": dt['familyName'].encode("utf-8"),
               "gCFstRegYm": gCFstRegYm,
               "gCModelNme": dt['vehicleName'].encode("utf-8"),
               "gCBrandId": cardict['gCBrandId'].encode(),  # dt['brandName'].encode("utf-8"),
               "gCModelCde": dt['vehicleCode'],
               "gCSearchCode": checkNo,
               "gCValidateCode": codestr,
               "gCPlateNo": plateNo,
               "gCEngNo": cardict['CEngNo'],
               "gNDisplacement": str(float(dt['displacement']) / 1000),
               "gCPlateTyp": cardict['gCPlateTyp'],
               "gCCarAge": "306007",  # age
               "gNSeatNum": seat,
               "gNPoWeight": cardict['NCurbWt'],
               "RVehlcleTonnage": int(float((cardict.get("RVehlcleTonnage", "0")))),
               "lNVhlActVal": gNDiscussActualValue,
               "lNDeductible_036001": "2000",
               "lNVhlActVal_036005": gNDiscussActualValue,
               "lNVhlActVal_036007": gNDiscussActualValue,
               "gCRegVhlTyp": cardict['gCRegVhlTyp'],
               "NCurbWt": cardict['NCurbWt'],
               "hCAppNme": cardict['hCAppNme'].encode("utf-8"),
               "jCGender": "1061",
               "jCOwnerAge": "341060",
               "JQgCVhlTyp": JQ_seatcode,  # 车辆类型代码
               "SYgCVhlTyp": SY_seatcode,  # 车辆类型代码
               "endDate": renewal_data_dt.get("endDate", utils.getlatedate(1)),  # 上期保险结束时间
               "insuranceType": insuranceType,  # 保险类型
               "syStart": renewal_data_dt.get("insuranceTime", {}).get("syStart", utils.getlatedate(1)),
               "jqStart": renewal_data_dt.get("insuranceTime", {}).get("jqStart", utils.getlatedate(1))
               }
    ####################################计算费用###############################################
    if isinstance(insuranceType, list):
        for i in insuranceType:
            feedict['insuranceType'] = i
            post_fee(requesteicc, feedict, renewal_data_dt)
    else:
        post_fee(requesteicc, feedict, renewal_data_dt)


# 入参 session 组成的fee 原始的入参
def post_fee(requesteicc, feedict, data):
    insuranceType = feedict.get("insuranceType", {})
    insuranceTypeGroupId = insuranceType.get("insuranceTypeGroupId", "")
    insuranceTypeGroup = insuranceType.get("insuranceTypeGroup", "")
    seat = feedict['gNSeatNum']

    searchVin = data['vinNo']
    insureCarId = data['insureCarId']
    isPhone = data['isPhone']
    sessionId = data['sessionId']
    client = data['client']
    plateNo = data['plateNumber']
    try:
        fee_url = 'http://carply.cic.cn/pcis/policy/universal/quickapp/actionservice.ai'
        d = getFeebody(feedict)
        feedata = 'ADAPTER_TYPE=JSON_TYPE&SERVICE_TYPE=ACTION_SERVIC&CODE_TYPE=CODE_TYPE&BEAN_HANDLE=baseAction&ACTION_HANDLE=perform&SERVICE_NAME=offerBizAction&SERVICE_MOTHOD=calcPremium&DW_DATA=' + d + '&HELPCONTROLMETHOD=common&SCENE=UNDEFINED&BIZ_SYNCH_CONTINUE=false&CUST_DATA=contiOfferMrk%253D1%2523%2523%2523multiOfferFlagMrk%253D1'
        log.info(u"发送费用计算请求")
        feeresp = requesteicc.post(url=fee_url, data=feedata, headers=headers)
        feeresp = feeresp.json()
        log.info(u"请求响应成功")
        count = 1

        while "终保日期" in feeresp['RESULT_MSG'] and "起保日期" in feeresp['RESULT_MSG'] and count < 4:
            str1 = "\d{4}-\d{2}-\d{2}"
            datelist = re.findall(str1, feeresp['RESULT_MSG'], re.S)
            # print(feeresp['RESULT_MSG'])
            if len(datelist) == 2:
                bigdate = compare_date(datelist[0], datelist[1])
                bigdate = compare_date(bigdate, utils.getlatedate(0))

            if len(datelist) == 3:
                bigdate = compare_date(datelist[0], datelist[1])
                bigdate = compare_date(bigdate, datelist[2])
                bigdate = compare_date(bigdate, utils.getlatedate(0))

            feedict['endDate'] = bigdate
            feedict['syStart'] = bigdate
            feedict['jqStart'] = bigdate
            d = getFeebody(feedict)
            log.error("CIC重复投保正在重新发送请求")
            feedata = 'ADAPTER_TYPE=JSON_TYPE&SERVICE_TYPE=ACTION_SERVIC&CODE_TYPE=CODE_TYPE&BEAN_HANDLE=baseAction&ACTION_HANDLE=perform&SERVICE_NAME=offerBizAction&SERVICE_MOTHOD=calcPremium&DW_DATA=' + d + '&HELPCONTROLMETHOD=common&SCENE=UNDEFINED&BIZ_SYNCH_CONTINUE=false&CUST_DATA=contiOfferMrk%253D1%2523%2523%2523multiOfferFlagMrk%253D1'
            feeresp = requesteicc.post(url=fee_url, data=feedata, headers=headers)
            count += count
            feeresp = feeresp.json()


        # 新的重复投保
        #

        if len(feeresp['WEB_DATA']) > 0 and "重复投保" not in feeresp['RESULT_MSG']:
            # print json.dumps(feeresp,ensure_ascii=False)
            feedt = parseFee(feeresp)
            lstrs = getPriumeInf(feedt)
            log.info(lstrs)
            # data=[开始时间,结束时间，座位数，组合id (insureTypeGroupId )，车辆id，公司id]
            soupDb(lstrs, [utils.getlatedate(1) + ' 00:00:00', utils.getlatedate(365) + " 23:59:59", seat,
                           insuranceTypeGroupId, insureCarId, "4"])
            # 发送成功队列
            send_mq(client, plateNo, "", "1", "4", sessionId, isPhone, insuranceTypeGroupId, insuranceTypeGroup)
            log.info(u"中华联合入库成功:%s|%s" % (plateNo, searchVin))
            # 更新redis数据
            r.set_vin(searchVin, "4", json.dumps(feedict, ensure_ascii=False))

        if len(feeresp['WEB_DATA']) <= 0 or "重复投保" in feeresp['RESULT_MSG']:
            log.error(u"中华联合 车架号：%s,错误信息%s:" % (searchVin, feeresp['RESULT_MSG'].replace("\n", "")))
            # 返回错误信息
            msg = feeresp['RESULT_MSG'].replace("\n", "")
            send_mq(client, plateNo, msg, "2", "4", sessionId, isPhone, insuranceTypeGroupId, insuranceTypeGroup)
            return 0
    except Exception as e:
        log.error(traceback.format_exc())
        send_mq(client, plateNo, "未知异常", "2", "4", sessionId, isPhone, insuranceTypeGroupId, insuranceTypeGroup)
        return 0
