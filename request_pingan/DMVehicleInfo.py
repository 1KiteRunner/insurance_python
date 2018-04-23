# -*- coding:utf-8 -*-
__author__ = 'weikai'
import json
import request_pingan.settings as se
from common.dama.damaUtil import dama
from common.log import Logger

# 获取验证码 打吗 校验
log = Logger()


# 至少需要车架号进行获取车管所验证码 carMark=车牌号 中间带-


def __getDMVehicleInfo(session, vehicleFrameNo, carMark=""):
    VECHICLE_URL = "https://icorepnbs.pingan.com.cn/icore_pnbs/do/app/quotation/getDMVehicleInfo"
    HEADERS = se.headers
    HEADERS[
        'Referer'] = "https://icorepnbs.pingan.com.cn/icore_pnbs/mainCtrl.tpl?applicantPersonFlag=1&familyPrd=&bsDetailCode=2-3-G-F&usageAttributeCode=02&ownershipAttributeCode=03&insuranceType=1&agentSalerName=&businessCertificateNum=&empBusinessCertificateNum=&deptCodeText=21069&secondLevelDepartmentCode=210&deptCode=21069&employeeCodeText=2100003024&employeeCode=2100003024&channelCode=G&agentCode=10690047&productCombineList=&partnerWorknetPanel=210697215001&worknetCode=&conferVal=1069004717001+1&agentNameLike=&agentCodeText=&brokerCode=&agentName=%E5%9C%A3%E6%B3%B0%E8%BE%BE%E4%BF%9D%E9%99%A9%E4%BB%A3%E7%90%86%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%E5%8D%97%E4%BA%AC%E5%B8%82%E6%B1%9F%E5%AE%81%E4%B8%9C%E5%B1%B1%E5%88%86%E5%85%AC%E5%8F%B8&conferNo=1069004717001&subConferNo=1&dealerCode=&autoInsurance=true&propertyInsurance=false&accidentInsurance=false&rateClassFlag=14&employeeName=%E8%80%BF%E8%B6%8A&saleGroupCode=21069000682&businessMode=&systemId=ICORE-PTS&applyApproach="
    VECHICLE_BODY = {"carMark": carMark,
                     "vehicleFrameNo": vehicleFrameNo,
                     "departmentCode": "21069",
                     "insuranceCode": "C51",
                     "rateClassFlag": "14"}
    log.info(u"请求车管所验证码")
    VECHICLE_RSP = session.post(
        url=VECHICLE_URL,
        data=json.dumps(VECHICLE_BODY),
        headers=HEADERS,
        verify=False)
    if "checkCode" in VECHICLE_RSP.text:
        VECHICLE_RSP_JSON = VECHICLE_RSP.json()
        log.info(u"获取车管所验证码成功")
        return_out = {}
        return_out["checkNo"] = VECHICLE_RSP_JSON['checkNo']
        return_out["checkCode"] = VECHICLE_RSP_JSON['checkCode']
        return_out["vehicleFrameNo"] = vehicleFrameNo
        return_out["carMark"] = carMark
        return return_out

    log.error(u"获取车管所验证码失败")
    return 0


# 入参 获取验证码的返回


def __queryDMVehicleInfoConfirm(
        session,
        checkCode,
        checkNo,
        vehicleFrameNo,
        carMark=""):
    log.info(u"验证码为 %s", checkCode)
    DMVEHICLE_CONFIRM_URL = "https://icorepnbs.pingan.com.cn/icore_pnbs/do/app/quotation/queryDMVehicleInfoConfirm"
    DMVEHICLE_CONFIRM_BODY = {"checkCode": checkCode,  # 验证码
                              "checkNo": checkNo,  # 唯一ID
                              "departmentCode": "21069", "rateClassFlag": "14", "insuranceCode": "C51",
                              "carMark": carMark,  # 车牌号
                              "vehicleFrameNo": vehicleFrameNo}

    HEADERS = se.headers
    HEADERS[
        'Referer'] = "https://icorepnbs.pingan.com.cn/icore_pnbs/mainCtrl.tpl?applicantPersonFlag=1&familyPrd=&bsDetailCode=2-3-G-F&usageAttributeCode=02&ownershipAttributeCode=03&insuranceType=1&agentSalerName=&businessCertificateNum=&empBusinessCertificateNum=&deptCodeText=21069&secondLevelDepartmentCode=210&deptCode=21069&employeeCodeText=2100003024&employeeCode=2100003024&channelCode=G&agentCode=10690047&productCombineList=&partnerWorknetPanel=210697215001&worknetCode=&conferVal=1069004717001+1&agentNameLike=&agentCodeText=&brokerCode=&agentName=%E5%9C%A3%E6%B3%B0%E8%BE%BE%E4%BF%9D%E9%99%A9%E4%BB%A3%E7%90%86%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%E5%8D%97%E4%BA%AC%E5%B8%82%E6%B1%9F%E5%AE%81%E4%B8%9C%E5%B1%B1%E5%88%86%E5%85%AC%E5%8F%B8&conferNo=1069004717001&subConferNo=1&dealerCode=&autoInsurance=true&propertyInsurance=false&accidentInsurance=false&rateClassFlag=14&employeeName=%E8%80%BF%E8%B6%8A&saleGroupCode=21069000682&businessMode=&systemId=ICORE-PTS&applyApproach="
    HEADERS['Origin'] = 'https://icorepnbs.pingan.com.cn'
    DMVEHICLE_CONFIRM_BODY = '{"checkCode":"' + checkCode + '","checkNo":"' + checkNo + '","departmentCode":"21069","rateClassFlag":"14","insuranceCode":"C51","carMark":"' + carMark + '","vehicleFrameNo":"' + vehicleFrameNo + '"}'
    DMVEHICLE_RSP = session.post(
        url=DMVEHICLE_CONFIRM_URL,
        data=DMVEHICLE_CONFIRM_BODY,
        headers=HEADERS,
        verify=False)
    # u'{"errorMessage":"未匹配到交管车辆信息，可提交电子联系单至平台进行核实！","errorCode":"-400","circErrorCode":"94054"}'
    # {"errorMessage":"录入的校验码有误 ","errorCode":"-400","circErrorCode":"93037"}
    DMVEHICLE_RSP_JSON = DMVEHICLE_RSP.json()

    if DMVEHICLE_RSP_JSON['circErrorCode'] == "0000":
        log.info(u"获取车管所信息成功")
        DMVEHICLE_RSP_JSON['verifyCode'] = checkCode
        return DMVEHICLE_RSP_JSON

    log.error(u"获取车管信息失败 %s ", vehicleFrameNo)
    log.error(DMVEHICLE_RSP.json()['errorMessage'])
    return DMVEHICLE_RSP.json()['errorMessage']


def queryDMVehicleInfoConfirm(session, vehicleFrameNo, carMark=""):
    CODE_RSP = __getDMVehicleInfo(session, vehicleFrameNo, carMark)
    # dmt = DamatuApi()
    # checkCode = dmt.decode(base64.b64decode(CODE_RSP['checkCode']), 200)
    checkCode = dama("3", CODE_RSP['checkCode'])
    # checkCode="8888"
    CODE_OUT = __queryDMVehicleInfoConfirm(
        session,
        checkCode,
        CODE_RSP['checkNo'],
        vehicleFrameNo,
        carMark)
    count = 1
    if isinstance(CODE_OUT, dict):
        return CODE_OUT

    if not isinstance(CODE_OUT, dict):
        if "录入的校验码有误" in CODE_OUT:
            while "录入的校验码有误" in CODE_OUT and count < 4:
                dama("99", CODE_RSP['checkCode'])
                CODE_RSP = __getDMVehicleInfo(session, vehicleFrameNo, carMark)
                # dmt = DamatuApi()
                # checkCode = dmt.decode(base64.b64decode(CODE_RSP['checkCode']), 200)
                checkCode = dama("3", CODE_RSP['checkCode'])
                CODE_OUT = __queryDMVehicleInfoConfirm(
                    session, checkCode, CODE_RSP['checkNo'], vehicleFrameNo, carMark)
                # CODE_OUT=queryDMVehicleInfoConfirm(session, vehicleFrameNo, carMark)
                count += 1
            return CODE_OUT

        return CODE_OUT
