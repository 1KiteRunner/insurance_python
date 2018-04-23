# -*- coding:utf-8 -*-
import time
import sys
from selenium import webdriver
import os
import requests

from common.sessionUtil import get_session
from  request_epicc.img.damatuWeb import DamatuApi
import base64
import urllib
from bs4 import BeautifulSoup
import pickle
import codecs
import time
import json
import datetime
from req_body.calAclBody import getCalActualBody
from req_body import caclBody

srssion = get_session('2')
sessBase = srssion
req_session = pickle.loads(codecs.decode(sessBase.encode(), "base64"))

def ifRenewal(licenseNo):
    mydata = "prpCrenewalVo.policyNo=&prpCrenewalVo.othFlag=&prpCrenewalVo.engineNo=&prpCrenewalVo.frameNo=&prpCrenewalVo.vinNo=&prpCrenewalVo.licenseNo=" + urllib.quote(licenseNo.encode('gb2312')) + "&prpCrenewalVo.licenseColorCode=&prpCrenewalVo.licenseType=02"
    res  = req_session.post("http://10.134.136.112:8000/prpall/business/selectRenewal.do?pageSize=10&pageNo=1",data=mydata).json()
    carData = res['data']
    if len(carData) == 0:
        print "非续保用户"
    else:
        renewal(carData)
def renewal(carData):
    bizNo = carData[0]['policyNo']
    vinNo = carData[0]['frameNo']


    url="http://10.134.136.112:8000/prpall/business/editCheckRenewal.do?bizNo="+bizNo
    res1 = req_session.get(url).json()
    proposalNo = res1['data'][0]['proposalNo']
    tomorrow = datetime.date.today() + datetime.timedelta(1)
    today = datetime.date.today()
    dateDic={
        'startDate':str(tomorrow),
        'endDate':str(datetime.datetime.strptime((str(today.year + 1) + '-' + str(today.month) + '-' + str(today.day)), "%Y-%m-%d").date()),
        'today':str(today)
    }

    print "开始获取车管所验证码"
    vcode_url = "http://10.134.136.112:8000/prpall/business/queryVehiclePMCheck.do?comCode=32012105&frameNo=" + vinNo + "&licenseNo="
    vcode_res = req_session.post(vcode_url)
    vcode_base64 = json.loads(vcode_res.content)['data'][0]['checkCode']
    checkNo = json.loads(vcode_res.content)['data'][0]['checkNo']
    dmt = DamatuApi()
    codestr = dmt.decode(base64.b64decode(vcode_base64), 200)

    """
    通过车架号查询车管所信息
   """
    carinfo_url = "http://10.134.136.112:8000/prpall/business/queryVehiclePMConfirm.do?comCode=32012105&checkNo=" + checkNo + "&checkCode=" + codestr
    carinfo_res = req_session.post(carinfo_url)

    """
    结果
    """
    engineNo = carData[0]['engineNo']
    licenseNo = carData[0]['licenseNo']
    ciEndDate = dateDic['endDate']
    operateDate = dateDic['today']
    enrollDate = time.strftime("%Y-%m-%d", time.localtime(int(json.loads(carinfo_res.content)['data'][0]['enrollDate']['time']) / 1000))
    insuredName = json.loads(carinfo_res.content)['data'][0]['carOwner']
    modelCode = json.loads(carinfo_res.content)['data'][0]['modelCode']




    url0="http://10.134.136.112:8000/prpall/business/copyProposal.do?bizNo="+proposalNo
    res0 = req_session.get(url0)
    soup0 = BeautifulSoup(res0.content.decode('gbk'), "html.parser")


    url1 = "http://10.134.136.112:8000/prpall/business/editCitemCar.do?editType=COPY_PROPOSAL&bizType=PROPOSAL&bizNo="+proposalNo+"&riskCode=DAA&applyNo=&startDate="+dateDic['startDate']+"&endDate="+dateDic['endDate']+"&startHour=0&endHour=24&endorType=&taskID_Ppms=&prpallLinkPpmsFlag=&operateDate="+dateDic['today']+"&motorFastTrack=&operatorProjectCode=&reload=&rnd446=Tue+Feb+23+09%3a21%3a14+UTC+0800+2017"
    res1 = req_session.get(url1)
    soup1 = BeautifulSoup(res1.content.decode('gbk'), "html.parser")

    url2 = "http://10.134.136.112:8000/prpall/business/editCitemKind.do?editType=COPY_PROPOSAL&bizType=PROPOSAL&bizNo="+proposalNo+"&riskCode=DAA&applyNo=&startDate="+dateDic['startDate']+"&endDate="+dateDic['endDate']+"&startHour=0&endHour=24&endorType=&taskID_Ppms=&prpallLinkPpmsFlag=&operateDate="+dateDic['today']+"&motorFastTrack=&operatorProjectCode=&reload=&rnd559=Tue+Feb+23+09%3a21%3a14+UTC+0800+2017"
    res2 = req_session.get(url2)
    soup2 = BeautifulSoup(res2.content.decode('gbk'), "html.parser")

    url3="http://10.134.136.112:8000/prpall/business/editCmainTotal.do?editType=COPY_PROPOSAL&bizType=PROPOSAL&bizNo="+proposalNo+"&riskCode=DAA&applyNo=&startDate="+dateDic['startDate']+"&endDate="+dateDic['endDate']+"&startHour=0&endHour=24&endorType=&taskID_Ppms=&prpallLinkPpmsFlag=&operateDate="+dateDic['today']+"&motorFastTrack=&operatorProjectCode=&reload=&rnd459=Tue+Feb+23+09%3a21%3a14+UTC+0800+2017"
    res3 = req_session.get(url3)
    soup3 = BeautifulSoup(res3.content.decode('gbk'), "html.parser")
    # print soup3.find(id="prpCmain.sumAmount").get('value')


    url4="http://10.134.136.112:8000/prpall/business/editCitemKindCI.do?editType=COPY_PROPOSAL&bizType=PROPOSAL&bizNo="+proposalNo+"&riskCode=DAA&applyNo=&startDate="+dateDic['startDate']+"&endDate="+dateDic['endDate']+"&startHour=0&endHour=24&endorType=&taskID_Ppms=&prpallLinkPpmsFlag=&operateDate="+dateDic['today']+"&motorFastTrack=&operatorProjectCode=&reload=&rnd669=Tue+Feb+23+09%3a21%3a14+UTC+0800+2017"
    res4 = req_session.get(url4)
    soup4 = BeautifulSoup(res4.content.decode('gbk'), "html.parser")
    print soup4

    personUrl = "http://10.134.136.112:8000/prpall/business/editCinsured.do?editType=COPY_PROPOSAL&bizType=PROPOSAL&bizNo="+proposalNo+"&riskCode=DAA&applyNo=&startDate="+dateDic['startDate']+"&endDate="+dateDic['endDate']+"&startHour=0&endHour=24&endorType=&taskID_Ppms=&prpallLinkPpmsFlag=&operateDate="+dateDic['today']+"&motorFastTrack=&operatorProjectCode=&reload=&rnd725=Tue+Feb+23+09%3a21%3a14+UTC+0800+2017"
    personRes = req_session.get(personUrl)
    personSoup = BeautifulSoup(personRes.content, "html.parser")
    IdMumber = personSoup.find(id="prpCinsureds[0].identifyNumber").get('value')  # 身份证号
    phoneNumber = personSoup.find(id="prpCinsureds[0].mobile").get('value')
    insuredAddress = personSoup.find(id="prpCinsureds[0].insuredAddress").get('value').encode('latin1').decode('gbk')

    purchasePrice = soup1.find(id='prpCitemCar.purchasePrice').get('value')
    exhaustScale = soup1.find(id='prpCitemCar.exhaustScale').get('value')
    prpCitemCar_brandName = soup1.find(id='prpCitemCar.brandName').get('value')#带中文的车型名称
    prpCitemCar_modelCode = soup1.find(id='prpCitemCar.modelCode').get('value')#车型行业编码
    ciStartDate = dateDic['startDate']
    taxPlatFormTime = soup4.find(id='taxPlatFormTime').get('value')
    seatCount = soup1.find(id='prpCitemCar.seatCount').get('value')
    prpCitemKindsTemp0_rate = soup2.find(id='prpCitemKindsTemp[0].rate').get('value')
    prpCitemKindsTemp3_premium = soup2.find(id='prpCitemKindsTemp[3].premium').get('value')
    prpCitemKindsTemp4_benchMarkPremium = soup2.find(id='prpCitemKindsTemp[4].benchMarkPremium').get('value')
    prpCitemKindsTemp3_benchMarkPremium = soup2.find(id='prpCitemKindsTemp[3].benchMarkPremium').get('value')
    randomProposalNo = soup0.find(id="randomProposalNo").get('value')
    prpCitemKindsTemp12_benchMarkPremium=""#soup2.find(id='prpCitemKindsTemp[12].benchMarkPremium').get('value')
    prpCitemKindsTemp11_disCount=soup2.find(id='prpCitemKindsTemp[11].disCount').get('value')
    prpCitemKindsTemp0_benchMarkPremium = soup2.find(id='prpCitemKindsTemp[0].benchMarkPremium').get('value')
    prpCitemKindsTemp10_benchMarkPremium = soup2.find(id='prpCitemKindsTemp[10].benchMarkPremium').get('value')
    prpCitemKindsTemp3_rate = soup2.find(id='prpCitemKindsTemp[3].rate').get('value')
    purchasePriceUp = soup1.find(id='purchasePriceUp').get('value')
    prpCitemKindsTemp10_premium =  soup2.find(id='prpCitemKindsTemp[10].premium').get('value')
    prpCitemKindsTemp_premium = ""#soup2.find(id='prpCitemKindsTemp[12].premium').get('value')
    prpCitemKindsTemp12_disCount = ""#soup2.find(id='prpCitemKindsTemp[12].disCount').get('value')
    prpCmain_underWriteEndDate = soup0.find(id='prpCmain.underWriteEndDate').get('value')
    prpCitemKindsTemp3_disCount = soup2.find(id='prpCitemKindsTemp[3].disCount').get('value')
    prpCmain_sumAmount = soup3.find(id='prpCmain.sumAmount').get('value')
    prpCitemKindsTemp10_disCount = soup2.find(id='prpCitemKindsTemp[10].disCount').get('value')
    prpCmain_sumDiscount = soup3.find(id='prpCmain.sumDiscount').get('value')
    prpCitemKindsTemp0_basePremium = soup2.find(id='prpCitemKindsTemp[0].basePremium').get('value')
    prpCitemKindsTemp13_benchMarkPremium = ""#soup2.find(id='prpCitemKindsTemp[13].benchMarkPremium').get('value')
    prpCitemKindsTemp0_disCount = soup2.find(id='prpCitemKindsTemp[0].disCount').get('value')
    basePremiu = soup2.find(id='prpCitemKindsTemp[2].basePremium').get('value')
    carLotEquQuality = soup1.find(id='prpCitemCar.carLotEquQuality').get('value')
    prpCitemKindsTemp4_premium = soup2.find(id='prpCitemKindsTemp[4].premium').get('value')
    prpCitemKindsTemp11_benchMarkPremium = soup2.find(id='prpCitemKindsTemp[11].benchMarkPremium').get('value')
    prpCitemKindsTemp2_benchMarkPremium = soup2.find(id='prpCitemKindsTemp[2].benchMarkPremium').get('value')
    prpCitemKindsTemp4_disCount = soup2.find(id='prpCitemKindsTemp[4].disCount').get('value')

    cacAclData={
        'operatorCode':'A320100259',
        'licenseNo': licenseNo,
        'enrollDate': enrollDate,
        'homePhone': phoneNumber,#
        'ciEndDate':ciEndDate,
        'operateDate': operateDate,
        'purchasePrice': purchasePrice,
        'pmCarOwner': insuredName,
        'exhaustScale': exhaustScale,
        'OperateDate': operateDate,
        'engineNo': engineNo,
        'brandName': prpCitemCar_brandName,
        'ciStartDate': ciStartDate,
        'checkNo': checkNo,
        'vinNo': vinNo,
        'modelCode': prpCitemCar_modelCode,
        'checkAnswer': codestr,
        'taxPlatFormTime': taxPlatFormTime,
        'checkCode': vcode_base64
    }
    calActualValue_data = getCalActualBody(cacAclData)
    calActualValue_url = "http://10.134.136.112:8000/prpall/business/calActualValue.do"
    actualValue = req_session.post(calActualValue_url, data=calActualValue_data).content


    cacPrumeData={
        'licenseNo': licenseNo,
        'engineNo': engineNo,
        'vinNo': vinNo,
        'enrollDate': enrollDate,
        'ciEndDate': ciEndDate,
        'brandName':prpCitemCar_brandName,
        'purchasePrice':purchasePrice,
        'actualValue':actualValue,
        'exhaustScale':exhaustScale,
        'seatCount':seatCount,
        'pmCarOwner':insuredName,
        'taxPayerIdentNo':IdMumber,
        'insuredAddress':insuredAddress,
        'homePhone': phoneNumber,
        'checkAnswer':codestr,
        'prpCitemKindsTemp0_rate':prpCitemKindsTemp0_rate,
        'prpCitemKindsTemp3_premium':prpCitemKindsTemp3_premium,
        'prpCitemKindsTemp4_benchMarkPremium':prpCitemKindsTemp4_benchMarkPremium,
        'prpCitemKindsTemp3_benchMarkPremium':prpCitemKindsTemp3_benchMarkPremium,
        'randomProposalNo':randomProposalNo,
        'prpCitemKindsTemp12_benchMarkPremium':prpCitemKindsTemp12_benchMarkPremium,
        'prpCitemKindsTemp11_disCount':prpCitemKindsTemp11_disCount,
        'prpCitemKindsTemp0_benchMarkPremium':prpCitemKindsTemp0_benchMarkPremium,
        'prpCitemKindsTemp10_benchMarkPremium':prpCitemKindsTemp10_benchMarkPremium,
        'prpCitemKindsTemp3_rate':prpCitemKindsTemp3_rate,
        'purchasePriceUp':purchasePriceUp,
        'prpCitemKindsTemp10_premium':prpCitemKindsTemp10_premium,
        'prpCitemKindsTemp_premium':prpCitemKindsTemp_premium,
        'prpCitemKindsTemp12_disCount':prpCitemKindsTemp12_disCount,
        'prpCmain_underWriteEndDate':prpCmain_underWriteEndDate,
        'prpCitemKindsTemp3_disCount':prpCitemKindsTemp3_disCount,
        'prpCmain_sumAmount':prpCmain_sumAmount,
        'prpCitemKindsTemp10_disCount':prpCitemKindsTemp10_disCount,
        'prpCmain_sumDiscount':prpCmain_sumDiscount,
        'prpCitemKindsTemp0_basePremium':prpCitemKindsTemp0_basePremium,
        'prpCitemKindsTemp13_benchMarkPremium':prpCitemKindsTemp13_benchMarkPremium,
        'prpCitemKindsTemp0_disCount':prpCitemKindsTemp0_disCount,
        'basePremiu':basePremiu,
        'carLotEquQuality':carLotEquQuality,
        'prpCitemKindsTemp4_premium':prpCitemKindsTemp4_premium,
        'prpCitemKindsTemp11_benchMarkPremium':prpCitemKindsTemp11_benchMarkPremium,
        'prpCitemKindsTemp2_benchMarkPremium':prpCitemKindsTemp2_benchMarkPremium,
        'prpCitemKindsTemp4_disCount':prpCitemKindsTemp4_disCount,
        'today':dateDic['today'],
        'checkCode': vcode_base64,
        'checkNo':checkNo,
        'modelCode':prpCitemCar_modelCode,
        'ciStartDate':dateDic['startDate']
    }
    data = caclBody.getCaclBody(cacPrumeData)
    res = req_session.post("http://10.134.136.112:8000/prpall/business/caculatePremiunForFG.do", data=data)
    print res.content


    # url2="http://10.134.136.112:8000/prpall/business/editCitemCar.do?editType=COPY_PROPOSAL&bizType=PROPOSAL&bizNo="+proposalNo+"&riskCode=DAA&applyNo=&startDate="+dateDic['startDate']+"&endDate="+dateDic['endDate']+"&startHour=0&endHour=24&endorType=&taskID_Ppms=&prpallLinkPpmsFlag=&operateDate="+dateDic['today']+"&motorFastTrack=&operatorProjectCode=&reload=&rnd446=Tue%20Feb%2021%2018:21:14%20UTC+0800%202017"
    # res2 = req_session.get(url2)
    # # print res.content.decode('gbk')
    # url3="http://10.134.136.112:8000/prpall/business/editCitemKind.do?editType=COPY_PROPOSAL&bizType=PROPOSAL&bizNo="+proposalNo+"&riskCode=DAA&applyNo=&startDate="+dateDic['startDate']+"&endDate="+dateDic['endDate']+"&startHour=0&endHour=24&endorType=&taskID_Ppms=&prpallLinkPpmsFlag=&operateDate="+dateDic['today']+"&motorFastTrack=&operatorProjectCode=&reload=&rnd559=Tue%20Feb%2021%2017:21:25%20UTC+0800%202017"
    # res3 = req_session.get(url2)
    # # print res2.content.decode('gbk')
    # url4 = "http://10.134.136.112:8000/prpall/business/editCengage.do?editType=COPY_PROPOSAL&bizType=PROPOSAL&bizNo=" + proposalNo + "&riskCode=DAA&applyNo=&startDate=" + dateDic['startDate'] + "&endDate=" + dateDic['endDate'] + "&startHour=0&endHour=24&endorType=&taskID_Ppms=&prpallLinkPpmsFlag=&operateDate=" + dateDic['today'] + "&motorFastTrack=&operatorProjectCode=&reload=&rnd559=Tue%20Feb%2021%2017:21:25%20UTC+0800%202017"
    # res4 = req_session.get(url2)
    # print res4.content.decode('gbk')
if __name__=="__main__":
    licenseNo=u"苏NXL789"
    ifRenewal(licenseNo)