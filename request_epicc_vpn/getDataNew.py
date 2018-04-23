# -*- coding:utf-8 -*-
import sys
import base64
import urllib
import cPickle as pickle
import codecs
import time
import json
import datetime

from bs4 import BeautifulSoup

from MyAdapter import MyAdapter
from common.sessionUtil import get_session
from common.timeUtil import getlatedate
from  request_epicc.img.damatuWeb import DamatuApi

from req_body.calAclBodyNew import getCalAclData
from req_body.caclBodyNew import getCaclData
from calcUserYears import calc_user_years
from common.log import Logger
from translateJsonToPremiun import readJson

log=Logger()
global null, false, true
sys.modules['MyAdapter.MyAdapter'] = MyAdapter
null = None
false = False
true = True
import re
from my_dbUtil.dbInsert import soupDb
from common.mongodb.mgdboperate import inser_user_renewal


def strat(renewal_data_dt,endData=""):
    log.error("start")
    srssion = get_session('2')
    sessBase = srssion
    req_session = pickle.loads(codecs.decode(sessBase.encode(), "base64"))
    req_session.mount('https://', MyAdapter())
    licenseNo = renewal_data_dt.get('plateNumber', '')
    searchVin = renewal_data_dt.get('vinNo', '')
    insuranceType = renewal_data_dt['insuranceType']
    insure_id = renewal_data_dt['insureCarId']
    group_id = insuranceType['insuranceTypeGroupId']
    newPrimue(licenseNo, searchVin, req_session, insuranceType,insure_id,group_id,endData)




def compare_date(str_date1, str_date2):
    str_date1 = str_date1.split(" ")[0]
    str_date2 = str_date2.split(" ")[0]
    str_date1 = datetime.datetime.strptime(str_date1, "%Y-%m-%d")
    str_date2 = datetime.datetime.strptime(str_date2, "%Y-%m-%d")
    if str_date1.date() >= str_date2.date():
        return str_date2.date()
    else:
        return str_date2.date()

def compare_time40(endtime="2017-04-03 23:59:59"):
    try:
        if " " not in endtime:
            endtime=endtime+" 23:59:59"

        currnt_time=int(time.time())
        endtime=conver_timestamp(endtime)
        out=(endtime-currnt_time)/86400
        return out
    except:
        return 10#如果有异常随便给个小于40的

def conver_timestamp(dt="2016-05-05 20:28:54"):
    # 转换成时间数组
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    timestamp = time.mktime(timeArray)
    return int(timestamp)

def check(licenseNo,licenseType="02"):
    log.info(u"开始查询续保")
    srssion = get_session('2')
    sessBase = srssion
    req_session = pickle.loads(codecs.decode(sessBase.encode(), "base64"))
    req_session.mount('https://', MyAdapter())
    if_renewal_url="http://10.134.136.112:8000/prpall/business/selectRenewalPolicyNo.do?licenseNo="+ urllib.quote(licenseNo.encode('gb2312')) + "&licenseFlag=1&licenseType="+licenseType
    if_renewal_res = req_session.post(if_renewal_url,verify=False).json()
    if int(if_renewal_res['data'][0]['renewalFlag']) == 0:
        log.error(licenseNo+"不可续保")
        return 0
    else:
        mydata = "prpCrenewalVo.policyNo=&prpCrenewalVo.othFlag=&prpCrenewalVo.engineNo=&prpCrenewalVo.frameNo=&prpCrenewalVo.vinNo=&prpCrenewalVo.licenseNo=" + urllib.quote(licenseNo.encode('gb2312')) + "&prpCrenewalVo.licenseColorCode=&prpCrenewalVo.licenseType="+licenseType
        data = req_session.post("http://10.134.136.112:8000/prpall/business/selectRenewal.do?pageSize=10&pageNo=1",data=mydata)
        carData = data.json()['data']
        for car in carData:
            car['endDate'] = car['endDate']['time']
        carData.sort(key=lambda obj: obj.get('endDate'))
        bizNo = carData[len(carData) - 1]['policyNo']
        res = req_session.post("http://10.134.136.112:8000/prpall/business/editCheckRenewal.do?bizNo=" + bizNo)
        proposalNo = res.json()['data'][0]['proposalNo']
        startDate = datetime.date.today() + datetime.timedelta(1)
        endDateSY1 = (str(startDate.year + 1) + '-' + str(startDate.month) + '-' + str(startDate.day))
        endDateSY = datetime.datetime.strptime(endDateSY1, "%Y-%m-%d").date() + datetime.timedelta(-1)
        today = datetime.date.today()
        editType = "COPY_PROPOSAL"
        if proposalNo is None:
            editType = "RENEWAL"
            proposalNo = bizNo
        url = "http://10.134.136.112:8000/prpall/business/editCitemCar.do?editType=" + editType + "&bizType=PROPOSAL&bizNo=" + proposalNo + "&riskCode=DAA&applyNo=&startDate=" + str(startDate) + "&endDate=" + str(endDateSY) + "&startHour=0&endHour=24&endorType=&taskID_Ppms=&prpallLinkPpmsFlag=&operateDate=" + str(today) + "&motorFastTrack=&operatorProjectCode=&reload=&rnd934="
        carRes = req_session.get(url)
        soup = BeautifulSoup(carRes.content, "html.parser")
        carDic = {}
        carDic['COMPANY_ID'] = '2'
        carDic['FLAG'] = '1'
        carDic['CCardDetail'] = ""
        carDic['brandName'] = soup.find(id="prpCitemCar.brandName").get('value').encode('latin1').decode('gbk')  # 车辆型号
        carDic['enrollDate'] = soup.find(id="prpCitemCar.enrollDate").get('value')  # 注册时间
        carDic['engineNo'] = soup.find(id="prpCitemCar.engineNo").get('value')  # 发动机号
        carDic['vinNo'] = soup.find(id="prpCitemCar.vinNo").get('value')  # 车架号
        carDic['licenseNo'] = soup.find(id='prpCitemCar.licenseNo').get('value').encode('latin1').decode('gbk')  # 车牌号
        carDic['endDate'] = time.strftime("%Y-%m-%d", time.localtime(int(carData[len(carData) - 1]['endDate']) / 1000))
        carDic['purchasePrice'] = soup.find(id='prpCitemCar.purchasePrice').get('value')
        carDic['exhaustScale'] = soup.find(id='prpCitemCar.exhaustScale').get('value')
        carDic['prpCitemCar_brandName'] = soup.find(id='prpCitemCar.brandName').get('value').encode('latin1').decode('gbk')
        carDic['carLotEquQuality'] = soup.find(id='prpCitemCar.carLotEquQuality').get('value')
        carDic['CModelCde'] = carDic['modelCode'] = soup.find(id='prpCitemCar.modelCode').get('value')
        carDic['NSeatNum'] = carDic['seatCount'] = soup.find(id='prpCitemCar.seatCount').get('value')
        personUrl = "http://10.134.136.112:8000/prpall/business/editCinsured.do?editType=" + editType + "&bizType=PROPOSAL&bizNo=" + proposalNo + "&riskCode=DAA&applyNo=&startDate=" + str(startDate) + "&endDate=" + str(endDateSY) + "&startHour=0&endHour=24&endorType=&taskID_Ppms=&prpallLinkPpmsFlag=&operateDate=" + str(today) + "&motorFastTrack=&operatorProjectCode=&reload=&rnd323="
        personRes = req_session.get(personUrl)
        personSoup = BeautifulSoup(personRes.content, "html.parser")
        carDic['identifyNumber'] = personSoup.find(id="prpCinsureds[0].identifyNumber").get('value')  # 身份证号
        carDic['insuredName'] = personSoup.find(id="prpCinsureds[0].insuredName").get('value').encode('latin1').decode('gbk')  # 车主姓名
        carDic['insuredAddress'] = personSoup.find(id="prpCinsureds[0].insuredAddress").get('value').encode('latin1').decode('gbk')  # 车主住址
        carDic['mobile'] = personSoup.find(id="prpCinsureds[0].mobile").get('value')  # 车主电话
        # inser_user_renewal(carDic)


        renew_order = data.json()['data']
        DAA = []
        DZA = []
        for order in  renew_order:
            if order['riskCode'] == "DZA":
                DZA.append(order)
            else:
                DAA.append(order)

        DAA.sort(key=lambda obj: obj.get('endDate').get('time'))
        DZA.sort(key=lambda obj: obj.get('endDate').get('time'))

        bizNo_dic = {}
        sy_endDate = ""
        sy_startDate = ""
        jq_endDate =  ""
        jq_startDate = ""
        if len(DAA):
            bizNo_dic['DAA'] = DAA[len(DAA)-1]['policyNo']
            sy_endDate = time.strftime("%Y-%m-%d", time.localtime(int(DAA[0]['endDate']['time'] / 1000)))
            sy_startDate = getlatedate(-365,sy_endDate)
        if len(DZA):
            bizNo_dic['DZA'] = DZA[len(DZA) - 1]['policyNo']
            jq_endDate = time.strftime("%Y-%m-%d", time.localtime(int(DZA[0]['endDate']['time'] / 1000)))
            jq_startDate = getlatedate(-365,jq_endDate)

        kind_info = ""
        for key in bizNo_dic:
            res = req_session.post("http://10.134.136.112:8000/prpall/business/editCheckRenewal.do?bizNo=" + bizNo_dic[key])
            proposalNo = res.json()['data'][0]['proposalNo']
            if proposalNo is None:
                proposalNo = bizNo_dic[key]

            if key=="DAA":
                order_url = "http://10.134.136.112:8000/prpall/business/editCitemKind.do?editType=" + editType + "&bizType=PROPOSAL&bizNo=" + proposalNo + "&riskCode=DAA&applyNo=&startDate=" + str(startDate) + "&endDate=" + str(endDateSY) + "&startHour=0&endHour=24&endorType=&taskID_Ppms=&prpallLinkPpmsFlag=&operateDate=" + str(today) + "&motorFastTrack=&operatorProjectCode=&reload=&rnd934="
                kind_info = DAA_parsing(req_session.get(order_url).text,kind_info)
            else:
                order_url = "http://10.134.136.112:8000/prpall/business/editCitemKindCI.do?editType=" + editType + "&bizType=PROPOSAL&bizNo=" + proposalNo + "&riskCode=DAA&applyNo=&startDate=" + str(startDate) + "&endDate=" + str(endDateSY) + "&startHour=0&endHour=24&endorType=&taskID_Ppms=&prpallLinkPpmsFlag=&operateDate=" + str(today) + "&motorFastTrack=&operatorProjectCode=&reload=&rnd934="
                kind_info = DZA_parsing(req_session.get(order_url).text, kind_info)
        kind_info['licenseNo'] = carDic['licenseNo']
        kind_info['vinNo'] = carDic['vinNo']
        kind_info['endDate'] = carDic['endDate']
        kind_info['insuredName'] = carDic['insuredName']
        kind_info['identifyNumber'] =carDic['identifyNumber']
        kind_info['NNewPurchaseValue'] = carDic['purchasePrice']
        kind_info['insuredAddress'] = carDic['insuredAddress']
        kind_info['enrollDate'] = carDic['enrollDate']
        kind_info['brandName'] = carDic['brandName']
        kind_info['CModelCde'] = carDic['CModelCde']
        kind_info['engineNo'] = carDic['engineNo']
        kind_info['insuranceTime']={
            'syEnd':sy_endDate,
            'syStart':sy_startDate,
            'jqStart':jq_startDate,
            'jqEnd':jq_endDate
        }
        inser_user_renewal(kind_info)
        log.error(licenseNo + "可以续保，续保信息入库成功")




        return carDic
        # dayGap = compare_time40(carDic['endDate'])
        # if dayGap < 0:
        #     carDic['endDate'] = ""
        #insert_user_renewal(COMPANY_ID, PLATE_NUMBER, USER_INFO, FLAG)
        # newPrimue(licenseNo, carDic['vinNo'] ,req_session ,insuranceType, carDic['endDate'])


def DAA_parsing(result,kind_info=""):
    res_soup = BeautifulSoup(result, "html.parser")
    choose_kind=[]
    for i in range(0,9):
        dt = {}
        find_id = "prpCitemKindsTemp["+str(i)+"].chooseFlag"
        if res_soup.find(id=find_id).get('checked')=="checked":
            dt['chooseFlag'] = '1'

        find_id = "prpCitemKindsTemp[" + str(i) + "].specialFlag"
        if res_soup.find(id=find_id).get('checked')=="checked":
            dt['specialFlag'] = '1'

        if dt.get('chooseFlag'):
            dt['amount'] = res_soup.find(id="prpCitemKindsTemp[" + str(i) + "].amount").get('value')
            dt['premium'] = res_soup.find(id="prpCitemKindsTemp[" + str(i) + "].premium").get('value')
            dt['disCount'] = res_soup.find(id="prpCitemKindsTemp[" + str(i) + "].disCount").get('value')

        if len(dt)!=0:
            dt['code'] = res_soup.find(id="prpCitemKindsTemp[" + str(i) + "].kindCode").get('value')
            choose_kind.append(dt)
    return homologous_order(choose_kind,kind_info)

def DZA_parsing(result,kind_info=""):
    res_soup = BeautifulSoup(result, "html.parser")
    choose_kind = []
    dt = {}
    if res_soup.find(id="prpCitemKindCI.familyNo").get('checked') == "checked":
        dt['chooseFlag'] = '1'
        dt['code'] = 'jq'
        dt['amount'] = res_soup.find(id="prpCitemKindCI.unitAmount").get('value')
        dt['disCount'] =  res_soup.find(id="prpCitemKindCI.adjustRate").get('value')
    choose_kind.append(dt)
    return homologous_order(choose_kind, kind_info)


def homologous_order(choose_kind,kind_info=""):
    if kind_info=="":
        kind_info={
          "licenseNo": "",
          "vinNo": "",
          "endDate": "",
          "CCardDetail": "",
          "CUsageCde": "",
          "insuredName": "",
          "identifyNumber": "",
          "NNewPurchaseValue": "",
          "COMPANY_ID": "2",
          "insuredAddress": "",
          "mobile": "",
          "enrollDate": "",
          "brandName": "",
          "CModelCde": "",
          "insuranceType": {
            "otherHurtPremium": {
              "Amount": "0",
              "isCheck": "0"
            },
            "driverDutyPremium": {
              "Amount": "0",
              "isCheck": "0"
            },
            "passengerDutyPremium": {
              "Amount": "0",
              "isCheck": "0"
            },
            "carDamagePremium": "0",
            "carFireBrokenBenchMarkPremium": "0",
            "carTheftPremium": "0",
            "otherHurtBenchMarkPremium": "0",
            "carTheftBenchMarkPremium": "0",
            "engineWadingBenchMarkPremium": "0",
            "JqSumPremium": "0",
            "carNickPremium": {
              "Amount": "0",
              "isCheck": "0"
            },
            "carDamageBenchMarkPremium": "0",
            "carNickBenchMarkPremium": "0",
            "engineWadingPremium": "0",
            "passengerBenchMarkPremium": "0",
            "SySumPremium": "0",
            "driverDutyBenchMarkPremium": "0",
            "carFirePremium": "0",
            "glassBrokenPremium": "0",
            "compulsoryInsurance": "0",
            "nAggTax": "0"
          },
          "NSeatNum": "",
          "engineNo": "0"
        }
    for kind in choose_kind:
        if '050202'==kind['code']:
            kind_info['insuranceType']['carDamagePremium']='1'
            if kind.get('specialFlag'):
                kind_info['insuranceType']['carDamageBenchMarkPremium'] = '1'
        elif '050602'==kind['code']:
            kind_info['insuranceType']['otherHurtPremium']['isCheck'] = '1'
            kind_info['insuranceType']['otherHurtPremium']['Amount'] = kind['amount']
            if kind.get('specialFlag'):
                kind_info['insuranceType']['otherHurtBenchMarkPremium'] = '1'
        elif '050501'==kind['code']:
            kind_info['insuranceType']['carTheftPremium'] = '1'
            if kind.get('specialFlag'):
                kind_info['insuranceType']['carTheftBenchMarkPremium'] = '1'
        elif '050711'==kind['code']:
            kind_info['insuranceType']['driverDutyPremium']['isCheck'] = '1'
            kind_info['insuranceType']['driverDutyPremium']['Amount'] = kind['amount']
            if kind.get('specialFlag'):
                kind_info['insuranceType']['driverDutyBenchMarkPremium'] = '1'
        elif '050712'==kind['code']:
            kind_info['insuranceType']['passengerDutyPremium']['isCheck'] = '1'
            kind_info['insuranceType']['passengerDutyPremium']['Amount'] = kind['amount']
            if kind.get('specialFlag'):
                kind_info['insuranceType']['passengerBenchMarkPremium'] = '1'
        elif '050211'==kind['code']:
            kind_info['insuranceType']['carNickPremium']['isCheck'] = '1'
            kind_info['insuranceType']['carNickPremium']['Amount'] = kind['amount']
            if kind.get('specialFlag'):
                kind_info['insuranceType']['carNickBenchMarkPremium'] = '1'
        elif '050232'==kind['code']:
            kind_info['insuranceType']['glassBrokenPremium'] = '1'
            if kind.get('specialFlag'):
                kind_info['insuranceType']['glassBrokenPremium'] = '1'
        elif '050311'==kind['code']:
            kind_info['insuranceType']['carFirePremium'] = '1'
            if kind.get('specialFlag'):
                kind_info['insuranceType']['carFirePremium'] = '1'
        elif '050461'==kind['code']:
            kind_info['insuranceType']['engineWadingPremium'] = '1'
            if kind.get('specialFlag'):
                kind_info['insuranceType']['engineWadingBenchMarkPremium'] = '1'
        elif 'jq' ==kind['code']:
            kind_info['insuranceType']['compulsoryInsurance'] = '1'
            kind_info['insuranceType']['nAggTax'] = '1'

    return kind_info

def get_checkAnwser(licenseNo,frameNo,req_session):
    DMV_url = "http://10.134.136.112:8000/prpall/business/queryVehiclePMCheck.do?comCode=32012105&frameNo=" + frameNo + "&licenseNo=" + urllib.quote(licenseNo.encode('gb2312'))
    DMV_res = req_session.post(DMV_url, verify=False).json()
    checkCode = DMV_res['data'][0]['checkCode']
    checkNo = DMV_res['data'][0]['checkNo']
    dmt = DamatuApi()
    checkAnswer = dmt.decode(base64.b64decode(checkCode), 200)
    DMV_carinfo_url = "http://10.134.136.112:8000/prpall/business/queryVehiclePMConfirm.do?comCode=32012105&checkNo=" + checkNo + "&checkCode=" + checkAnswer
    DMV_carinfo_res = req_session.post(DMV_carinfo_url, verify=False).json()
    if DMV_carinfo_res['data'][0]['errMessage'] is not None:
        errMessage = DMV_carinfo_res['data'][0]['errMessage'].encode('utf-8')
        if '录入的校验码有误 ' == errMessage:
            log.error("打码失败")
            get_checkAnwser(licenseNo, frameNo, req_session)
    return {'DMV_res':DMV_res,'DMV_carinfo_res':DMV_carinfo_res,'checkAnswer':checkAnswer}

def newPrimue(licenseNo,frameNo,req_session,insuranceType ,insure_id,group_id,endDate=""):
    checkResult = get_checkAnwser(licenseNo, frameNo, req_session)
    DMV_res = checkResult['DMV_res']
    DMV_carinfo_res = checkResult['DMV_carinfo_res']
    checkCode = DMV_res['data'][0]['checkCode']
    checkNo = DMV_res['data'][0]['checkNo']

    checkAnswer = checkResult['checkAnswer']

    # 通过车架号获取行业的modelCode
    modelCode_url = "http://10.134.136.112:8000/prpall/business/queryVehicleByPrefillVIN.do?vinNo=" + frameNo + "&licenseNo=" + urllib.quote(licenseNo.encode('gb2312')) + "&engineNo=&enrollDate="
    modelCode_res = req_session.post(modelCode_url,verify=False).json()

    # 通过modelCode查询车型列表
    carType_list_url = "http://10.134.136.112:8000/prpall/vehicle/vehicleQuery.do?brandName=" + modelCode_res['msg'] + "&modelCode="
    carType_list__res = req_session.post(carType_list_url,verify=False).json()
    enrollDate = str(time.strftime("%Y-%m-%d", time.localtime(int(DMV_carinfo_res['data'][0]['enrollDate']['time']) / 1000)))
    tomorrow = datetime.date.today() + datetime.timedelta(1)
    today = datetime.date.today()
    pmCarOwner = DMV_carinfo_res['data'][0]['carOwner']
    exhaustScale = DMV_carinfo_res['data'][0]['displacement']
    engineNo = DMV_carinfo_res['data'][0]['engineNo']
    brandName = carType_list__res['data'][0]['vehicleName']
    purchasePriceOld = carType_list__res['data'][0]['priceTr']
    modelCode = carType_list__res['data'][0]['vehicleId']

    dateDic = {
        'startDate': str(tomorrow),
        'endDate': str(datetime.datetime.strptime((str(today.year + 1) + '-' + str(today.month) + '-' + str(today.day)),"%Y-%m-%d").date()),
        'today': str(today),
        'enrollDate': enrollDate
    }
    if endDate!="":
        endDate = datetime.datetime.strptime(endDate, "%Y-%m-%d").date()
        dateDic['startDate'] = str(endDate)
        endDate = datetime.datetime.strptime((str(endDate.year + 1) + '-' + str(endDate.month) + '-' + str(endDate.day)),"%Y-%m-%d").date() + datetime.timedelta(-1)
        dateDic['endDate'] = str(endDate)


    useYears = calc_user_years(dateDic['startDate'],enrollDate)
    calAclDic = {
        "enrollDate": enrollDate,
        'ciEndDate': dateDic['endDate'],
        'licenseNo': licenseNo,
        'pmCarOwner': pmCarOwner,
        'exhaustScale': exhaustScale,
        'today': dateDic['today'],
        'engineNo': engineNo,
        'brandName': brandName,
        'purchasePriceOld': purchasePriceOld,
        'checkAnswer': checkAnswer,
        'ciStartDate': dateDic['startDate'],
        'checkNo': checkNo,
        'prpCitemCar_useYears': useYears,  ###需要计算一下
        'frameNo': frameNo,
        'modelCode': modelCode,
        'operationTimeStamp': str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),  # 需要重新获取下
        'checkCode': checkCode,
        'seatCount': DMV_carinfo_res['data'][0]['seatCount']
    }

    acl_price = caclAcl(calAclDic,req_session)
    calAclDic['aclPrice'] = acl_price
    price_res = caclPremium(calAclDic,insuranceType,req_session)

    while((price_res['data'][0].get('errMessage',"") is not None) and (price_res['data'][0].get('errMessage',"") !="") or ("0" in price_res.get('msg',""))):
        if "0" in price_res.get('msg', ""):
            carAlis = price_res['msg'].split("\n")[4].split(" ")[1]
            data = "pageNo_=1&riskCode=DAA&totalRecords_=&pageSize_=10&taxFlag=0&comCode=32012105&pm_vehicle_switch=1&carShipTaxPlatFormFlag=&TCVehicleVO.searchCode=&TCVehicleVO.vehicleAlias="+urllib.quote(carAlis.encode('gb2312'))+"&TCVehicleVO.vehicleId=&TCVehicleVO.brandId=&TCVehicleVO.brandName=&TCVehicleVO.vehicleName=SVW7167QSD&brandName=" + modelCode_res['msg'] + "&pageSizeSelect=10&quotationFlag="
            url = "http://10.134.136.112:8000/prpall/vehicle/vehicleQuery.do?pageSize=10&pageNo=1"
            res = req_session.post(url,data = data,verify=False).json()
            if len(res['data'])==0:
                log.error(price_res.get('msg',""))
                return price_res.get('msg',"")
            else:
                acl_price_url = 'http://10.134.136.112:8000/prpall/business/calActualValue.do'
                useYears = calc_user_years(dateDic['startDate'], enrollDate)
                exhaustScale = res['data'][0]['vehicleQuality']
                brandName = res['data'][0]['vehicleName']
                purchasePriceOld = res['data'][0]['priceTr']
                modelCode = res['data'][0]['vehicleId']
                calAclDic = {
                    "enrollDate": enrollDate,
                    'ciEndDate': dateDic['endDate'],
                    'licenseNo': licenseNo,
                    'pmCarOwner': pmCarOwner,
                    'exhaustScale': exhaustScale,
                    'today': dateDic['today'],
                    'engineNo': engineNo,
                    'brandName': brandName,
                    'purchasePriceOld': purchasePriceOld,
                    'checkAnswer': checkAnswer,
                    'ciStartDate': dateDic['startDate'],
                    'checkNo': checkNo,
                    'prpCitemCar_useYears': useYears,  ###需要计算一下
                    'frameNo': frameNo,
                    'modelCode': modelCode,
                    'operationTimeStamp': str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),  # 需要重新获取下
                    'checkCode': checkCode,
                    'seatCount': DMV_carinfo_res['data'][0]['seatCount']
                }
                acl_price = caclAcl(calAclDic, req_session)
                calAclDic['aclPrice'] = acl_price
                price_res = caclPremium(calAclDic, insuranceType, req_session)
                if price_res['data'][0]['errMessage'] !="":
                    log.info(price_res['data'][0]['errMessage'])
        if (price_res['data'][0].get('errMessage',"") is not None) and (price_res['data'][0].get('errMessage',"") !=""):
            if ("9308" in price_res['data'][0]['errMessage'].encode('utf-8')) or (('重复投保' in price_res['data'][0]['errMessage'])):
                str1 = "\d{4}-\d{2}-\d{2}"
                datelist = re.findall(str1, price_res['data'][0]['errMessage'], re.S)
                if len(datelist) == 2:
                  endDate = compare_date(datelist[0], datelist[1])
                  dayGap = compare_time40(str(endDate))
                  if dayGap >= 40:
                      log.error("重复投保，上期保单超过40天")
                      return price_res['data'][0]['errMessage'].encode('utf-8')
                  else:
                      dateDic['startDate'] = str(endDate)
                      endDate = datetime.datetime.strptime((str(endDate.year + 1) + '-' + str(endDate.month) + '-' + str(endDate.day)),"%Y-%m-%d").date() + datetime.timedelta(-1)
                      dateDic['endDate'] = str(endDate)
                      useYears = calc_user_years(dateDic['startDate'], enrollDate)
                      calAclDic = {
                          "enrollDate": enrollDate,
                          'ciEndDate': dateDic['endDate'],
                          'licenseNo': licenseNo,
                          'pmCarOwner': pmCarOwner,
                          'exhaustScale': exhaustScale,
                          'today': dateDic['today'],
                          'engineNo': engineNo,
                          'brandName': brandName,
                          'purchasePriceOld': purchasePriceOld,
                          'checkAnswer': checkAnswer,
                          'ciStartDate': dateDic['startDate'],
                          'checkNo': checkNo,
                          'prpCitemCar_useYears': useYears,  ###需要计算一下
                          'frameNo': frameNo,
                          'modelCode': modelCode,
                          'operationTimeStamp': str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),  # 需要重新获取下
                          'checkCode': checkCode,
                          'seatCount': DMV_carinfo_res['data'][0]['seatCount']
                      }
                      acl_price = caclAcl(calAclDic, req_session)
                      calAclDic['aclPrice'] = acl_price
                      price_res = caclPremium(calAclDic, insuranceType, req_session)
                      if price_res['data'][0]['errMessage'] != "" and price_res['data'][0]['errMessage'] is not None:
                          return price_res['data'][0]['errMessage']
                          log.error(price_res['data'][0]['errMessage'])

    log.error("开始解析保费信息")
    PremiumInfo = readJson(price_res['data'][0]['biInsuredemandVoList'][0]['prpCitemKinds'],price_res['data'][0].get('ciInsureVOList',""))
    log.info(PremiumInfo)
    # data=[开始时间,结束时间，座位数，组合id，车辆id，公司id]
    company_id='2'
    data_list = [dateDic['startDate'],dateDic['endDate'],DMV_carinfo_res['data'][0]['seatCount'],group_id,insure_id,company_id]

    soupDb(PremiumInfo,data_list)

#计算车辆实际价格
def caclAcl(calAclDic,req_session):
    log.info(u"开始计算车辆实际价格")
    acl_price_url = 'http://10.134.136.112:8000/prpall/business/calActualValue.do'
    calAclData = getCalAclData(calAclDic)
    acl_price = req_session.post(acl_price_url, data=calAclData, verify=False).content
    log.info(u"计算车辆实际价格结束"+calAclDic['licenseNo']+acl_price)
    return acl_price

def caclPremium(calAclDic,insuranceType,req_session):
    log.info(u"开始计算保费")
    cacl_primue_url = "http://10.134.136.112:8000/prpall/business/caculatePremiunForFG.do"
    caclData = getCaclData(calAclDic, insuranceType)
    price_res = req_session.post(cacl_primue_url, data=caclData, verify=False).json()
    log.info(u"保费计算结束结束" + calAclDic['licenseNo'])
    return price_res



if __name__=="__main__":
    check(u"苏A61337")





