# -*- coding:utf-8 -*-
import traceback

from common.log import Logger

log=Logger()
global null, false, true
null = None
false = False
true = True
def post_checkAnswer(dt):
    currentPageIndex = dt['currentPageIndex']
    pageSize = dt['pageSize']
    autoload = dt['autoload']
    chassisNo = dt['vinNo']
    enrollDate = dt['enrollDate']
    checkCode = dt['checkAnswer']
    jsCheckCode = dt['jsCheckCode']
    jsCheckNo = dt['jsCheckNo']
    licenseType = dt['licenseType']
    vehicleCategory = dt['vehicleCategory']
    ecdemicVehicle = dt['ecdemicVehicle']
    salesChannelCode = dt['salesChannelCode']
    cacheableFlag = dt['cacheableFlag']
    req_session = dt['req_session']
    searchTag = dt['searchTag']
    url = "http://b2b.ccic-net.com.cn/mss/view/vehicleInsurance/accurateQuotation/vehicleInfoQuery.jsp"
    req_data={
        "currentPageIndex":currentPageIndex,
        "pageSize": pageSize,
        "autoload": autoload,
        "modelName": dt.get('gCIndustryModelName',''),
        "chassisNo": chassisNo,
        "motorNo": "",
        "enrollDate": enrollDate,
        "checkCode": checkCode,
        "jsCheckCode": jsCheckCode,
        "jsCheckNo": jsCheckNo,
        "licenseNo": "",
        "licenseType": licenseType,
        "vehicleCategory": vehicleCategory,
        "ecdemicVehicle": ecdemicVehicle,
        "orgCode": "",
        "salesChannelCode": salesChannelCode,
        "vehicleStyleDesc": "",
        "cacheableFlag": cacheableFlag,
        'searchTag' :searchTag,
        "_action": "queryVehicleConfigurationAction"
    }
    try:
        res = req_session.post(url,data = req_data).content
    except:
        log.error(traceback.format_exc())
        log.error("网络异常")
    return eval(res)