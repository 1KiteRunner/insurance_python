# -*- coding:utf-8 -*-
import json
import jsonpath
def readJson(sy_resp,jq_resp):
    compulsory_insurance = False
    NAggTax = False
    JQ_disCount = 1
    if jq_resp is not None:
        try:
            compulsory_insurance = float(jq_resp[0]['ciInsureDemand'].get("premium","0"))
            NAggTax = jq_resp[0]['ciInsureTax'].get("sumTax","0")
            JQ_disCount = 1 + float(jq_resp[0]['ciInsureDemand']['claimCoeff'])
        except:
            compulsory_insurance = False
            NAggTax = False


    Sy_disCount = 1
    Premium = {}
    BaoE = {}
    MarkPremium = {}
    Premium['compulsory_insurance'] = compulsory_insurance
    Premium['NAggTax'] = NAggTax

    carDamageMark = jsonpath.jsonpath(sy_resp, "$.[?(@.kindCode=='050930')]")
    if carDamageMark:
        MarkPremium['carDamageBenchMarkPremium'] = carDamageMark[0]['premium']

    carTheftBenchMark = jsonpath.jsonpath(sy_resp, "$.[?(@.kindCode=='050932')]")
    if carTheftBenchMark:
        MarkPremium['carTheftBenchMarkPremium'] = carTheftBenchMark[0]['premium']

    otherHurtBenchMark = jsonpath.jsonpath(sy_resp, "$.[?(@.kindCode=='050931')]")
    if otherHurtBenchMark:
        MarkPremium['otherHurtBenchMarkPremium'] = otherHurtBenchMark[0]['premium']

    driverDutyBenchMark = jsonpath.jsonpath(sy_resp, "$.[?(@.kindCode=='050933')]")
    if driverDutyBenchMark:
        MarkPremium['driverDutyBenchMarkPremium'] = driverDutyBenchMark[0]['premium']

    passengerBenchMark = jsonpath.jsonpath(sy_resp, "$.[?(@.kindCode=='050934')]")
    if passengerBenchMark:
        MarkPremium['passengerBenchMarkPremium'] = passengerBenchMark[0]['premium']

    carNickBenchMark = jsonpath.jsonpath(sy_resp, "$.[?(@.kindCode=='050937')]")
    if carNickBenchMark:
        MarkPremium['carNickBenchMarkPremium'] = carNickBenchMark[0]['premium']

    carFireBrokenBenchMark = jsonpath.jsonpath(sy_resp, "$.[?(@.kindCode=='050935')]")
    if carFireBrokenBenchMark:
        MarkPremium['carNickBenchMarkPremium'] = carFireBrokenBenchMark[0]['premium']

    engineWadingBenchMark = jsonpath.jsonpath(sy_resp, "$.[?(@.kindCode=='050938')]")
    if engineWadingBenchMark:
        MarkPremium['carNickBenchMarkPremium'] = engineWadingBenchMark[0]['premium']

    carDamage = jsonpath.jsonpath(sy_resp, "$.[?(@.kindCode=='050202')]")
    if carDamage:#车损险
        Sy_disCount = carDamage[0]['disCount']
        Premium['carDamagePremium'] = carDamage[0]['premium']

    carTheft = jsonpath.jsonpath(sy_resp, "$.[?(@.kindCode=='050501')]")
    if carTheft:#盗抢险
        Sy_disCount = carTheft[0]['disCount']
        Premium['carTheftPremium'] = carTheft[0]['premium']

    otherHurt = jsonpath.jsonpath(sy_resp, "$.[?(@.kindCode=='050602')]")
    if  otherHurt:#三者险
        Sy_disCount = otherHurt[0]['disCount']
        Premium['otherHurtPremium'] = otherHurt[0]['premium']
        BaoE['otherHurtBaoE'] = otherHurt[0]['amount']

    driverDuty = jsonpath.jsonpath(sy_resp, "$.[?(@.kindCode=='050711')]")
    if driverDuty:#司机座位险
        Sy_disCount = driverDuty[0]['disCount']
        Premium['driverDutyPremium'] = driverDuty[0]['premium']
        BaoE['driverDutyBaoE'] = driverDuty[0]['amount']

    passengerDuty = jsonpath.jsonpath(sy_resp, "$.[?(@.kindCode=='050712')]")
    if  passengerDuty:#乘客座位险
        Sy_disCount = passengerDuty[0]['disCount']
        Premium['passengerDutyPremium'] = passengerDuty[0]['premium']
        BaoE['passengerDutyBaoe'] = passengerDuty[0]['amount']

    carNick = jsonpath.jsonpath(sy_resp, "$.[?(@.kindCode=='050211')]")
    if  carNick:#车身划痕险
        Sy_disCount =  carNick[0]['disCount']
        Premium['carNickPremium'] = carNick[0]['premium']
        BaoE['carNickBaoE'] = carNick[0]['amount']

    glassBroken = jsonpath.jsonpath(sy_resp, "$.[?(@.kindCode=='050232')]")
    if  glassBroken:#玻璃破碎险
        Sy_disCount = glassBroken[0]['disCount']
        Premium['glassBrokenPremium'] = glassBroken[0]['premium']

    carFire = jsonpath.jsonpath(sy_resp, "$.[?(@.kindCode=='050311')]")
    if  carFire:#自燃
        Sy_disCount = carFire[0]['disCount']
        Premium['carFirePremium'] = carFire[0]['premium']

    engineWading = jsonpath.jsonpath(sy_resp, "$.[?(@.kindCode=='050461')]")
    if  engineWading:#发动机涉水
        Sy_disCount = engineWading[0]['disCount']
        Premium['engineWadingPremium'] = engineWading[0]['premium']

    disCount={
        "sy_disCount":Sy_disCount,
        "jq_disCount":JQ_disCount
    }
    PremiumInfo = [Premium,BaoE,MarkPremium,disCount]
    return PremiumInfo
