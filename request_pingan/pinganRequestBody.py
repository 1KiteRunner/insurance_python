# -*- coding:utf-8 -*-
__author__ = 'weikai'
import sys
import json,traceback
from request_pingan.pingan_feebody import get_fee
from common.MqSend import send_mq
from request_cic.login import *
import request_pingan.settings as se
from request_pingan.parse import parse_toibcswriter
from common.log import Logger
from my_dbUtil.dbInsert import soupDb
from common.redisUtil import CRedis

log = Logger()

reload(sys)
sys.setdefaultencoding('utf8')
global null, false, true
null = None
false = False
true = True


def get_pingan_redis_body(sessionoop, dtjson):
    try:
        searchVin = dtjson.get("vinNo", "")
        if searchVin == "":
            return 0
        r = CRedis()
        alldata = r.get_vin(searchVin, "1")
        if alldata is None:
            return 0
        # 发送请求 切换域名session
        log.info(u"从redis中查询出信息")
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
        )

        insuranceType = dtjson.get("insuranceType", {})
        insuranceTypeGroupId = insuranceType.get("insuranceTypeGroupId", "")
        insuranceTypeGroup = insuranceType.get("insuranceTypeGroup", "")
        insureCarId = dtjson['insureCarId']
        CPlateNo = dtjson.get("plateNumber", "")
        client = dtjson['client']
        sessionId = dtjson['sessionId']
        isPhone = dtjson['isPhone']

        alldata = eval(alldata)
        alldata['insuranceType'] = insuranceType
        fee_resp = get_fee(icorepnbs_request, alldata)
        if isinstance(fee_resp, dict):
            data = []
            data.append(fee_resp['c01beginTime'])
            data.append(fee_resp['c01endTime'])
            data.append(fee_resp['vehicleSeats'])
            data.append(insuranceTypeGroupId)
            data.append(insureCarId)
            data.append("1")
            log.info("平安开始入库 %s", CPlateNo)
            soupDb(fee_resp['fee'], data)
            log.info("平安入库成功 %s ", CPlateNo)
            send_mq(client, CPlateNo, "", "1", "1", sessionId, isPhone, insuranceTypeGroupId, insuranceTypeGroup)
            return 1

        if isinstance(fee_resp, list):
            fee_resp = json.dumps(fee_resp, encoding=False)
            log.error(fee_resp)
            return 0

        log.error(fee_resp)
        # send_mq(client,CPlateNo,fee_resp,"2","1",sessionId,isPhone,insuranceTypeGroupId,insuranceTypeGroup)
        return 0
    except Exception as e:
        log.error(traceback.format_exc())
        log.error(e)
        return 0
