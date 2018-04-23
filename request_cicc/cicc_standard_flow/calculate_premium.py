# -*- coding:utf-8 -*-
import json
import datetime
global null, false, true
null = None
false = False
true = True
from request_cicc.data.insuranceType import get_insurance_type
from request_cicc.interface import calculateActualValue
from request_cicc.interface.calcUserYears import calc_user_years


def calculate_premium(dt):
    seatCount = dt['seatCount']
    enrollDate = dt['enrollDate']
    endDate = dt['endDate']
    driverName = dt['driverName']
    driverIDNumber = dt['driverIDNumber']
    licenseNo = dt['licenseNo']
    modelName = dt['modelName']
    motorNo = dt['motorNo']
    exhaustScale = dt['exhaustScale']
    jyPrice = dt['jyPrice']
    jyindustryModelCode = dt['jyindustryModelCode']
    net = dt['net']
    jyNoticeType = dt['jyNoticeType']
    powerScale = dt['powerScale']
    chassisNo = dt['vinNo']
    vehicleCategory = dt['vehicleCategory']
    tonCount = dt['tonCount']
    jyCarName = dt['jyCarName']
    modelCode = dt['modelCode']
    insuranceType = dt['insuranceType']
    salesChannelCode = dt['salesChannelCode']
    vehicleId = dt['vehicleId']
    req_session = dt['req_session']


    amount = calculateActualValue.calculateActualValue(jyPrice, "85", seatCount, "A0", "",enrollDate, endDate)
    if endDate == "":
        useYears = calc_user_years(str(datetime.date.today() + datetime.timedelta(1)), enrollDate)
        startDate = str(datetime.date.today() + datetime.timedelta(1)) + ' ' + '00'
        tomorrow = datetime.date.today() + datetime.timedelta(1)
        endDate = str(datetime.datetime.strptime((str(tomorrow.year + 1) + '-' + str(tomorrow.month) + '-' + str(tomorrow.day)),"%Y-%m-%d").date()) + ' ' + '00'
    else:
        useYears = calc_user_years(endDate, enrollDate)
        endDate = str(endDate)
        endDate = datetime.datetime.strptime(endDate, "%Y-%m-%d").date()
        startDate = str(endDate) + ' ' + '00'
        endDate = str(datetime.datetime.strptime((str(endDate.year + 1) + '-' + str(endDate.month) + '-' + str(endDate.day)),"%Y-%m-%d").date()) + ' ' + '00'


    applicantInfo = 'applicantNature=3&&applicantName=' + driverName + '&&applicantPhone=&&appCertificateType=01&&appCertificateNum=' + driverIDNumber + '&&applicantAddress=&&appPostCode=&&isNeedEInvoice=0&&applicantEmail=',
    carStr = {
        "firstYearDate": "",
        "licenseType": "02",
        "toncount": "0.0",
        "platformPriceType": "01",
        "loanVehicleFlag": "0",
        "carChecker": "",
        "passportOwner": driverName,
        "motorNo": motorNo,
        "enrollDate": enrollDate,
        "argueSolution": "1",
        "useNatureCode": "85",
        "fuelType": "0",
        "isAboutRural": "1",
        "runMiles": "",
        "licenseNo": licenseNo,
        "modelName": modelName,
        "exhaustScale": exhaustScale,
        "replacementValue": jyPrice,
        "transfer": "0",
        "carKindCode": "A0",
        "useYears": useYears,
        "industryModelCode": jyindustryModelCode,
        "transferDate": "",
        "driverBirthYear": "1978",
        "net": net,
        "industryVehicleCode": jyNoticeType,
        "powerScale": powerScale,
        "vinNo": chassisNo,
        "arguesolution": "1",
        "runRegion": "11",
        "driverGender": "1",
        "organizationCode": "",
        "idNumber": driverIDNumber,
        "seatCount": seatCount,
        "carTypeAlias": modelName,
        "isAboutAgri": "0",
        "vehicleCategory": vehicleCategory,
        "tonCount": tonCount,
        "queryAreaCode": "",
        "shCertificateDate": "",
        "noLicenseFlag": "0",
        "arbitBoardname": "A01",
        "ecdemicVehicle": "0",
        "unitType": "16",
        "ownerIdentityType": "01",
        "chassisNo": chassisNo,
        "purchasePrice": jyPrice,
        "driverArea": "11",
        "licenseColorCode": "",
        "actualValue": str(amount),
        "specialCarFlag": "0",
        "CarName": jyCarName,
        "carCheckTime": "",
        "discountRateNum": "",
        "modelCode": modelCode
    }
    # print json.dumps(carStr,ensure_ascii=False)
    insuredInfo = 'relationShip=1&&insuredNature=3&&insuredName=' + driverName + '&&insuredPhone=&&insCertificateType=01&&insCertificateNum=' + driverIDNumber +  '&&insuredAddress=&&insPostCode=&&insNation=&&insBirthday=&&insIdentifyCom=&&insIdentifyStartDate=&&insIdentifyEndDate='
    kindsInfo = [{
        "adjustRate": "",
        "modeCode": "",
        "serialNo": 1,
        "unitAmount": "",
        "rate": "",
        "value": "",
        "deductibleRate": "",
        "disCount": "",
        "amount": "122000",
        "unCommon": "",
        "benchmarkPremium": "",
        "premium": "",
        "kindName": "交通事故强制责任险",
        "kindFlag": 0,
        "kindCode": "BZ",
        "quantity": ""
    },
        {
            "adjustRate": "",
            "modeCode": "",
            "serialNo": 1,
            "unitAmount": "",
            "rate": "",
            "value": "",
            "deductibleRate": "",
            "disCount": "",
            "amount": amount,
            "unCommon": "",
            "benchmarkPremium": "",
            "premium": "",
            "kindName": "车辆损失保险",
            "kindFlag": 1,
            "kindCode": "A",
            "quantity": ""
        },
        {
            "adjustRate": "",
            "modeCode": "",
            "serialNo": 1,
            "unitAmount": "",
            "rate": "",
            "value": "",
            "deductibleRate": "",
            "disCount": "",
            "amount": "500000",
            "unCommon": "",
            "benchmarkPremium": "",
            "premium": "",
            "kindName": "第三者责任保险",
            "kindFlag": 1,
            "kindCode": "B",
            "quantity": ""
        },
        {
            "adjustRate": "",
            "modeCode": "",
            "serialNo": 1,
            "unitAmount": "10000",
            "rate": "",
            "value": "",
            "deductibleRate": "",
            "disCount": "",
            "amount": "10000",
            "unCommon": "",
            "benchmarkPremium": "",
            "premium": "",
            "kindName": "车上人员责任保险（司机）",
            "kindFlag": 0,
            "kindCode": "D3",
            "quantity": 1
        },
        {
            "adjustRate": "",
            "modeCode": "",
            "serialNo": 1,
            "unitAmount": "10000",
            "rate": "",
            "value": "",
            "deductibleRate": "",
            "disCount": "",
            "amount": (int(seatCount) - 1) * 10000,
            "unCommon": "",
            "benchmarkPremium": "",
            "premium": "",
            "kindName": "车上人员责任保险（乘客）",
            "kindFlag": 1,
            "kindCode": "D4",
            "quantity": int(int(seatCount) - 1)
        },
        {
            "adjustRate": "",
            "modeCode": "",
            "serialNo": 1,
            "unitAmount": "",
            "rate": "",
            "value": "",
            "deductibleRate": "",
            "disCount": "",
            "amount": "",
            "unCommon": "",
            "benchmarkPremium": "",
            "premium": "",
            "kindName": "不计免赔额特约",
            "kindFlag": 0,
            "kindCode": "M",
            "quantity": ""
        }]
    if insuranceType != "" and insuranceType != None:
        kindsInfo = get_insurance_type(eval(json.dumps(insuranceType)), amount, seatCount,chassisNo)
    jqflag = syflag = 0
    insuranceType = eval(json.dumps(insuranceType))
    if insuranceType.get("compulsoryInsurance", "1") == "1":
        jqflag = 1
    if insuranceType.get("otherHurtPremium", {}).get("isCheck", "1") == "1" or \
                    insuranceType.get("carNickPremium", {}).get("isCheck", "1") == "1" or \
                    insuranceType.get("driverDutyPremium", {}).get("isCheck", "1") == "1" or \
                    insuranceType.get("passengerDutyPremium", {}).get("isCheck", "1") == "1" or \
                    insuranceType.get("carTheftPremium", "1") == "1" or \
                    insuranceType.get("engineWadingPremium", "1") == "1" or \
                    insuranceType.get("carTheftPremium", "1") == "1" or \
                    insuranceType.get("carDamagePremium", "1") == "1":
        syflag = 1
    if jqflag ==1 and syflag==0:
        insuranceType_flag = '1'
    else:
        insuranceType_flag = '3'
    calculatePriumeData = {
        '_action': 'calculatePremium',
        'account': '',
        'accountName': '',
        'agentInfo': 'agentCode=&&agentName=undefined&&agreement=&&agreementName=请选择',
        'applicantInfo': applicantInfo,
        'applicationId': '',
        'appointDriverInfo': 'DriverInoIni',
        'automaticRenewalInfo': '{"automaticRenewalFlag":"1","autoRendepositBank":"工商银行","autoRenAccountName":"","autoRenAccountNO":"","autoRenCertificateType":"01","autoRenCertificateNO":"","autoRenMobileNO":"","autoRenewalPointBI":"","autoRenewalPointCI":"","autoRendepositCode":"0102","automaticRenewalStatus":"1"}',
        'businessNature': '0101',
        'carStr': json.dumps(carStr, ensure_ascii=False),
        'carTaxStr': 'taxFlag=0&&deDuctiondueCode=&&deDuctiondueType=&&deDuctionDocumentNumber=&&taxDepartment=&&deDuctiondueProportion=&&deDuction=&&taxDepartment_P=&&taxDocumentNumber=&&sumTaxValue=&&annualTaxDue=&&sumOverdue=&&sumTaxDefault=',
        'channelInfo': 'ProjectSerialNo=&&ProjectName=&&RepairChannelCode=&&RepairChannelName=',
        'commericalSpecial': '',
        "endDate": endDate,
        'expectDiscount': '',
        'firstYearDate': '',
        'insuranceOrderNo': '',
        'insuranceType': insuranceType_flag,
        'insuredInfo': insuredInfo,
        'kindsInfo': json.dumps(kindsInfo, ensure_ascii=False),
        'operatorCode': salesChannelCode,
        'orgCode': '',
        'queryAreaCode': '',
        'renewPolicyNo': '',
        'shortRateFlag': '1',
        'specialAgreement': '[]',
        'startDate': startDate,
        'taxExtendInfo': '',
        'trafficSpecial': '',
        'underWriteType': '0',
        'usbKeyInfo': '',
        'vehicleId': vehicleId,
        'verifyAnswer': ''
    }
    url = "http://b2b.ccic-net.com.cn/mss/view/vehicleInsurance/accurateQuotation/accurateQuotationForAgencyBusiness.jsp"
    premuim_info = req_session.post(url,data=calculatePriumeData).content

    return eval(premuim_info)
