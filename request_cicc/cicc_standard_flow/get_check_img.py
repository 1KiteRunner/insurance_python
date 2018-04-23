# -*- coding:utf-8 -*-
#通过车架号获取车管所信息并获取验证码请求
global null, false, true
null = None
false = False
true = True
import traceback

from common.log import Logger

log=Logger()

def get_check_img(dt):
    req_session = dt['req_session']
    chassisNo = dt['vinNo']
    enrollDate = dt['enrollDate']
    licenseType = dt['licenseType']
    vehicleCategory = dt['vehicleCategory']
    ecdemicVehicle = dt['ecdemicVehicle']
    salesChannelCode = dt['salesChannelCode']
    cacheableFlag = dt['cacheableFlag']
    searchTag = dt['searchTag']
    url = "http://b2b.ccic-net.com.cn/mss/view/vehicleInsurance/accurateQuotation/vehicleInfoQuery.jsp"
    req_data = {
        "currentPageIndex":"1",
        "pageSize": "8",
        "autoload": "true",
        "modelName": "",
        "chassisNo": chassisNo,
        "motorNo": "",
        "enrollDate": enrollDate,
        "checkCode": "",
        "jsCheckCode": "",
        "jsCheckNo": "",
        "licenseNo": "",
        "licenseType": licenseType,
        "vehicleCategory": vehicleCategory,
        "ecdemicVehicle": ecdemicVehicle,
        "orgCode": "",
        "salesChannelCode": salesChannelCode,
        "vehicleStyleDesc": "",
        "cacheableFlag": '0',
        'searchTag': searchTag,
        "_action": "queryVehicleConfigurationAction"
    }
    try:
        DVM_res = req_session.post(url,data=req_data).content
    except:
        log.error(traceback.format_exc())
        log.error("网络异常")
    return eval(DVM_res)
