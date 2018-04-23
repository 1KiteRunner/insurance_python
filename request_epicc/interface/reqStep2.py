# -*- coding:utf-8 -*-
import sys
import re

import  requests

reload(sys)
sys.setdefaultencoding('utf-8')
import json
import datetime
import ast
from  request_epicc import settings as se
from common.log import  Logger
import urllib
import jsonpath
import translateJsonToPremiun
import dbInsert
from JqEpicc import get_jq_epicc
from obtainVerificationCode import  getobtainVerificationCode
log=Logger()
def step2_1(sessionid,licenseNo,IDnumber,proSelected,citySelected,body,insureCarId):
    headers = se.headers
    gender = ""
    if int(IDnumber[16:17]) % 2 == 0:
        gender = 2
    else:
        gender = 1
    birthday = IDnumber[6:10] + '/' + IDnumber[10:12] + '/' + IDnumber[12:14]
    nowdate = str(datetime.date.today()).replace('-', '/')

    body = eval(body)
    # 车架号
    rackNo = jsonpath.jsonpath(body, '$.appliCarInfo.rackNo')[0]
    # tokenNo
    tokenNo = jsonpath.jsonpath(body, '$.tokenNo')[0]
    lastHas050200 = jsonpath.jsonpath(body, '$.lastHas050200')[0]
    lastHas050210 = jsonpath.jsonpath(body, '$.lastHas050210')[0]
    lastHas050291 = jsonpath.jsonpath(body, '$.lastHas050291')[0]
    # lastHas050310 = jsonpath.jsonpath(body, '$.lastHas050310')[0]
    lastHas050500 = jsonpath.jsonpath(body, '$.lastHas050500')[0]
    isOutRenewal = jsonpath.jsonpath(body, '$.isOutRenewal')[0]
    # guoHuSelect = jsonpath.jsonpath(body, '$.guoHuSelect')[0]
    # appliCarInfo = jsonpath.jsonpath(body, '$.appliCarInfo.seatFlag')[0]
    nonlocalflag = jsonpath.jsonpath(body, '$.nonlocalflag')[0]
    assignDriver = jsonpath.jsonpath(body, '$.assignDriver')[0]
    enrolldate = jsonpath.jsonpath(body, '$.appliCarInfo.enrollDate')[0]
    enrolldateFormat = enrolldate.replace('/', '-')
    haveLoan = jsonpath.jsonpath(body, '$.haveLoan')[0]
    LoanName = jsonpath.jsonpath(body, '$.loanName')[0]
    carOwerIdentifyType = jsonpath.jsonpath(body, '$.carOwnerInfo.carOwerIdentifyType')[0]
    carOwnerIdentifyNumber = e = jsonpath.jsonpath(body, '$.carOwnerInfo.carOwnerIdentifyNumber')[0]
    carOwner = jsonpath.jsonpath(body, '$.carOwnerInfo.carOwner')[0]
    engineNo = jsonpath.jsonpath(body, '$.appliCarInfo.engineNo')[0]
    seatFlag = jsonpath.jsonpath(body, '$.appliCarInfo.seatFlag')[0]
    startDateSY = jsonpath.jsonpath(body, '$.startDateSY')[0]
    startDateSYFormat = startDateSY.replace('/', '-')
    endDateSY = jsonpath.jsonpath(body, '$.endDateSY')[0]
    endDateSYFormat = endDateSY.replace('/', '-')
    seat = jsonpath.jsonpath(body, '$.appliCarInfo.seat')[0]
    standardName = jsonpath.jsonpath(body, '$.appliCarInfo.standardName')[0]
    insuredIdentifyAddr = jsonpath.jsonpath(body, '$.insuredInfo.insuredIdentifyAddr')[0]
    #获取interimNo
    data9 = {
            'haveLoan': '2',
            'licenseno': licenseNo,
            'bjfuel_type': '',
            'deliverInfoCity': citySelected[0:6],
            'insuredMobile': '13888888888',
            'insuredAndOwnerrelate': '',
            'carKindCI': '',
            'deliverInfoPro': proSelected[0:6],
            'invoiceTitle': '',
            'beforeProposalNo': tokenNo,
            'LoanName': '',
            'transferdate': '',
            'certificate_no': '',
            'aliasName': '',
            'proSelected': proSelected,
            'argueSolution': '',
            'guohuselect': '0',
            'frameno': rackNo,
            'endhour': '24',
            'vinno': rackNo,
            'endHourCI': '24',
            'citySelected': citySelected,
            'carKindSX': '',
            'deliverInfoDistrict': '',
            'areaCodeLast': proSelected,
            'enrolldate': enrolldateFormat,
            'certificate_type': '',
            'seatcount': seat,
            'licenseflag': '1',
            'insuredIdentifSex':gender,
            'appliPhoneNumber': '13888888888',
            'travelMilesvalue': '',
            'appliEmail': '135@163.com',
            'insuredIdentifyType': carOwerIdentifyType,
            'isRenewal': '1',
            'monopolyname': '',
            'enddate': endDateSYFormat,
            'insuredIdentifyAddr': insuredIdentifyAddr,
            'fullAmountName': seat,
            'arbitboardname': '',
            'linkAddress': '',
            'endDateCI':endDateSYFormat,
            'assignDriver': '2',
            'startHourCI': '0',
            'carIdentifyAddressSX': '',
            'appliAddName': carOwner,
            'engineno': engineNo,
            'weiFaName': '6',
            'taxPayerIdentType': '',
            'carDrivers': '[]',
            'appliIdentifyType': '01',
            'cityCodeLast': citySelected,
            'interimNo': '',
            'insuredBirthday': birthday,
            'standardName': standardName,
            'itemKindFlag': '1',
            'runAreaCodeName': '11',
            'certificate_date': '',
            'mobileflag': '1',
            'taxPayerIdentNo': IDnumber,
            'lastcarownername': carOwner,
            'appliIdentifyNumber': IDnumber,
            'startdate': startDateSYFormat,
            'carOwner': carOwner,
            'certificatedate': '',
            'ccaId': '',
            'appliMobile': '15251891862',
            'sessionId': sessionid,
            'startDateCI': startDateSYFormat,
            'insuredEmail': '135@163.com',
            'taxPayerName': '',
            'insuredIdentifyNumber': IDnumber,
            'carOwerIdentifyType': carOwerIdentifyType,
            'carNameSX': '',
            'appliName': carOwner,
            'starthour': '0'
        }
    re9 = requests.post(se.interim_url,headers =headers, data=data9)
    interimNo = str(re9.json()['interimNo'])

    # 请求验证码并且发送返回字符串验证码
    log.info(u"请求车管所验证码=====http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerificationCode============================开始")
    codestr = getobtainVerificationCode(licenseNo, sessionid, rackNo)
    log.info( u"请求车管所验证码=====http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerificationCode============================结束")
    ######################################
    log.info(u"发送验证码=====http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerifQueryCar============================开始")

    # 发送验证码
    data3 = 'icationCode=' + codestr + '&channelNo=2&sessionId=' + sessionid
    re3 = requests.post(se.postVerifQueryCar_url,headers=headers, data=data3)
    body3 = re3.json()
    body3 = ast.literal_eval(body3['message'])
    code = body3['head']['errorCode']
    while code == '93037':
        # 请求验证码并且发送返回字符串验证码
        log.info(u"请求车管所验证码=====http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerificationCode============================开始")
        codestr = getobtainVerificationCode(licenseNo, sessionid, rackNo)
        log.info(u"请求车管所验证码=====http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerificationCode============================结束")
        ######################################
        log.info(u"发送验证码=====http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerifQueryCar============================开始")

        log.info(u"验证码为=%s,文件名为=%s" % (codestr))
        data3 = 'icationCode=' + codestr + '&channelNo=2&sessionId=' + sessionid
        re3 = requests.post(se.postVerifQueryCar_url,headers=headers, data=data3)
        body3 = re3.json()
        body3 = ast.literal_eval(body3['message'])
        code = body3['head']['errorCode']

    #check
    data5 = 'lastcarownername=' + urllib.quote(carOwner) + '&channelNo=2&areaCodeLast='+proSelected+'&cityCodeLast='+citySelected+'&proSelected='+proSelected+'&citySelected='+citySelected+'&startdate=' + startDateSYFormat + '&starthour=0&enddate=' + endDateSYFormat + '&endhour=24&licenseno=' + urllib.quote(licenseNo) + '&engineno=' + engineNo + '&vinno=' + rackNo + '&frameno=' + rackNo + '&seatcount=' + seat + '&carOwner=' + urllib.quote(carOwner) + '&isRenewal=1&enrolldate=' + enrolldateFormat + '&guohuselect=0&licenseflag=1&isOutRenewal=0&lastHas050200=1&lastHas050210=0&lastHas050500=0&seatflag=1&transferdate=' + urllib.quote(nowdate) + '&ccaID=&ccaEntryId=&ccaFlag=&lastdamagedbi=0&guohuflag=0&runAreaCodeName=&assignDriver=2&haveLoan=2&LoanName=&weiFaName=&carDrivers=&oldPolicyNo=' + tokenNo + '&interimNo=' + interimNo + '&certificatedateSH=&insuredIdentifyNumber=' + IDnumber + '&appliIdentifyNumber=' + IDnumber + '&carIdentifyNumber=' + IDnumber + '&sessionId=' + sessionid
    re5 = requests.post(se.check_url,headers=headers, data=data5)
    if ast.literal_eval(re5.json()['common'])['resultCode']=='3':
        carInfos = eval(re5.json()['carInfos'])
        carModelAndName = re5.json()['carModelAndName']
        carName = carModelAndName.split("CarName")[1]
        modelCode = re.findall(r"carModel(.+?)CarName", carModelAndName, re.S)[0]
        log.info(u"vehicleChecked=====http://www.epicc.com.cn/wap/carProposal/carSelect/vehicleChecked=============开始")
        vehicleCheckedurl = 'http://www.epicc.com.cn/wap/carProposal/carSelect/vehicleChecked'
        headers['Referer'] = 'http://www.epicc.com.cn/wap/carProposal/car/carInput2'
        Checkeddata = {
            'carModel': carName,
            'queryCode': modelCode,
            'vinNo': rackNo,
            'citySelected': citySelected,
            'frameNo': rackNo,
            'channelNo': '2',
            'countryNature': '',
            'parentId': modelCode,
            'sessionId': sessionid,
            'seatCount': seat,
            'enrollDate': enrolldateFormat,
            'engineNo': engineNo,
            'licenseFlag': '1',
            'proSelected': proSelected,
            'carRequestType': '04',
            'modelCode': carInfos[0]['vehicleId']
        }
        Checkeddata = urllib.urlencode(Checkeddata)
        Checkeddataresponse = requests.post(vehicleCheckedurl, data=Checkeddata, headers=headers)
        log.info('vehicleCheckedresponse=%s' % Checkeddataresponse)
        #########################################################################
        data5 = 'lastcarownername=' + urllib.quote(carOwner) + '&channelNo=2&areaCodeLast=' + proSelected + '&cityCodeLast=' + citySelected + '&proSelected=' + proSelected + '&citySelected=' + citySelected + '&startdate=' + startDateSYFormat + '&starthour=0&enddate=' + endDateSYFormat + '&endhour=24&licenseno=' + urllib.quote(licenseNo) + '&engineno=' + engineNo + '&vinno=' + rackNo + '&frameno=' + rackNo + '&seatcount=' + seat + '&carOwner=' + urllib.quote(carOwner) + '&isRenewal=1&enrolldate=' + enrolldateFormat + '&guohuselect=0&licenseflag=1&isOutRenewal=0&lastHas050200=1&lastHas050210=0&lastHas050500=0&seatflag=1&transferdate=' + urllib.quote(nowdate) + '&ccaID=&ccaEntryId=&ccaFlag=&lastdamagedbi=0&guohuflag=0&runAreaCodeName=&assignDriver=2&haveLoan=2&LoanName=&weiFaName=&carDrivers=&oldPolicyNo=' + tokenNo + '&interimNo=' + interimNo + '&certificatedateSH=&insuredIdentifyNumber=' + IDnumber + '&appliIdentifyNumber=' + IDnumber + '&carIdentifyNumber=' + IDnumber + '&sessionId=' + sessionid
        re5 = requests.post(se.check_url, headers=headers, data=data5)

    #第一次爬取
    data4 = ('proSelected='+proSelected+'&citySelected='+citySelected+'&areaCodeLast='+proSelected+'&cityCodeLast='+citySelected+'&mobile=15905175343&email=%s&identifytype=%s'
             '&identifynumber=%s'
             '&birthday=%s'
             '&sex=%s'
             '&beforeProposalNo=%s'
             '&startdate=%s'
             '&starthour=0'
             '&enddate=%s'
             '&endhour=24'
             '&licenseno=%s'
             '&nonlocalflag=%s'
             '&licenseflag=1'
             '&engineno=%s'
             '&vinno=%s'
             '&frameno=%s'
             '&enrolldate=%s'
             '&transfervehicleflag=0'
             '&insuredname=%s'
             '&fullAmountName='
             '&startDateCI=%s'
             '&starthourCI=0'
             '&endDateCI=%s'
             '&endhourCI=24'
             '&sessionId=%s'
             '&seatflag=%s'
             '&isOutRenewal=%s'
             '&lastHas050200=%s'
             '&lastHas050210=%s'
             '&lastHas050500=%s'
             '&lastHas050291=%s'
             '&transferdate=%s'
             '&guohuselect=0'
             '&runAreaCodeName='
             '&assignDriver=%s'
             '&haveLoan=%s'
             '&LoanName=%s'
             '&weiFaName='
             '&seatCount=%s'
             '&carDrivers='
             '&travelMilesvalue='
             '&lastdamageBI=0'
             '&ccaFlag='
             '&ccaID='
             '&ccaEntryId='
             '&noDamyearsBI=1' %  (urllib.quote('2290@qq.com'),carOwerIdentifyType,carOwnerIdentifyNumber,urllib.quote(birthday),gender,tokenNo,startDateSYFormat,endDateSYFormat,urllib.quote(licenseNo),nonlocalflag,engineNo,rackNo,rackNo,enrolldateFormat,urllib.quote(carOwner),urllib.quote(startDateSY),urllib.quote(endDateSY),sessionid,seatFlag,isOutRenewal,lastHas050200,lastHas050210,lastHas050500,lastHas050291,urllib.quote(nowdate),assignDriver,haveLoan,LoanName,seat))
    re4 = requests.post(url='http://www.epicc.com.cn/wap/carProposal/calculateFee/renewalfee',headers=headers,data=data4)
    amount = jsonpath.jsonpath(eval(json.dumps(re4.json(), ensure_ascii=False, indent=4)), '$.commonPackage.items')[0][0].get('amount', "0")

    data6 = ('channelNo=2&proSelected='+proSelected+'&citySelected='+citySelected+'&areaCodeLast='+proSelected+'&cityCodeLast='+citySelected+'&mobile=15905175343&email=%s&identifytype=%s'
             '&identifynumber=%s'
             '&birthday=%s'
             '&sex=%s'
             '&beforeProposalNo=%s'
             '&startdate=%s'
             '&starthour=0'
             '&enddate=%s'
             '&endhour=24'
             '&licenseno=%s'
             '&nonlocalflag=%s'
             '&licenseflag=1'
             '&engineno=%s'
             '&vinno=%s'
             '&frameno=%s'
             '&enrolldate=%s'
             '&transfervehicleflag=0'
             '&insuredname=%s'
             '&fullAmountName='
             '&startDateCI=%s'
             '&starthourCI=0'
             '&endDateCI=%s'
             '&endhourCI=24'
             '&sessionId=%s'
             '&seatflag=%s'
             '&isOutRenewal=%s'
             '&lastHas050200=%s'
             '&lastHas050210=%s'
             '&lastHas050500=%s'
             '&lastHas050291=%s'
             '&transferdate=%s'
             '&guohuselect=0'
             '&runAreaCodeName='
             '&assignDriver=%s'
             '&haveLoan=%s'
             '&LoanName=%s'
             '&weiFaName='
             '&seatCount=%s'
             '&carDrivers='
             '&travelMilesvalue='
             '&lastdamageBI=0'
             '&ccaFlag='
             '&ccaID='
             '&ccaEntryId='
             '&noDamyearsBI=1&ccaFlag=&ccaID=&ccaEntryId=&BZ_selected=2&select_050200=%s&select_050600=500000&select_050500=%s&select_050701=10000&select_050702=10000&select_050310=%s&select_050231=10&select_050270=&select_050210=2000&select_050252=-1&select_050291=1&select_050911=1&select_050912=1&select_050921=1&select_050922=1&select_050924=1&select_050928=1&select_050330=&select_050935=1&select_050918=-1&select_050919=&select_050917=-1&select_050451=-1&select_050642=-1&select_050641=&select_050643=-1&select_050929=1' % (urllib.quote('2290@qq.com'),carOwerIdentifyType,carOwnerIdentifyNumber,urllib.quote(birthday),gender,tokenNo,startDateSYFormat,endDateSYFormat,urllib.quote(licenseNo),nonlocalflag,engineNo,rackNo,rackNo,enrolldateFormat,urllib.quote(carOwner),urllib.quote(startDateSY),urllib.quote(endDateSY),sessionid,seatFlag,isOutRenewal,lastHas050200,lastHas050210,lastHas050500,lastHas050291,urllib.quote(nowdate),assignDriver,haveLoan,LoanName,seat,amount,amount,amount))
    re4 = requests.post(se.secondTimeCalculate_url,headers=headers,data=data6)
    re4 = re4.json()



    log.info(u"计算JQ=====开始")
    jq_dt = {}
    jq_dt['transferdate'] = nowdate
    jq_dt['licenseno'] = licenseNo
    jq_dt['identifynumber'] = IDnumber
    jq_dt['startDateCI'] = nowdate
    jq_dt['proSelected'] = proSelected
    jq_dt['startdate'] = startDateSYFormat
    jq_dt['vinno'] = rackNo
    jq_dt['citySelected'] = citySelected
    jq_dt['insuredname'] = carOwner
    jq_dt['areaCodeLast'] = proSelected
    jq_dt['sessionId'] = sessionid
    jq_dt['taxpayername'] = carOwner
    jq_dt['frameno'] = rackNo
    jq_dt['cityCodeLast'] = citySelected
    jq_dt['endDateCI'] = endDateSY
    jq_dt['enddate'] = endDateSYFormat
    jq_dt['enrolldate'] = enrolldateFormat
    jq_dt['birthday'] = birthday
    jq_dt['engineno'] = engineNo
    jq_dt['sex'] = gender
    jq_dt['seatCount'] = seat
    jq_resp = get_jq_epicc(jq_dt)

    try:
        PremiumInfo = translateJsonToPremiun.readJson(re4['commonPackage']['items'], seat,jq_resp)
    except:
        return re4
    data = [licenseNo, rackNo, startDateSYFormat, endDateSYFormat, seat]
    dbInsert.soupDb(PremiumInfo, data, insureCarId)
    log.info(u"计算JQ=====结束")

def step2_2(sessionid,licenseNo,IDnumber,proSelected,citySelected,body,insureCarId):
    headers = se.headers
    gender = ""
    if int(IDnumber[16:17]) % 2 == 0:
        gender = "2"
    else:
        gender = "1"
    birthday = IDnumber[6:10] + '/' + IDnumber[10:12] + '/' + IDnumber[12:14]
    nowdate = str(datetime.date.today()).replace('-', '/')
    # data = 'proSelected='+proSelected+'&citySelected='+citySelected+'&beforeProposalNo=' + IDnumber + '&licenseNo=' + urllib.quote(licenseNo) + '&sessionId=' + sessionid
    # res = requests.post(url=se.query_carData_url, headers=headers, data=data)
    # body = ast.literal_eval(res.json()['message'])
    # 车架号
    rackNo = body['appliCarInfo']['rackNo']
    # tokenNo
    #tokenNo = jsonpath.jsonpath(body, '$.tokenNo')[0]
    tokenNo=body.get('tokenNo','0')

    engineNo = body['appliCarInfo']['engineNo']
    standardName = body['appliCarInfo']['brandName']
    seat = body['appliCarInfo']['seat']
    enrolldate = body['appliCarInfo']['enrollDate']
    enrolldateFormat = enrolldate.replace('/', '-')
    carOwerIdentifyType = body['carOwnerInfo']['carOwerIdentifyType']
    carOwnerIdentifyNumber = IDnumber
    carOwner = body['carOwnerInfo']['carOwner']
    if carOwner=='':
        carOwner=body['insuredInfo']['insuredName']

    seatFlag = body['appliCarInfo']['seatFlag']
    datetime.date.today() + datetime.timedelta(2)
    startDateSY = datetime.date.today() + datetime.timedelta(2)
    startDateSYFormat = str(startDateSY).replace('/', '-')
    endDateSY1 = (str(startDateSY.year+1)+'-'+str(startDateSY.month)+'-'+str(startDateSY.day))
    endDateSY = datetime.datetime.strptime(endDateSY1, "%Y-%m-%d").date() + datetime.timedelta(-1)
    endDateSYFormat = str(endDateSY).replace('/', '-')
    insuredIdentifyAddr = body['insuredInfo']['insuredIdentifyAddr']
    insuredIdentifyType = body['insuredInfo']['insuredIdentifyType']
    appliIdentifyType = body['appliInfo']['appliIdentifyType']
    # 获取interimNo
    data9 = 'mobileflag=1&licenseno='+urllib.quote(licenseNo)+'&sessionId='+sessionid+'&proSelected='+proSelected+'&citySelected='+citySelected+'&areaCodeLast='+proSelected+'&cityCodeLast='+citySelected+'&insuredIdentifSex='+gender+'&insuredBirthday='+urllib.quote(birthday)+'&lastcarownername='+urllib.quote(carOwner)+'&startdate=&starthour=&enddate=&endhour=&startDateCI=&startHourCI=&endDateCI=&endHourCI=&engineno='+engineNo+'&vinno='+rackNo+'&frameno='+rackNo+'&enrolldate='+enrolldateFormat+'&standardName='+urllib.quote(standardName)+'&seatcount='+seat+'&linkAddress=&runAreaCodeName=&assignDriver=&carDrivers=&haveLoan=&LoanName=&guohuselect=&transferdate=&fullAmountName=&appliEmail=13888888%40163.com&appliIdentifyNumber='+IDnumber+'&appliIdentifyType=01&appliMobile=13888888888&appliName='+urllib.quote(carOwner)+'&taxPayerIdentNo=&taxPayerName=&aliasName=&carOwerIdentifyType='+carOwerIdentifyType+'&carOwner='+urllib.quote(carOwner)+'&insuredEmail=13888888%40163.com&insuredIdentifyAddr=&insuredIdentifyType=01&insuredIdentifyNumber='+IDnumber+'&insuredMobile=13888888888&argueSolution=&insuredAndOwnerrelate=&arbitboardname=&appliAddName=&deliverInfoPro=&deliverInfoCity=&deliverInfoDistrict=&appliPhoneNumber=&invoiceTitle=&itemKindFlag=1&travelMilesvalue=&licenseflag=1&certificatedate=&monopolyname=&weiFaName=&isRenewal=0&interimNo=&beforeProposalNo=&taxPayerIdentType=&carKindCI=&bjfuel_type=&certificate_type=&certificate_no=&certificate_date=&carIdentifyAddressSX=&carNameSX=&carKindSX=&ccaId='
    re9 = requests.post(se.interim_url, headers=headers, data=data9)
    interimNo = str(re9.json()['interimNo'])

    # 请求验证码并且发送返回字符串验证码
    log.info(
        u"请求车管所验证码=====http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerificationCode============================开始")
    codestr = getobtainVerificationCode(licenseNo, sessionid, rackNo)
    log.info(
        u"请求车管所验证码=====http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerificationCode============================结束")
    ######################################
    log.info(
        u"发送验证码=====http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerifQueryCar============================开始")

    # 发送验证码
    data3 = 'icationCode=' + codestr + '&channelNo=2&sessionId=' + sessionid
    re3 = requests.post(se.postVerifQueryCar_url, headers=headers, data=data3)
    body3 = re3.json()
    body3 = ast.literal_eval(body3['message'])
    code = body3['head']['errorCode']
    while code == '93037':
        # 请求验证码并且发送返回字符串验证码
        log.info(
            u"请求车管所验证码=====http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerificationCode============================开始")
        codestr = getobtainVerificationCode(licenseNo, sessionid, rackNo)
        log.info(
            u"请求车管所验证码=====http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerificationCode============================结束")
        ######################################
        log.info(
            u"发送验证码=====http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerifQueryCar============================开始")

        log.info(u"codestr=%s" % (codestr))
        data3 = 'icationCode=' + codestr + '&channelNo=2&sessionId=' + sessionid
        re3 = requests.post(se.postVerifQueryCar_url, headers=headers, data=data3)
        body3 = re3.json()
        body3 = ast.literal_eval(body3['message'])
        code = body3['head']['errorCode']
    # check
    data5 = 'lastcarownername='+urllib.quote(carOwner)+'&channelNo=2&areaCodeLast='+proSelected+'&cityCodeLast='+citySelected+'&proSelected='+proSelected+'&citySelected='+citySelected+'&startdate='+startDateSYFormat+'&starthour=0&enddate='+endDateSYFormat+'&endhour=24&licenseno='+urllib.quote(licenseNo)+'&engineno='+engineNo+'&vinno='+rackNo+'&frameno='+rackNo+'&seatcount='+seat+'&carOwner='+urllib.quote(carOwner)+'&isRenewal=0&enrolldate='+enrolldateFormat+'&guohuselect=0&licenseflag=1&isOutRenewal=0&lastHas050200=0&lastHas050210=0&lastHas050500=0&seatflag=&transferdate='+urllib.quote(nowdate)+'&sessionId='+sessionid+'&ccaID=&ccaEntryId=&ccaFlag=&lastdamagedbi=&guohuflag=0&runAreaCodeName=&assignDriver=2&haveLoan=2&LoanName=&weiFaName=&carDrivers=&oldPolicyNo=&interimNo='+interimNo+'&certificatedateSH=&insuredIdentifyNumber='+IDnumber+'&appliIdentifyNumber='+IDnumber+'&carIdentifyNumber='+IDnumber
    re5 = requests.post(se.check_url, headers=headers, data=data5)
    if ast.literal_eval(re5.json()['common'])['resultCode']=='3':
        carInfos = eval(re5.json()['carInfos'])
        carModelAndName = re5.json()['carModelAndName']
        carName = carModelAndName.split("CarName")[1]
        modelCode = re.findall(r"carModel(.+?)CarName", carModelAndName, re.S)[0]
        log.info(u"vehicleChecked=====http://www.epicc.com.cn/wap/carProposal/carSelect/vehicleChecked=============开始")
        vehicleCheckedurl = 'http://www.epicc.com.cn/wap/carProposal/carSelect/vehicleChecked'
        headers['Referer'] = 'http://www.epicc.com.cn/wap/carProposal/car/carInput2'
        Checkeddata = {
            'carModel': carName,
            'queryCode': modelCode,
            'vinNo': rackNo,
            'citySelected': citySelected,
            'frameNo': rackNo,
            'channelNo': '2',
            'countryNature': '',
            'parentId': modelCode,
            'sessionId': sessionid,
            'seatCount': seat,
            'enrollDate': enrolldateFormat,
            'engineNo': engineNo,
            'licenseFlag': '1',
            'proSelected': proSelected,
            'carRequestType': '04',
            'modelCode': carInfos[0]['vehicleId']
        }
        Checkeddata = urllib.urlencode(Checkeddata)
        Checkeddataresponse = requests.post(vehicleCheckedurl, data=Checkeddata, headers=headers)
        log.info('vehicleCheckedresponse=%s' % Checkeddataresponse)
        #########################################################################
        data5 = 'lastcarownername=' + urllib.quote(carOwner) + '&channelNo=2&areaCodeLast=' + proSelected + '&cityCodeLast=' + citySelected + '&proSelected=' + proSelected + '&citySelected=' + citySelected + '&startdate=' + startDateSYFormat + '&starthour=0&enddate=' + endDateSYFormat + '&endhour=24&licenseno=' + urllib.quote(licenseNo) + '&engineno=' + engineNo + '&vinno=' + rackNo + '&frameno=' + rackNo + '&seatcount=' + seat + '&carOwner=' + urllib.quote(carOwner) + '&isRenewal=1&enrolldate=' + enrolldateFormat + '&guohuselect=0&licenseflag=1&isOutRenewal=0&lastHas050200=1&lastHas050210=0&lastHas050500=0&seatflag=1&transferdate=' + urllib.quote(nowdate) + '&ccaID=&ccaEntryId=&ccaFlag=&lastdamagedbi=0&guohuflag=0&runAreaCodeName=&assignDriver=2&haveLoan=2&LoanName=&weiFaName=&carDrivers=&oldPolicyNo=' + tokenNo + '&interimNo=' + interimNo + '&certificatedateSH=&insuredIdentifyNumber=' + IDnumber + '&appliIdentifyNumber=' + IDnumber + '&carIdentifyNumber=' + IDnumber + '&sessionId=' + sessionid
        re5 = requests.post(se.check_url, headers=headers, data=data5)

    # 第一次爬取
    data4 = {
        'haveLoan': '2',
        'licenseno': licenseNo,
        'ccaEntryId': '',
        'identifynumber': IDnumber,
        'weiFaName': '',
        'lastHas050500': '0',
        'sex': gender,
        'isRenewal': '0',
        'proSelected': proSelected,
        'nonlocalflag': '0',
        'ccaID': '',
        'startdate': startDateSYFormat,
        'endhour': '24',
        'vinno': rackNo,
        'citySelected': citySelected,
        'lastHas050210': '0',
        'insuredname': carOwner,
        'areaCodeLast': proSelected,
        'enrolldate': enrolldateFormat,
        'lastHas050200': '0',
        'licenseflag': '1',
        'isOutRenewal': '0',
        'email': '13888888@163.com',
        'ccaFlag': '',
        'frameno': rackNo,
        'fullAmountName': '',
        'channelNo': '2',
        'assignDriver': '2',
        'seatCount': seat,
        'LoanName': '',
        'lastHas050291': '',
        'guohuselect': '0',
        'cityCodeLast': citySelected,
        'runAreaCodeName': '',
        'enddate': endDateSYFormat,
        'transferdate': nowdate,
        'mobile': '13770898724',
        'transfervehicleflag': '0',
        'identifytype': carOwerIdentifyType,
        'travelMilesvalue': '',
        'seatflag': '',
        'sessionId': sessionid,
        'birthday': birthday,
        'engineno': engineNo,
        'carDrivers': '',
        'newcarflag': '0',
        'starthour': '0'
        }
    data4 = urllib.urlencode(data4)
    re4 = requests.post(url='http://www.epicc.com.cn/wap/carProposal/calculateFee/fee', headers=headers,data=data4)
    amount = jsonpath.jsonpath(eval(json.dumps(re4.json(), ensure_ascii=False, indent=4)), '$.commonPackage.items')[0][0].get('amount', "0")

    data6 = {
        "channelNo": "2",
        'haveLoan': '2',
        'licenseno': licenseNo,
        'ccaEntryId': '',
        'identifynumber': IDnumber,
        'weiFaName': '',
        'lastHas050500': '0',
        'sex': gender,
        'isRenewal': '0',
        'proSelected': proSelected,
        'nonlocalflag': '0',
        'ccaID': '',
        'startdate': startDateSYFormat,
        'endhour': '24',
        'vinno': rackNo,
        'citySelected': citySelected,
        'lastHas050210': '0',
        'insuredname': carOwner,
        'areaCodeLast': proSelected,
        'enrolldate': enrolldateFormat,
        'lastHas050200': '0',
        'licenseflag': '1',
        'isOutRenewal': '0',
        'email': '13888888@163.com',
        'ccaFlag': '',
        'frameno': rackNo,
        'fullAmountName': '',
        'channelNo': '2',
        'assignDriver': '2',
        'seatCount': seat,
        'LoanName': '',
        'lastHas050291': '',
        'guohuselect': '0',
        'cityCodeLast': citySelected,
        'runAreaCodeName': '',
        'enddate': endDateSYFormat,
        'transferdate': nowdate,
        'mobile': '13770898724',
        'transfervehicleflag': '0',
        'identifytype': carOwerIdentifyType,
        'travelMilesvalue': '',
        'seatflag': '',
        'sessionId': sessionid,
        'birthday': birthday,
        'engineno': engineNo,
        'carDrivers': '',
        'newcarflag': '0',
        'starthour': '0',
        #################
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
    data6 = urllib.urlencode(data6)
    re4 = requests.post("http://www.epicc.com.cn/wap/carProposal/calculateFee/sy", headers=headers, data=data6)
    re4 = re4.json()
    log.info(u"计算JQ=====开始")
    jq_dt = {}
    jq_dt['transferdate'] = nowdate
    jq_dt['licenseno'] = licenseNo
    jq_dt['identifynumber'] = IDnumber
    jq_dt['startDateCI'] = nowdate
    jq_dt['proSelected'] = proSelected
    jq_dt['startdate'] = startDateSYFormat
    jq_dt['vinno'] = rackNo
    jq_dt['citySelected'] = citySelected
    jq_dt['insuredname'] = carOwner
    jq_dt['areaCodeLast'] = proSelected
    jq_dt['sessionId'] = sessionid
    jq_dt['taxpayername'] = carOwner
    jq_dt['frameno'] = rackNo
    jq_dt['cityCodeLast'] = citySelected
    jq_dt['endDateCI'] = endDateSY
    jq_dt['enddate'] = endDateSYFormat
    jq_dt['enrolldate'] = enrolldateFormat
    jq_dt['birthday'] = birthday
    jq_dt['engineno'] = engineNo
    jq_dt['sex'] = gender
    jq_dt['seatCount'] = seat
    jq_resp = get_jq_epicc(jq_dt)
    try:
        PremiumInfo = translateJsonToPremiun.readJson(re4['commonPackage']['items'], seat,jq_resp)
    except:
        return re4
    data = [licenseNo, rackNo, startDateSYFormat, endDateSYFormat, seat]
    dbInsert.soupDb(PremiumInfo, data, insureCarId)
    log.info(u"计算JQ=====结束")
