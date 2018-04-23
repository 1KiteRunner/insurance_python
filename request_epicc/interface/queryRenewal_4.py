# -*- coding:utf-8 -*-
__author__ = 'weikai'
import sys

import  requests

reload(sys)
sys.setdefaultencoding('utf-8')
import json
import datetime
import ast
from  request_epicc import settings as se
from common.log import  Logger
from carInput1_1 import carInput1_1
from request_epicc.img import imagebse64
from request_epicc import utils
import urllib
import jsonpath
import translateJsonToPremiun
import dbInsert
log=Logger()

headers=se.headers
headers['Referer']='http://www.epicc.com.cn/wap/carProposal/car/carInput1'
s = requests.session()
s.headers.update(headers)
sessionid= carInput1_1(s)
licenseNo ="苏AB9N73"
beforeProposalNo = "320124196612020626"
gender = ""
if int(beforeProposalNo[16:17])%2==0:
     gender = 2
else:
     gender = 1
birthday = beforeProposalNo[6:10]+'/'+beforeProposalNo[10:12]+'/'+beforeProposalNo[12:14]
nowdate = str(datetime.date.today()).replace('-','/')
data='proSelected=32000000&citySelected=32010000&beforeProposalNo='+beforeProposalNo+'&licenseNo='+urllib.quote(licenseNo)+'&sessionId=' \
     + sessionid

res=s.post(url=se.queryRenewal_url,data=data)
body = res.json()
body=json.dumps(body,ensure_ascii=False,indent=4)
body=eval(body)
# log.info(u'用户信息为:%s:' % body)
#车牌号
licenseNo=jsonpath.jsonpath(body,'$.appliCarInfo.licenseNo')[0]
#车架号
rackNo=jsonpath.jsonpath(body,'$.appliCarInfo.rackNo')[0]
#tokenNo #beforeProposalNo
tokenNo=jsonpath.jsonpath(body,'$.tokenNo')[0]
lastHas050200=jsonpath.jsonpath(body,'$.lastHas050200')[0]
lastHas050210=jsonpath.jsonpath(body,'$.lastHas050210')[0]
lastHas050291=jsonpath.jsonpath(body,'$.lastHas050291')[0]
lastHas050310=jsonpath.jsonpath(body,'$.lastHas050310')[0]
lastHas050500=jsonpath.jsonpath(body,'$.lastHas050500')[0]
isOutRenewal=jsonpath.jsonpath(body,'$.isOutRenewal')[0]
guoHuSelect=jsonpath.jsonpath(body,'$.guoHuSelect')[0]
appliCarInfo=jsonpath.jsonpath(body,'$.appliCarInfo.seatFlag')[0]
nonlocalflag=jsonpath.jsonpath(body,'$.nonlocalflag')[0]
assignDriver=jsonpath.jsonpath(body,'$.assignDriver')[0]
enrolldate=jsonpath.jsonpath(body,'$.appliCarInfo.enrollDate')[0]
enrolldateFormat = enrolldate.replace('/','-')
haveLoan=jsonpath.jsonpath(body,'$.haveLoan')[0]
LoanName=jsonpath.jsonpath(body,'$.loanName')[0]
carOwerIdentifyType=jsonpath.jsonpath(body,'$.carOwnerInfo.carOwerIdentifyType')[0]
carOwnerIdentifyNumber=e=jsonpath.jsonpath(body,'$.carOwnerInfo.carOwnerIdentifyNumber')[0]
carOwner=jsonpath.jsonpath(body,'$.carOwnerInfo.carOwner')[0]
rackNo=jsonpath.jsonpath(body,'$.appliCarInfo.rackNo')[0]
engineNo=jsonpath.jsonpath(body,'$.appliCarInfo.engineNo')[0]
seatFlag=jsonpath.jsonpath(body,'$.appliCarInfo.seatFlag')[0]
startDateSY = jsonpath.jsonpath(body,'$.startDateSY')[0]
startDateSYFormat = startDateSY.replace('/','-')
endDateSY = jsonpath.jsonpath(body,'$.endDateSY')[0]
endDateSYFormat = endDateSY.replace('/','-')
seat = jsonpath.jsonpath(body,'$.appliCarInfo.seat')[0]
standardName = jsonpath.jsonpath(body,'$.appliCarInfo.standardName')[0]
insuredIdentifyAddr = jsonpath.jsonpath(body,'$.insuredInfo.insuredIdentifyAddr')[0]
# log.info('licenseNo=%s:'% licenseNo)
# log.info('rackNo=%s:' % rackNo)
# log.info('tokenNo=%s:' % tokenNo)
# log.info('carOwner=%s:' % carOwner)
# log.info('engineNo=%s:' % engineNo)
# log.info('carOwnerIdentifyNumber=%s:' % carOwnerIdentifyNumber)
# log.info('lastHas050200=%s:'% lastHas050200)
# log.info('lastHas050210=%s:' % lastHas050210)
# log.info('lastHas050291=%s:' % lastHas050291)
# log.info('lastHas050500=%s:'% lastHas050500)
# log.info('isOutRenewal=%s:' % isOutRenewal)
# log.info('guoHuSelect=%s:' % guoHuSelect)
# log.info('appliCarInfo=%s:'% appliCarInfo)
# log.info('nonlocalflag=%s:' % nonlocalflag)
# log.info('assignDriver=%s:' % assignDriver)
# log.info('enrolldate=%s:'% enrolldate)
# log.info('haveLoan=%s:' % haveLoan)
# log.info('LoanName=%s:' % LoanName)

url9 = "http://www.epicc.com.cn/wap/carProposal/car/interim"
data9 ='mobileflag=1&licenseno='+urllib.quote(licenseNo)+'&sessionId='+sessionid+'&proSelected=32000000&citySelected=32010000&areaCodeLast=32000000&cityCodeLast=32010000&insuredIdentifSex=2&insuredBirthday='+urllib.quote(birthday)+'&lastcarownername='+urllib.quote(carOwner)+'&startdate='+startDateSYFormat+'&starthour=0&enddate='+endDateSYFormat+'&endhour=24&startDateCI='+startDateSYFormat+'&startHourCI=0&endDateCI='+endDateSYFormat+'&endHourCI=24&engineno='+engineNo+'&vinno='+rackNo+'&frameno='+rackNo+'&enrolldate='+enrolldateFormat+'&standardName='+urllib.quote(standardName)+'&seatcount='+seat+'&linkAddress=&runAreaCodeName=11&assignDriver=2&carDrivers=%5B%5D&haveLoan=2&LoanName=&guohuselect=0&transferdate=&fullAmountName=8&appliEmail=135%40163.com&appliIdentifyNumber='+beforeProposalNo+'&appliIdentifyType=01&appliMobile=15251891862&appliName='+urllib.quote(carOwner)+'&taxPayerIdentNo='+beforeProposalNo+'&taxPayerName=&aliasName=&carOwerIdentifyType=01&carOwner='+urllib.quote(carOwner)+'&insuredEmail=135%40163.com&insuredIdentifyAddr='+urllib.quote(insuredIdentifyAddr)+'&insuredIdentifyType=01&insuredIdentifyNumber='+beforeProposalNo+'&insuredMobile=13888888888&argueSolution=&insuredAndOwnerrelate=&arbitboardname=&appliAddName='+urllib.quote(carOwner)+'&deliverInfoPro=320000&deliverInfoCity=320100&deliverInfoDistrict=&appliPhoneNumber=13888888888&invoiceTitle=&itemKindFlag=1&travelMilesvalue=&licenseflag=1&certificatedate=&monopolyname=&weiFaName=6&isRenewal=1&interimNo=&beforeProposalNo='+tokenNo+'&taxPayerIdentType=&carKindCI=&bjfuel_type=&certificate_type=&certificate_no=&certificate_date=&carIdentifyAddressSX=&carNameSX=&carKindSX=&ccaId='
re9 = s.post(se.interim_url,data=data9)
re9 = s.post(url9,data=data9)
interimNo = str(re9.json()['interimNo'])

#####获取车管所验证码
headers['Referer']='http://www.epicc.com.cn/wap/carProposal/car/carInput2'
data2='licenseNo='+urllib.quote(licenseNo)+'&frameNo='+rackNo+'&channelNo=2&sessionId='+sessionid
re2=s.post(url='http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerificationCode',data=data2)
body2 = re2.json()
code_msg=body2['message']
code_msg=eval(code_msg)
#log.info("code_msg=%s" % code_msg)
check_code = jsonpath.jsonpath(code_msg,'$.check_code')[0]

log.info("check_code=%s" % check_code)
fname='../image/'+utils.getTimstamp()+'.jpg'
#log.info('code =%s'% check_code)
log.info('picnam =%s'% fname)
imagebse64.base642img(check_code,fname)
codestr=utils.pic2Str(fname)
log.info(u"验证码为=%s,文件名为=%s"% (codestr, fname))

#发送验证码
data3='icationCode='+codestr+'&channelNo=2&sessionId='+sessionid
re3=s.post(url='http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerifQueryCar',data=data3)
body3=re3.json()
body3 = ast.literal_eval(body3['message'])
code = body3['head']['errorCode']
while code=='93037':
     #####获取车管所验证码
     headers['Referer'] = 'http://www.epicc.com.cn/wap/carProposal/car/carInput2'
     data2 = 'licenseNo=' + urllib.quote(licenseNo) + '&frameNo=' + rackNo + '&channelNo=2&sessionId=' + sessionid
     re2 = s.post(url='http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerificationCode', data=data2)
     body2 = re2.json()
     code_msg = body2['message']
     code_msg = eval(code_msg)
     # log.info("code_msg=%s" % code_msg)
     check_code = jsonpath.jsonpath(code_msg, '$.check_code')[0]

     log.info("check_code=%s" % check_code)
     fname = '../image/' + utils.getTimstamp() + '.jpg'
     # log.info('code =%s'% check_code)
     log.info('picnam =%s' % fname)
     imagebse64.base642img(check_code, fname)
     codestr = utils.pic2Str(fname)
     log.info(u"验证码为=%s,文件名为=%s" % (codestr, fname))
     data3 = 'icationCode=' + codestr + '&channelNo=2&sessionId=' + sessionid
     re3 = s.post(url='http://www.epicc.com.cn/wap/carProposal/JSArea/obtainVerifQueryCar', data=data3)
     body3 = re3.json()
     body3 = ast.literal_eval(body3['message'])
     code = body3['head']['errorCode']




headers['Referer']='http://www.epicc.com.cn/wap/carProposal/car/carInput2'
data5='lastcarownername='+urllib.quote(carOwner)+'&channelNo=2&areaCodeLast=32000000&cityCodeLast=32010000&proSelected=32000000&citySelected=32010000&startdate='+startDateSYFormat+'&starthour=0&enddate='+endDateSYFormat+'&endhour=24&licenseno='+urllib.quote(licenseNo)+'&engineno='+engineNo+'&vinno='+rackNo+'&frameno='+rackNo+'&seatcount='+seat+'&carOwner='+urllib.quote(carOwner)+'&isRenewal=1&enrolldate='+enrolldateFormat+'&guohuselect=0&licenseflag=1&isOutRenewal=0&lastHas050200=1&lastHas050210=0&lastHas050500=0&seatflag=1&transferdate='+urllib.quote(nowdate)+'&ccaID=&ccaEntryId=&ccaFlag=&lastdamagedbi=0&guohuflag=0&runAreaCodeName=&assignDriver=2&haveLoan=2&LoanName=&weiFaName=&carDrivers=&oldPolicyNo='+tokenNo+'&interimNo='+interimNo+'&certificatedateSH=&insuredIdentifyNumber='+beforeProposalNo+'&appliIdentifyNumber='+beforeProposalNo+'&carIdentifyNumber='+beforeProposalNo+'&sessionId='+sessionid
re5 = s.post('http://www.epicc.com.cn/wap/carProposal/underWrite/underwriteCheckProfitAjax',data=data5)



data4=("proSelected=32000000&citySelected=32010000&areaCodeLast=32000000&cityCodeLast=32010000&mobile=15905175343&email=%s\
&identifytype=%s\
&identifynumber=%s\
&birthday=%s\
&sex=%s\
&beforeProposalNo=%s\
&startdate=%s\
&starthour=0\
&enddate=%s\
&endhour=24\
&licenseno=%s\
&nonlocalflag=%s\
&licenseflag=1\
&engineno=%s\
&vinno=%s\
&frameno=%s\
&enrolldate=%s\
&transfervehicleflag=0\
&insuredname=%s\
&fullAmountName=\
&startDateCI=%s\
&starthourCI=0\
&endDateCI=%s\
&endhourCI=24\
&sessionId=%s\
&seatflag=%s\
&isOutRenewal=%s\
&lastHas050200=%s\
&lastHas050210=%s\
&lastHas050500=%s\
&lastHas050291=%s\
&transferdate=%s\
&guohuselect=0\
&runAreaCodeName=\
&assignDriver=%s\
&haveLoan=%s\
&LoanName=%s\
&weiFaName=\
&seatCount=%s\
&carDrivers=\
&travelMilesvalue=\
&lastdamageBI=0\
&ccaFlag=\
&ccaID=\
&ccaEntryId=\
&noDamyearsBI=1" % (urllib.quote('2290@qq.com'),carOwerIdentifyType,carOwnerIdentifyNumber,urllib.quote(birthday),gender,tokenNo,startDateSYFormat,endDateSYFormat,urllib.quote(licenseNo),nonlocalflag,engineNo,rackNo,rackNo,enrolldateFormat,urllib.quote(carOwner),urllib.quote(startDateSY),urllib.quote(endDateSY),sessionid,seatFlag,isOutRenewal,lastHas050200,lastHas050210,lastHas050500,lastHas050291,urllib.quote(nowdate),assignDriver,haveLoan,LoanName,seat))
headers['Referer']='http://www.epicc.com.cn/wap/carProposal/car/calculateFee'
#data4=urllib.quote(data4)
re4=s.post(url='http://www.epicc.com.cn/wap/carProposal/calculateFee/renewalfee',data=data4)
amount = jsonpath.jsonpath(eval(json.dumps(re4.json(),ensure_ascii=False,indent=4)),'$.commonPackage.items')[0][0].get('amount',"0")


# headers["8rtCaPoAWP"]=re4.cookies.get("8rtCaPoAWP")
# headers["EcutH7WVc8"]=re4.cookies.get("EcutH7WVc8")
# headers["JSESSIONID"]=re4.cookies.get("JSESSIONID")
data6=("channelNo=2&proSelected=32000000&citySelected=32010000&areaCodeLast=32000000&cityCodeLast=32010000&mobile=15905175343&email=%s\
&identifytype=%s\
&identifynumber=%s\
&birthday=%s\
&sex=%s\
&beforeProposalNo=%s\
&startdate=%s\
&starthour=0\
&enddate=%s\
&endhour=24\
&licenseno=%s\
&nonlocalflag=%s\
&licenseflag=1\
&engineno=%s\
&vinno=%s\
&frameno=%s\
&enrolldate=%s\
&transfervehicleflag=0\
&insuredname=%s\
&fullAmountName=\
&startDateCI=%s\
&starthourCI=0\
&endDateCI=%s\
&endhourCI=24\
&sessionId=%s\
&seatflag=%s\
&isOutRenewal=%s\
&lastHas050200=%s\
&lastHas050210=%s\
&lastHas050500=%s\
&lastHas050291=%s\
&transferdate=%s\
&guohuselect=0\
&runAreaCodeName=\
&assignDriver=%s\
&haveLoan=%s\
&LoanName=%s\
&weiFaName=\
&seatCount=%s\
&carDrivers=\
&travelMilesvalue=\
&lastdamageBI=0\
&ccaFlag=\
&ccaID=\
&ccaEntryId=\
&noDamyearsBI=1&ccaFlag=&ccaID=&ccaEntryId=&BZ_selected=2&select_050200=%s&select_050600=500000&select_050500=%s&select_050701=10000&select_050702=10000&select_050310=%s&select_050231=10&select_050270=&select_050210=2000&select_050252=-1&select_050291=1&select_050911=1&select_050912=1&select_050921=1&select_050922=1&select_050924=1&select_050928=1&select_050330=&select_050935=-1&select_050918=-1&select_050919=&select_050917=-1&select_050451=-1&select_050642=-1&select_050641=&select_050643=-1&select_050929=1" % (urllib.quote('2290@qq.com'),carOwerIdentifyType,carOwnerIdentifyNumber,urllib.quote(birthday),gender,tokenNo,startDateSYFormat,endDateSYFormat,urllib.quote(licenseNo),nonlocalflag,engineNo,rackNo,rackNo,enrolldateFormat,urllib.quote(carOwner),urllib.quote(startDateSY),urllib.quote(endDateSY),sessionid,seatFlag,isOutRenewal,lastHas050200,lastHas050210,lastHas050500,lastHas050291,urllib.quote(nowdate),assignDriver,haveLoan,LoanName,seat,amount,amount,amount))

#data4=urllib.quote(data4)
re4=s.post(url='http://www.epicc.com.cn/wap/carProposal/calculateFee/sy',data=data6)

re4=re4.json()
# re4=json.dumps(re4,ensure_ascii=False,indent=4)
PremiumInfo = translateJsonToPremiun.readJson(re4['commonPackage']['items'],seat)
data = [licenseNo,rackNo,startDateSYFormat,endDateSYFormat,seat]
dbInsert.soupDb(PremiumInfo,data)


