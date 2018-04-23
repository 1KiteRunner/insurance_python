# -*- coding:utf-8 -*-
import ast
from request_cicc.data import postData as dataFac
from request_cicc.data import testData as SE
def getCarModel(session,modelName,chassisNo,motorNo,enrollDate,licenseNo):
    getCarModelData = dataFac.getCarModelData(modelName,chassisNo,motorNo,enrollDate,licenseNo)
    carModelRes = session.post(SE.carModel_url,data=getCarModelData)
    return carModelRes.content

def selectMinPriceModel(carModelRes):
    carModelRes = carModelRes.replace('null', '""')
    carModelRes = carModelRes.replace("'", '"')
    carModelResJson = ast.literal_eval(carModelRes)
    carModelItems = carModelResJson['result']['items']
    carPrice = 0
    minPriceIndex = 0
    curIndex = 0


    if len(carModelItems) > 0:
        for carModel in carModelItems:
            if carPrice > float(carModel['replacementValue']):
                carPrice = carModel['replacementValue']
                minPriceIndex = curIndex
            curIndex = ++curIndex
            return carModelItems[minPriceIndex]
            # print json.dumps(carModelItems[minPriceIndex],ensure_ascii=False,indent=4)
    else:
        return None
def postSelectCarModel(session,modelName,chassisNo,motorNo,enrollDate,licenseNo,carModel,jsCheckCode,codeStr,jsCheckNo):
    postSelectCarModelData = dataFac.getPostSelectCarModelData(modelName,chassisNo,motorNo,enrollDate,licenseNo,carModel,jsCheckCode,codeStr,jsCheckNo)
    VCodeRes = session.post(SE.postSelectModel_url,data=postSelectCarModelData).content
    VCodeRes = VCodeRes.replace('null', '""')
    VCodeRes = VCodeRes.replace("'", '"')
    return ast.literal_eval(VCodeRes)