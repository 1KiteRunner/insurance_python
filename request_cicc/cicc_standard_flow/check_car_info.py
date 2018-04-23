# -*- coding:utf-8 -*-
global null, false, true
null = None
false = False
true = True
import traceback

from common.log import Logger

log=Logger()
def check_car_info(dt):
    req_session = dt['req_session']
    licenseType = dt['licenseType']
    accurateNewMark = dt['accurateNewMark']
    pageSize = dt['pageSize']
    newinsurancecreatedate = dt['newinsurancecreatedate']
    specialModelFlag = dt['specialModelFlag']
    enrollDate = dt['enrollDate']
    newcarKindCode = dt['newcarKindCode']
    businessNewNature = dt['businessNewNature']
    salesChannelCode = dt['salesChannelCode']
    checkCode = dt['checkAnswer']
    cacheableFlag = dt['cacheableFlag']
    newuseNatureCode = dt['newuseNatureCode']
    autoload = dt['autoload']
    jsCheckNo = dt['jsCheckNo']
    vehicleCategory = dt['vehicleCategory']
    zdNature = dt['zdNature']
    currentPageIndex = dt['currentPageIndex']
    jsCheckCode = dt['jsCheckCode']
    ecdemicVehicle = dt['ecdemicVehicle']
    modelCode = dt['modelCode']
    chassisNo = dt['vinNo']
    searchTag = dt['searchTag']
    url = "http://b2b.ccic-net.com.cn/mss/view/vehicleInsurance/accurateQuotation/vehicleInfoQuery.jsp"
    req_data = {
        'modelName':dt.get('gCIndustryModelName',''),
        'chassisNo': chassisNo,
        'motorNo': '',
        'enrollDate': enrollDate,
        'checkCode': checkCode,
        'jsCheckCode': jsCheckCode,
        'jsCheckNo': jsCheckNo,
        'licenseNo': '',
        'licenseType': licenseType,
        'vehicleCategory': vehicleCategory,
        'ecdemicVehicle': ecdemicVehicle,
        'orgCode': '',
        'salesChannelCode': salesChannelCode,
        'vehicleStyleDesc': '',
        'cacheableFlag': cacheableFlag,
        'autoload': autoload,
        'currentPageIndex': currentPageIndex,
        'pageSize': pageSize,
        'modelCode': modelCode,
        'vehicleId': '',
        'newinsurancecreatedate': newinsurancecreatedate,
        'zdNature': zdNature,
        'zdUnitType': '',
        'newcarKindCode': newcarKindCode,
        'newuseNatureCode': newuseNatureCode,
        'accurateNewMark': accurateNewMark,
        'businessNewNature': businessNewNature,
        'specialModelFlag': specialModelFlag,
        'shCertificateDate': '',
        'searchTag':searchTag,
        '_action': 'saveVehicleModel'
    }
    try:
        res = req_session.post(url, data=req_data).content
    except:
        log.error(traceback.format_exc())
        log.error("网络异常")
    return eval(res)

