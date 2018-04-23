# -*- coding:utf-8 -*-
__author__ = 'weikai'
import sys

import  requests

reload(sys)
sys.setdefaultencoding('utf-8')
import json
import re
from  request_epicc import settings as se
from common.log import  Logger
from carInput1_1 import carInput1_1
from  JqEpicc import get_jq_epicc
from request_epicc import utils
import urllib
import translateJsonToPremiun
import jsonpath
import traceback
from obtainVerificationCode import  getobtainVerificationCode
import dbInsert

#requests = requests.session()
log=Logger()
headers=se.headers
def new_user(sessionid,proSelected,citySelected,areaCodeLast,cityCodeLast,insuredIdentifyNumber,carOwner,licenseno,frameNo,engineNo,insureCarId):
    try:
        #sessionid= carInput1_1()
        Mobile='13888888888'
        Email='2222222@qq.com'
        #proSelected='32000000'
        #citySelected='32010000'
        #areaCodeLast='32000000'
        #cityCodeLast='32010000'
        #insuredIdentifyNumber='320322198801026557'
        #carOwner='魏凯'
        #车牌号|车架号|发动机号
        #licenseno='苏A44444'
        #frameNo='LVZA43F93EC554224'
        #engineNo='14096911'
        #licenseno='苏AB1P05'
        #frameNo='LBELMBKC0EY555590'
        #engineNo='EW606024'
        if insuredIdentifyNumber=="":
            insuredIdentifyNumber="320324196302144552"
        insuredBirthday=utils.getbirthday(insuredIdentifyNumber)

        sex=utils.getgender(insuredIdentifyNumber)
        transferdate=utils.getnowdate()

        headers['Referer']='http://www.epicc.com.cn/wap/carProposal/car/carInput1'

        log.info(u"请求=================================http://www.epicc.com.cn/wap/carProposal/car/interim============================开始")
        interimurl='http://www.epicc.com.cn/wap/carProposal/car/interim'
        headers['Referer']='http://www.epicc.com.cn/wap/carProposal/car/carInput1'
        interimbydoy={
            "haveLoan": "",
            "licenseno": licenseno,
            "bjfuel_type": "",
            "deliverInfoCity": "",
            "insuredMobile": Mobile,
            "insuredAndOwnerrelate": "",
            "carKindCI": "",
            "deliverInfoPro": "",
            "invoiceTitle": "",
            "beforeProposalNo": "",
            "LoanName": "",
            "transferdate": transferdate,
            "certificate_no": "",
            "aliasName": "",
            "proSelected": proSelected,
            "argueSolution": "",
            "guohuselect": "",
            "frameno": "",
            "endhour": "",
            "vinno": "",
            "endHourCI": "",
            "citySelected": citySelected,
            "carKindSX": "",
            "deliverInfoDistrict": "",
            "areaCodeLast": areaCodeLast,
            "enrolldate": "",
            "certificate_type": "",
            "seatcount": "",
            "licenseflag": "1",
            "insuredIdentifSex": "1",
            "appliPhoneNumber": "",
            "travelMilesvalue": "",
            "appliEmail": Email,
            "insuredIdentifyType": "01",
            "isRenewal": "0",
            "monopolyname": "",
            "enddate": "",
            "insuredIdentifyAddr": "",
            "fullAmountName": "",
            "arbitboardname": "",
            "linkAddress": "",
            "endDateCI": "",
            "assignDriver": "",
            "startHourCI": "",
            "carIdentifyAddressSX": "",
            "appliAddName": "",
            "engineno": "",
            "weiFaName": "",
            "taxPayerIdentType": "",
            "carDrivers": "",
            "appliIdentifyType": "01",
            "cityCodeLast": cityCodeLast,
            "interimNo": "",
            "insuredBirthday": insuredBirthday,
            "standardName": "",
            "itemKindFlag": "1",
            "runAreaCodeName": "",
            "certificate_date": "",
            "mobileflag": "1",
            "taxPayerIdentNo": "",
            "lastcarownername": "",
            "appliIdentifyNumber": insuredIdentifyNumber,
            "startdate": "",
            "carOwner": carOwner,
            "certificatedate": "",
            "ccaId": "",
            "appliMobile": Mobile,
            "sessionId": sessionid,
            "startDateCI": "",
            "insuredEmail": Email,
            "taxPayerName": "",
            "insuredIdentifyNumber": insuredIdentifyNumber,
            "carOwerIdentifyType": "",
            "carNameSX": "",
            "appliName": carOwner,
            "starthour": ""
        }
        interimdata=urllib.urlencode(interimbydoy)
        interim_reponse=requests.post(interimurl,data=interimdata,headers=headers)
        interim_reponse = interim_reponse.json()
        #print type(interim_reponse)
        #interimNo=interim_reponse['interimNo']
        interimNo=interim_reponse.get("interimNo","")
        log.info(u'interim_reponse====:%s:' % interim_reponse)
        log.info(u'interimNo====:%s:' % interimNo)
        log.info(u"请求=================================http://www.epicc.com.cn/wap/carProposal/car/interim============================结束")

        #######################################
        #请求验证码并且发送返回字符串验证码
        log.info(u"请求车管所验证码=====http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerificationCode============================开始")
        codestr=getobtainVerificationCode(licenseno,sessionid,frameNo)
        log.info(u"请求车管所验证码=====http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerificationCode============================结束")
        ######################################
        log.info(u"发送验证码=====http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerifQueryCar============================开始")

        #发送验证码
        #{"body":{"trafficControlDockingQueryCarResBodyCar":[]},"head":{"checkStr":"","errorCode":"93037","errorMsg":"录入的校验码有误","requestCode":"","requestType":"","sessionId":"60150209-6827-41d7-a99d-cd775b0d830a","uuid":"d2ed2e76-b6ef-4d98-bec5-b8cfb1c582f0"}}

        obtainVerifQueryCarbody='icationCode='+codestr+'&channelNo=2&sessionId='+sessionid

        obtainVerifQueryCarresponse=requests.post(url='http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerifQueryCar',headers=headers,data=obtainVerifQueryCarbody)
        obtainVerifQueryCarresponse=obtainVerifQueryCarresponse.json()
        #print type(obtainVerifQueryCarresponse)
        #print(obtainVerifQueryCarresponse)

        code = eval(obtainVerifQueryCarresponse['message'])['head']['errorCode']
        count=1
        while code=='93037' and count < 5:
                codestr=getobtainVerificationCode(licenseno,sessionid,frameNo)
                obtainVerifQueryCarbody='icationCode='+codestr+'&channelNo=2&sessionId='+sessionid
                obtainVerifQueryCarresponse=requests.post(url='http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerifQueryCar',headers=headers,data=obtainVerifQueryCarbody)
                obtainVerifQueryCarresponse=obtainVerifQueryCarresponse.json()
                code=eval(obtainVerifQueryCarresponse['message'])['head']['errorCode']
                count=count+1

        #print obtainVerifQueryCarresponse
        #拿到返回消息 注册时间vehicle_register_date (2014-12-3000:00:00) 时间最后几个00 去掉限坐人数+1 是座位数limit_load_person
        #print(obtainVerifQueryCarresponse['message'])

        #限坐人数+1=座位数
        obtainVerifQueryCarresponsedict=eval(obtainVerifQueryCarresponse['message'])
        limit_load_person=obtainVerifQueryCarresponsedict['body']['trafficControlDockingQueryCarResBodyCar'][0]['limit_load_person']
        #获取车辆类型所使用的quercode
        vehicle_model=obtainVerifQueryCarresponsedict['body']['trafficControlDockingQueryCarResBodyCar'][0]['vehicle_model']
        #登记日期
        vehicle_register_date=(obtainVerifQueryCarresponsedict['body']['trafficControlDockingQueryCarResBodyCar'][0]['vehicle_register_date']).replace('00:00:00',"")

        log.info('limit_load_person=%s' %limit_load_person)
        log.info('vehicle_model=%s' %vehicle_model)
        log.info('vehicle_register_date=%s' %vehicle_register_date)

        log.info(u"发送验证码=====http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerifQueryCar============================结束")

        ####################################
        log.info(u"获取车子类型=====http://www.epicc.com.cn/wap/carProposal/carSelect/vehicleFind============================开始")
        vehicleFindurl = 'http://www.epicc.com.cn/wap/carProposal/carSelect/vehicleFind'
        #queryCode='DXK6440AF3'
        vehicleFindbody={
            "frameNo": frameNo,
            "queryCode": vehicle_model,
            "vinNo": frameNo,
            "citySelected": citySelected,
            "licenseNo": licenseno,
            "channelNo": "2",
            "enrollDate": vehicle_register_date,
            "isRenewal": "0",
            "sessionId": sessionid,
            "engineNo": engineNo,
            "licenseFlag": "1",
            "proSelected": proSelected
        }
        vehicleFinddata=urllib.urlencode(vehicleFindbody)
        vehicleFind_reponse=requests.post(vehicleFindurl,data=vehicleFinddata,headers=headers)
        #vehicleFindm_reponse = vehicleFind_reponse.json()
        #print type(vehicleFind_reponse)
        vehicleFind_reponse=vehicleFind_reponse.json()
        vehicleFindm_body=json.dumps(vehicleFind_reponse,ensure_ascii=False)
        #vehicleFindm_body=eval(vehicleFind_reponse)

        vehicleFindm_body='{"content":'+vehicleFindm_body+'}'
        #log.info(u'vehicleFindm_body====:%s:' % vehicleFindm_body)
        vehicleFindm_body=eval(vehicleFindm_body)
        interimNoList=jsonpath.jsonpath(vehicleFindm_body,'$.content[*]')
        #print(interimNoList)
        #print(type(interimNoList))
        seat=''
        for i in interimNoList:
            if vehicle_model==i['vehicleFgwCode'] or i['seat']==str(limit_load_person+1) :
                seat=i['seat']
                parentId=i['parentId']
                log.info('seat=%s'%seat)
                log.info('parentId=%s'%parentId)
                break
        log.info(u"获取车子类型=====http://www.epicc.com.cn/wap/carProposal/carSelect/vehicleFind============================结束")
        #########################################################################
        log.info(u"vehicleChecked=====http://www.epicc.com.cn/wap/carProposal/carSelect/vehicleChecked=============开始")
        vehicleCheckedurl='http://www.epicc.com.cn/wap/carProposal/carSelect/vehicleChecked'
        headers['Referer']='http://www.epicc.com.cn/wap/carProposal/car/carInput2'
        vehicleCheckeddata={
            "carModel": vehicle_model,
            "queryCode": vehicle_model,#BDFIXLUC0016
            "vinNo": frameNo,
            "citySelected": citySelected,
            "frameNo": frameNo,
            "channelNo": "2",
            "countryNature": "undefined",
            "parentId": parentId,#"BDFIXLUC0016",
            "sessionId": sessionid,
            "seatCount": seat,
            "enrollDate": vehicle_register_date,
            "engineNo": engineNo,
            "licenseFlag": "1",
            "proSelected": proSelected,
            "carRequestType": "03",#固定值查询模式 03carMode是编码 04是中文
            "modelCode": "undefined"#DFCQBD0018
        }
        vehicleCheckeddata=urllib.urlencode(vehicleCheckeddata)
        vehicleCheckedresponse=requests.post(vehicleCheckedurl,data=vehicleCheckeddata,headers=headers)
        log.info('vehicleCheckedresponse=%s' % vehicleCheckedresponse)
        log.info(u"vehicleChecked=====http://www.epicc.com.cn/wap/carProposal/carSelect/vehicleChecked=============结束")
        #########################################################################
        log.info(u"underwriteCheckProfitAjax=====http://www.epicc.com.cn/wap/carProposal/underWrite/underwriteCheckProfitAjax=============开始")
        headers['Referer']='http://www.epicc.com.cn/wap/carProposal/car/carInput2'
        CheckProfiturl='http://www.epicc.com.cn/wap/carProposal/underWrite/underwriteCheckProfitAjax'
        startdate=utils.getlatedate(2)
        enddate=utils.getlatedate(366)
        transferdate=utils.getnowdate()
        CheckProfitdata={
            "haveLoan": "2",
            "licenseno": licenseno,
            "ccaEntryId": "",
            "weiFaName": "",
            "lastHas050500": "0",
            "isRenewal": "0",
            "insuredIdentifyNumber": insuredIdentifyNumber,
            "proSelected": proSelected,
            "oldPolicyNo": "",
            "isOutRenewal": "0",
            "carIdentifyNumber": insuredIdentifyNumber,
            "ccaID": "",
            "startdate": startdate,
            "endhour": "24",
            "vinno": frameNo,
            "citySelected": citySelected,
            "lastHas050210": "0",
            "areaCodeLast": areaCodeLast,
            "enrolldate": vehicle_register_date,
            "interimNo": interimNo,
            "seatcount": seat,
            "lastHas050200": "0",
            "licenseflag": "1",
            "channelNo": "2",
            "guohuflag": "0",
            "ccaFlag": "",
            "frameno": frameNo,
            "certificatedateSH": "",
            "assignDriver": "2",
            "lastdamagedbi": "",
            "guohuselect": "0",
            "cityCodeLast": cityCodeLast,
            "lastcarownername": "",
            "runAreaCodeName": "",
            "enddate": enddate,
            "transferdate": transferdate,
            "appliIdentifyNumber": insuredIdentifyNumber,
            "carOwner": carOwner,
            "seatflag": "1",
            "sessionId": sessionid,
            "LoanName": "",
            "engineno": engineNo,
            "carDrivers": "",
            "starthour": "0"
        }

        CheckProfitdata=urllib.urlencode(CheckProfitdata)
        #print(CheckProfitdata)
        CheckProfitresponse=requests.post(url=CheckProfiturl,headers=headers,data=CheckProfitdata)
        CheckProfitresponse=CheckProfitresponse.json()
        #CheckProfitresponse=json.dumps(CheckProfitresponse, ensure_ascii=False, indent=4)
        #print CheckProfitresponse
        resultCode=eval(CheckProfitresponse['common'])['resultCode']


        ###########################################################code=1成功  , code=3车辆信息不一致 重新获取信的车辆信息
        if resultCode=='3':
            log.info(u'选择车辆信息不一致,进行重新选择')
            #发送vehicleChecked获取参数
            carModel=CheckProfitresponse['carModel']
            carModelAndName=CheckProfitresponse['carModelAndName']
            #modelCode= carModelAndName中间一截  BCACDTUC0035
            modelCode=re.findall(r"carModel(.+?)CarName",carModelAndName,re.S)[0]
            carName=carModelAndName.split("CarName")[1]
            log.info(u"vehicleChecked=====http://www.epicc.com.cn/wap/carProposal/carSelect/vehicleChecked=============开始")
            vehicleCheckedurl='http://www.epicc.com.cn/wap/carProposal/carSelect/vehicleChecked'
            headers['Referer']='http://www.epicc.com.cn/wap/carProposal/car/carInput2'
            Checkeddata={
                      'carModel': carName,
                      'queryCode': modelCode,
                      'vinNo': frameNo,
                      'citySelected': citySelected,
                      'frameNo': frameNo,
                      'channelNo': '2',
                      'countryNature': '',
                      'parentId': modelCode,
                      'sessionId': sessionid,
                      'seatCount': '',
                      'enrollDate': vehicle_register_date,
                      'engineNo': engineNo,
                      'licenseFlag': '1',
                      'proSelected': proSelected,
                      'carRequestType': '04',
                      'modelCode':carModel
                    }

            Checkeddata=urllib.urlencode(Checkeddata)
            Checkeddataresponse=requests.post(vehicleCheckedurl,data=Checkeddata,headers=headers)
            log.info('vehicleCheckedresponse=%s' % Checkeddataresponse)
            #########################################################################
            log.info(u"underwriteCheckProfitAjax2=====http://www.epicc.com.cn/wap/carProposal/underWrite/underwriteCheckProfitAjax=============开始")
            headers['Referer']='http://www.epicc.com.cn/wap/carProposal/car/carInput2'
            CheckProfiturl='http://www.epicc.com.cn/wap/carProposal/underWrite/underwriteCheckProfitAjax'
            startdate=utils.getlatedate(2)
            enddate=utils.getlatedate(366)
            transferdate=utils.getnowdate()
            CheckProfitdata2={
                "haveLoan": "2",
                "licenseno": licenseno,
                "ccaEntryId": "",
                "weiFaName": "",
                "lastHas050500": "0",
                "isRenewal": "0",
                "insuredIdentifyNumber": insuredIdentifyNumber,
                "proSelected": proSelected,
                "oldPolicyNo": "",
                "isOutRenewal": "0",
                "carIdentifyNumber": insuredIdentifyNumber,
                "ccaID": "",
                "startdate": startdate,
                "endhour": "24",
                "vinno": frameNo,
                "citySelected": citySelected,
                "lastHas050210": "0",
                "areaCodeLast": areaCodeLast,
                "enrolldate": vehicle_register_date,
                "interimNo": interimNo,
                "seatcount": seat,
                "lastHas050200": "0",
                "licenseflag": "1",
                "channelNo": "2",
                "guohuflag": "0",
                "ccaFlag": "",
                "frameno": frameNo,
                "certificatedateSH": "",
                "assignDriver": "2",
                "lastdamagedbi": "",
                "guohuselect": "0",
                "cityCodeLast": cityCodeLast,
                "lastcarownername": "",
                "runAreaCodeName": "",
                "enddate": enddate,
                "transferdate": transferdate,
                "appliIdentifyNumber": insuredIdentifyNumber,
                "carOwner": carOwner,
                "seatflag": "1",
                "sessionId": sessionid,
                "LoanName": "",
                "engineno": engineNo,
                "carDrivers": "",
                "starthour": "0"
            }

            CheckProfitdata2=urllib.urlencode(CheckProfitdata2)
            #print(CheckProfitdata)
            CheckProfitresponse2=requests.post(url=CheckProfiturl,headers=headers,data=CheckProfitdata2)
            CheckProfitresponse2=CheckProfitresponse2.json()
            log.info(CheckProfitresponse2)


        log.info(u"underwriteCheckProfitAjax=====http://www.epicc.com.cn/wap/carProposal/underWrite/underwriteCheckProfitAjax=============结束")
        #######################计算费用########################
        log.info(u"计算费用one=====http://www.epicc.com.cn/wap/carProposal/calculateFee/fee==================================开始")
        feeurl ='http://www.epicc.com.cn/wap/carProposal/calculateFee/fee'
        headers['Referer']='http://www.epicc.com.cn/wap/carProposal/car/calculateFee'
        feedata={
            "haveLoan": "2",
            "licenseno": licenseno,
            "ccaEntryId": "",
            "identifynumber": insuredIdentifyNumber,
            "weiFaName": "",
            "lastHas050500": "0",
            "sex": sex,
            "isRenewal": "0",
            "proSelected": proSelected,
            "nonlocalflag": "01",
            "ccaID": "",
            "startdate": startdate,
            "endhour": "24",
            "vinno": frameNo,
            "citySelected": citySelected,
            "lastHas050210": "0",
            "insuredname": carOwner,
            "areaCodeLast": areaCodeLast,
            "enrolldate": vehicle_register_date,
            "lastHas050200": "0",
            "licenseflag": "1",
            "isOutRenewal": "0",
            "email": Email,
            "ccaFlag": "",
            "frameno": frameNo,
            "fullAmountName": "",
            "channelNo": "2",
            "assignDriver": "2",
            "seatCount": seat,
            "LoanName": "",
            "lastHas050291": "",
            "guohuselect": "0",
            "cityCodeLast": cityCodeLast,
            "runAreaCodeName": "",
            "enddate": enddate,
            "transferdate": transferdate,
            "mobile": Mobile,
            "transfervehicleflag": "0",
            "identifytype": "01",
            "travelMilesvalue": "",
            "seatflag": "1",
            "sessionId":sessionid ,
            "birthday": insuredBirthday,
            "engineno": engineNo,
            "carDrivers": "",
            "newcarflag": "0",
            "starthour": "0"
        }

        feedata=urllib.urlencode(feedata)
        #print(feedata)
        feeresponse=requests.post(url=feeurl,headers=headers,data=feedata)
        feebody=feeresponse.json()
        feebody=json.dumps(feebody,ensure_ascii=False,indent=4)
        #print feebody
        amount = jsonpath.jsonpath(eval(feebody),'$.commonPackage.items')[0][0].get('amount',"0")
        log.info('amount===%s'% amount)


        log.info(u"计算费用one=====http://www.epicc.com.cn/wap/carProposal/calculateFee/fee==================================结束")

        log.info(u"计算费用2=====http://www.epicc.com.cn/wap/carProposal/calculateFee/fee==================================开始")
        feeurl ='http://www.epicc.com.cn/wap/carProposal/calculateFee/fee'
        headers['Referer']='http://www.epicc.com.cn/wap/carProposal/car/calculateFee'
        feedata2={
            "channelNo":"2",
            "haveLoan": "2",
            "licenseno": licenseno,
            "ccaEntryId": "",
            "identifynumber": insuredIdentifyNumber,
            "weiFaName": "",
            "lastHas050500": "0",
            "sex": sex,
            "isRenewal": "0",
            "proSelected": proSelected,
            "nonlocalflag": "01",
            "ccaID": "",
            "startdate": startdate,
            "endhour": "24",
            "vinno": frameNo,
            "citySelected": citySelected,
            "lastHas050210": "0",
            "insuredname": carOwner,
            "areaCodeLast": areaCodeLast,
            "enrolldate": vehicle_register_date,
            "lastHas050200": "0",
            "licenseflag": "1",
            "isOutRenewal": "0",
            "email": Email,
            "ccaFlag": "",
            "frameno": frameNo,
            "fullAmountName": "",
            "channelNo": "2",
            "assignDriver": "2",
            "seatCount": seat,
            "LoanName": "",
            "lastHas050291": "",
            "guohuselect": "0",
            "cityCodeLast": cityCodeLast,
            "runAreaCodeName": "",
            "enddate": enddate,
            "transferdate": transferdate,
            "mobile": Mobile,
            "transfervehicleflag": "0",
            "identifytype": "01",
            "travelMilesvalue": "",
            "seatflag": "1",
            "sessionId":sessionid ,
            "birthday": insuredBirthday,
            "engineno": engineNo,
            "carDrivers": "",
            "newcarflag": "0",
            "starthour": "0",
            ###########
            'select_050270': '',
            'select_050921': '1',
            'ccaEntryId': '',
            'select_050701': '10000',
            'select_050702': '10000',
            'select_050231': '10',
            'select_050600': '500000',
            'select_050310': amount,
            'select_050928': '1',
            'select_050330': '',
            'select_050210': '2000',
            'select_050924': '1',
            'BZ_selected': '2',
            'select_050641': '',
            'ccaID': '',
            'select_050643': '-1',
            'select_050642': '-1',
            'select_050252': '-1',
            'select_050291': '1',
            'select_050451': '-1',
            'select_050922': '1',
            'ccaFlag': '',
            'select_050200': amount,
            'select_050917': '-1',
            'select_050911': '1',
            'select_050935': '1',
            'select_050912': '1',
            'select_050919': '',
            'select_050918': '-1',
            'select_050500': amount,
            'select_050929': '1'
        }

        feedata2=urllib.urlencode(feedata2)
        fee2url='http://www.epicc.com.cn/wap/carProposal/calculateFee/sy'
        feeresponse=requests.post(url=fee2url,headers=headers,data=feedata2)
        feebody=feeresponse.json()
        log.info(u"计算费用2=====http://www.epicc.com.cn/wap/carProposal/calculateFee/fee==================================结束")
        log.info(u"计算JQ=====开始")
        jq_dt = {}
        jq_dt['transferdate'] = transferdate
        jq_dt['licenseno'] = licenseno
        jq_dt['identifynumber'] = insuredIdentifyNumber
        jq_dt['startDateCI'] = startdate
        jq_dt['proSelected'] = proSelected
        jq_dt['startdate'] = startdate
        jq_dt['vinno'] = frameNo
        jq_dt['citySelected'] = citySelected
        jq_dt['insuredname'] = carOwner
        jq_dt['areaCodeLast'] = areaCodeLast
        jq_dt['sessionId'] = sessionid
        jq_dt['taxpayername'] = carOwner
        jq_dt['frameno'] = frameNo
        jq_dt['cityCodeLast'] = cityCodeLast
        jq_dt['endDateCI'] = enddate
        jq_dt['enddate'] = enddate
        jq_dt['enrolldate'] = vehicle_register_date
        jq_dt['birthday'] = insuredBirthday
        jq_dt['engineno'] = engineNo
        jq_dt['sex'] = sex
        jq_dt['seatCount'] = seat
        jq_resp = get_jq_epicc(jq_dt)
        log.info("jq_resp %s" % jq_resp)
        log.info(u"计算JQ=====结束")
        try:
            PremiumInfo = translateJsonToPremiun.readJson(feebody['commonPackage']['items'], seat,jq_resp)
        except:
            return feebody
        data = [licenseno, frameNo, startdate, enddate, seat]
        dbInsert.soupDb(PremiumInfo, data, insureCarId)

    except Exception ,e:
        log.error(e)
        log.error(traceback.format_exc())
        log.error('获取数据异常车牌号==%s'% licenseno)
        return '获取数据异常车牌号%s'% licenseno


if __name__ == '__main__':
    sessionid = carInput1_1('32010000', '32000000')
    new_user(sessionid, '32000000', '32010000', '32000000', '32010000', '320125198610093122', '杨小香', '苏AB3Q98',
             'LNBSCCAH3EF031577', 'KL1392', '3430')
