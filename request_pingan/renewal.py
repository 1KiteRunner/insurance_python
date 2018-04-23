# -*- coding:utf-8 -*-
__author__ = 'weikai'
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from common.sessionUtil import set_session
from common.log import Logger
import request_pingan.settings as se
from request_pingan.parse import parse_toibcswriter, parse_renewal_data, parse_user_data, parse_lastyear_info

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
log = Logger()


def is_renewal(sessionoop, plateNumber="苏A-HJ108"):
    '''
    :param sessionoop: 登录之后的request对象
    查询是否续保用户 如果为续保用户返回用户信息 如果不是返回0
    :return:
    '''

    toibcswriter_url = "https://icore-pts.pingan.com.cn/ebusiness/auto/newness/toibcswriter.do?transmitId=apply"
    headers = se.headers
    headers['Referer'] = "https://icore-pts.pingan.com.cn/ebusiness/frames/main_02.jsp"
    toibcswriter_resp = sessionoop.get(url=toibcswriter_url, headers=headers, verify=False)
    toibcswriter_body = toibcswriter_resp.text
    dt_toibcswriter = parse_toibcswriter(toibcswriter_body)
    cypherText = dt_toibcswriter['cypherText']
    timestamp = dt_toibcswriter['timestamp']

    # 切换域名请求 获取cookies 为下面使用

    icorepnbs_request = requests.session()
    icorepnbs_request.headers.update(se.headers)
    systemTransfer_url = "https://icorepnbs.pingan.com.cn/icore_pnbs/do/usermanage/systemTransfer"
    systemTransfer_data = {
        "channelSourceCode": "G",
        "partnerWorkNetCode": "",
        "operablePartnerWorknetList": "210697215001",
        "agentCode": "10690047",
        "BrandDetailName": "",
        "umCode": "STDJNDS-00001",
        "businessSourceDetailCode": "3",
        "saleAgentName": "耿越",
        "transitSystemSource": "ICORE-PTS",
        "saleAgentCode": "2100003024",
        "cypherText": cypherText,
        "isUseCyberArk": "Y",
        "channelSourceDetailCode": "F",
        "dealerCodes": "",
        "userName": "圣泰达保险代理有限公司南京市江宁东山分公司",
        "businessCertificateNumText": "",
        "timestamp": timestamp,
        "transferId": "apply",
        "brokerCode": "",
        "dataSource": "ICORE-PTS",
        "departmentCode": "21069",
        "brandDetail": "",
        "businessSourceCode": "2",
        "agentSalerNameText": "",
        "relationQueryFlag": "Y",
        "departmentCodeList": "",
        "systemId": "ICORE-PTS",
        "partnerType": "0",
        "empBusinessCertificateNumText": ""
    }

    headers = se.headers
    headers['Referer'] = "https://icore-pts.pingan.com.cn/ebusiness/auto/newness/toibcswriter.do?transmitId=apply"
    headers['Content-Type'] = "application/x-www-form-urlencoded"
    headers['Cache-Control'] = "max-age=0"
    icorepnbs_request.post(
        url=systemTransfer_url,
        data=systemTransfer_data,
        headers=headers,
        verify=False
        # cookies=cookies
    )

    # 通过车牌号查询平安上次保单 如果存在保单 那么视为续保 即使不是续保 用户信息也可带出
    headers = se.headers
    headers[
        'Referer'] = "https://icorepnbs.pingan.com.cn/icore_pnbs/bussiness/quotationAndApply/templates/view/popup/quickSearch_result.html?r=0.05557662411592902"
    headers['Accept'] = "application/json, text/plain, */*"
    headers['Content-Type'] = "application/json;charset=UTF-8"
    quickSearch_url = "https://icorepnbs.pingan.com.cn/icore_pnbs/do/quote/quickSearch"
    # quickSearch_data='{"departmentCode":"21069","employeeCode":"2100003024","isLoanVehicle":"0","vehicleLicenceCode":"苏A-B5U69"}' A-HJ108
    quickSearch_data = {"departmentCode": "21069", "employeeCode": "2100003024", "isLoanVehicle": "0",
                        "vehicleLicenceCode": plateNumber}
    quickSearch_data = json.dumps(quickSearch_data)
    # quickSearch_resp=icorepnbs_request.post(url=quickSearch_url,data=quickSearch_data,headers=headers, verify=False,cookies={"BIGipServerICORE-PNBS_DMZ_PrdPool":"1462181036.42357.0000"})
    # cookies =requests.utils.cookiejar_from_dict(cookies, cookiejar=icorepnbs_request.cookies, overwrite=True)
    # icorepnbs_request.cookies=cookies
    quickSearch_resp = icorepnbs_request.post(url=quickSearch_url, data=quickSearch_data, headers=headers, verify=False)
    quickSearch_resp_text = quickSearch_resp.text
    if quickSearch_resp.url != u"https://icorepnbs.pingan.com.cn/icore_pnbs/do/quote/quickSearch":
        log.error(u"查询续保用户session超时")
        log.error(quickSearch_resp.text)
        log.error(u"车牌号%s", plateNumber)
        return icorepnbs_request
    elif len(quickSearch_resp_text) < 15:
        log.info(u"not pingan renewal user %s", plateNumber)
        return icorepnbs_request
    elif "applyPolicy" or "deptChineseName" or "deptChineseName" in quickSearch_resp_text:
        # print(quickSearch_resp_text)
        user_data = parse_renewal_data(quickSearch_resp.json())
        # log.info("user_data %s ",user_data)
        if user_data != 0:
            log.info(u"平安续保用户 %s", plateNumber)
            user_data['request'] = icorepnbs_request
            return user_data
        log.error("error reneawl.py line 108")
        return icorepnbs_request

    log.error(u"未知问题 unknown error %s", plateNumber)
    return icorepnbs_request


def quickSearchVoucher(session, dtrenewal):
    c51policyNo = dtrenewal.get("c51policyNo", "")
    c01PolicyNo = dtrenewal.get("c01policyNo", "")

    ownershipAttributeCode = dtrenewal.get('ownershipAttributeCode', "03")
    qick_url = "https://icorepnbs.pingan.com.cn/icore_pnbs/do/app/quotation/quickSearchVoucher"
    headers = se.headers
    headers[
        'Referer'] = "https://icorepnbs.pingan.com.cn/icore_pnbs/mainCtrl.tpl?applicantPersonFlag=1&familyPrd=&bsDetailCode=2-3-G-F&usageAttributeCode=02&ownershipAttributeCode=03&insuranceType=1&agentSalerName=&businessCertificateNum=&empBusinessCertificateNum=&deptCodeText=21069&secondLevelDepartmentCode=210&deptCode=21069&employeeCodeText=2100003024&employeeCode=2100003024&channelCode=G&agentCode=10690047&productCombineList=&partnerWorknetPanel=210697215001&worknetCode=&conferVal=1069004717001+1&agentNameLike=&agentCodeText=&brokerCode=&agentName=%E5%9C%A3%E6%B3%B0%E8%BE%BE%E4%BF%9D%E9%99%A9%E4%BB%A3%E7%90%86%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%E5%8D%97%E4%BA%AC%E5%B8%82%E6%B1%9F%E5%AE%81%E4%B8%9C%E5%B1%B1%E5%88%86%E5%85%AC%E5%8F%B8&conferNo=1069004717001&subConferNo=1&dealerCode=&autoInsurance=true&propertyInsurance=false&accidentInsurance=false&rateClassFlag=14&employeeName=%E8%80%BF%E8%B6%8A&saleGroupCode=21069000682&businessMode=&systemId=ICORE-PTS&applyApproach="
    body = {
        "departmentCode": "21069",
        "secondLevelDepartmentCode": "210",
        "saleAgentCode": "2100003024",
        "businessSourceCode": "2",
        "businessSourceDetailCode": "3",
        "channelSourceCode": "G",
        "channelSourceDetailCode": "F",
        "productCode": "",
        "bidFlag": "0",
        "planCode": "C01",
        "usageAttributeCode": "02",
        "ownershipAttributeCode": ownershipAttributeCode,
        "isSelectDriver": 0,
        "insuredNumber": 1,
        "loanVehicle": "0",
        "voucherType": "1",
        "isFromCNBS": "0",
        "nbaHotshot": "nbaHotshot",
        "c51PolicyNo": c51policyNo,
        "rateClassFlag": "14",
        "insuranceType": "1"
    }

    body2 = {
        "departmentCode": "21069",
        "secondLevelDepartmentCode": "210",
        "saleAgentCode": "2100003024",
        "businessSourceCode": "2",
        "businessSourceDetailCode": "3",
        "channelSourceCode": "G",
        "channelSourceDetailCode": "F",
        "productCode": "",
        "bidFlag": "0",
        "planCode": "C01",
        "usageAttributeCode": "02",
        "ownershipAttributeCode": ownershipAttributeCode,
        "isSelectDriver": 0,
        "insuredNumber": 1,
        "loanVehicle": "0",
        "voucherType": "1",
        "isFromCNBS": "0",
        "nbaHotshot": "nbaHotshot",
        "c01PolicyNo": c01PolicyNo,
        "rateClassFlag": "14",
        "insuranceType": "1"
    }
    body3 = {
        "departmentCode": "21069",
        "secondLevelDepartmentCode": "210",
        "saleAgentCode": "2100003024",
        "businessSourceCode": "2",
        "businessSourceDetailCode": "3",
        "channelSourceCode": "G",
        "channelSourceDetailCode": "F",
        "productCode": "",
        "bidFlag": "0",
        "planCode": "C01",
        "usageAttributeCode": "02",
        "ownershipAttributeCode": ownershipAttributeCode,
        "isSelectDriver": 0,
        "insuredNumber": 1,
        "loanVehicle": "0",
        "voucherType": "1",
        "isFromCNBS": "0",
        "nbaHotshot": "nbaHotshot",
        "c01PolicyNo": c01PolicyNo,
        "c51PolicyNo": c51policyNo,
        "rateClassFlag": "14",
        "insuranceType": "1"
    }
    if c51policyNo != "":
        body = json.dumps(body)
    if c01PolicyNo != "":
        body = json.dumps(body2)
    if c01PolicyNo != "" and c51policyNo != "":
        body = json.dumps(body3)

    qick_rsp = session.post(url=qick_url, data=body, headers=headers, verify=False)
    if "autoModelType" in qick_rsp.text:
        r_data = parse_user_data(qick_rsp.json())
        insuranceType = parse_lastyear_info(qick_rsp.json())
        r_data['request'] = session
        jq_totalAmount = dtrenewal.get('jq_totalAmount', "0")
        sy_totalAmount = dtrenewal.get('sy_totalAmount', "0")
        insuranceType['SySumPremium'] = sy_totalAmount
        insuranceType['JqSumPremium'] = jq_totalAmount
        r_data['insuranceType'] = insuranceType
        return r_data
    log.error("获取续保信息失败")
    return 0


def keep_session(sessionoop):
    try:
        toibcswriter_url = "https://icore-pts.pingan.com.cn/ebusiness/auto/newness/toibcswriter.do?transmitId=apply"
        headers = se.headers
        headers['Referer'] = "https://icore-pts.pingan.com.cn/ebusiness/frames/main_02.jsp"
        toibcswriter_resp = sessionoop.get(url=toibcswriter_url, headers=headers, verify=False)
        toibcswriter_body = toibcswriter_resp.text
        dt_toibcswriter = parse_toibcswriter(toibcswriter_body)
        cypherText = dt_toibcswriter['cypherText']
        timestamp = dt_toibcswriter['timestamp']
        log.info("session is alive")
    except Exception as e:
        log.error("session is death")
