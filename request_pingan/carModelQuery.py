# -*- coding:utf-8 -*-
__author__ = 'weikai'
import json
import request_pingan.settings as se
from common.log import Logger

log = Logger()


def query_carmodel(session, vehicleFrameNo, departmentCode="21069"):
    '''
    通过车架号获取车辆信息
    :param session:request对象
    :param vehicleFrameNo:车架号
    :param departmentCode:部门编号 默认21069
    :return:返回车辆信息
    '''
    QUERY_URL = "https://icorepnbs.pingan.com.cn/icore_pnbs/do/app/quotation/autoModelCodeQuery"
    headers = se.headers

    headers[
        'Referer'] = "https://icorepnbs.pingan.com.cn/icore_pnbs/mainCtrl.tpl?applicantPersonFlag=1&familyPrd=&bsDetailCode=2-3-G-F&usageAttributeCode=02&ownershipAttributeCode=03&insuranceType=1&agentSalerName=&businessCertificateNum=&empBusinessCertificateNum=&deptCodeText=21069&secondLevelDepartmentCode=210&deptCode=21069&employeeCodeText=2100003024&employeeCode=2100003024&channelCode=G&agentCode=10690047&productCombineList=&partnerWorknetPanel=210697215001&worknetCode=&conferVal=1069004717001+1&agentNameLike=&agentCodeText=&brokerCode=&agentName=%E5%9C%A3%E6%B3%B0%E8%BE%BE%E4%BF%9D%E9%99%A9%E4%BB%A3%E7%90%86%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%E5%8D%97%E4%BA%AC%E5%B8%82%E6%B1%9F%E5%AE%81%E4%B8%9C%E5%B1%B1%E5%88%86%E5%85%AC%E5%8F%B8&conferNo=1069004717001&subConferNo=1&dealerCode=&autoInsurance=true&propertyInsurance=false&accidentInsurance=false&rateClassFlag=14&employeeName=%E8%80%BF%E8%B6%8A&saleGroupCode=21069000682&businessMode=&systemId=ICORE-PTS&applyApproach="
    headers['Content-Type'] = "application/json;charset=UTF-8"
    body = {
        "vehicleFrameNo": vehicleFrameNo,
        "departmentCode": departmentCode,
        "insuranceType": "1"}
    body = json.dumps(body)
    QUERY_RSP = session.post(
        url=QUERY_URL,
        data=body,
        headers=headers,
        verify=False)
    if len(QUERY_RSP.text) > 20:
        QUERY_RSP_JSON = QUERY_RSP.json()['encodeDict']
        QUERY_RSP_JSON.sort(key=lambda obj: obj.get('displayPrice'))
        return QUERY_RSP_JSON[0]

    log.error(u"未查询到车辆信息autoModelCodeQuery %s ", vehicleFrameNo)
    return 0


def c51DiscountTax(session, autoModelCode, departmentCode="21069"):
    '''
    :param session: request对象
    :param autoModelCode: 车辆型号
    :return:
    '''
    c51DiscountTax_url = "https://icorepnbs.pingan.com.cn/icore_pnbs/do/app/quotation/c51DiscountTax"
    headers = se.headers
    headers['Content-Type'] = "application/json;charset=UTF-8"
    headers[
        'Referer'] = "https://icorepnbs.pingan.com.cn/icore_pnbs/mainCtrl.tpl?applicantPersonFlag=1&familyPrd=&bsDetailCode=2-3-G-F&usageAttributeCode=02&ownershipAttributeCode=03&insuranceType=1&agentSalerName=&businessCertificateNum=&empBusinessCertificateNum=&deptCodeText=21069&secondLevelDepartmentCode=210&deptCode=21069&employeeCodeText=2100003024&employeeCode=2100003024&channelCode=G&agentCode=10690047&productCombineList=&partnerWorknetPanel=210697215001&worknetCode=&conferVal=1069004717001+1&agentNameLike=&agentCodeText=&brokerCode=&agentName=%E5%9C%A3%E6%B3%B0%E8%BE%BE%E4%BF%9D%E9%99%A9%E4%BB%A3%E7%90%86%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%E5%8D%97%E4%BA%AC%E5%B8%82%E6%B1%9F%E5%AE%81%E4%B8%9C%E5%B1%B1%E5%88%86%E5%85%AC%E5%8F%B8&conferNo=1069004717001&subConferNo=1&dealerCode=&autoInsurance=true&propertyInsurance=false&accidentInsurance=false&rateClassFlag=14&employeeName=%E8%80%BF%E8%B6%8A&saleGroupCode=21069000682&businessMode=&systemId=ICORE-PTS&applyApproach="
    body = {"departmentCode": departmentCode, "autoModelCode": autoModelCode}
    body = json.dumps(body)
    c51DiscountTax_rsp = session.post(
        url=c51DiscountTax_url,
        data=body,
        headers=headers,
        verify=False)
    return c51DiscountTax_rsp


# 如果车架号查询不出车辆信息 通过交管所返回的车辆型号进行查询
def queryAutoModelType(session, brandPara="LZ6500BQ9LE"):
    QUERY_URL = "https://icorepnbs.pingan.com.cn/icore_pnbs/do/app/quotation/queryAutoModelType"
    headers = se.headers

    headers[
        'Referer'] = "https://icorepnbs.pingan.com.cn/icore_pnbs/mainCtrl.tpl?applicantPersonFlag=1&familyPrd=&bsDetailCode=2-3-G-F&usageAttributeCode=02&ownershipAttributeCode=03&insuranceType=1&agentSalerName=&businessCertificateNum=&empBusinessCertificateNum=&deptCodeText=21069&secondLevelDepartmentCode=210&deptCode=21069&employeeCodeText=2100003024&employeeCode=2100003024&channelCode=G&agentCode=10690047&productCombineList=&partnerWorknetPanel=210697215001&worknetCode=&conferVal=1069004717001+1&agentNameLike=&agentCodeText=&brokerCode=&agentName=%E5%9C%A3%E6%B3%B0%E8%BE%BE%E4%BF%9D%E9%99%A9%E4%BB%A3%E7%90%86%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%E5%8D%97%E4%BA%AC%E5%B8%82%E6%B1%9F%E5%AE%81%E4%B8%9C%E5%B1%B1%E5%88%86%E5%85%AC%E5%8F%B8&conferNo=1069004717001&subConferNo=1&dealerCode=&autoInsurance=true&propertyInsurance=false&accidentInsurance=false&rateClassFlag=14&employeeName=%E8%80%BF%E8%B6%8A&saleGroupCode=21069000682&businessMode=&systemId=ICORE-PTS&applyApproach="
    headers['Content-Type'] = "application/json;charset=UTF-8"
    body = {
        "brandPara": brandPara,
        "departmentCode": "21069",
        "insuranceType": "1",
        "rateClassFlag": "14"}
    body = json.dumps(body)
    QUERY_RSP = session.post(
        url=QUERY_URL,
        data=body,
        headers=headers,
        verify=False)
    if len(QUERY_RSP.text) > 20 and QUERY_RSP.status_code == 200:
        QUERY_RSP_JSON = QUERY_RSP.json()['data']['encodeDict']
        QUERY_RSP_JSON.sort(key=lambda obj: obj.get('displayPrice'))
        return QUERY_RSP_JSON[0]

    log.error(u"未查询到车辆信息autoModelCodeQuery %s ", brandPara)
    return 0
