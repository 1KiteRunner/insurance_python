# -*- coding:utf-8 -*-
import datetime as dtime
import ast
import re
from datetime import datetime
import traceback

import getCarModel
import calculatePost
import translate
from my_dbUtil.dbInsert import soupDb
from common.MqSend import send_mq
from  common.log import Logger

log=Logger()


def compare_date(str_date1, str_date2):
    str_date1 = str_date1.split(" ")[0]
    str_date2 = str_date2.split(" ")[0]
    str_date1 = datetime.strptime(str_date1, "%Y-%m-%d")
    str_date2 = datetime.strptime(str_date2, "%Y-%m-%d")
    if str_date1.date() >= str_date2.date():
        return str_date2.date()
    else:
        return str_date2.date()
def startCicc(loginRes,data):
    session = loginRes[0]
    userId = loginRes[1]
    modelName = data['vehicleBrand'].encode('utf-8')
    chassisNo = data['vinNo'].encode('utf-8')
    motorNo = data['engineNo'].encode('utf-8')
    enrollDate = data['firstRegister'].encode('utf-8')
    licenseNo = data['plateNumber'].encode('utf-8')
    driverName = data['custName'].encode('utf-8')
    driverIDNumber = data['identitCard'].encode('utf-8')
    INSURE_CAR_ID = data['insureCarId']
    client=data['client']
    sessionId=data['sessionId']
    isPhone=data['isPhone']
    insuranceType=data['insuranceType'] #保险组合类型
    groupId = insuranceType['insuranceTypeGroupId']
    insuranceTypeGroup=insuranceType['insuranceTypeGroup']
    carModelRes = getCarModel.getCarModel(session,modelName,chassisNo,motorNo,enrollDate,licenseNo)
    carModelRes = carModelRes.replace('null', '""')
    carModelRes = carModelRes.replace("'", '"')
    carModelResJson = ast.literal_eval(carModelRes)
    jsCheckCode = carModelResJson['result']['items'][0]['jsCheckCode']
    # codeStr = request_cicc.util.pic2Str(base64.b64decode(jsCheckCode))
    jsCheckNo = carModelResJson['result']['items'][0]['jsCheckNo']
    carModel = getCarModel.selectMinPriceModel(carModelRes)
    vcodeRes = getCarModel.postSelectCarModel(session,modelName,chassisNo,motorNo,enrollDate,licenseNo,carModel,jsCheckCode,"1111",jsCheckNo)
    log.info(u"大地 ,%s,第一次上报验证码完成" % licenseNo )
    # codeStr = request_cicc.util.pic2Str(base64.b64decode(vcodeRes['result']['jsCheckCode']))
    codeStr = "1111"
    try:
        enrollDate = vcodeRes['result']['jsEnrollDate']
    except:
        enrollDate = data['firstRegister'].encode('utf-8')
    log.info(enrollDate)
    endDate = data.get('preInsureEndDate','')
    priumeDic = calculatePost.calculatePremium(insuranceType,session,userId,driverName,driverIDNumber,licenseNo,chassisNo,motorNo,enrollDate,codeStr,modelName,carModel['replacementValue'],vcodeRes,endDate)
    log.info(u"大地 ,%s,第二次上报验证码完成" % licenseNo)
    result = priumeDic['result'][0]
    calculateErrMeg = result.get('insuranceApplication.calculateErrMeg',None)
    while calculateErrMeg is not None:
        endDate = ""
        if "车主名称与交管信息不一致" in calculateErrMeg:
            log.error(u"大地重复投保 %s ,返回信息 %s " % (licenseNo,calculateErrMeg))
            str2 = calculateErrMeg.split("：")
            str2 = str2[2].split(';')
            driverName =  str2[0]
        if "保单发生重复投保" in calculateErrMeg:
            str1 = "\d{4}-\d{2}-\d{2}"
            datelist = re.findall(str1, calculateErrMeg, re.S)
            log.error(u"大地重复投保 %s ,返回信息 %s " % (licenseNo,calculateErrMeg))
            if len(datelist) == 2:
                endDate = compare_date(datelist[0], datelist[1])
        priumeDic = calculatePost.calculatePremium(insuranceType,session, userId, driverName, driverIDNumber, licenseNo, chassisNo,motorNo, enrollDate, codeStr, modelName,carModel['replacementValue'], vcodeRes,endDate)
        result = priumeDic['result'][0]
        calculateErrMeg = result.get('insuranceApplication.calculateErrMeg', None)
        if calculateErrMeg is not None:
            if (not "车主名称与交管信息不一致" in calculateErrMeg) and  (not "保单发生重复投保" in calculateErrMeg):
                send_mq(client,licenseNo,"车主名称与交管信息不一致 or 保单发生重复投保 ","2","5",sessionId,isPhone,groupId,insuranceTypeGroup)
                log.error(u"%s %s" % (licenseNo,calculateErrMeg))
                break
    try:
        PremiumInfo = translate.getPriumeInf(priumeDic,vcodeRes['result']['seatCount'])
        send_mq(client,licenseNo,"","1","5",sessionId,isPhone,groupId,insuranceTypeGroup)
    except:
        print traceback.format_exc()
        out=priumeDic['result'][0].get('insuranceApplication.calculateErrMeg',"")
        send_mq(client,licenseNo,out,"2","5",sessionId,isPhone,groupId,insuranceTypeGroup)
        log.error(u"大地爬取失败 %s " % licenseNo)
        return out
    tomorrow = dtime.date.today() + dtime.timedelta(1)
    startDate = tomorrow.strftime("%Y-%m-%d")
    endDate =str(tomorrow.year + 1) + '-' + str(tomorrow.month) + '-' + str(tomorrow.day)
    data=[startDate,endDate,vcodeRes['result']['seatCount'],groupId,INSURE_CAR_ID,"5"]
    #data=[开始时间,结束时间，座位数，组合id，车辆id，公司id]
    soupDb(PremiumInfo,data)
    log.info(u"大地入库成功 %s " % licenseNo)



# if __name__=="__main__":
#     startCicc()