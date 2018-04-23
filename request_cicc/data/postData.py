# -*- coding:utf-8 -*-
from request_cicc.data import testData as SE
import datetime
import json
import urllib
from request_cicc.interface.calcUserYears import calc_user_years
from request_cicc.interface import calculateActualValue
from request_cicc.data.insuranceType import get_insurance_type
def init_loginData():
    login_data = {
        'j_username': SE.loginUserName,
        'j_password': SE.loginPWD,
        'j_captcha': ""
    }
    return login_data

def getCarModelData(modelName,chassisNo,motorNo,enrollDate,licenseNo):
    getCarModelData = {
        'currentPageIndex': '1',
        'pageSize': '8',
        'autoload': 'true',
        'modelName': modelName,  # 'JL7152L13',
        'chassisNo': chassisNo,  # 'LB37724S2GX041139',
        'motorNo': motorNo,  # 'G4XV06160',
        'enrollDate': enrollDate,  # '2016-05-09',
        'licenseNo': licenseNo,  # '苏8F7Z32',
        'licenseType': '02',
        'vehicleCategory': 'K31',
        'ecdemicVehicle': '0',
        'salesChannelCode': 'PI90000121',
        'orgCode': '',
        'vehicleStyleDesc': modelName,  # 'JL7152L13',
        'cacheableFlag': '',
        '_action': 'queryVehicleConfigurationAction'
    }
    return getCarModelData

def getPostSelectCarModelData(modelName,chassisNo,motorNo,enrollDate,licenseNo,carModel,jsCheckCode,codeStr,jsCheckNo):
    postSelectCarModelData = {
        'modelName':"",
        'chassisNo': chassisNo,
        'motorNo': "",
        'enrollDate': enrollDate,
        'licenseNo': "",
        'licenseType': '02',
        'vehicleCategory': 'K31',
        'ecdemicVehicle': '0',
        'orgCode': '',
        'salesChannelCode': 'PI90000121',
        'vehicleStyleDesc': "",
        'cacheableFlag': '1',
        'autoload': 'true',
        'currentPageIndex': '1',
        'pageSize': '8',
        'modelCode': carModel['modelCode'],
        'vehicleId': '',
        'newinsurancecreatedate': str(datetime.date.today()),
        'zdNature': '3',
        'zdUnitType': '',
        'newcarKindCode': 'A0',
        'newuseNatureCode': '85',
        'accurateNewMark': '1',
        'businessNewNature': '0101',
        'specialModelFlag': '0',
        'jsCheckNo': jsCheckNo,##
        'jsCheckCode': jsCheckCode,###
        "checkCode": codeStr,
        'shCertificateDate': '',
        '_action': 'saveVehicleModel'
    }
    return postSelectCarModelData

def getCalculatePriumeData(insuranceType,userId,driverName,driverIDNumber,licenseNo,chassisNo,motorNo,enrollDate,codeStr,modelName,price,vcodeRes,endDate=""):
    seatCount = vcodeRes['result']['seatCount']
    amount = calculateActualValue.calculateActualValue(vcodeRes['result']['jyPrice'], "85", seatCount, "A0", "",enrollDate,endDate)
    cost = price
    if endDate=="":
        startDate = str(datetime.date.today() + datetime.timedelta(1)) + ' ' + '00'
        tomorrow = datetime.date.today() + datetime.timedelta(1)
        endDate = str(datetime.datetime.strptime((str(tomorrow.year + 1) + '-' + str(tomorrow.month) + '-' + str(tomorrow.day)), "%Y-%m-%d").date()) + ' ' + '00'
        useYears = calc_user_years(str(datetime.date.today() + datetime.timedelta(1)),enrollDate)
    else:
        endDate = str(endDate)
        endDate = datetime.datetime.strptime(endDate,"%Y-%m-%d").date()
        startDate = str(endDate) + ' ' + '00'
        endDate = str(datetime.datetime.strptime((str(endDate.year + 1) + '-' + str(endDate.month) + '-' + str(endDate.day)),"%Y-%m-%d").date()) + ' ' + '00'
        useYears = calc_user_years(str(datetime.date.today() + datetime.timedelta(1)), enrollDate)
    applicantInfo = 'applicantNature=3&&applicantName='+driverName+'&&applicantPhone=&&appCertificateType=01&&appCertificateNum='+driverIDNumber+'&&applicantAddress=&&appPostCode=&&isNeedEInvoice=0&&applicantEmail=',
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
        "modelName": vcodeRes['result']['modelName'],
        "exhaustScale": vcodeRes['result']['exhaustScale'],
        "replacementValue": vcodeRes['result']['jyPrice'],
        "transfer": "0",
        "carKindCode": "A0",
        "useYears": useYears,
        "industryModelCode": vcodeRes['result']['jyindustryModelCode'],
        "transferDate": "",
        "driverBirthYear": "1978",
        "net": vcodeRes['result']['net'],
        "industryVehicleCode": vcodeRes['result']['jyNoticeType'],
        "powerScale": vcodeRes['result']['powerScale'],
        "vinNo": chassisNo,
        "arguesolution": "1",
        "runRegion": "11",
        "driverGender": "1",
        "organizationCode": "",
        "idNumber": driverIDNumber,
        "seatCount": vcodeRes['result']['seatCount'],
        "carTypeAlias": vcodeRes['result']['modelName'],
        "isAboutAgri": "0",
        "vehicleCategory": vcodeRes['result']['vehicleCategory'],
        "tonCount": vcodeRes['result']['tonCount'],
        "queryAreaCode": "",
        "shCertificateDate": "",
        "noLicenseFlag": "0",
        "arbitBoardname": "A01",
        "ecdemicVehicle": "0",
        "unitType": "16",
        "ownerIdentityType": "01",
        "chassisNo": chassisNo,
        "purchasePrice": vcodeRes['result']['jyPrice'],
        "driverArea": "11",
        "licenseColorCode": "",
        "actualValue": str(amount),
        "specialCarFlag": "0",
        "CarName": vcodeRes['result']['jyCarName'],
        "carCheckTime": "",
        "discountRateNum": "",
        "modelCode": vcodeRes['result']['modelCode']
    }
    #print json.dumps(carStr,ensure_ascii=False)
    insuredInfo = 'relationShip=1&&insuredNature=3&&insuredName='+driverName+\
                  '&&insuredPhone=&&insCertificateType=01&&insCertificateNum='+driverIDNumber+\
                  '&&insuredAddress=&&insPostCode=&&insNation=&&insBirthday=&&insIdentifyCom=&&insIdentifyStartDate=&&insIdentifyEndDate='
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
            "amount": (int(seatCount)-1)*10000,
            "unCommon": "",
            "benchmarkPremium": "",
            "premium": "",
            "kindName": "车上人员责任保险（乘客）",
            "kindFlag": 1,
            "kindCode": "D4",
            "quantity":  int(int(seatCount)-1)
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
    if insuranceType!="" or insuranceType!=None:
       kindsInfo=get_insurance_type(eval(json.dumps(insuranceType)),amount,seatCount,chassisNo)

    calculatePriumeData={
        '_action':'calculatePremium',
        'account': '',
        'accountName': '',
        'agentInfo': 'agentCode=&&agentName=undefined&&agreement=&&agreementName=请选择',
        'applicantInfo': applicantInfo,
        'applicationId': '',
        'appointDriverInfo': 'DriverInoIni',
        'automaticRenewalInfo':'{"automaticRenewalFlag":"1","autoRendepositBank":"工商银行","autoRenAccountName":"","autoRenAccountNO":"","autoRenCertificateType":"01","autoRenCertificateNO":"","autoRenMobileNO":"","autoRenewalPointBI":"","autoRenewalPointCI":"","autoRendepositCode":"0102","automaticRenewalStatus":"1"}',
        'businessNature': '0101',
        'carStr':json.dumps(carStr,ensure_ascii=False),
        'carTaxStr': 'taxFlag=0&&deDuctiondueCode=&&deDuctiondueType=&&deDuctionDocumentNumber=&&taxDepartment=&&deDuctiondueProportion=&&deDuction=&&taxDepartment_P=&&taxDocumentNumber=&&sumTaxValue=&&annualTaxDue=&&sumOverdue=&&sumTaxDefault=',
        'channelInfo': 'ProjectSerialNo=&&ProjectName=&&RepairChannelCode=&&RepairChannelName=',
        'commericalSpecial': '',
        "endDate": endDate,
        'expectDiscount': '',
        'firstYearDate': '',
        'insuranceOrderNo': '',
        'insuranceType': '3',
        'insuredInfo': insuredInfo,
        'kindsInfo':json.dumps(kindsInfo,ensure_ascii=False),
        'operatorCode': userId,
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
        'vehicleId': vcodeRes['result']['id'],
        'verifyAnswer': ''
    }
    return calculatePriumeData
    # return "orgCode=&insuranceType=2&shortRateFlag=1&operatorCode=8000192691&startDate=2017-01-05+00&endDate=2018-01-05+00&expectDiscount=&applicationId=&vehicleId=13375982&carStr=%7B%22chassisNo%22%3A%22LVRHFADL0EN572132%22%2C%22enrollDate%22%3A%222016-05-07%22%2C%22JSCheckCode%22%3A%223Af1%22%2C%22JSCheckNo%22%3A%2272CCIC320017001483523334942979%22%2C%22JSCheckCode2%22%3A%22%2F9j%2F4AAQSkZJRgABAQAAAQABAAD%2F2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj%2F2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj%2FwAARCAAYAFQDASIAAhEBAxEB%2F8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL%2F8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4%2BTl5ufo6erx8vP09fb3%2BPn6%2F8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL%2F8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3%2BPn6%2F9oADAMBAAIRAxEAPwD2Gz0PSE0vRWSws2uNQgtWmjNvEoYhcM5cLv3PlQSSeIxgDndtazoeg2txp5OhQsluzTEwwLhlEbIQ4%2FiA3g4bIzg9QMZFkZDH4cO2ZT9jtgo%2BTPQcr2%2F76%2FHisv4hX0Wo6XfXtvHfXlvA%2B2aHSSY7l%2FLJDR7gwIZWBBCMrEwlehKsAdMunaDcW9qs2iaY7RASXKyWcfDIfTbwQQXAHPydOaranBpkd2yJoVjarE2xhLZxMC28gFiob5WRdwx82GGQCCB558E9c1zVpNVkLtDo41L7Np0d%2BQ13F5XDRzlQSp5XhiX%2Bc7mYEMep8T6hb6Vp%2Bp6pKJ3tLSKS4UKuS0KBj8u4jnC4AP5jFAGvq1hol%2FcwQWGmWPk74iGjthGDKJAwV2AB24XkD7wyDkEimXenaDHNZslpYzxtcF2lMSBhHvJ2NGqKAAG2g4JKqMknJPjPwmv5tL8eeIdInkmke%2FjXW0%2F0Wa3SOZjsuCvmokmPMKlOCNqjJ3bgfYPFzPp8Fu9rBNqG22QpFbqkbOCx6b2Uf7Ry3r7CgDpl07w6uny313o2m2dnFF5zzXEEKosYGSxPYADJJxisvUdD0ayuLaObTdFSWW5e4mlis1izGp%2BVWHzFjsCrnPzFOAAQB5t8CbrVPFtlp%2Bv6vceIhc3TSTDF%2BwsigkeLy4oElwsaqgBMi7txJBbgj1nxhCFVpWMwhubaWzlMblGAZTtwwIZTkk5ByMcUAZwg0O4%2B2XcGi20cdkhiaJre1aN5HYFCwUl1YII5ACV%2BS4XILcJBJpVhazWtlHpdgZVWNXaS0jYea7A7Xbb0xnGOfyry%2FwCCLtb2fi6wjZmt4%2FFF4UEr7yWCooLO%2BS3bO48859a9A%2B3x3F7dSpc%2BfcxS7WOfmRtoYbsH5WAZCB6EdsZAOJ8fWVtbazBcWsFtb%2FbbWO4lhtkURRycxsqsI0ZxmP7zjcfYBVUrQ%2BKsaxaxpiRsroNPj2sqbQwLyHOPU%2FzooA6y1utMNh4fmF7ZuIrWBbqNZFZkCquS4Bz04ORxjFV%2FFy6fqWs2503xJJp84jmljnsrlWUgFCysZEeINvYMOjBQxBUbySigA8H6D4b8OWd1bw%2BIrV2mupr15pLyIyS3Eu0tKxUqBjCqAqqPkBxycrq1npmr2t2zS2MkFvNFd%2FJcgAMrLKFBU4OxlU8EdOQc4oooAztV0nSJZ7XWL4QyX2kN%2Fo8qSuWj89VVxsXg4BXJIwoyTxyN0Xlomo6aZL%2B1aeEIZ1XC%2BUgIILn2UgE9sUUUAZ%2Fwz03TfAekaHoUGvWeqW9pbXCTXqMiKu6cyDKCRiM%2BYeeVAQ5IJUHsdR1bRL%2F9zPrel%2FYmidZFW5CTBzgK6Sq4MZA38gbslSGXbyUUAee6X4Z8MaLrl%2FLoWo7Y7mYy3MsupSzRlpDlpG3yMpb5QC5wxPHrXQXosZm1CWyu7F4YH8wSJMoBUjJUc4O36j8cjBRQBw%2FxIlEup6avnRTPHYojbGB2fO5CnHQhSvFFFFAH%2F9k%3D%22%2C%22motorNo%22%3A%22EA025760%22%2C%22modelName%22%3A%22%E7%A6%8F%E7%89%B9CAF7152B5%E8%BD%BF%E8%BD%A6%22%2C%22licenseNo%22%3A%22%E8%8B%8FAN2R01%22%2C%22licenseType%22%3A%2202%22%2C%22carKindCode%22%3A%22A0%22%2C%22useNatureCode%22%3A%2285%22%2C%22firstYearDate%22%3A%22%22%2C%22shCertificateDate%22%3A%22%22%2C%22transferDate%22%3A%22%22%2C%22carTypeAlias%22%3A%22%E7%A6%8F%E7%89%B9CAF7152B5%E8%BD%BF%E8%BD%A6%22%2C%22industryModelCode%22%3A%22BCAAJOUB0010%22%2C%22CarName%22%3A%22%E7%A6%8F%E7%89%B9CAF7152B5+%E6%97%B6%E5%B0%9A%E5%9E%8B%22%2C%22industryVehicleCode%22%3A%22CAF7152B5%22%2C%22queryAreaCode%22%3A%22%22%2C%22modelCode%22%3A%22FTBAFD0090%22%2C%22fuelType%22%3A%220%22%2C%22licenseColorCode%22%3A%22%22%2C%22seatCount%22%3A%225%22%2C%22toncount%22%3A%220.0%22%2C%22net%22%3A%221115.0%22%2C%22exhaustScale%22%3A%221499.0%22%2C%22powerScale%22%3A%2281.0%22%2C%22replacementValue%22%3A%2276900.0%22%2C%22actualValue%22%3A%2273670.20%22%2C%22vehicleCategory%22%3A%22K31%22%2C%22useYears%22%3A%220%22%2C%22transfer%22%3A%220%22%2C%22loanVehicleFlag%22%3A%220%22%2C%22ecdemicVehicle%22%3A%220%22%2C%22isAboutAgri%22%3A%220%22%2C%22specialCarFlag%22%3A%220%22%2C%22carChecker%22%3A%22%22%2C%22carCheckTime%22%3A%22%22%2C%22runMiles%22%3A%22%22%2C%22passportOwner%22%3A%22%E7%AC%AA%E4%B8%96%E7%9B%BC%22%2C%22isAboutRural%22%3A%221%22%2C%22ownerIdentityType%22%3A%2201%22%2C%22organizationCode%22%3A%22%22%2C%22unitType%22%3A%2216%22%2C%22driverBirthYear%22%3A%221978%22%2C%22driverGender%22%3A%221%22%2C%22arguesolution%22%3A%221%22%2C%22arbitBoardname%22%3A%22A01%22%2C%22driverArea%22%3A%2211%22%2C%22vinNo%22%3A%22LVRHFADL0EN572132%22%2C%22purchasePrice%22%3A%2276900.0%22%2C%22tonCount%22%3A%220.0%22%2C%22idNumber%22%3A%22320124199111151023%22%2C%22noLicenseFlag%22%3A%220%22%2C%22argueSolution%22%3A%221%22%2C%22runRegion%22%3A%2211%22%2C%22platformPriceType%22%3A%2201%22%7D&appointDriverInfo=DriverInoIni&kindsInfo=%5B%7B%22kindCode%22%3A%22A%22%2C%22kindName%22%3A%22%E8%BD%A6%E8%BE%86%E6%8D%9F%E5%A4%B1%E4%BF%9D%E9%99%A9%22%2C%22serialNo%22%3A1%2C%22quantity%22%3A%22%22%2C%22amount%22%3A%2273670%22%2C%22value%22%3A%22%22%2C%22deductibleRate%22%3A%22%22%2C%22unitAmount%22%3A%22%22%2C%22modeCode%22%3A%22%22%2C%22kindFlag%22%3A1%2C%22rate%22%3A%22%22%2C%22adjustRate%22%3A%22%22%2C%22disCount%22%3A%22%22%2C%22benchmarkPremium%22%3A%22%22%2C%22premium%22%3A%22%22%2C%22unCommon%22%3A%22%22%7D%2C%7B%22kindCode%22%3A%22B%22%2C%22kindName%22%3A%22%E7%AC%AC%E4%B8%89%E8%80%85%E8%B4%A3%E4%BB%BB%E4%BF%9D%E9%99%A9%22%2C%22serialNo%22%3A1%2C%22quantity%22%3A%22%22%2C%22amount%22%3A%22500000%22%2C%22value%22%3A%22%22%2C%22deductibleRate%22%3A%22%22%2C%22unitAmount%22%3A%22%22%2C%22modeCode%22%3A%22%22%2C%22kindFlag%22%3A1%2C%22rate%22%3A%22%22%2C%22adjustRate%22%3A%22%22%2C%22disCount%22%3A%22%22%2C%22benchmarkPremium%22%3A%22%22%2C%22premium%22%3A%22%22%2C%22unCommon%22%3A%22%22%7D%2C%7B%22kindCode%22%3A%22G1%22%2C%22kindName%22%3A%22%E5%85%A8%E8%BD%A6%E7%9B%97%E6%8A%A2%E4%BF%9D%E9%99%A9%22%2C%22serialNo%22%3A1%2C%22quantity%22%3A%22%22%2C%22amount%22%3A%2273670%22%2C%22value%22%3A%22%22%2C%22deductibleRate%22%3A100%2C%22unitAmount%22%3A%22%22%2C%22modeCode%22%3A%22%22%2C%22kindFlag%22%3A1%2C%22rate%22%3A%22%22%2C%22adjustRate%22%3A%22%22%2C%22disCount%22%3A%22%22%2C%22benchmarkPremium%22%3A%22%22%2C%22premium%22%3A%22%22%2C%22unCommon%22%3A%22%22%7D%2C%7B%22kindCode%22%3A%22M%22%2C%22kindName%22%3A%22%E4%B8%8D%E8%AE%A1%E5%85%8D%E8%B5%94%E9%A2%9D%E7%89%B9%E7%BA%A6%22%2C%22serialNo%22%3A1%2C%22quantity%22%3A%22%22%2C%22amount%22%3A%22%22%2C%22value%22%3A%22%22%2C%22deductibleRate%22%3A%22%22%2C%22unitAmount%22%3A%22%22%2C%22modeCode%22%3A%22%22%2C%22kindFlag%22%3A0%2C%22rate%22%3A%22%22%2C%22adjustRate%22%3A%22%22%2C%22disCount%22%3A%22%22%2C%22benchmarkPremium%22%3A%22%22%2C%22premium%22%3A%22%22%2C%22unCommon%22%3A%22%22%7D%5D&carTaxStr=&taxExtendInfo=&insuredInfo=relationShip%3D1%26%26insuredNature%3D3%26%26insuredName%3D%E7%AC%AA%E4%B8%96%E7%9B%BC%26%26insuredPhone%3D%26%26insCertificateType%3D01%26%26insCertificateNum%3D320124199111151023%26%26insuredAddress%3D%26%26insPostCode%3D%26%26insNation%3D%26%26insBirthday%3D%26%26insIdentifyCom%3D%26%26insIdentifyStartDate%3D%26%26insIdentifyEndDate%3D&applicantInfo=applicantNature%3D3%26%26applicantName%3D%E7%AC%AA%E4%B8%96%E7%9B%BC%26%26applicantPhone%3D%26%26appCertificateType%3D01%26%26appCertificateNum%3D320124199111151023%26%26applicantAddress%3D%26%26appPostCode%3D%26%26isNeedEInvoice%3D0%26%26applicantEmail%3D&verifyAnswer=&channelInfo=ProjectSerialNo%3D%26%26ProjectName%3D%26%26RepairChannelCode%3D%26%26RepairChannelName%3D&renewPolicyNo=&accountName=&account=&commericalSpecial=&trafficSpecial=&insuranceOrderNo=&businessNature=0101&agentInfo=agentCode%3D%26%26agentName%3Dundefined%26%26agreement%3D%26%26agreementName%3D%E8%AF%B7%E9%80%89%E6%8B%A9%C2%A0%C2%A0&specialAgreement=%5B%5D&usbKeyInfo=&queryAreaCode=&firstYearDate=&underWriteType=0&automaticRenewalInfo=%7B%22automaticRenewalFlag%22%3A%221%22%2C%22autoRendepositBank%22%3A%22%E5%B7%A5%E5%95%86%E9%93%B6%E8%A1%8C%22%2C%22autoRenAccountName%22%3A%22%22%2C%22autoRenAccountNO%22%3A%22%22%2C%22autoRenCertificateType%22%3A%2201%22%2C%22autoRenCertificateNO%22%3A%22%22%2C%22autoRenMobileNO%22%3A%22%22%2C%22autoRenewalPointBI%22%3A%22%22%2C%22autoRenewalPointCI%22%3A%22%22%2C%22autoRendepositCode%22%3A%220102%22%2C%22automaticRenewalStatus%22%3A%221%22%7D&_action=calculatePremium"
def mmm():
    m = {
        "firstYearDate": "",
        "startDate": "2017-01-06 00",
        "kindsInfo": "[{\"kindCode\":\"A\",\"kindName\":\"车辆损失保险\",\"serialNo\":1,\"quantity\":\"\",\"amount\":\"68133\",\"value\":\"\",\"deductibleRate\":\"\",\"unitAmount\":\"\",\"modeCode\":\"\",\"kindFlag\":1,\"rate\":\"\",\"adjustRate\":\"\",\"disCount\":\"\",\"benchmarkPremium\":\"\",\"premium\":\"\",\"unCommon\":\"\"},{\"kindCode\":\"B\",\"kindName\":\"第三者责任保险\",\"serialNo\":1,\"quantity\":\"\",\"amount\":\"500000\",\"value\":\"\",\"deductibleRate\":\"\",\"unitAmount\":\"\",\"modeCode\":\"\",\"kindFlag\":1,\"rate\":\"\",\"adjustRate\":\"\",\"disCount\":\"\",\"benchmarkPremium\":\"\",\"premium\":\"\",\"unCommon\":\"\"},{\"kindCode\":\"G1\",\"kindName\":\"全车盗抢保险\",\"serialNo\":1,\"quantity\":\"\",\"amount\":\"68133\",\"value\":\"\",\"deductibleRate\":100,\"unitAmount\":\"\",\"modeCode\":\"\",\"kindFlag\":1,\"rate\":\"\",\"adjustRate\":\"\",\"disCount\":\"\",\"benchmarkPremium\":\"\",\"premium\":\"\",\"unCommon\":\"\"},{\"kindCode\":\"D3\",\"kindName\":\"车上人员责任保险（司机）\",\"serialNo\":1,\"quantity\":1,\"amount\":\"10000\",\"value\":\"\",\"deductibleRate\":\"\",\"unitAmount\":\"10000\",\"modeCode\":\"\",\"kindFlag\":1,\"rate\":\"\",\"adjustRate\":\"\",\"disCount\":\"\",\"benchmarkPremium\":\"\",\"premium\":\"\",\"unCommon\":\"\"},{\"kindCode\":\"D4\",\"kindName\":\"车上人员责任保险（乘客）\",\"serialNo\":1,\"quantity\":\"4\",\"amount\":\"40000\",\"value\":\"\",\"deductibleRate\":\"\",\"unitAmount\":\"10000\",\"modeCode\":\"\",\"kindFlag\":1,\"rate\":\"\",\"adjustRate\":\"\",\"disCount\":\"\",\"benchmarkPremium\":\"\",\"premium\":\"\",\"unCommon\":\"\"},{\"kindCode\":\"F\",\"kindName\":\"玻璃单独破碎险\",\"serialNo\":1,\"quantity\":\"\",\"amount\":\"\",\"value\":\"\",\"deductibleRate\":\"\",\"unitAmount\":\"\",\"modeCode\":\"1\",\"kindFlag\":0,\"rate\":\"\",\"adjustRate\":\"\",\"disCount\":\"\",\"benchmarkPremium\":\"\",\"premium\":\"\",\"unCommon\":\"\"},{\"kindCode\":\"L\",\"kindName\":\"车身划痕损失险\",\"serialNo\":1,\"quantity\":\"\",\"amount\":\"2000\",\"value\":\"\",\"deductibleRate\":\"\",\"unitAmount\":\"\",\"modeCode\":\"\",\"kindFlag\":1,\"rate\":\"\",\"adjustRate\":\"\",\"disCount\":\"\",\"benchmarkPremium\":\"\",\"premium\":\"\",\"unCommon\":\"\"},{\"kindCode\":\"Z\",\"kindName\":\"自燃损失险\",\"serialNo\":1,\"quantity\":\"\",\"amount\":\"68133\",\"value\":\"\",\"deductibleRate\":\"\",\"unitAmount\":\"\",\"modeCode\":\"\",\"kindFlag\":1,\"rate\":\"\",\"adjustRate\":\"\",\"disCount\":\"\",\"benchmarkPremium\":\"\",\"premium\":\"\",\"unCommon\":\"\"},{\"kindCode\":\"M\",\"kindName\":\"不计免赔额特约\",\"serialNo\":1,\"quantity\":\"\",\"amount\":\"\",\"value\":\"\",\"deductibleRate\":\"\",\"unitAmount\":\"\",\"modeCode\":\"\",\"kindFlag\":0,\"rate\":\"\",\"adjustRate\":\"\",\"disCount\":\"\",\"benchmarkPremium\":\"\",\"premium\":\"\",\"unCommon\":\"\"}]",
        "agentInfo": "agentCode=&&agentName=undefined&&agreement=&&agreementName=请选择  ",
        "applicantInfo": "applicantNature=3&&applicantName=笪世盼&&applicantPhone=&&appCertificateType=01&&appCertificateNum=320124199111151023&&applicantAddress=&&appPostCode=&&isNeedEInvoice=0&&applicantEmail=",
        "endDate": "2018-01-06 00",
        "applicationId": "",
        "channelInfo": "ProjectSerialNo=&&ProjectName=&&RepairChannelCode=&&RepairChannelName=",
        "vehicleId": "13382473",
        "insuranceType": "2",
        "queryAreaCode": "",
        "accountName": "",
        "expectDiscount": "",
        "verifyAnswer": "",
        "renewPolicyNo": "",
        "insuredInfo": "relationShip=1&&insuredNature=3&&insuredName=笪世盼&&insuredPhone=&&insCertificateType=01&&insCertificateNum=320124199111151023&&insuredAddress=&&insPostCode=&&insNation=&&insBirthday=&&insIdentifyCom=&&insIdentifyStartDate=&&insIdentifyEndDate=",
        "commericalSpecial": "",
        "specialAgreement": "[]",
        "underWriteType": "0",
        "operatorCode": "8000192691",
        "orgCode": "",
        "trafficSpecial": "",
        "insuranceOrderNo": "",
        "account": "",
        "automaticRenewalInfo": "{\"automaticRenewalFlag\":\"1\",\"autoRendepositBank\":\"工商银行\",\"autoRenAccountName\":\"\",\"autoRenAccountNO\":\"\",\"autoRenCertificateType\":\"01\",\"autoRenCertificateNO\":\"\",\"autoRenMobileNO\":\"\",\"autoRenewalPointBI\":\"\",\"autoRenewalPointCI\":\"\",\"autoRendepositCode\":\"0102\",\"automaticRenewalStatus\":\"1\"}",
        "appointDriverInfo": "DriverInoIni",
        "businessNature": "0101",
        "_action": "calculatePremium",
        "carStr": "{\"chassisNo\":\"LVRHFADL0EN572132\",\"enrollDate\":\"2015-05-08\",\"JSCheckCode\":\"kuyc\",\"JSCheckNo\":\"72CCIC320017001483579186152434\",\"JSCheckCode2\":\"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\",\"motorNo\":\"EA025760\",\"modelName\":\"福特CAF7152B5轿车\",\"licenseNo\":\"苏AN2R01\",\"licenseType\":\"02\",\"carKindCode\":\"A0\",\"useNatureCode\":\"85\",\"firstYearDate\":\"\",\"shCertificateDate\":\"\",\"transferDate\":\"\",\"carTypeAlias\":\"福特CAF7152B5轿车\",\"industryModelCode\":\"BCAAJOUB0010\",\"CarName\":\"福特CAF7152B5 时尚型\",\"industryVehicleCode\":\"CAF7152B5\",\"queryAreaCode\":\"\",\"modelCode\":\"FTBAFD0090\",\"fuelType\":\"0\",\"licenseColorCode\":\"\",\"seatCount\":\"5\",\"toncount\":\"0.0\",\"net\":\"1115.0\",\"exhaustScale\":\"1499.0\",\"powerScale\":\"81.0\",\"replacementValue\":\"76900.0\",\"actualValue\":\"68133.40\",\"vehicleCategory\":\"K31\",\"useYears\":\"1\",\"transfer\":\"0\",\"loanVehicleFlag\":\"0\",\"ecdemicVehicle\":\"0\",\"isAboutAgri\":\"0\",\"specialCarFlag\":\"0\",\"carChecker\":\"\",\"carCheckTime\":\"\",\"runMiles\":\"\",\"passportOwner\":\"笪世盼\",\"isAboutRural\":\"1\",\"ownerIdentityType\":\"01\",\"organizationCode\":\"\",\"unitType\":\"16\",\"driverBirthYear\":\"1978\",\"driverGender\":\"1\",\"arguesolution\":\"1\",\"arbitBoardname\":\"A01\",\"driverArea\":\"11\",\"vinNo\":\"LVRHFADL0EN572132\",\"purchasePrice\":\"76900.0\",\"tonCount\":\"0.0\",\"idNumber\":\"320124199111151023\",\"noLicenseFlag\":\"0\",\"argueSolution\":\"1\",\"runRegion\":\"11\",\"platformPriceType\":\"01\"}",
        "taxExtendInfo": "",
        "usbKeyInfo": "",
        "carTaxStr": "",
        "shortRateFlag": "1"
    }
