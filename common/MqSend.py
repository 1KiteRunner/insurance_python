# -*- coding:utf-8 -*-
__author__ = 'weikai'
import json


# 发送队列
def send_mq(
        client,
        plateNumber,
        failedReason,
        crawlFlag,  # 字符串 1成功 2 失败
        companyid,  # "1" 平安
        sessionId,
        isPhone,
        insuranceTypeGroupId,
        insuranceTypeGroup,
        licenseType='02',
        vehicle_style='K33'):
    sendbody = {
        'plateNumber': plateNumber,
        'failedReason': failedReason,
        'crawlFlag': crawlFlag,
        "companyId": companyid,
        "sessionId": sessionId,
        "isPhone": isPhone,
        "insuranceTypeGroupId": insuranceTypeGroupId,
        "insuranceTypeGroup": insuranceTypeGroup,
        "licenseType": licenseType,
        "vehicle_style": vehicle_style}
    try:
        client.send(
            body=json.dumps(sendbody, ensure_ascii=False).encode(),
            destination="/queue/CRAWLING_DONE")
    except Exception as e:
        print(e)


def send_mq_update_carinfo(client, body):
    carInfo = {
        "licenseNo": body.get("gCPlateNo", ""),
        "vinNo": body.get("gCFrmNo", ""),
        "endDate": "",
        "CCardDetail": body.get("gCRegVhlTyp", ""),
        "brandName": body.get("gCNoticeType", ""),
        "insuredName": body.get("hCAppNme", ""),
        "identifyNumber": "",
        "CUsageCde": "",
        "NNewPurchaseValue": "",
        "COMPANY_ID": "4",
        "insuredAddress": "",
        "mobile": "",
        "enrollDate": body.get("CFstRegYm", ""),
        "engineNo": body.get("CEngNo", ""),
        "CModelCde": body.get("BrandEN", ""),
        "NSeatNum": body.get("gNSeatNum", "")
    }
    try:
        client.send(
            body=json.dumps(carInfo, ensure_ascii=False).encode(),
            destination="/queue/UPDATE_CAR_INFO")
    except Exception as e:
        print(e)


# 发送核保队列
def send_hebao_mq(
        client,
        plateNumber,
        failedReason,
        hebaoFlag,  # 字符串 1成功 2 失败 3 审核中
        companyid,  # "1" 平安
        sessionId,
        isPhone,
        insuranceTypeGroupId,
        insuranceTypeGroup,
        licenseType='02'):
    sendbody = {
        'plateNumber': plateNumber,
        'failedReason': failedReason,
        'hebaoFlag': hebaoFlag,
        "companyId": companyid,
        "sessionId": sessionId,
        "isPhone": isPhone,
        "insuranceTypeGroupId": insuranceTypeGroupId,
        "insuranceTypeGroup": insuranceTypeGroup,
        "licenseType": licenseType,
}
    try:
        client.send(
            body=json.dumps(sendbody, ensure_ascii=False).encode(),
            destination="/queue/CRAWLING_UNDERWRITE")
    except Exception as e:
        print(e)