# -*- coding:utf-8 -*-
import requests
from common.dama.damaUtil import dama
from request_cicc.data import testData as SE
import request_cicc.util
from request_cicc.data import postData as dataFac
from bs4 import BeautifulSoup
from common.sessionUtil import set_session
import base64
def login():
    session = requests.session()
    session.get(SE.index_url)
    res = session.get(SE.login_vcode_url)
    codestr = request_cicc.util.pic2Str(res.content)
    #codestr=dama("2",base64.encodestring(res.content))
    login_data = dataFac.init_loginData()
    login_data['j_captcha'] = codestr
    result = session.post(SE.login_url,data=login_data)
    resultStr = result.content
    while u'验证码错误' in unicode(resultStr,'utf-8'):
        res = session.get(SE.login_vcode_url)
        codestr = request_cicc.util.pic2Str(res.content)
        login_data['j_captcha'] = codestr
        result = session.post(SE.login_url, data=login_data)
        resultStr = result.content
    soup = BeautifulSoup(resultStr, "html.parser")
    userId = soup.find(id='userCode').get('value')
    allsession=[session,userId]
    #往redis中插入session
    set_session(allsession,"5")
    return allsession

if __name__ == '__main__':
    loginRes = login()
#     session = loginRes[0]
#     userId = loginRes[1]
#     carModelRes = getCarModel.getCarModel(session,SE.modelName,SE.chassisNo,SE.motorNo,SE.enrollDate,SE.licenseNo)
#     carModel = getCarModel.selectMinPriceModel(carModelRes)
#     vcodeRes = getCarModel.postSelectCarModel(session,SE.modelName,SE.chassisNo,SE.motorNo,SE.enrollDate,SE.licenseNo,carModel)
#     codeStr = request_cicc.util.pic2Str(base64.b64decode(vcodeRes['result']['jsCheckCode']))
#     priumeDic = calculatePost.calculatePremium(session,userId,SE.driverName,SE.driverIDNumber,SE.licenseNo,SE.chassisNo,SE.motorNo,SE.enrollDate,codeStr,SE.modelName,carModel['replacementValue'],vcodeRes)
#     PremiumInfo = translate.getPriumeInf(priumeDic,vcodeRes['result']['seatCount'])
#     tomorrow = datetime.date.today() + datetime.timedelta(1)
#     startDate = str(tomorrow)
#     endDate =str(tomorrow.year + 1) + '-' + str(tomorrow.month) + '-' + str(tomorrow.day)
#     data=[SE.licenseNo,SE.chassisNo,startDate,endDate,vcodeRes['result']['seatCount']]
#     dbInsert.soupDb(PremiumInfo,data)
    # print json.dumps(carModel, ensure_ascii=False, indent=4)

