# -*- coding:utf-8 -*-
__author__ = 'weikai'
from request_huanong.hn_settings import headers
import urllib
import json
from common.log import Logger
from request_cic.getCarModel import get_car_model
from request_huanong.body_temp import carModelbody
from request_cic.utils import getCuttime


# 通过车管所信息 获取车辆具体数据
def get_car_model1(session, carinfo, flag=0):
    licenseType = carinfo['licenseType']
    colorCode = carinfo['colorCode']
    netWeight = carinfo['netWeight']
    enrollDate = carinfo['enrollDate']
    seatCount = carinfo['seatCount']
    modelName = carinfo['modelName']
    exhaustScale = carinfo['exhaustScale']
    licenseNo = carinfo['licenseNo']
    haulage = carinfo['haulage']
    engineNo = carinfo['engineNo']
    vinNo = carinfo['vinNo']
    vehicleStyle = carinfo['vehicleStyle']
    remark = carinfo['remark']
    body = {
        "licenseType": licenseType,
        "colorCode": colorCode,
        "netWeight": netWeight,
        "carKindCodeNew": "",
        "modelAlias": "",
        "chgOwnerFlag": "0",
        "carChecker": "",
        "abnormalCarFlag": "0",
        "lastYearDamage": "",
        "carLicenceDate": "",
        "enrollDate": enrollDate,
        "seatCountOld": seatCount,
        "carCheckerReason": "000",
        "useNatureCode": "85",
        "certificateType": "",
        "fuelType": "0",
        "licenseNo": licenseNo,
        "modelName": modelName,
        "exhaustScale": exhaustScale,
        "transferDate": "",
        "specialCarFlag": "",
        "useNatureCodeNew": "N85",
        "carKindCode": "KA",
        "useYears": "0",
        "industryModelCode": "",
        "exhaustScaleOld": exhaustScale,
        "haulage": haulage,
        "engineNo": engineNo,
        "tradeName": "",
        "certificateNo": "",
        "ecdemicVehicleFlag": "0",
        "runAreaName": "中华人民共和国境内(不含港澳台)",
        "powerScale": "",
        "fixedLine": "",
        "vinNo": vinNo,
        "noticeType": "",
        "carKindCatalogCode": "",
        "sortCode": "",
        "noDamageYears": "0",
        "certificateDate": "",
        "carRegiste": "0",
        "runAreaCode": "11",
        "seatCount": seatCount,
        "purchasePriceOld": "",
        "isPrintModelAlias": "0",
        "carName": "",
        "tonCount": "",
        "vehicleDamaged": "1",
        "bookingTime": "",
        "runMiles": "45000",
        "loanVehicleFlag": "0",
        "noLicenseFlag": "0",
        "expecLossRatio": "",
        "isNewCarFlag": "0",
        "purchasePrice": "",
        "licenseColorCode": "01",
        "actualValue": "",
        "depreciation": "0.60",
        "tonCountOld": "",
        "carCheckTime": "",
        "vehicleStyle": vehicleStyle,
        "modelCode": "",
        "carCheckStatus": "1"
    }
    log = Logger()
    url = "http://qcar.chinahuanong.com.cn/quotepriceasync/carModelInquiry.do"
    headers['Content-Type'] = "application/x-www-form-urlencoded; charset=UTF-8"
    #print(json.dumps(body, ensure_ascii=False))
    body = "car=" + urllib.quote(json.dumps(body)) + "&ptCode="
    # print(json.dumps(body,ensure_ascii=False))
    rsp = session.post(url=url, data=body, headers=headers)

    if "carModel" in rsp.text:
        log.info(u"查询出车辆信息")
        carModelList = rsp.json()['carModel']
        # print(json.dumps(carModelList,ensure_ascii=False))
        carModelList = sorted(carModelList, key=lambda x: float(x["vehicleJingyou"]["price"]))
        # print(json.dumps(carModelList, ensure_ascii=False))
        # print(carModelList)
        # print(carModelList[0])

        carModelbody['licenseType'] = licenseType
        carModelbody['colorCode'] = colorCode
        carModelbody['netWeight'] = netWeight
        modelAlias = carModelList[0].get("vehicleJingyou", {}).get("vehicleAlias", "")
        if modelAlias == "":
            modelAlias = carModelList[0].get("vehicleJingyou", {}).get("vehicleClassName", "")
        carModelbody['modelAlias'] = modelAlias
        carModelbody['enrollDate'] = enrollDate
        carModelbody['seatCountOld'] = seatCount
        carModelbody['seatCountOld'] = seatCount
        carModelbody['modelName'] = modelName
        carModelbody['licenseNo'] = licenseNo
        carModelbody['exhaustScale'] = exhaustScale
        carModelbody['carKindCode'] = carModelList[0]['vehicleJingyou']['carKindCode']
        carModelbody['industryModelCode'] = carModelList[0]['industryModelCode']
        carModelbody['exhaustScaleOld'] = exhaustScale
        carModelbody['modelCodePlat'] = carModelList[0]['modelCode']
        carModelbody['engineNo'] = engineNo
        carModelbody['tradeName'] = carModelList[0]['vehicleJingyou']['factoryName']
        carModelbody['brand'] = carModelList[0]['vehicleJingyou']['brandName']
        carModelbody['modelNamePlat'] = modelName
        carModelbody['vinNo'] = vinNo
        # carModelbody['carKindCatalogCode']=carKindCatalogCode
        carModelbody['purchasePriceOld'] = carModelList[0]['vehicleJingyou']['price']
        carModelbody['netWeightOld'] = carModelList[0]['vehicleJingyou']['fullWeight']
        carModelbody['deptName'] = carModelList[0]['vehicleJingyou']['familyName']
        carModelbody['purchasePrice'] = carModelList[0]['vehicleJingyou']['price']
        carModelbody['modelCode'] = carModelList[0]['modelCode']
        carModelbody['vehicleStyle'] = vehicleStyle

        body2 = "car=" + urllib.quote(json.dumps(carModelbody)) + "&ptCode=&startDate=" + getCuttime().split(" ")[
            0] + "+0%3A0%3A0"
        # print(json.dumps(body2, ensure_ascii=False))
        rsp2 = session.post(url=url, data=body2, headers=headers)
        if "carModel" in rsp2.text:
            carModelList2 = rsp2.json()['carModel']
            carModelList2 = sorted(carModelList2, key=lambda x: float(x["vehicleJingyou"]["price"]))
            return carModelList2[0]
        else:
            return carModelList[0]

    else:
        if flag == 0:
            log.error(u"通过中华联合去查询车辆信息")
            car_model = get_car_model(vinNo)
            if car_model != None:
                modelName = car_model['gCIndustryModelName']
                carinfo['modelName'] = modelName
                return get_car_model1(session, carinfo, flag=1)
        else:
            log.error(u"未查询到车辆信息")
            return 0
