# -*- coding:utf-8 -*-
__author__ = 'weikai'
import sys
from request_huanong.hn_settings import headers
from request_huanong.body_temp import premiumTemp
import copy
from request_huanong.hn_util import calc_user_years
from request_cic.utils import getlatedate
from request_cic.feebody2 import compare_date
from request_cicc.interface.calculateActualValue import calculateActualValue
from request_huanong.hn_insuranceType import get_hn_insurance_type
import datetime
from request_huanong.hn_parse import hn_getPriumeInf
import urllib, re
from common.log import Logger
from  common import redisUtil
import json
import jsonpath

reload(sys)
sys.setdefaultencoding('utf8')
global null, false, true
null = None
false = False
true = True
r = redisUtil.CRedis()


def get_hn_body(alldata):
    body = copy.deepcopy(premiumTemp)
    carowner = alldata['car']['remark']
    headers['Content-Type'] = "application/x-www-form-urlencoded; charset=UTF-8"
    body['vehicleJingyou'] = alldata['vehicleJingyou']

    body['car']['licenseType'] = alldata['car']['licenseType']
    body['car']['colorCode'] = alldata['car']['colorCode']
    body['car']['netWeight'] = alldata['car']['netWeight']
    seats = str(alldata['car']['seatCount'])
    body['car']['seatCount'] = seats
    alldata['vehicleJingyou']['seat']=seats
    body['car']['seatCountOld'] = seats
    if int(seats) < 6:
        carKindCodeNew = "K1"
    elif int(seats) >= 6 and int(seats) < 10:
        carKindCodeNew = "K2"
    elif int(seats) >= 10 and int(seats) < 20:
        carKindCodeNew = "K3"
    elif int(seats) >= 20 and int(seats) < 36:
        carKindCodeNew = "K4"
    elif int(seats) >= 36:
        carKindCodeNew = "K5"
    else:
        carKindCodeNew = "K1"

    enrollDate = alldata['car']['enrollDate']
    body['car']['carKindCodeNew'] = carKindCodeNew  # 座位数类型
    body['car']['modelAlias'] = alldata.get("vehicleJingyou", {}).get("vehicleAlias",
                                                                      "")  # alldata['vehicleJingyou']['vehicleAlias']
    body['car']['enrollDate'] = enrollDate

    body['car']['licenseNo'] = alldata['car']['licenseNo']
    body['car']['modelName'] = alldata['car']['modelName']
    body['car']['carKindCode'] = alldata['vehicleJingyou']['carKindCode']
    body['car']['exhaustScale'] = str(alldata['car']['exhaustScale'])

    body['car']['industryModelCode'] = alldata['other']['industryModelCode']
    body['car']['exhaustScaleOld'] = alldata['car']['exhaustScale']
    body['car']['modelCodePlat'] = alldata['other']['modelCode']
    body['car']['modelCode'] = alldata['other']['modelCode']
    body['car']['engineNo'] = alldata['car']['engineNo']
    body['car']['tradeName'] = alldata['vehicleJingyou']['factoryName']
    body['car']['brand'] = alldata['other']['brandCN']
    body['car']['modelNamePlat'] = alldata['car']['modelName']
    body['car']['vinNo'] = alldata['car']['vinNo']
    body['car']['noticeType'] = alldata['vehicleJingyou']['searchCode']  # CAF7209A
    purchasePriceOld = alldata['vehicleJingyou']['price']
    body['car']['purchasePriceOld'] = purchasePriceOld
    body['car']['purchasePrice'] = purchasePriceOld
    body['car']['netWeightOld'] = str("%.3f" % alldata['car']['netWeight'])
    body['car']['carName'] = alldata['car']['modelName']
    body['car']['tonCount'] = str("%.4f" % alldata['car']['tonCount'])
    body['car']['vehicleStyle'] = alldata['car']['vehicleStyle']
    body['car']['vehicleCode'] = alldata['vehicleJingyou']['vehicleCode']

    Address = alldata.get("carInfo", {}).get("insuredAddress", "")
    mobile = alldata.get("carInfo", {}).get("mobile", "")
    taxPayerIdentifyNumber = alldata.get("carInfo", {}).get("identifyNumber", "")

    Address = [Address, "江苏南京"][Address == ""]
    mobile = [mobile, ""][mobile == ""]
    taxPayerIdentifyNumber = [taxPayerIdentifyNumber, ""][taxPayerIdentifyNumber == ""]

    # body tax信息
    body['tax']['taxPayerIdentifyNumber'] = taxPayerIdentifyNumber  # 身份证号码
    body['tax']['taxPayer'] = taxPayerIdentifyNumber  # 身份证号码
    body['tax']['taxPayerName'] = carowner
    body['tax']['net'] = alldata['car']['netWeight']  # 整备质量
    body['tax']['taxPayerAddress'] = Address  # 身份证号码

    # body person
    body['persons'][0]['insuredName'] = carowner
    body['persons'][0]['insuredAddress'] = Address
    body['persons'][0]['mobile'] = mobile
    body['persons'][0]['identifyNumber'] = taxPayerIdentifyNumber

    # body base
    operateDate = getlatedate(0)  # 当前时间
    startDate = alldata.get('carInfo', {}).get("insuranceTime", {}).get("syStart", getlatedate(1))
    endDate = getlatedate(364, startDate)
    startDateCI = alldata.get('carInfo', {}).get("insuranceTime", {}).get("jqStart", getlatedate(1))
    endDateCI = getlatedate(364, startDateCI)  # 交强结束
    '''
    MyendDate = alldata['carInfo']['endDate']
    if MyendDate != "":
        datestr = compare_date(MyendDate, getlatedate(0))
        startDate = getlatedate(1, datestr)  ##商业开始
        endDate = getlatedate(365, datestr)  # 商业结束
        startDateCI = startDate  # 交强开始
        endDateCI = endDate  # 交强结束
    else:
        startDate = getlatedate(1)  ##商业开始
        endDate = getlatedate(365)  # 商业结束
        startDateCI = startDate  # 交强开始
        endDateCI = endDate  # 交强结束
    '''
    body['base']['operateDate'] = operateDate
    body['base']['startDate'] = startDate
    body['base']['endDate'] = endDate
    body['base']['startDateCI'] = startDateCI
    body['base']['endDateCI'] = endDateCI

    body['car']['useYears'] = calc_user_years(startDate, enrollDate)  # 使用年限
    CarActualValue = calculateActualValue(purchasePriceOld, '85', seats, 'A0', '', enrollDate,
                                          today=datetime.datetime.strptime(startDate, "%Y-%m-%d"))
    body['car']['actualValue'] = str(CarActualValue)
    CarActualValue = str("%.2f" % CarActualValue)
    body['car']['actualValueOld'] = CarActualValue  # 车辆实际价格


    # 拼装险种组合
    insuranceType = alldata['carInfo']['insuranceType']
    kinds = get_hn_insurance_type(insuranceType, float(CarActualValue), seats, purchasePriceOld)
    body['kinds'] = kinds
    if insuranceType.get("compulsoryInsurance", "1") == "0":
        body["tax"] = {}
    return body


def get_hn_premium(session, alldata=None, body_org=None):
    # 获取body体
    log = Logger()
    try:
        if body_org == None:
            body_org = get_hn_body(alldata)

        # print(json.dumps(body_org,ensure_ascii=False))
        url = "http://qcar.chinahuanong.com.cn/quotepriceasync/preciseQuote.do"
        body = "model=" + urllib.quote(json.dumps(body_org))
        headers['Content-Type'] = "application/x-www-form-urlencoded; charset=UTF-8"
        rsp = session.post(url=url, data=body, headers=headers)
        rsp_text = rsp.text

        if "终保日期" in rsp_text and "起保日期" in rsp_text:
            log.error(u"华农重复投保 正在重复请求")
            str1 = "\d{4}-\d{2}-\d{2}"
            datelist = re.findall(str1, rsp_text, re.S)
            if len(datelist) == 2:
                bigdate = compare_date(datelist[0], datelist[1])
                bigdate = compare_date(bigdate, getlatedate(0))
                endDate = getlatedate(0, bigdate)
                # alldata['carInfo']['endDate'] = endDate
                alldata['carInfo']['insuranceTime']['jqStart'] = endDate
                alldata['carInfo']['insuranceTime']['syStart'] = endDate
                # rsp = get_hn_premium(session, alldata)
                return get_hn_premium(session, alldata)
                # rsp_text = rsp.text
        if "重复投保" in rsp_text and "reinsureStr" in rsp_text:
            errmsg = rsp.json()
            msg = errmsg['base']['reinsureStr']
            log.error(msg)
            return msg

        if "发生异常" in rsp_text:
            log.error(rsp_text)
            return rsp.text
        if "agentComm" in rsp_text:
            all = {}
            rsp_json = rsp.json()
            PriumeInf = hn_getPriumeInf(rsp_json)
            all['fee'] = PriumeInf
            all['c01beginTime'] = body_org['base']['startDate']
            all['c01endTime'] = body_org['base']['endDate']
            all['vehicleSeats'] = body_org['vehicleJingyou']['seat']
            JQ = jsonpath.jsonpath(body_org, "$.kinds[?(@.kindCode=='BZ')]")
            if JQ != False:
                r.set_vin(body_org['car']['vinNo'], "13", json.dumps(body_org, ensure_ascii=False))
            return all
    except Exception as e:
        import traceback
        log.error(e)
        log.error(traceback.format_exc())
        return "未知异常"


if __name__ == "__main__":
    from common.sessionUtil import get_session
    from request_huanong.hn_carInfo import get_carInof
    from request_huanong.hn_getCarModel import get_car_model1

    session = get_session("13")
    rsp = get_carInof(session, "LVSHCFAE7AF522519")
    print json.dumps(rsp, ensure_ascii=False)
    vehicleJingyou = get_car_model1(session, rsp)
    print json.dumps(vehicleJingyou, ensure_ascii=False)
    alldata = {}
    alldata['car'] = rsp
    alldata['vehicleJingyou'] = vehicleJingyou['vehicleJingyou']
    vehicleJingyou.pop('vehicleJingyou')
    alldata['other'] = vehicleJingyou
    alldata['carInfo'] = {}
    alldata['carInfo']['endDate'] = "2017-05-12"
    alldata['carInfo']['insuredAddress'] = ""
    alldata['carInfo']['mobile'] = ""
    alldata['carInfo']['identifyNumber'] = ""
    from body_temp import insuranceType

    alldata['carInfo']['insuranceType'] = insuranceType

    get_hn_premium(session, alldata)
