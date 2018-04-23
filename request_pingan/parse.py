# -*- coding:utf-8 -*-
__author__ = 'weikai'
from bs4 import BeautifulSoup
import jsonpath
from request_pingan.utils import conver_timestamp, conver_time

global null, false, true
null = None
false = False
true = True


def parse_toibcswriter(html):
    '''
    :param html:
    :return:https://icore-pts.pingan.com.cn/ebusiness/auto/newness/toibcswriter.do?transmitId=apply 解析返回的信息
    '''
    soup = BeautifulSoup(html, "html.parser")
    cypherText = soup.find(id="cypherText").get('value')
    timestamp = soup.find(id="timestamp").get('value')
    return {"cypherText": cypherText, "timestamp": timestamp}


def parse_renewal_data(jsonbody):
    '''
    :param jsonbody:
    :return:{"jq_totalAmount": "760", "ownershipAttributeCode": "03", "brandChnName": "上海通用东岳", "jq_insuranceEndTime": "2018-01-06 23:59:59", "vehicleLicenceCode": "苏C-296QC", "c01policyNo": "11014093980066845942", "sy_totalAmount": "2090.93", "vehicleTypeCode": "A012", "engineNo": "143450846", "ownerName": "魏居章", "vehicleFrameNo": "LSGPB54U9FD091410", "c51policyNo": "11014093900201786963", "sy_insuranceEndTime": "2018-01-06 23:59:59", "makerModel": "YLD1046SHT"}
    '''
    # 交强险 按照时间排序数组 取时间最大的
    # 商业险
    jq_code_body = jsonpath.jsonpath(jsonbody, "$.policy[?(@.planCode=='C51')]")
    sy_code_body = jsonpath.jsonpath(jsonbody, "$.policy[?(@.planCode=='C01')]")
    userdata = __parse_code_body(jq_code_body, sy_code_body)

    if userdata != 0:
        return userdata
    # quote开头的为询价单 不做续保信息返回
    return 0


def __parse_code_body(jq_code_body, sy_code_body):
    userdata = {}
    if jq_code_body != False:
        for i in jq_code_body:
            i['insuranceEndTime'] = conver_timestamp(i['insuranceEndTime'])
            i['insuranceBeginTime'] = conver_timestamp(i['insuranceBeginTime'])
        jq_code_body.sort(key=lambda obj: obj.get('insuranceEndTime'))
        jq = jq_code_body[len(jq_code_body) - 1]
        userdata['engineNo'] = jq['engineNo']
        userdata['vehicleFrameNo'] = jq['vehicleFrameNo']
        userdata['vehicleLicenceCode'] = jq['vehicleLicenceCode']
        userdata['jq_totalAmount'] = jq['totalAmount']
        userdata['makerModel'] = jq['makerModel']
        userdata['vehicleTypeCode'] = jq['vehicleTypeCode']
        userdata['brandChnName'] = jq.get("brandChnName", "")
        userdata['jq_insuranceBeginTime'] = conver_time(jq['insuranceBeginTime'])
        userdata['jq_insuranceEndTime'] = conver_time(jq['insuranceEndTime'])
        userdata['ownerName'] = jq['ownerName']
        userdata['ownershipAttributeCode'] = jq['ownershipAttributeCode']
        userdata['c51policyNo'] = jq.get("policyNo", "")
        if userdata['c51policyNo'] == "":
            userdata['c51QuotationNo'] = jq.get("quotationNo", "")

    if sy_code_body != False:
        for i in sy_code_body:
            i['insuranceEndTime'] = conver_timestamp(i['insuranceEndTime'])
            i['insuranceBeginTime'] = conver_timestamp(i['insuranceBeginTime'])
        sy_code_body.sort(key=lambda obj: obj.get('insuranceEndTime'))
        sy = sy_code_body[len(sy_code_body) - 1]
        userdata['engineNo'] = sy['engineNo']
        userdata['vehicleFrameNo'] = sy['vehicleFrameNo']
        userdata['vehicleLicenceCode'] = sy['vehicleLicenceCode']
        userdata['sy_totalAmount'] = sy['totalAmount']
        userdata['makerModel'] = sy['makerModel']
        userdata['vehicleTypeCode'] = sy['vehicleTypeCode']
        userdata['brandChnName'] = sy.get("brandChnName", "")
        userdata['sy_insuranceBeginTime'] = conver_time(sy['insuranceBeginTime'])
        userdata['sy_insuranceEndTime'] = conver_time(sy['insuranceEndTime'])
        userdata['ownerName'] = sy.get("ownerName", "")
        userdata['ownershipAttributeCode'] = sy['ownershipAttributeCode']
        userdata['c01policyNo'] = sy.get("policyNo", "")
        if userdata['c01policyNo'] == "":
            userdata['c51QuotationNo'] = sy.get("quotationNo", "")
    if len(userdata) != 0:
        return userdata
    return 0


# 从续保信息中获取用户以及车辆信息
def parse_user_data(jsonbody):
    data_info = {}
    data_info['autoModelType'] = jsonbody['autoModelType']
    data_info['vehicleTarget'] = jsonbody['voucher']['vehicleTarget']
    data_info['insurantInfo'] = jsonbody['voucher']['insurantInfo']
    data_info['extendInfo'] = jsonbody['voucher']['extendInfo']
    return data_info


def parse_fee(jsonbody):
    '''
    :param jsonbody:
    :return:保费信息
    '''
    ls = []
    all = {}
    c01DutyList = jsonbody.get("voucher", {}).get("c01DutyList", "")
    if c01DutyList != "":
        for i in c01DutyList:
            dtc = {}
            # if i.get("dutyName","")!="":

            dtc['dutyName'] = i.get("dutyName", "")
            dtc["dutyCode"] = i["dutyCode"]
            dtc["totalActualPremium"] = i["totalActualPremium"]
            dtc['insuredAmount'] = i['insuredAmount']
            # else:
            # continue
            ls.append(dtc)
            all['SY'] = ls
    else:
        all['SY'] = False

    sy_xishu = jsonbody.get("voucher", {}).get("c01DisplayRateFactorList", "")
    if sy_xishu != "":
        for i in sy_xishu:
            if i.get("factorCode", "") == "F999":
                if i['factorRatioBGD'] != 0:
                    all["sy_xishu"] = i['factorRatioBGD']
                elif i['factorRatioVHL'] != 0:
                    all["sy_xishu"] = i['factorRatioVHL']
                elif i['factorRatioCOM'] != 0:
                    all["sy_xishu"] = i['factorRatioCOM']
                elif i['factorRatioOTHERS'] != 0:
                    all["sy_xishu"] = i['factorRatioOTHERS']
                else:
                    all["sy_xishu"] = i['factorRatioBGD']

    jq_baofei = jsonbody['voucher']['c51BaseInfo']['totalActualPremium']
    jq_xishu = float(jsonbody['voucher']['c51BaseInfo']['totalActualPremium']) / float(
        jsonbody['voucher']['c51BaseInfo']['totalStandardPremium'])
    cartax = jsonbody['voucher']['vehicleTaxInfo']['totalTaxMoney']
    all['jq_baofei'] = jq_baofei
    all['jq_xishu'] = jq_xishu
    all['cartax'] = cartax
    all['seats'] = jsonbody['voucher']['vehicleTarget']['vehicleSeats']
    return __parse_fee(all)


def __parse_fee(jsonbody):
    # 车辆超过三年的车没有划痕险
    ifel = lambda x: x if x is False else x[0]['totalActualPremium']
    ifel2 = lambda x: x if x is False else x[0]['insuredAmount']
    BaoE = MarkPremium = {}
    carNickPremium = jsonpath.jsonpath(jsonbody, "$.SY[?(@.dutyCode=='17')]")
    carDamagePremium = jsonpath.jsonpath(jsonbody, "$.SY[?(@.dutyCode=='01')]")
    carTheftPremium = jsonpath.jsonpath(jsonbody, "$.SY[?(@.dutyCode=='03')]")
    otherHurtPremium = jsonpath.jsonpath(jsonbody, "$.SY[?(@.dutyCode=='02')]")
    driverDutyPremium = jsonpath.jsonpath(jsonbody, "$.SY[?(@.dutyCode=='04')]")
    passengerDutyPremium = jsonpath.jsonpath(jsonbody, "$.SY[?(@.dutyCode=='05')]")
    glassBrokenPremium = jsonpath.jsonpath(jsonbody, "$.SY[?(@.dutyCode=='08')]")
    carFirePremium = jsonpath.jsonpath(jsonbody, "$.SY[?(@.dutyCode=='18')]")
    engineWadingPremium = jsonpath.jsonpath(jsonbody, "$.SY[?(@.dutyCode=='41')]")
    repairFactoryPremium = jsonpath.jsonpath(jsonbody, "$.SY[?(@.dutyCode=='57')]")
    Premium = {
        "compulsory_insurance": jsonbody['jq_baofei'],  # 交强险
        "NAggTax": jsonbody['cartax'],  # 车船税
        "carDamagePremium": ifel(carDamagePremium),  # 车损险
        "carTheftPremium": ifel(carTheftPremium),  # 盗抢险
        "otherHurtPremium": ifel(otherHurtPremium),  # 三者险
        "driverDutyPremium": ifel(driverDutyPremium),  # 车上人员险（司机）
        "passengerDutyPremium": ifel(passengerDutyPremium),  # 车上人员险(乘客)
        "carNickPremium": ifel(carNickPremium),  # 划痕险
        "glassBrokenPremium": ifel(glassBrokenPremium),  # 玻璃破碎险
        "carFirePremium": ifel(carFirePremium),  # 自燃损失险
        "engineWadingPremium": ifel(engineWadingPremium),  # 发动机涉水险
        "repairFactoryPremium": ifel(repairFactoryPremium),
        "seatCount": jsonbody['seats']
    }

    otherHurtBaoE = jsonpath.jsonpath(jsonbody, "$.SY[?(@.dutyCode=='02')]")
    carDamageBaoE = jsonpath.jsonpath(jsonbody, "$.SY[?(@.dutyCode=='01')]")
    driverDutyBaoE = jsonpath.jsonpath(jsonbody, "$.SY[?(@.dutyCode=='04')]")
    passengerDutyBaoe = jsonpath.jsonpath(jsonbody, "$.SY[?(@.dutyCode=='05')]")
    carNickBaoE = jsonpath.jsonpath(jsonbody, "$.SY[?(@.dutyCode=='17')]")
    if passengerDutyBaoe != False:
        passengerDutyBaoe = passengerDutyBaoe[0]['insuredAmount'] * (int(jsonbody['seats']) - 1)
    else:
        passengerDutyBaoe = False
    BaoE = {
        "carTheftBaoE": ifel2(carDamageBaoE),
        "carDamageBaoE": ifel2(carDamageBaoE),
        "otherHurtBaoE": ifel2(otherHurtBaoE),
        "driverDutyBaoE": ifel2(driverDutyBaoE),
        "passengerDutyBaoe": passengerDutyBaoe,
        "carNickBaoE": ifel2(carNickBaoE)
    }
    carDamageBenchMarkPremium = jsonpath.jsonpath(jsonbody, "$.SY[?(@.dutyCode=='27')]")
    carTheftBenchMarkPremium = jsonpath.jsonpath(jsonbody, "$.SY[?(@.dutyCode=='48')]")
    otherHurtBenchMarkPremium = jsonpath.jsonpath(jsonbody, "$.SY[?(@.dutyCode=='28')]")
    driverDutyBenchMarkPremium = jsonpath.jsonpath(jsonbody, "$.SY[?(@.dutyCode=='49')]")
    passengerBenchMarkPremium = jsonpath.jsonpath(jsonbody, "$.SY[?(@.dutyCode=='80')]")
    carNickBenchMarkPremium = jsonpath.jsonpath(jsonbody, "$.SY[?(@.dutyCode=='75')]")  # 划痕险不计免赔含税保费
    carFireBrokenBenchMarkPremium = jsonpath.jsonpath(jsonbody, "$.SY[?(@.dutyCode=='77')]")
    engineWadingBenchMarkPremium = jsonpath.jsonpath(jsonbody, "$.SY[?(@.dutyCode=='79')]")
    MarkPremium = {
        "carDamageBenchMarkPremium": ifel(carDamageBenchMarkPremium),  # 车损险不计免赔
        "carTheftBenchMarkPremium": ifel(carTheftBenchMarkPremium),  # 盗抢险不计免赔
        "otherHurtBenchMarkPremium": ifel(otherHurtBenchMarkPremium),  # 三者责任险的不计免赔
        "driverDutyBenchMarkPremium": ifel(driverDutyBenchMarkPremium),  # 车上人员责任险（司机）不计免赔含税保费
        "passengerBenchMarkPremium": ifel(passengerBenchMarkPremium),  # 车上人员责任险（乘客）不计免赔含税保费
        "carNickBenchMarkPremium": ifel(carNickBenchMarkPremium),  # 划痕险不计免赔含税保费
        "carFireBrokenBenchMarkPremium": ifel(carFireBrokenBenchMarkPremium),  # 自燃损失险不计免赔含税保费
        "engineWadingBenchMarkPremium": ifel(engineWadingBenchMarkPremium)  # 发动机涉水险不计免赔含税保费
    }
    disCount = {
        "sy_disCount": jsonbody.get("sy_xishu", False),
        "jq_disCount": jsonbody.get("jq_xishu", False)
    }
    Premium2 = {}
    BaoE2 = {}
    MarkPremium2 = {}
    disCount2 = {}
    for i in Premium:
        if Premium[i] != False:
            Premium2[i] = Premium[i]

    for i in BaoE:
        if BaoE[i] != False:
            BaoE2[i] = BaoE[i]

    for i in MarkPremium:
        if MarkPremium[i] != False:
            MarkPremium2[i] = MarkPremium[i]
    for i in disCount:
        if disCount[i] != False:
            disCount2[i] = disCount[i]
    PremiumInfo = [Premium2, BaoE2, MarkPremium2, disCount2]
    print(PremiumInfo)
    return PremiumInfo


# 解析上年度的保费信息
# c01商业 C51交强
def parse_lastyear_info(body):
    SY_RSP = body.get("voucher", {}).get("c01DutyList", False)
    JQ_RSP = body.get("voucher", {}).get("c51DutyList", False)
    JqSumPremium = "0"
    if JQ_RSP != False and len(JQ_RSP) > 0:
        compulsoryInsurance = nAggTax = "1"
    else:
        compulsoryInsurance = nAggTax = "0"
        JqSumPremium = "0"

    if SY_RSP != False:
        carNickPremium = jsonpath.jsonpath(SY_RSP, "$.[?(@.dutyCode=='17')]")
        carDamagePremium = jsonpath.jsonpath(SY_RSP, "$.[?(@.dutyCode=='01')]")
        carTheftPremium = jsonpath.jsonpath(SY_RSP, "$.[?(@.dutyCode=='03')]")
        otherHurtPremium = jsonpath.jsonpath(SY_RSP, "$.[?(@.dutyCode=='02')]")
        driverDutyPremium = jsonpath.jsonpath(SY_RSP, "$.[?(@.dutyCode=='04')]")
        passengerDutyPremium = jsonpath.jsonpath(SY_RSP, "$.[?(@.dutyCode=='05')]")
        glassBrokenPremium = jsonpath.jsonpath(SY_RSP, "$.[?(@.dutyCode=='08')]")
        carFirePremium = jsonpath.jsonpath(SY_RSP, "$.[?(@.dutyCode=='18')]")
        engineWadingPremium = jsonpath.jsonpath(SY_RSP, "$.[?(@.dutyCode=='41')]")
        repairFactoryPremium = jsonpath.jsonpath(SY_RSP, "$.[?(@.dutyCode=='57')]")
        # 不计免赔
        carDamagePremiumBench = jsonpath.jsonpath(SY_RSP, "$.[?(@.dutyCode=='27')]")
        carTheftPremiumBench = jsonpath.jsonpath(SY_RSP, "$.[?(@.dutyCode=='48')]")
        otherHurtPremiumBench = jsonpath.jsonpath(SY_RSP, "$.[?(@.dutyCode=='28')]")
        driverDutyPremiumBench = jsonpath.jsonpath(SY_RSP, "$.[?(@.dutyCode=='49')]")
        passengerDutyPremiumBench = jsonpath.jsonpath(SY_RSP, "$.[?(@.dutyCode=='80')]")
        carNickPremiumBench = jsonpath.jsonpath(SY_RSP, "$.[?(@.dutyCode=='75')]")  # 划痕险不计免赔含税保费
        carFirePremiumBench = jsonpath.jsonpath(SY_RSP, "$.[?(@.dutyCode=='77')]")
        engineWadingPremiumBench = jsonpath.jsonpath(SY_RSP, "$.[?(@.dutyCode=='79')]")

        msg = {
            'compulsoryInsurance': compulsoryInsurance, 'nAggTax': nAggTax,
            'otherHurtPremium': {"isCheck": ("1" if otherHurtPremium != False else "0"), "Amount": (
                otherHurtPremium[0]['insuredAmount'] if otherHurtPremium != False else "0")},
            'carNickPremium': {"isCheck": ("1" if carNickPremium != False else "0"),
                               "Amount": (carNickPremium[0]['insuredAmount'] if carNickPremium != False else "0")},
            'driverDutyPremium': {"isCheck": ("1" if driverDutyPremium != False else "0"), "Amount": (
                driverDutyPremium[0]['insuredAmount'] if driverDutyPremium != False else "0")},
            'passengerDutyPremium': {"isCheck": ("1" if passengerDutyPremium != False else "0"), "Amount": (
                passengerDutyPremium[0]['insuredAmount'] if passengerDutyPremium != False else "0")},
            'glassBrokenPremium': ("1" if glassBrokenPremium != False else "0"),
            'carFirePremium': ("1" if carFirePremium != False else "0"),
            'engineWadingPremium': ("1" if engineWadingPremium != False else "0"),
            'carTheftPremium': ("1" if carTheftPremium != False else "0"),
            'carDamagePremium': ("1" if carDamagePremium != False else "0"),
            "repairFactoryPremium": ("1" if repairFactoryPremium != False else "0"),
            'carDamageBenchMarkPremium': ("1" if carDamagePremiumBench != False else "0"),
            'otherHurtBenchMarkPremium': ("1" if otherHurtPremiumBench != False else "0"),
            'carTheftBenchMarkPremium': ("1" if carTheftPremiumBench != False else "0"),
            'driverDutyBenchMarkPremium': ("1" if driverDutyPremiumBench != False else "0"),
            'passengerBenchMarkPremium': ("1" if passengerDutyPremiumBench != False else "0"),
            'carNickBenchMarkPremium': ("1" if carNickPremiumBench != False else "0"),
            'carFireBrokenBenchMarkPremium': ("1" if carFirePremiumBench != False else "0"),
            'engineWadingBenchMarkPremium': ("1" if engineWadingPremiumBench != False else "0"),
            'SySumPremium': "0",
            'JqSumPremium': "0"
        }
        return msg

    msg2 = {
        'compulsoryInsurance': compulsoryInsurance, 'nAggTax': nAggTax,
        'otherHurtPremium': {"isCheck": "0", "Amount": "0"},
        'carNickPremium': {"isCheck": "0", "Amount": "0"},
        'driverDutyPremium': {"isCheck": "0", "Amount": "0"},
        'passengerDutyPremium': {"isCheck": "0", "Amount": "0"},
        'glassBrokenPremium': "0",
        'carFirePremium': "0",
        'engineWadingPremium': "0",
        'carTheftPremium': "0",
        'carDamagePremium': "0",
        'carDamageBenchMarkPremium': "0",
        'otherHurtBenchMarkPremium': "0",
        'carTheftBenchMarkPremium': "0",
        'driverDutyBenchMarkPremium': "0",
        'passengerBenchMarkPremium': "0",
        'carNickBenchMarkPremium': "0",
        'carFireBrokenBenchMarkPremium': "0",
        'engineWadingBenchMarkPremium': "0",
        'SySumPremium': "0",
        'JqSumPremium': JqSumPremium
    }
    return msg2

if __name__ == "__main__":
    # print parsedataObjs(demo)
    f = open("C:\Users\weikai\Desktop\\2.json", "r")
    body = eval(f.read())
    print parse_fee(body)
    #print cic_parse_lastyear_premium(body)
    pass
