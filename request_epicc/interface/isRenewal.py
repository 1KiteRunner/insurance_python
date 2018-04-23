# -*- coding:utf-8 -*-
__author__ = 'weikai'
import urllib
import ast
import json

import  requests

import reqStep2
from  request_epicc import settings as se
from common.log import  Logger
from carInput1_1 import carInput1_1
from newuser import new_user

#判断用户是老用户还是新用户
#{"resultCode":"1","resultMsg":"可续保","studentNo":0}
#{"resultCode":"3","resultMsg":"不可续保","studentNo":0}
# {"insuredPhNo":"18251867797","EngineNo":"1405110930","VEHICLE_MODELSH":"哈弗牌CC6460RM01","insuredIDNumber":"320125198711304822","carddate":"2014-12-29","address":"溧水区永阳镇中山东路290号1栋4号","insuredName":"王秋兰","LicenseNo":"苏AQ6C06","regisdate":"2014-12-29","FrameNo":"LGWEF4A56EF280301"}
log=Logger()
def isRenewal2(ununse,userInfo):

    cityCodeLast = citySelected = userInfo['cityCode']
    IDnumber = insuredIdentifyNumber = userInfo['identitCard']
    carOwner = str(userInfo['custName'])
    licenseNo = licenseno = str(userInfo['plateNumber'])
    frameNo = userInfo['vinNo']
    engineNo = userInfo['engineNo']
    insureCarId=userInfo['insureCarId']
    areaCodeLast = proSelected = citySelected[0:2] + '000000'

    # proSelected, citySelected, areaCodeLast, cityCodeLast, insuredIdentifyNumber, carOwner, licenseno, frameNo, engineNo
    headers=se.headers
    sessionId = carInput1_1(citySelected,proSelected)
    headers['Referer']='http://www.epicc.com.cn/wap/carProposal/car/carInput1'
    #城市编码 车牌号 sessionId

    checkIsNewData='channelNo=2&citySelected='+citySelected+'&licenseNo='+urllib.quote(licenseNo)+'&ccaFlag=&sessionId=' + sessionId
    re=requests.post(url=se.isRenewal_url,data=checkIsNewData,headers=headers)
    body = re.json()
    log.info(u'body[\'resultMsg\'] = %s : '% body['resultMsg'])

    if body['resultMsg']==u'不可续保':
        log.info(u'用户数据:'+checkIsNewData+u'...不可续保')
        checkIsReuseData = 'channelNo=2&citySelected='+citySelected+'&licenseNo='+urllib.quote(licenseNo)+'&ccaFlag=&sessionId=' + sessionId
        re = requests.post(url=se.carDataReuse_url, data=checkIsReuseData, headers=headers)
        if eval(re.json()['message'])['resultCode']=='1':
            data = 'proSelected=' + proSelected + '&citySelected=' + citySelected + '&beforeProposalNo=' + IDnumber + '&licenseNo=' + urllib.quote(licenseNo) + '&sessionId=' + sessionId
            res = requests.post(url=se.query_carData_url, headers=headers, data=data)
            body = ast.literal_eval(res.json()['message'])
            if body['common']['resultCode'] == '2':
                new_user(sessionId, proSelected, citySelected, areaCodeLast, cityCodeLast, insuredIdentifyNumber,carOwner, licenseno, frameNo, engineNo,insureCarId)
            elif body['common']['resultCode'] == '0':
                new_user(sessionId, proSelected, citySelected, areaCodeLast, cityCodeLast, insuredIdentifyNumber,
                         carOwner, licenseno, frameNo, engineNo, insureCarId)
            else:
                reqStep2.step2_2(sessionId,licenseNo,IDnumber,proSelected,citySelected,body,insureCarId)
        else:
            new_user(sessionId,proSelected,citySelected,areaCodeLast,cityCodeLast,insuredIdentifyNumber,carOwner,licenseno,frameNo,engineNo,insureCarId)

    elif body['resultMsg']==u'可以续保':
        log.info(u'用户数据:'+checkIsNewData+u'...可以续保')
        data = {
            'licenseNo': licenseNo,
            'sessionId': sessionId,
            'proSelected': proSelected,
            'beforeProposalNo': IDnumber,
            'citySelected': citySelected
        }
        data = urllib.urlencode(data)
        res = requests.post(url=se.queryRenewal_url, headers=headers, data=data)
        body = res.json()
        body = json.dumps(body, ensure_ascii=False, indent=4)
        try:
            ast.literal_eval(body)['appliCarInfo']
            reqStep2.step2_1(sessionId, licenseNo, IDnumber, proSelected, citySelected,body,insureCarId)
        except:
            new_user(sessionId, proSelected, citySelected, areaCodeLast, cityCodeLast, insuredIdentifyNumber, carOwner,licenseno, frameNo, engineNo,insureCarId)
    else:
        log.info(u'用户数据:'+checkIsNewData+u'状态未知')
        return u'状态未知'
