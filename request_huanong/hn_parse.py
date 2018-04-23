# -*- coding:utf-8 -*-
__author__ = 'weikai'
import jsonpath


def hn_getPriumeInf(jsonbody):
    #print(jsonbody)
    JQ = jsonpath.jsonpath(jsonbody, "$.kinds[?(@.kindCode=='BZ')]")  # 交强险
    SY = jsonpath.jsonpath(jsonbody, "$.kinds[?(@.kindCode!='BZ')]")  # 拿商业险系数
    carNickPremium = jsonpath.jsonpath(jsonbody, "$.kinds[?(@.kindCode=='L')]")
    carDamagePremium = jsonpath.jsonpath(jsonbody, "$.kinds[?(@.kindCode=='A')]")
    carTheftPremium = jsonpath.jsonpath(jsonbody, "$.kinds[?(@.kindCode=='G')]")
    otherHurtPremium = jsonpath.jsonpath(jsonbody, "$.kinds[?(@.kindCode=='B')]")
    driverDutyPremium = jsonpath.jsonpath(jsonbody, "$.kinds[?(@.kindCode=='D3')]")
    passengerDutyPremium = jsonpath.jsonpath(jsonbody, "$.kinds[?(@.kindCode=='D4')]")
    glassBrokenPremium = jsonpath.jsonpath(jsonbody, "$.kinds[?(@.kindCode=='F')]")
    carFirePremium = jsonpath.jsonpath(jsonbody, "$.kinds[?(@.kindCode=='Z')]")
    engineWadingPremium = jsonpath.jsonpath(jsonbody, "$.kinds[?(@.kindCode=='X1')]")

    # 不计免赔
    carNickPremiumBench = jsonpath.jsonpath(jsonbody, "$.kinds[?(@.kindCode=='ML')]")
    carDamagePremiumBench = jsonpath.jsonpath(jsonbody, "$.kinds[?(@.kindCode=='MA')]")
    carTheftPremiumBench = jsonpath.jsonpath(jsonbody, "$.kinds[?(@.kindCode=='MG')]")
    otherHurtPremiumBench = jsonpath.jsonpath(jsonbody, "$.kinds[?(@.kindCode=='MB')]")
    driverDutyPremiumBench = jsonpath.jsonpath(jsonbody, "$.kinds[?(@.kindCode=='MD3')]")
    passengerDutyPremiumBench = jsonpath.jsonpath(jsonbody, "$.kinds[?(@.kindCode=='MD4')]")
    carFirePremiumBench = jsonpath.jsonpath(jsonbody, "$.kinds[?(@.kindCode=='MZ')]")
    engineWadingPremiumBench = jsonpath.jsonpath(jsonbody, "$.kinds[?(@.kindCode=='MX1')]")

    tax = jsonbody.get("tax", {}).get("sumPayment", "")

    Premium = {
        "compulsory_insurance": JQ[0]["premium"] if JQ != False else False,  # 交强险
        "NAggTax": [tax, False][tax == ""],  # 车船税
        "carDamagePremium": carDamagePremium[0]["premium"] if carDamagePremium != False else False,  # 车损险
        "carTheftPremium": carTheftPremium[0]["premium"] if carTheftPremium != False else False,  # 盗抢险
        "otherHurtPremium": otherHurtPremium[0]["premium"] if otherHurtPremium != False else False,  # 三者险
        "driverDutyPremium": driverDutyPremium[0]["premium"] if driverDutyPremium != False else False,  # 车上人员险（司机）
        "passengerDutyPremium": passengerDutyPremium[0]["premium"] if passengerDutyPremium != False else False,
        # 车上人员险(乘客)
        "carNickPremium": carNickPremium[0]["premium"] if carNickPremium != False else False,  # 划痕险
        "glassBrokenPremium": glassBrokenPremium[0]["premium"] if glassBrokenPremium != False else False,  # 玻璃破碎险
        "carFirePremium": carFirePremium[0]["premium"] if carFirePremium != False else False,  # 自燃损失险
        "engineWadingPremium": engineWadingPremium[0]["premium"] if engineWadingPremium != False else False,  # 发动机涉水险
        "seatCount": jsonbody.get("vehicleJingyou", {}).get("seat", "5")
    }

    BaoE = {
        "carTheftBaoE": carTheftPremium[0]["amount"] if carTheftPremium != False else False,
        "carDamageBaoE": carDamagePremium[0]["amount"] if carDamagePremium != False else False,
        "otherHurtBaoE": otherHurtPremium[0]["amount"] if otherHurtPremium != False else False,
        "driverDutyBaoE": driverDutyPremium[0]["amount"] if driverDutyPremium != False else False,
        "passengerDutyBaoe": passengerDutyPremium[0]["amount"] if passengerDutyPremium != False else False,
        "carNickBaoE": carNickPremium[0]["amount"] if carNickPremium != False else False
    }

    MarkPremium = {
        "carDamageBenchMarkPremium": carDamagePremiumBench[0]["premium"] if carDamagePremiumBench != False else False,
        # 车损险不计免赔
        "carTheftBenchMarkPremium": carTheftPremiumBench[0]["premium"] if carTheftPremiumBench != False else False,
        # 盗抢险不计免赔
        "otherHurtBenchMarkPremium": otherHurtPremiumBench[0]["premium"] if otherHurtPremiumBench != False else False,
        # 三者责任险的不计免赔
        "driverDutyBenchMarkPremium": driverDutyPremiumBench[0][
            "premium"] if driverDutyPremiumBench != False else False,
        # 车上人员责任险（司机）不计免赔含税保费
        "passengerBenchMarkPremium": passengerDutyPremiumBench[0][
            "premium"] if passengerDutyPremiumBench != False else False,
        # 车上人员责任险（乘客）不计免赔含税保费
        "carNickBenchMarkPremium": carNickPremiumBench[0]["premium"] if carNickPremiumBench != False else False,
        # 划痕险不计免赔含税保费
        "carFireBrokenBenchMarkPremium": carFirePremiumBench[0]["premium"] if carFirePremiumBench != False else False,
        # 自燃损失险不计免赔含税保费
        "engineWadingBenchMarkPremium": engineWadingPremiumBench[0][
            "premium"] if engineWadingPremiumBench != False else False,
        # 发动机涉水险不计免赔含税保费
    }
    sy_disCount = jsonbody.get("base", {}).get("entireRecommenDiscount", False)
    if sy_disCount == "":
        sy_disCount = jsonbody.get("base", {}).get("minDiscount", False)

    disCount = {
        "sy_disCount": (sy_disCount) if sy_disCount != False else False,
        "jq_disCount": ((JQ[0]["premium"] / JQ[0]["benchMarkPremium"])) if JQ != False else False
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
    #print PremiumInfo
    return PremiumInfo


# 解析上年保险组合
def hn_parse_renrwal(JQ_RSP, SY_RSP):
    if JQ_RSP != False:
        JQ = jsonpath.jsonpath(JQ_RSP, "$.kinds[?(@.kindCode=='BZ')]")  # 交强险
        compulsoryInsurance = nAggTax = "1"
        JqSumPremium = JQ_RSP['base']['sumPremium']
    else:
        compulsoryInsurance = nAggTax = "0"
        JqSumPremium = "0"
        # "1" if carNickPremium != False else "0"
    if SY_RSP != False:
        carNickPremium = jsonpath.jsonpath(SY_RSP, "$.kinds[?(@.kindCode=='L')]")
        carDamagePremium = jsonpath.jsonpath(SY_RSP, "$.kinds[?(@.kindCode=='A')]")
        carTheftPremium = jsonpath.jsonpath(SY_RSP, "$.kinds[?(@.kindCode=='G')]")
        otherHurtPremium = jsonpath.jsonpath(SY_RSP, "$.kinds[?(@.kindCode=='B')]")
        driverDutyPremium = jsonpath.jsonpath(SY_RSP, "$.kinds[?(@.kindCode=='D4')]")
        passengerDutyPremium = jsonpath.jsonpath(SY_RSP, "$.kinds[?(@.kindCode=='D3')]")
        glassBrokenPremium = jsonpath.jsonpath(SY_RSP, "$.kinds[?(@.kindCode=='F')]")
        carFirePremium = jsonpath.jsonpath(SY_RSP, "$.kinds[?(@.kindCode=='Z')]")
        engineWadingPremium = jsonpath.jsonpath(SY_RSP, "$.kinds[?(@.kindCode=='X1')]")

        # 不计免赔
        carNickPremiumBench = jsonpath.jsonpath(SY_RSP, "$.kinds[?(@.kindCode=='ML')]")
        carDamagePremiumBench = jsonpath.jsonpath(SY_RSP, "$.kinds[?(@.kindCode=='MA')]")
        carTheftPremiumBench = jsonpath.jsonpath(SY_RSP, "$.kinds[?(@.kindCode=='MG')]")
        otherHurtPremiumBench = jsonpath.jsonpath(SY_RSP, "$.kinds[?(@.kindCode=='MB')]")
        driverDutyPremiumBench = jsonpath.jsonpath(SY_RSP, "$.kinds[?(@.kindCode=='MD4')]")
        passengerDutyPremiumBench = jsonpath.jsonpath(SY_RSP, "$.kinds[?(@.kindCode=='MD3')]")
        carFirePremiumBench = jsonpath.jsonpath(SY_RSP, "$.kinds[?(@.kindCode=='MZ')]")
        engineWadingPremiumBench = jsonpath.jsonpath(SY_RSP, "$.kinds[?(@.kindCode=='MX1')]")
        msg = {
            'compulsoryInsurance': compulsoryInsurance, 'nAggTax': nAggTax,
            'otherHurtPremium': {"isCheck": ("1" if otherHurtPremium != False else "0"),
                                 "Amount": (otherHurtPremium[0]['amount'] if otherHurtPremium != False else "0")},
            'carNickPremium': {"isCheck": ("1" if carNickPremium != False else "0"),
                               "Amount": (carNickPremium[0]['amount'] if carNickPremium != False else "0")},
            'driverDutyPremium': {"isCheck": ("1" if driverDutyPremium != False else "0"),
                                  "Amount": (driverDutyPremium[0]['amount'] if driverDutyPremium != False else "0")},
            'passengerDutyPremium': {"isCheck": ("1" if passengerDutyPremium != False else "0"), "Amount": (
                passengerDutyPremium[0]['amount'] if passengerDutyPremium != False else "0")},
            'glassBrokenPremium': ("1" if glassBrokenPremium != False else "0"),
            'carFirePremium': ("1" if carFirePremium != False else "0"),
            'engineWadingPremium': ("1" if engineWadingPremium != False else "0"),
            'carTheftPremium': ("1" if carTheftPremium != False else "0"),
            'carDamagePremium': ("1" if carDamagePremium != False else "0"),
            'carDamageBenchMarkPremium': ("1" if carDamagePremiumBench != False else "0"),
            'otherHurtBenchMarkPremium': ("1" if otherHurtPremiumBench != False else "0"),
            'carTheftBenchMarkPremium': ("1" if carTheftPremiumBench != False else "0"),
            'driverDutyBenchMarkPremium': ("1" if driverDutyPremiumBench != False else "0"),
            'passengerBenchMarkPremium': ("1" if passengerDutyPremiumBench != False else "0"),
            'carNickBenchMarkPremium': ("1" if carNickPremiumBench != False else "0"),
            'carFireBrokenBenchMarkPremium': ("1" if carFirePremiumBench != False else "0"),
            'engineWadingBenchMarkPremium': ("1" if engineWadingPremiumBench != False else "0"),
            'SySumPremium': SY_RSP['base']['sumPremium'],
            'JqSumPremium': JqSumPremium
        }
        return msg
    else:
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
    from test.test4 import body

    # print hn_getPriumeInf(body)

    body = {
        "kinds": [
            {
                "unitAmount": 0.0,
                "amount": 49200.0,
                "flag": "11",
                "deductible": 0.0,
                "kindCode": "A",
                "quantity": 0
            },
            {
                "unitAmount": 0.0,
                "amount": 500000.0,
                "flag": "11",
                "deductible": 0.0,
                "kindCode": "B",
                "quantity": 0
            },
            {
                "unitAmount": 10000.0,
                "amount": 10000.0,
                "flag": "11",
                "deductible": 0.0,
                "kindCode": "D3",
                "quantity": 1
            },
            {
                "unitAmount": 0.0,
                "amount": 0.0,
                "flag": "20",
                "deductible": 0.0,
                "kindCode": "M",
                "quantity": 0
            }
        ],
        "car": {
            "licenseNo": "苏JLS055",
            "modelName": "五菱LZW6432KF",
            "vinNo": "LZWADAGA9C4170171",
            "exhaustScale": 1.206,
            "frameNo": "LZWADAGA9C4170171",
            "colorCode": "01",
            "licenseType": "02",
            "runAreaCode": "11",
            "purchasePrice": 49200.0,
            "enrollDate": "2012-04-27",
            "engineNo": "8C32410600",
            "licenseColorCode": "01",
            "runMiles": 20000.0,
            "netWeight": 1230.0,
            "useNatureCode": "85",
            "vehicleStyle": "K31",
            "fuelType": "",
            "modelCode": "TYBAYD0037",
            "modelAlias": "五菱LZW6432KF"
        },
        "tax": {

        },
        "devices": [

        ],
        "persons": [
            {
                "insuredName": "严乃井",
                "carRelation": "1",
                "insuredType": "3",
                "insuredFlag": "010000",
                "insuredAddress": "阜宁县",
                "mobile": "",
                "phoneNumber": "87241053",
                "postCode": "224400",
                "identifyNumber": "320923196809182714",
                "identifyType": "01"
            },
            {
                "insuredName": "严乃井",
                "identifyNumber": "320923196809182714",
                "insuredType": "3",
                "insuredFlag": "100000",
                "insuredAddress": "阜宁县",
                "mobile": "",
                "phoneNumber": "87241053",
                "postCode": "224400",
                "identifyType": "01"
            },
            {
                "insuredName": "严乃井",
                "identifyNumber": "320923196809182714",
                "insuredType": "3",
                "insuredFlag": "001000",
                "insuredNature": "1",
                "identifyType": "01"
            }
        ],
        "base": {
            "endDate": "2014-04-15",
            "sumexcludeTaxPremiumBI": 0.0,
            "expenseRateBI": 0.0,
            "arbitBoardName": "",
            "shareHolderFlag": "0",
            "sumAmount": 559200.0,
            "isAboutArgi": "0",
            "argueSolution": "1",
            "sumvalueAddedTaxCI": 0.0,
            "commissionAmountBI": 0.0,
            "sumCpCmPremium": 0.0,
            "commercialPremium": 0.0,
            "performanceRateBI": 0.0,
            "sumexcludeTaxPremiumCI": 0.0,
            "expenseRateCI": 0.0,
            "compulsoryPremium": 0.0,
            "sumPremium": 2648.27,
            "sumvalueAddedTaxBI": 0.0,
            "commissionAmountCI": 0.0,
            "commissionAmountBILim": 0.0,
            "commissionAmountCILim": 0.0,
            "performanceRateCI": 0.0
        }
    }
    print hn_parse_renrwal(False, body)
