# -*- coding:utf-8 -*-
from request_cicc.data import postData as dataFac
from request_cicc.data import testData as SE
def calculatePremium(insuranceType,session,userId,driverName,driverIDNumber,licenseNo,chassisNo,motorNo,enrollDate,codeStr,modelName,price,vcodeRes,endDate=""):
    session.headers.update({"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})
    calculatePriumeData = dataFac.getCalculatePriumeData(insuranceType,userId,driverName,driverIDNumber,licenseNo,chassisNo,motorNo,enrollDate,codeStr,modelName,price,vcodeRes,endDate)
    priumeRes = session.post(SE.calculate_url,data=calculatePriumeData)
    return eval(priumeRes.content.replace("'",'"').replace("null",'" "'))
