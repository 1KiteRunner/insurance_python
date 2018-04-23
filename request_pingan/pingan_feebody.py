# -*- coding:utf-8 -*-
__author__ = 'weikai'

import time
import re
import json
from datetime import datetime
import sys
from request_pingan.utils import getlatedate, getbirthday, getgender
import request_pingan.settings as se
from request_pingan.parse import parse_fee
from common.log import Logger
from request_pingan.insuranceType import get_insurance_type
import request_pingan.options as list_op
from common import redisUtil

r = redisUtil.CRedis()
reload(sys)
sys.setdefaultencoding('utf8')
global null, false, true
null = None
false = False
true = True

log = Logger()


# 日期比较 返回值 为大的日期


def compare_date(str_date1, str_date2):
    str_date1 = str_date1.split(" ")[0]
    str_date2 = str_date2.split(" ")[0]
    str_date1 = datetime.strptime(str_date1, "%Y-%m-%d")
    str_date2 = datetime.strptime(str_date2, "%Y-%m-%d")
    if str_date1.date() >= str_date2.date():
        return str(str_date1.date())

    return str(str_date2.date())


def get_fee(session, dtall):
    insuranceType = dtall.get("insuranceType", "")
    mainQuotationNo = "Q106900390000467963406"  # 询价单号
    username = dtall['DMVehicleInfo']['owner']  # "魏居章"

    certificateTypeNo = dtall.get("certificateTypeNo", "")
    if certificateTypeNo != '':
        sexCode = getgender(certificateTypeNo)  # 性别男M 女为F
        birthday = getbirthday(certificateTypeNo)
        certificateNo = certificateTypeNo
    else:
        certificateNo = dtall.get("insurantInfo", {}).get("certificateTypeNo", "320324198305024977")
        # certificateNo = "320324198305024977"
        if len(certificateNo) < 15:
            certificateNo = "320324198305024977"
        sexCode = getgender(certificateNo)  # 性别男M 女为F
        birthday = getbirthday(certificateNo)

    jq_insuranceEndTime = dtall.get('jq_insuranceEndTime', '')
    sy_insuranceEndTime = dtall.get('sy_insuranceEndTime', '')
    year = getlatedate(365)[0:4]
    if jq_insuranceEndTime != '' and year not in jq_insuranceEndTime:
        datestr = compare_date(jq_insuranceEndTime, getlatedate(0))
        c51beginTime = getlatedate(1, datestr) + ' 00:00:00'
        c51endTime = getlatedate(365, datestr) + " 23:59:59"
    else:
        c51beginTime = getlatedate(1) + ' 00:00:00'
        c51endTime = getlatedate(365) + " 23:59:59"

    if sy_insuranceEndTime != '' and year not in sy_insuranceEndTime:
        datestr = compare_date(sy_insuranceEndTime, getlatedate(0))
        c01beginTime = getlatedate(1, datestr) + ' 00:00:00'
        c01endTime = getlatedate(365, datestr) + " 23:59:59"
    else:
        c01beginTime = getlatedate(1) + ' 00:00:00'
        c01endTime = getlatedate(365) + " 23:59:59"
    # c01beginTime = "2017-02-21 00:00:00"
    # c01endTime = "2018-02-20 23:59:59"
    # c51beginTime = "2017-02-21 00:00:00" #交强险
    # c51endTime = "2018-02-20 23:59:59"
    verifyCode = dtall['DMVehicleInfo']['verifyCode']  # = "AZG4"  # 验证码

    firstRegisterDate = dtall['DMVehicleInfo'][
        'vehicleRegisterDate']  # 格式为“20150108”
    firstRegisterDate = firstRegisterDate[:4] + "-" + firstRegisterDate[4:6] + "-" + firstRegisterDate[6:]
    # firstRegisterDate = "2015-01-08"  # 初登日期
    vehicleLicenceCode = dtall['DMVehicleInfo']['carMark']  # = "苏C-296QC"
    vehicleFrameNo = dtall['DMVehicleInfo'][
        'rackNo']  # = "LSGPB54U9FD091410"  # 车架
    engineNo = dtall['DMVehicleInfo']['engineNo']  # = "143450846"
    model = dtall.get("model", "")
    if model == "" or model == 0:
        autoModelCode = dtall['DMVehicleInfo'][
            'vehicleModel']  # = "YLD1046SHT"  # 车辆类型
        autoModelName = modifyAutoModelName = circVehicleModel = dtall[
            'DMVehicleInfo']['vehicleModel']  # "别克SGM7162DMAB轿车"
        circVehicleChineseBrand = brandName = dtall[
            'DMVehicleInfo']['vehicleBrand1']  # = "上海通用东岳"
        vehicleTypeCode = ""
        brandParaOutYear = ""
        purchasePriceDefaultValue = dtall['DMVehicleInfo']['salePrice']  # = 104700  # 车子实际价格

    else:
        autoModelCode = dtall['model'][
            'autoModelCode']  # = "YLD1046SHT"  # 车辆类型
        autoModelName = modifyAutoModelName = circVehicleModel = dtall[
            'model']['autoModelName']  # "别克SGM7162DMAB轿车"
        circVehicleChineseBrand = brandName = dtall[
            'model']['brandName']  # = "上海通用东岳"
        vehicleTypeCode = dtall.get(
            'model', {}).get(
            'vehicleTypeNew', '')  # = "A012"
        brandParaOutYear = dtall.get(
            'model', {}).get(
            'firstSaleDate', '')  # = "2014"
        purchasePriceDefaultValue = dtall['model'][
            'purchasePrice']  # = 104700  # 车子实际价格
    vehicleSeats = dtall.get('DMVehicleInfo', {}).get("limitLoadPerson", "")
    if vehicleSeats == "" or vehicleSeats == "0":
        vehicleSeats = dtall['model']['seats']  # = "5"

    exhaustCapability = float(dtall['DMVehicleInfo']['pmVehicleList'][0]['displacement'])  # = 1.598  # 排量

    ownerVehicleTypeCode = dtall['DMVehicleInfo']['vehicleStyle']  # = "K33"

    VehicleTypeChose = list_op.list_options

    ownerVehicleTypeDesc = VehicleTypeChose[ownerVehicleTypeCode]  # "轿车"  # 车辆类型
    if int(vehicleSeats) < 6:
        vehicleTypeName = "六座以下客车"
    elif int(vehicleSeats) >= 6 or int(vehicleSeats) < 10:
        vehicleTypeName = "六座至十座以下客车"
    elif int(vehicleSeats) >= 10 or int(vehicleSeats) < 20:
        vehicleTypeName = "十座至二十座以下客车"
    elif int(vehicleSeats) >= 20 or int(vehicleSeats) < 36:
        vehicleTypeName = "十座至二十座以下客车"
    elif int(vehicleSeats) >= 36:
        vehicleTypeName = "三十六座及三十六座以上客车"
    else:
        vehicleTypeName = "六座以下客车"

    # vehicleClassCode = "1"
    licenceTypeCode = dtall['DMVehicleInfo']['vehicleType']  # ="02"
    licenceTypeBody = list_op.licenceTypeBody
    licenceTypeName = licenceTypeBody[licenceTypeCode]  # = "小型汽车"
    wholeWeight = dtall['DMVehicleInfo']['wholeWeight']  # = "1.38"
    usageAttributeCode = "02"
    ownershipAttributeCode = "03"

    # insuredAmount = 88995  # 保险车辆价格
    # insuredAmount=70000
    insuredAmount = defaultCalculate(session, purchasePriceDefaultValue, firstRegisterDate, c01beginTime,
                                     vehicleTypeCode)
    body = {
        "mainQuotationNo": mainQuotationNo,
        "saleInfo": {
            "departmentCode": "21069",
            "dealerCode": "",
            "businessSourceCode": "2",
            "businessSourceDetailCode": "3",
            "channelSourceCode": "G",
            "channelSourceDetailCode": "F",
            "agentInfoList": [
                {
                    "agencyCode": "",
                    "agentCode": "10690047",
                    "agentAgreementNo": "1069004717001",
                    "supplementAgreementNo": "1",
                    "agencySaleName": "",
                    "agencySaleProfCertifNo": ""
                }
            ],
            "brokerInfoList": [
                {
                    "brokerCode": ""
                }
            ],
            "employeeInfoList": [
                {
                    "employeeCode": "2100003024",
                    "employeeProfCertifNo": ""
                }
            ],
            "primaryIntroducerInfo": null,
            "partnerInfoList": [
                {
                    "partnerType": "01",
                    "partnerCode": "210697215001"
                }
            ]
        },
        "quotationBaseInfo": {
            "totalStandardPremium": 0,
            "documentGroupId": ""
        },
        "sendInfo": {
            "sendWay": "03",
            "country": "01",
            "province": "",
            "receiveTimeZone": "0"
        },
        "aplylicantInfoList": [
            {
                "sexCode": sexCode,
                "nationality": "156",
                "personnelType": "1",
                "certificateType": "01",
                "homeTelephone": "",
                "address": "",
                "isConfirm": 5,
                "invoicePrintType": "03",
                "taxpayerCertificateType": "",
                "taxpayerCertificateNo": "",
                "billingAddress": "",
                "billingPhone": "",
                "billingDepositBank": "",
                "billingDepositBankAccount": ""
            }
        ],
        "insurantInfoList": [],
        "quotationList": [
            {
                "applyPlans": "C51C01",
                "c01CircInfoDTO": {},
                "c01IsApply": false,
                "c01RateFactorPremCalcResult": {},
                "c51CircInfoDTO": {},
                "c51IsApply": false,
                "combineQuotationNo": "",
                "confirmTime": int(time.time() * 1000),
                "displayNo": "01",
                "voucher": {
                    "applicantInfo": {
                        "certificateTypeCode": "01",
                        "city": "",
                        "communicationAddress": "",
                        "country": "00",
                        "county": "",
                        "invoicePrintType": "05",
                        "isConfirm": 5,
                        "linkmodeType": "03",
                        "nationality": "156",
                        "personnelFlag": "1",
                        "province": "",
                        "sexCode": sexCode
                    },
                    "baseInfo": {
                        "departmentCode": "21069",
                        "disputedSettleModeCode": 1,
                        "rateClassFlag": "14"
                    },
                    "c01BaseInfo": {
                        "agentAgreementNo": "1069004717001",
                        "agentCode": "10690047",
                        "agentName": "圣泰达保险代理有限公司南京市江宁东山分公司",
                        "brokerCode": "",
                        "calculateResult": {
                            "beginTime": c01beginTime,
                            "endTime": c01endTime,
                            "shortTermRatio": 1
                        },
                        "channelAdjustDeploitationFeeRate": "",
                        "channelAdjustPoudndageRate": "",
                        "channeladjustPromptingFee": "",
                        "departmentCode": "21069",
                        "disputedSettleModeCode": 1,
                        "insuranceBeginTime": c01beginTime,
                        "insuranceEndTime": c01endTime,
                        "insuranceType": "1",
                        "isCalculateWithoutCirc": "N",
                        "isReportElectronRelation": "",
                        "isRound": "N",
                        "isaccommodation": "N",
                        "lastPolicyNo": "",
                        "planCode": "C01",
                        "productCode": "",
                        "productName": "",
                        "quoteTimes": 0,
                        "rateChannelAdjustFlag": "",
                        "rateClassFlag": "14",
                        "remark": "",
                        "renewalTypeCode": "0",
                        "shortTimeCoefficient": 1,
                        "supplementAgreementNo": "1",
                        "totalActualPremium": "",
                        "totalAgreePremium": "",
                        "totalDiscountCommercial": "",
                        "totalStandardPremium": ""
                    },
                    "c01DisplayRateFactorList": [
                        {
                            "factorCode": "F15",
                            "factorValue": 0,
                            "ratingTableNo": "I100003001"
                        },
                        {
                            "factorCode": "F30",
                            "factorValueName": "",
                            "ratingTableNo": "I100003001"
                        },
                        {
                            "factorCode": "F76",
                            "factorValueName": "",
                            "ratingTableNo": "I100003001"
                        },
                        {
                            "factorCode": "F74",
                            "factorValueName": "",
                            "ratingTableNo": "I100003001"
                        },
                        {
                            "factorCode": "F34",
                            "factorValueName": "",
                            "ratingTableNo": "I100003001"
                        }
                    ],
                    "c01DutyList": [
                        {
                            "dutyCode": "27"
                        },
                        {
                            "dutyCode": "28"
                        },
                        {
                            "dutyCode": "48"
                        },
                        {
                            "basePremium": 0,
                            "dutyCode": "01",
                            "insuredAmount": 30196.8,
                            "premiumRate": 0,
                            "pureRiskPremium": "",
                            "riskPremium": "",
                            "totalActualPremium": 0,
                            "totalAgreePremium": 0,
                            "totalStandardPremium": 0
                        },
                        {
                            "basePremium": 0,
                            "dutyCode": "02",
                            "insuredAmount": "50",
                            "premiumRate": 0,
                            "pureRiskPremium": "",
                            "riskPremium": "",
                            "totalActualPremium": 0,
                            "totalAgreePremium": 0,
                            "totalStandardPremium": 0
                        },
                        {
                            "basePremium": 0,
                            "dutyCode": "03",
                            "insuredAmount": 30196.8,
                            "insuredAmountDefaultValue": 30196.8,
                            "premiumRate": 0,
                            "pureRiskPremium": "",
                            "riskPremium": "",
                            "totalActualPremium": 0,
                            "totalAgreePremium": 0,
                            "totalStandardPremium": 0
                        }
                    ],
                    "c01ExtendInfo": {
                        "analogyVehicleFlag": "0",
                        "applyYears": "",
                        "brandDetail": "",
                        "commercialClaimRecord": "09",
                        "dealerCode": "",
                        "expectationUnderwriteLimit": "2",
                        "offerLastPolicyFlag": "N",
                        "ownerVehicleTypeCode": ownerVehicleTypeCode,
                        "partnerWorknetCode": "210697215001",
                        "useMobileLocation": "N"
                    },
                    "c01SpecialPromiseList": [],
                    "c51BaseInfo": {
                        "agentAgreementNo": "1069004717001",
                        "agentCode": "10690047",
                        "agentName": "圣泰达保险代理有限公司南京市江宁东山分公司",
                        "brokerCode": "",
                        "calculateResult": {
                            "beginTime": c51beginTime,
                            "endTime": c51endTime,
                            "shortTermRatio": 1
                        },
                        "departmentCode": "21069",
                        "disputedSettleModeCode": 1,
                        "formatType": "06",
                        "insuranceBeginTime": c51beginTime,
                        "insuranceEndTime": c51endTime,
                        "insuranceType": "1",
                        "isCalculateWithoutCirc": "N",
                        "isReportElectronRelation": "",
                        "isRound": "N",
                        "lastPolicyNo": "",
                        "planCode": "C51",
                        "quoteTimes": 0,
                        "rateClassFlag": "14",
                        "renewalTypeCode": "0",
                        "shortTimeCoefficient": 1,
                        "supplementAgreementNo": "1",
                        "totalActualPremium": "",
                        "totalAgreePremium": "",
                        "totalDiscountCommercial": "",
                        "totalStandardPremium": ""
                    },
                    "c51DisplayRateFactorList": [
                        {
                            "factorCode": "F54",
                            "factorRatioCOM": "1",
                            "factorValue": "A4",
                            "ratingTableNo": ""
                        },
                        {
                            "factorCode": "F55",
                            "factorValue": "V4",
                            "ratingTableNo": ""
                        },
                        {
                            "factorCode": "F999",
                            "factorRatioCOM": 0,
                            "factorValue": "",
                            "ratingTableNo": ""
                        }
                    ],
                    "c51DutyList": [
                        {
                            "dutyCode": 45,
                            "insuredAmount": "110000"
                        },
                        {
                            "dutyCode": 46,
                            "insuredAmount": "10000"
                        },
                        {
                            "dutyCode": 47,
                            "insuredAmount": "2000"
                        }
                    ],
                    "c51ExtendInfo": {
                        "brandDetail": "",
                        "dealerCode": "",
                        "expectationUnderwriteLimit": "2",
                        "ownerVehicleTypeCode": ownerVehicleTypeCode,
                        "partnerWorknetCode": "210697215001",
                        "useMobileLocation": "N"
                    },
                    "c51SpecialPromiseList": [],
                    "insurantInfo": {
                        "certificateTypeCode": "01",
                        "city": "",
                        "communicationAddress": "",
                        "country": "00",
                        "county": "",
                        "isShowCustomerHistory": false,
                        "linkmodeType": "03",
                        "nationality": "156",
                        "personnelFlag": "1",
                        "province": "",
                        "sameAsText": "--请选择--",
                        "sexCode": sexCode
                    },
                    "ownerDriver": {
                        "birthday": birthday,
                        "certificateTypeCode": "01",
                        "certificateTypeNo": certificateNo,
                        "linkmodeType": "03",
                        "nationality": "156",
                        "personnelFlag": "1",
                        "personnelName": username,
                        "sexCode": sexCode
                    },
                    "receiverInfo": {
                        "country": "01",
                        "province": "",
                        "receiveAddress": "",
                        "receiveTimeZone": "0",
                        "sendWay": "03"
                    },
                    "saleInfo": {
                        "businessSourceCode": "2",
                        "businessSourceDetailCode": "3",
                        "channelSourceCode": "G",
                        "channelSourceDetailCode": "F",
                        "departmentCode": "21069",
                        "developFlg": "N",
                        "saleAgentCode": "2100003024"
                    },
                    "vehicleTarget": {
                        "addr": {
                            "country": "01"
                        },
                        "analogyPrice": 0,
                        "autoModelCode": autoModelCode,
                        "autoModelName": autoModelName,
                        "brandName": brandName,
                        "brandParaOutYear": brandParaOutYear,
                        "cache": {
                            "brand": ""
                        },
                        "changeOwnerFlag": "0",
                        "circVehicleChineseBrand":circVehicleChineseBrand,
                        "circVehicleModel": circVehicleModel,
                        "energyType": "0",
                        "engineNo": engineNo,
                        "exhaustCapability": exhaustCapability,
                        "firstRegisterDate": firstRegisterDate,
                        "fleetMark": "0",
                        "fleetNo": "",
                        "isAbnormalCar": "0",
                        "isMiniVehicle": "N",
                        "licenceTypeCode": "02",
                        "licenceTypeName": licenceTypeName,
                        "loanVehicleFlag": "0",
                        "modifyAutoModelName": modifyAutoModelName,
                        "ownerVehicleTypeCode": ownerVehicleTypeCode,
                        "ownerVehicleTypeDesc": ownerVehicleTypeDesc,
                        "ownershipAttributeCode": ownershipAttributeCode,
                        "price": purchasePriceDefaultValue,
                        "purchasePriceDefaultValue": purchasePriceDefaultValue,
                        "specialCarFlag": " ",
                        "specialCarLicenseChoice": "",
                        "transferDate": "",
                        "usageAttributeCode": usageAttributeCode,
                        "vehicleClassCode": "1",
                        "vehicleFrameNo": vehicleFrameNo,
                        "vehicleLicenceCode": vehicleLicenceCode,
                        "vehicleLossInsuredValue": insuredAmount,
                        "vehicleSeats": vehicleSeats,
                        "vehicleTonnages": 0,
                        "vehicleTypeCode": vehicleTypeCode,
                        "vehicleTypeDetailCode": "",
                        "vehicleTypeName": vehicleTypeName,
                        "verifyCode": verifyCode,
                        "wholeWeight": wholeWeight
                    },
                    "vehicleTaxInfo": {
                        "deduction": "",
                        "deductionDueCode": "",
                        "deductionDueProportion": "",
                        "deductionDueType": "",
                        "delinquentTaxDue": true,
                        "fuelType": "0",
                        "isNeedAddTax": "01",
                        "taxPayerId": certificateNo,
                        "taxType": "1",
                        "totalTaxMoney": ""
                    }
                }
            }
        ]
    }

    #
    if insuranceType != "":
        body['quotationList'][0]['voucher']['c01DutyList'] = get_insurance_type(insuranceType, insuredAmount,
                                                                                vehicleSeats, vehicleFrameNo)
        # 只交 交强险
        if insuranceType['compulsoryInsurance'] == '1' and len(body['quotationList'][0]['voucher']['c01DutyList']) == 0:
            body['quotationList'][0]['applyPlans'] = "C51"
            body['quotationList'][0]['voucher']['c01BaseInfo']['planCode'] = ""

    fee_url = "https://icorepnbs.pingan.com.cn/icore_pnbs/do/app/quotation/applyQueryAndQuote"
    headers = se.headers
    headers[
        'Referer'] = "https://icorepnbs.pingan.com.cn/icore_pnbs/mainCtrl.tpl?applicantPersonFlag=1&familyPrd=&bsDetailCode=2-3-G-F&usageAttributeCode=02&ownershipAttributeCode=03&insuranceType=1&agentSalerName=&businessCertificateNum=&empBusinessCertificateNum=&deptCodeText=21069&secondLevelDepartmentCode=210&deptCode=21069&employeeCodeText=2100003024&employeeCode=2100003024&channelCode=G&agentCode=10690047&productCombineList=&partnerWorknetPanel=210697215001&worknetCode=&conferVal=1069004717001+1&agentNameLike=&agentCodeText=&brokerCode=&agentName=%E5%9C%A3%E6%B3%B0%E8%BE%BE%E4%BF%9D%E9%99%A9%E4%BB%A3%E7%90%86%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%E5%8D%97%E4%BA%AC%E5%B8%82%E6%B1%9F%E5%AE%81%E4%B8%9C%E5%B1%B1%E5%88%86%E5%85%AC%E5%8F%B8&conferNo=1069004717001&subConferNo=1&dealerCode=&autoInsurance=true&propertyInsurance=false&accidentInsurance=false&rateClassFlag=14&employeeName=%E8%80%BF%E8%B6%8A&saleGroupCode=21069000682&businessMode=&systemId=ICORE-PTS&applyApproach="
    body_str = json.dumps(body, ensure_ascii=False)
    fee_rsp = session.post(
        url=fee_url,
        data=body_str.encode(),
        headers=headers,
        verify=False)
    #
    fee_rsp_text = fee_rsp.text
    fee_rsp_json = __rsp2josn(fee_rsp)
    # print(json.dumps(fee_rsp_json, ensure_ascii=False))
    if isinstance(fee_rsp_json, dict):
        pass
    else:
        return fee_rsp_json

    # 如果车型不对
    if "chooseVehType" in fee_rsp_text:
        applyQueryResult = fee_rsp_json["applyQueryResult"]
        # for key in applyQueryResult:
        vehiclePriceList = applyQueryResult['vehiclePriceList']
        vehiclePriceList.sort(key=lambda obj: obj.get('purchasePrice'))
        autoModelCode = vehiclePriceList[0]['circAutoModelCode']
        body["quotationList"][0]["applyQueryResult"] = applyQueryResult
        body["quotationList"][0]['processType'] = "chooseVehType"
        body["quotationList"][0]['message'] = u"申请报价完成"
        body["quotationList"][0]['isAutoSaveFlag'] = false
        body["quotationList"][0]["accommodIsOpen"] = false

        body["quotationList"][0]["selectCircAutoModelCode"] = autoModelCode

        body_str2 = json.dumps(body, ensure_ascii=False)
        fee_rsp = session.post(
            url=fee_url,
            data=body_str2.encode(),
            headers=headers,
            verify=False)
        fee_rsp_text = fee_rsp.text
        fee_rsp_json = __rsp2josn(fee_rsp)
        if isinstance(fee_rsp_json, dict):
            pass
        else:
            return fee_rsp_json

    if "renewalAndC51DisTax" in fee_rsp_text:
        applyQueryResult = fee_rsp_json["applyQueryResult"]
        body["quotationList"][0]["applyQueryResult"] = applyQueryResult
        body["quotationList"][0]['processType'] = "renewalAndC51DisTax"
        body["quotationList"][0]['message'] = u"申请报价完成"
        body["quotationList"][0]['isAutoSaveFlag'] = false
        body["quotationList"][0]["accommodIsOpen"] = false
        body["quotationList"][0]["isShowChannelAndAgent"] = false
        body["quotationList"][0]["vehicleTypeDetailList"] = []
        body["quotationList"][0]["circAutoModelType"] = fee_rsp_json.get("circAutoModelType", "")
        body["quotationList"][0]["c01MD5Result"] = fee_rsp_json["c01MD5Result"]
        body["quotationList"][0]["voucher"] = fee_rsp_json["voucher"]
        body_str3 = json.dumps(body, ensure_ascii=False)
        fee_rsp = session.post(
            url=fee_url,
            data=body_str3.encode(),
            headers=headers,
            verify=False)
        fee_rsp_text = fee_rsp.text
        fee_rsp_json = __rsp2josn(fee_rsp)
        if isinstance(fee_rsp_json, dict):
            pass
        else:
            return fee_rsp_json
    if 'showCompareList' in fee_rsp_text:
        c01CompareDetailList = fee_rsp_json["c01CompareDetailList"]
        c01CompareDetailList[0]["userSelectCircVal"] = true
        applyQueryResult = fee_rsp_json["applyQueryResult"]
        body["quotationList"][0]["applyQueryResult"] = applyQueryResult
        body["quotationList"][0]['processType'] = "showCompareList"
        body["quotationList"][0]['message'] = u"申请报价完成"
        body["quotationList"][0]['isAutoSaveFlag'] = false
        body["quotationList"][0]["accommodIsOpen"] = false
        body["quotationList"][0]["isShowChannelAndAgent"] = false
        body["quotationList"][0]["vehicleTypeDetailList"] = []
        body["quotationList"][0]["c01MD5Result"] = fee_rsp_json["c01MD5Result"]
        body["quotationList"][0]["voucher"] = fee_rsp_json["voucher"]
        body["quotationList"][0]['c01CompareDetailList'] = c01CompareDetailList
        body_str3 = json.dumps(body, ensure_ascii=False)
        fee_rsp = session.post(
            url=fee_url,
            data=body_str3.encode(),
            headers=headers,
            verify=False)
        fee_rsp_text = fee_rsp.text
        fee_rsp_json = __rsp2josn(fee_rsp)

        if isinstance(fee_rsp_json, dict):
            pass
        else:
            return fee_rsp_json

    if '起保日期必须在当前日期的规定时间范围内' in fee_rsp_text:
        log.error("平台返回信息:起保日期必须在当前日期的规定时间范围内 %s" % vehicleLicenceCode)
        return "平台返回信息:起保日期必须在当前日期的规定时间范围内"

    if '险种组合不满足' in fee_rsp_text:
        return '险种组合不满足'

    str1 = "\d{4}-\d{2}-\d{2} "

    # 车龄超过3年不保划痕 超过十年 不包自然 涉水 国产车 超过十年不包 车损以及盗抢
    if "车身划痕险车龄超3年禁止承保" in fee_rsp_text:
        return "车身划痕险车龄超3年禁止承保"
    elif "超过10年车龄" in fee_rsp_text:
        return "超过十年 不包自然 涉水 国产车 超过十年不包 车损以及盗抢"
        # elif "10年不承保车损":
        #   return "流程号：46, 转保国产车车龄≥10年不承保车损@@@流程号：57, 转保国产车车龄≥10年不承保盗抢"
    # 平安改变 增加重复投保
    if len(fee_rsp_json.get("applyQueryResult", {}).get("circInfoDTO", {}).get("thirdVehicleReinsureList", [])) > 0:
        log.error("平安重复投保，正在重试")
        date_end = \
            fee_rsp_json.get("applyQueryResult", {}).get("circInfoDTO", {}).get("thirdVehicleReinsureList", [])[0].get(
                "dateExpire", "")
        if date_end != "":
            date_end = date_end.split(" ")[0]
            dtall['jq_insuranceEndTime'] = getlatedate(1)
            dtall['sy_insuranceEndTime'] = date_end
            fee = get_fee(session, dtall)
            return fee

    if "申请报价完成并保存报价单成功" in fee_rsp_text:
        all = {}
        fee = parse_fee(fee_rsp_json)
        all['fee'] = fee
        all['c01beginTime'] = c01beginTime
        all['c01endTime'] = c01endTime
        all['vehicleSeats'] = vehicleSeats
        log.info(all)
        r.set_vin(vehicleFrameNo, "1", dtall)
        return all

    elif '重复投保' in fee_rsp_text:
        datelist = re.findall(str1, fee_rsp_json['c51CaculateResult'][
            'c51ResultDTO']['circMessage'], re.S)
        if len(datelist) == 2:
            bigdate = compare_date(datelist[0], datelist[1])
            bigdate = compare_date(bigdate, getlatedate(0))
            dtall['jq_insuranceEndTime'] = bigdate
            # dtall['sy_insuranceEndTime'] = bigdate
            fee = get_fee(session, dtall)
            return fee

        errormsg = fee_rsp_json.get("c51CaculateResult", {}).get("c51ResultDTO", {}).get("circMessage", "")
        return errormsg

    # elif 'afterForceQuote' in fee_rsp_text:


    else:
        error = fee_rsp_json.get(
            "applyQueryResult",
            {}).get(
            "circInfoDTO",
            {}).get(
            "thirdVehicleReinsureList",
            "")
        noQuoteReason = fee_rsp_json.get("c01CaculateResult", {}).get("c01ResultDTO", {}).get("decisionTreeResult",
                                                                                              {}).get("noQuoteReason",
                                                                                                      "")
        if len(noQuoteReason) != 0:
            log.error(noQuoteReason)
            return noQuoteReason
        if len(error) != 0:
            log.error(json.dumps(error, ensure_ascii=False))
            log.error(u"报价失败")
            return error
        else:
            return "未知问题"


def defaultCalculate(
        session,
        purchasePriceToWrite,
        dateFirstRegister,
        insuranceBeginTime,
        vehicleType):
    Calculate_url = "https://icorepnbs.pingan.com.cn/icore_pnbs/do/app/calculate/defaultCalculate?_cflag=calculateStealRobInsuredAmount"
    headers = se.headers
    headers['Content-Type'] = "application/json;charset=UTF-8"
    headers[
        'Referer'] = "https://icorepnbs.pingan.com.cn/icore_pnbs/mainCtrl.tpl?applicantPersonFlag=1&familyPrd=&bsDetailCode=2-3-G-F&usageAttributeCode=02&ownershipAttributeCode=03&insuranceType=1&agentSalerName=&businessCertificateNum=&empBusinessCertificateNum=&deptCodeText=21069&secondLevelDepartmentCode=210&deptCode=21069&employeeCodeText=2100003024&employeeCode=2100003024&channelCode=G&agentCode=10690047&productCombineList=&partnerWorknetPanel=210697215001&worknetCode=&conferVal=1069004717001+1&agentNameLike=&agentCodeText=&brokerCode=&agentName=%E5%9C%A3%E6%B3%B0%E8%BE%BE%E4%BF%9D%E9%99%A9%E4%BB%A3%E7%90%86%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%E5%8D%97%E4%BA%AC%E5%B8%82%E6%B1%9F%E5%AE%81%E4%B8%9C%E5%B1%B1%E5%88%86%E5%85%AC%E5%8F%B8&conferNo=1069004717001&subConferNo=1&dealerCode=&autoInsurance=true&propertyInsurance=false&accidentInsurance=false&rateClassFlag=14&employeeName=%E8%80%BF%E8%B6%8A&saleGroupCode=21069000682&businessMode=&systemId=ICORE-PTS&applyApproach="

    body = {
        "purchasePriceToWrite": purchasePriceToWrite,
        "dateFirstRegister": dateFirstRegister,
        "monthDeprecition": "0.006",
        "insuranceBeginTime": insuranceBeginTime,
        "calculateType": "calculateStealRobInsuredAmount",
        "calculateParamNames": "purchasePriceToWrite,dateFirstRegister,monthDeprecition,insuranceBeginTime",
        "departmentCode": "210",
        "vehicleType": vehicleType,
        "vehicleTypeDetail": "",
        "usageAttributeCode": "02"}
    body = json.dumps(body)
    Calculate_url_rsp = session.post(
        url=Calculate_url,
        data=body,
        headers=headers,
        verify=False)

    return Calculate_url_rsp.json()['calculateResult']['stealRobInsuredAmount']


def __rsp2josn(rsp):
    if rsp.status_code == 500:
        log.error(u"平安报价出错")
        error = re.findall(r"<errorMsg[^<]*>(.*?)</errorMsg>", rsp.text, re.S)
        if isinstance(error, list):
            log.error(error[0])
            return error[0]

        return 0
    if rsp.status_code == 200:
        return rsp.json()


if __name__ == "__main__":
    usename = u"魏凯".encode("utf-8")
    print usename + "(车险-行驶证车主)"
